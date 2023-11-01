# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import os

from tensorflow.keras import Sequential, models

from monapipe.resource_handler import ResourceHandler

PATH = os.path.dirname(__file__)

RESOURCE_HANDLER = ResourceHandler(PATH)


def load() -> Sequential:
    """Loading method of the `attribution` resource.

    Returns:
        The model.

    """
    model = models.load_model(os.path.join(PATH, "no_encoding"))
    return model
