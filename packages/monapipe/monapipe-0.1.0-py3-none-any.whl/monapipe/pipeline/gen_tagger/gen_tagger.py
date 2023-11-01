# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from spacy.language import Language
from spacy.tokens import Span

from monapipe.pipeline.methods import add_extension


class GenTagger:
    """The super class `GenTagger`."""

    assigns = {"doc.spans": "doc.spans['gi']", "span._.gi": "gi_span._.gi"}

    def __init__(self, nlp: Language, label_condition: str):
        self.label_condition = label_condition

        add_extension(Span, "gi", {})
