from typing import List, Literal, Optional

from prodigy.types import RecipeSettingsType, StreamType
from prodigy_teams_recipes_sdk import (
    BoolProps,
    Dataset,
    Goal,
    ImageClassification,
    Input,
    InputDataset,
    OptionalProps,
    props,
    task_recipe,
)


@task_recipe(
    title="Image Annotation & Classification",
    description="Annotate bounding boxes and segments, or assign categories to images.",
    view_id="image",
    field_props={
        # fmt: off
        "dataset": props.dataset_choice,
        "label": props.label,
        "segment": BoolProps(title="Annotate bounding boxes or segments", description="You'll be able to draw rectangular, polygon or freehand shapes onto the image and assign labels to them."),
        "classify": OptionalProps(optional_title="Annotate image categories", description="Select one or more category labels that apply to the image"),
        "goal": props.goal,
        "exclude": props.exclude,
        # fmt: on
    },
)
def image(
    *,
    dataset: Dataset[Literal["image"]],
    input: Input,
    label: List[str],
    segment: bool = True,
    classify: Optional[ImageClassification] = None,
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    config = {
        "labels": label,
        "feed_overlap": goal == "overlap",
    }
    stream = input.load(rehash=True, dedup=False, input_key="image")
    view_id = "image"

    if segment:
        view_id = "image_manual"

    if classify is not None:
        is_binary = len(label) == 1
        stream = make_image_classification_tasks(stream, label, is_binary, segment)
        view_id = "choice"

        if is_binary and segment:
            config["choice_style"] = "multiple"
            config["choice_auto_accept"] = False
        elif is_binary:
            view_id = "classification"
        else:
            single = classify.labels_exclusive
            config["choice_style"] = "single" if single else "multiple"
            config["choice_auto_accept"] = single

        if segment:
            blocks = [
                {
                    "view_id": "image_manual",
                },
                {
                    "view_id": view_id,
                    "image": None,
                    "text": None,
                },
            ]
            config["blocks"] = blocks
            view_id = "blocks"

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "view_id": view_id,
        "config": config,
        "exclude": exclude_names,
    }


def make_image_classification_tasks(
    stream: StreamType,
    labels: List[str],
    is_binary: bool = False,
    segment: bool = False,
) -> StreamType:
    if is_binary and not segment:
        for eg in stream:
            eg["label"] = labels[0]
            yield eg
    else:
        # Add "options" to each outgoing task.
        labels = labels or []
        options = [{"id": label, "text": label} for label in labels]
        for eg in stream:
            eg["options"] = options
            yield eg
