# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from typing import Any, List, Tuple

import numpy as np
import torch
from sklearn.preprocessing import MultiLabelBinarizer
from spacy.language import Language
from spacy.tokens import Doc
from transformers import BertModel, BertTokenizer

import monapipe.resource_handler as resources
from monapipe.config import SETTINGS
from monapipe.pipeline.attribution_tagger.attribution_tagger import AttributionTagger
from monapipe.pipeline.methods import requires


@Language.factory(
    "neural_attribution_tagger",
    assigns=AttributionTagger.assigns,
    default_config={},
)
def neural_attribution_tagger(nlp: Language, name: str) -> Any:
    """Spacy pipeline component.
        Add speaker attribution to each clause.
        Uses the model from Dönicke et al. (2022):
        "Modelling Speaker Attribution in Narrative Texts With Biased and Bias-Adjustable Neural Networks".
        (https://gitlab.gwdg.de/mona/neural-attribution)

    Args:
        nlp: Spacy object.
        name: Component name.

    Returns:
        `NeuralAttributionTagger`.

    """
    return NeuralAttributionTagger(nlp)


class NeuralAttributionTagger(AttributionTagger):
    """The class `NeuralAttributionTagger`."""

    def __init__(self, nlp: Language):
        requires(self, nlp, ["clausizer"])

        super().__init__(nlp)

        # BERT tokenizer and model
        self._tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-german-cased")
        self._model = BertModel.from_pretrained(
            "dbmdz/bert-base-german-cased", output_hidden_states=True
        )

        # attribution categories
        self._label_names = ["Figur", "Erzählinstanz", "Verdacht Autor"]
        self._label_encoder = MultiLabelBinarizer()
        self._label_encoder.fit([self._label_names])

    def __call__(self, doc: Doc) -> Doc:
        attribution_model = resources.access("attribution")

        # create embeddings for each clause
        clause_embeddings = []
        sents = [None] + list(doc.sents) + [None]
        for i in range(1, len(sents) - 1):
            context_tokens = []
            try:
                context_tokens.extend(list(sents[i - 1]))
            except TypeError:
                pass  # first sentence
            context_tokens.extend(list(sents[i]))
            try:
                context_tokens.extend(list(sents[i + 1]))
            except TypeError:
                pass  # last sentence
            context_tokens = [token for token in context_tokens if not token.is_space]
            tokens = [token.text for token in context_tokens]
            string = " ".join(tokens)
            embeddings, subtokens = self._create_embeddings(string)
            subtoken_to_token_mappings = self._map_subtokens_to_tokens(subtokens, tokens)
            subtoken_clauses = [context_tokens[i]._.clause for i in subtoken_to_token_mappings]
            for clause in sents[i]._.clauses:
                clause_embedding = self._pad_sample(
                    [
                        [float(subtoken_clauses[i] == clause)] + embedding
                        for i, embedding in enumerate(embeddings)
                    ],
                    123,
                )
                clause_embeddings.append(clause_embedding)

        # predict labels for each clause
        X = self._prepare(clause_embeddings)
        Y = attribution_model.predict(X, verbose=0)
        labels = [[round(x) for x in outputs] for outputs in Y]
        labels = self._label_encoder.inverse_transform(np.asarray(labels))

        # assign labels to each clause
        for i in range(1, len(sents) - 1):
            for clause in sents[i]._.clauses:
                clause._.attribution = set(labels.pop(0))

        return doc

    def _cuda(self, obj: Any) -> Any:
        """Add an object to GPU if available, else to CPU.

        Args:
            obj (obj): The object.

        Returns:
            obj: The object.

        """
        device = SETTINGS["torch_device"]
        obj = obj.to(device)
        return obj

    def _create_embeddings(self, string: str) -> Tuple[List[List[float]], List[str]]:
        """Create word embeddings for a string.

        Args:
            string: The string.

        Returns:
            List of word embeddings, one for each word in the string.
            List of words in the string (as produced by the tokenizer).

        """
        model = self._cuda(self._model)
        model = model.eval()
        string_ids = self._tokenizer.encode(string, add_special_tokens=False)
        tokens = self._tokenizer.convert_ids_to_tokens(string_ids)
        string_ids = torch.LongTensor(string_ids)
        string_ids = self._cuda(string_ids)
        string_ids = string_ids.unsqueeze(0)
        with torch.no_grad():
            out = model(input_ids=string_ids)
        hidden_states = out[2]
        embeddings = hidden_states[-1][0]
        embeddings = [[float(x) for x in embedding] for embedding in embeddings]
        return embeddings, tokens

    def _map_subtokens_to_tokens(self, subtokens: List[str], tokens: List[str]) -> List[int]:
        """Map subtokens (i.e. tokens produced by the BERT tokenizer) to tokens (as in the data).

        Args:
            subtokens: List of subtokens.
                Example: ['(', '›abheben‹', 'ist', 'übrigens', 'auch', 'trivial', ';', 'entschuldigen', 'Sie', ',', 'Rex', ')', '.']
            tokens: List of tokens.
                Example: ['(', '›', 'ab', '##heben', '[UNK]', 'ist', 'übrigens', 'auch', 'tri', '##via', '##l', ';', 'entschuldigen', 'Sie', ',', 'Re', '##x', ')', '.']

        Returns:
            For each subtoken the index of the corresponding token.
                Example: [0, 1, 1, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10, 10, 11, 12]

        """
        subtoken_to_token_mappings = []
        current_token_index = 0
        current_token_pos = 0
        for subtoken in subtokens:
            current_token = tokens[current_token_index]
            subtoken = subtoken.strip("#")
            if current_token[current_token_pos:].startswith(subtoken):
                subtoken_to_token_mappings.append(current_token_index)
                current_token_pos += len(subtoken)
            elif subtoken == "[UNK]":  # "‹"
                subtoken_to_token_mappings.append(current_token_index)
                current_token_pos += 1
            else:
                raise ValueError("Subtokens cannot be mapped to tokens!")
            if current_token_pos == len(current_token):
                current_token_index += 1
                current_token_pos = 0
        return subtoken_to_token_mappings

    def _pad_sample(self, sample: List[List[float]], max_len: int) -> List[List[float]]:
        """Pad an embedding to a given length. The embedding is centered.
            If it is too long, an equal number of word vectors is removed from the left and from the right.
            If it is too short, an equal number of zero vectors is inserted at the left and at the right.

        Args:
            sample: The embedding as a list of word vectors.
            max_len: The wanted size of the embedding.

        Returns:
            The padded version of the embedding.

        """
        zero_vector = [0.0] * len(sample[0])
        diff = max_len - len(sample)
        if diff == 0:
            return sample
        d = int(abs(diff) / 2.0)
        if diff > 0:
            return ([zero_vector] * (diff % 2)) + ([zero_vector] * d) + sample + ([zero_vector] * d)
        if diff < 0:
            return sample[d + (diff % 2) : (-d if d > 0 else len(sample))]

    def _prepare(self, X: List[Any]) -> np.ndarray:
        """Transform an array-like object to Numpy format.

        Args:
            X: Array-like object.

        Returns:
            Numpy array.

        """
        return np.asarray(X, dtype=np.float32)
