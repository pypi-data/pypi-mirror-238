# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import importlib
from typing import Any

from spacy.language import Language
from spacy.tokens import Doc
from torch.utils.data import DataLoader

import monapipe.resource_handler as resources
from monapipe.config import SETTINGS
from monapipe.pipeline.event_tagger.event_tagger import EventTagger
from monapipe.pipeline.methods import requires


@Language.factory("neural_event_tagger", assigns=EventTagger.assigns, default_config={})
def neural_event_tagger(nlp: Language, name: str) -> Any:
    """Spacy pipeline component.
        Integration of event classification from EvENT project.
        Uses the code and models from here:
        https://github.com/uhh-lt/event-classification


    Args:
        nlp: Spacy object.
        name: Component name.

    Returns:
        `NeuralEventTagger`.

    """
    return NeuralEventTagger(nlp)


class NeuralEventTagger(EventTagger):
    """The class `NeuralEventTagger`."""

    def __init__(self, nlp: Language):
        requires(self, nlp, ["clausizer"])

        super().__init__(nlp)

    def __call__(self, doc: Doc) -> Doc:
        model, tokenizer = resources.access("event_classification")

        path = ".".join(["monapipe", "resources", "event_classification", "event_classify"])
        module_datasets = importlib.import_module(path + ".datasets")
        module_eval = importlib.import_module(path + ".eval")

        special_tokens = True
        batch_size = 8

        annotations = []
        annotation_start_to_clause = {}
        for clause in doc._.clauses:
            annotation = {
                "start": clause[0].idx,
                "end": clause[-1].idx,
                "spans": [(clause[0].idx, clause[-1].idx)],
                "predicted": None,
            }
            annotations.append(annotation)
            annotation_start_to_clause[clause[0].idx] = clause
        data = {"text": doc.text, "annotations": annotations, "title": None}
        data["annotations"].extend(annotations)

        dataset = module_datasets.JSONDataset(
            dataset_file=None, data=[data], include_special_tokens=special_tokens
        )
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            collate_fn=lambda list_: module_datasets.SpanAnnotation.to_batch(list_, tokenizer),
        )

        device = SETTINGS["torch_device"]
        model.to(device)
        result = module_eval.evaluate(loader, model, device=device)
        data = dataset.get_annotation_json(result)[0]
        for annotation in data["annotations"]:
            annotation_start_to_clause[annotation["start"]]._.event = annotation[
                "additional_predictions"
            ]

        return doc
