# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from typing import Optional

from spacy.language import Language
from spacy.tokens import Span, Token

from monapipe.pipeline.methods import add_extension


class SpeechTagger:
    """The super class `SpeechTagger`."""

    assigns = {
        "doc.spans": "doc.spans['speech']",
        "span._.speech": "speech_span._.speech",
        "token._.speech": "token._.speech",
    }

    def __init__(self, nlp: Language, sentence_level: Optional[bool]):
        self.sentence_level = sentence_level

        add_extension(Token, "speech", {})
        add_extension(Span, "speech", {})
