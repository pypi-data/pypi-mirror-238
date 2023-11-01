# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import sentry_sdk

from monapipe.silence import (
    silence_logging,
    silence_tensorflow,
    silence_tqdm,
    silence_transformers,
    silence_warnings,
)

silence_logging()
silence_tensorflow()
silence_tqdm()
silence_transformers()
silence_warnings()
