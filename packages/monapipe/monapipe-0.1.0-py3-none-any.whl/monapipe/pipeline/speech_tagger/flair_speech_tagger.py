# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from typing import Any, Dict

import flair
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
from spacy.language import Language
from spacy.tokens import Doc, Span

import monapipe.resource_handler as resources
from monapipe.config import SETTINGS
from monapipe.pipeline.methods import requires, update_token_span_groups
from monapipe.pipeline.speech_tagger.methods import (
    create_speech_segments_from_token_tags,
)
from monapipe.pipeline.speech_tagger.speech_tagger import SpeechTagger


@Language.factory(
    "flair_speech_tagger",
    assigns=SpeechTagger.assigns,
    default_config={"sentence_level": False},
)
def flair_speech_tagger(nlp: Language, name: str, sentence_level: bool) -> Any:
    """Spacy pipeline component.
        Tags tokens and clauses with speech tags.
        Wrapper for the "Redewiedergabe" taggers from https://github.com/redewiedergabe/tagger.

    Args:
        nlp: Spacy object.
        name: Component name.
        sentence_level: If True, the taggers take each sentence separately as input;
            if False, the taggers take chunks of up to 100 tokens as input.

    Returns:
        `FlairSpeechTagger`.

    """
    return FlairSpeechTagger(nlp, sentence_level)


class FlairSpeechTagger(SpeechTagger):
    """The class `FlairSpeechTagger`."""

    def __init__(self, nlp: Language, sentence_level: bool):
        requires(self, nlp, ["parser"])

        super().__init__(nlp, sentence_level)

    def __call__(self, doc: Doc) -> Doc:
        flair.device = torch.device(SETTINGS["torch_device"])

        speech_taggers = resources.access("speech_taggers")

        for token in doc:
            token._.speech = {}

        if self.sentence_level:
            for sent in doc.sents:
                text = " ".join([token.text for token in sent if not token.is_space])
                text = Sentence(text, use_tokenizer=False)
                self._add_speech_tags_to_tokens(sent, text, speech_taggers, "indirect")
                self._add_speech_tags_to_tokens(sent, text, speech_taggers, "freeIndirect")
                self._add_speech_tags_to_tokens(sent, text, speech_taggers, "direct")
                self._add_speech_tags_to_tokens(sent, text, speech_taggers, "reported")
        else:
            chunks = []
            chunk = []
            for sent in doc.sents:
                tokens = list(sent)
                if len(chunk) + len(tokens) <= 100 or len(chunk) == 0:
                    chunk.extend(tokens)
                else:
                    chunks.append(chunk)
                    chunk = tokens
            if len(chunk) > 0:
                chunks.append(chunk)
            for chunk in chunks:
                text = " ".join([token.text for token in chunk if not token.is_space])
                text = Sentence(text, use_tokenizer=False)
                self._add_speech_tags_to_tokens(chunk, text, speech_taggers, "indirect")
                self._add_speech_tags_to_tokens(chunk, text, speech_taggers, "freeIndirect")
                self._add_speech_tags_to_tokens(chunk, text, speech_taggers, "direct")
                self._add_speech_tags_to_tokens(chunk, text, speech_taggers, "reported")

        create_speech_segments_from_token_tags(
            doc, ["indirect", "freeIndirect", "direct", "reported"]
        )

        update_token_span_groups(doc, ["speech"])

        return doc

    def _add_speech_tags_to_tokens(
        self, sent: Span, text: Sentence, taggers: Dict[str, SequenceTagger], speech_type: str
    ):
        """Add speech tags to tokens in a sentence.

        Args:
            sent: The sentence in spacy format.
            text: The sentence in flair format.
            taggers: The speech taggers; keys are speech types, values are taggers.
            speech_type: The speech type to tag.

        """
        taggers[speech_type].predict(text)
        offset = 0
        for i, token in enumerate(sent):
            if token.is_space:
                offset += 1
            else:
                tag = text.tokens[i - offset].get_labels()[0]
                if tag.value == speech_type:
                    token._.speech[speech_type] = tag.score
