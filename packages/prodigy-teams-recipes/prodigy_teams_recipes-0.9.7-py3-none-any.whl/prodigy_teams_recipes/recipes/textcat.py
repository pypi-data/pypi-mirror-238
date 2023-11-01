from dataclasses import dataclass
from typing import List, Literal, Optional, Union

import prodigy.recipes.textcat
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    Dataset,
    FloatProps,
    Goal,
    Input,
    InputDataset,
    UseModel,
    props,
    task_recipe,
    teams_type,
)


@teams_type(
    field_props={
        # fmt: off
        "update": props.update_model,
        "threshold": FloatProps(title="Threshold", description="Score threshold to pre-select label, e.g. 0.75 to select all labels with a score of 0.75 and above", step=0.1, min=0.0, max=1.0),
        # fmt: on
    },
)
@dataclass
class TextcatModel(UseModel):
    threshold: float = 0.5


@teams_type(
    "skip",
    title="Don't use model",
    field_props={"labels_exclusive": props.labels_exclusive},
)
@dataclass
class NoTextcatModel:
    labels_exclusive: bool = False


@task_recipe(
    title="Text Classification",
    description="Assign categories to whole documents or sentences.",
    view_id="choice",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "goal": props.goal,
        "model": props.model,
        "exclude": props.exclude,
    },
    cli_names={
        "model-textcatmodel.name": "model.name",
        "model-textcatmodel.threshold": "model.threshold",
        "model-textcatmodel.update": "model.update",
        "model-skip.labels-exclusive": "labels-exclusive",
    },
)
def textcat(
    *,
    dataset: Dataset[Literal["textcat"]],
    model: Union[TextcatModel, NoTextcatModel],
    input: Input,
    label: List[str],
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    stream = input.load(rehash=True, dedup=True, input_key="text")
    labels = label
    threshold = None
    spacy_model = None
    update = None
    exclusive = False
    if isinstance(model, TextcatModel):
        spacy_model = model.name
        nlp = spacy_model.load()
        update = prodigy.recipes.textcat.get_update(nlp) if model.update else None
        threshold = model.threshold
        labels, exclusive = prodigy.recipes.textcat.get_textcat_labels(nlp, label)
        is_binary = len(labels) == 1
        stream = prodigy.recipes.textcat.preprocess_stream(
            stream, nlp, labels=labels, threshold=threshold
        )
    else:
        exclusive = model.labels_exclusive
        is_binary = len(labels) == 1
        if not is_binary:
            stream = prodigy.recipes.textcat.add_label_options(stream, label)
        else:
            stream = prodigy.recipes.textcat.add_labels_to_stream(stream, label)

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "update": update,
        "view_id": "classification" if is_binary else "choice",
        "exclude": exclude_names,
        "config": {
            "choice_style": "single" if exclusive else "multiple",
            "choice_auto_accept": exclusive,
            "feed_overlap": goal == "overlap",
        },
    }
