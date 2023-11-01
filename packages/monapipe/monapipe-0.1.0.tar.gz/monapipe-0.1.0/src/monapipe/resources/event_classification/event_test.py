import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import event_classify
from event_classify.eval import evaluate
from event_classify.util import get_model, split_text
from event_classify.datasets import JSONDataset, SpanAnnotation
from event_classify.parser import Parser
from event_classify.preprocessing import build_pipeline
from settings import RESOURCES_PATH
from torch.utils.data import DataLoader

model_path = os.path.join(RESOURCES_PATH, "demo_model")
model, tokenizer = get_model(model_path)

device = "cuda:0"
special_tokens = True
batch_size = 8

nlp = build_pipeline(Parser.SPACY)

full_text = "Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt. Er lag auf seinem panzerartig harten Rücken und sah, wenn er den Kopf ein wenig hob, seinen gewölbten, braunen, von bogenförmigen Versteifungen geteilten Bauch, auf dessen Höhe sich die Bettdecke, zum gänzlichen Niedergleiten bereit, kaum noch erhalten konnte. Seine vielen, im Vergleich zu seinem sonstigen Umfang kläglich dünnen Beine flimmerten ihm hilflos vor den Augen."
splits = split_text(full_text)

data = {"text": full_text, "title": "test_file", "annotations": []}
for split in splits:
    doc = nlp(split.text)
    annotations = event_classify.preprocessing.get_annotation_dicts(doc)
    for annotation in annotations:
        annotation["start"] += split.offset
        annotation["end"] += split.offset
        new_spans = []
        for span in annotation["spans"]:
            new_spans.append(
                (
                    span[0] + split.offset,
                    span[1] + split.offset,
                )
            )
        annotation["spans"] = new_spans
    data["annotations"].extend(annotations)

dataset = JSONDataset(
    dataset_file=None, data=[data], include_special_tokens=special_tokens
)
loader = DataLoader(
    dataset,
    batch_size=batch_size,
    collate_fn=lambda list_: SpanAnnotation.to_batch(list_, tokenizer),
)

model.to(device)
evaluation_result = evaluate(loader, model, device=device)
# We only pass in one document, so we only use [0]
data = dataset.get_annotation_json(evaluation_result)[0]
print(data)
#json.dump(data, out_file)