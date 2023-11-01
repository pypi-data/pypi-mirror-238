# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from spacy.language import Language
from spacy.tokens import Span

from monapipe.pipeline.methods import add_extension


class EventTagger:
    """The super class `EventTagger`."""

    assigns = {"span._.event": "clause._.event"}

    def __init__(self, nlp: Language):
        add_extension(Span, "event")
