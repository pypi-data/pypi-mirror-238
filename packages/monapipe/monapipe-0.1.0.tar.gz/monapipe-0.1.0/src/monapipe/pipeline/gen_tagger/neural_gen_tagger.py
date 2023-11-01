# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from typing import Any

from spacy.language import Language
from spacy.tokens import Doc

import monapipe.resource_handler as resources
from monapipe.pipeline.gen_tagger.gen_tagger import GenTagger
from monapipe.pipeline.methods import requires, update_token_span_groups
from monapipe.pipeline.reflection_tagger.methods import create_passages_from_clause_tags


@Language.factory(
    "neural_gen_tagger",
    assigns=GenTagger.assigns,
    default_config={"label_condition": "multi"},
)
def neural_gen_tagger(nlp: Language, name: str, label_condition: str) -> Any:
    """Spacy pipeline component.
        Add generalising passages to the document.
        Uses the code and models from here:
        https://github.com/tschomacker/generalizing-passages-identification-bert

    Args:
        nlp: Spacy object.
        name: Component name.
        label_condition: Label condition ("multi" or "binary").

    Returns:
        `NeuralGenTagger`.

    """
    return NeuralGenTagger(nlp, label_condition)


class NeuralGenTagger(GenTagger):
    """The class `NeuralGenTagger`."""

    def __init__(self, nlp: Language, label_condition: str):
        requires(self, nlp, ["clausizer"])

        if label_condition not in ["binary", "multi"]:
            raise ValueError('Label condition must be "binary" or "multi".')

        super().__init__(nlp, label_condition)

    def __call__(self, doc: Doc) -> Doc:
        models = resources.access("generalizing_passages_identification_bert")
        model = models["gi_" + self.label_condition]
        tag_names = (
            ["NONE", "ALL", "BARE", "DIV", "EXIST", "MEIST", "NEG"]
            if self.label_condition == "multi"
            else ["GI"]
        )

        clause_tags = []
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

            for clause in sents[i]._.clauses:
                clause_open = False
                clause_text_embed_in_context = ""
                for token in context_tokens:
                    if token._.clause is not None:
                        # token is part of the current clause
                        if token._.clause == clause:
                            if not clause_open:
                                # start the clause mark up
                                clause_text_embed_in_context += "<b>"
                                clause_open = True
                        # token is NOT part of the current clause
                        else:
                            if clause_open:
                                # close the clause mark up
                                clause_text_embed_in_context += "</b>"
                                clause_open = False
                        clause_text_embed_in_context += " " + token.text
                    # punctation
                    else:
                        clause_text_embed_in_context += token.text
                    # closing the mark up, in case the passage conists of a single clause
                if clause_open:
                    clause_text_embed_in_context += "</b>"

                prediction = [round(x) for x in model.predict(clause_text_embed_in_context)]
                clause_tags.append(
                    set(
                        [
                            tag_name
                            for tag_i, tag_name in enumerate(tag_names)
                            if bool(prediction[tag_i]) and tag_name != "NONE"
                        ]
                    )
                )

        create_passages_from_clause_tags(doc, "gi", clause_tags)

        update_token_span_groups(doc, ["gi"])

        return doc
