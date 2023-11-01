from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from prodigy.types import RecipeSettingsType, StreamType
from prodigy_teams_recipes_sdk import (
    ChoiceProps,
    Dataset,
    Goal,
    Input,
    InputDataset,
    IntProps,
    props,
    task_recipe,
    teams_type,
)

av_mode = ChoiceProps(
    title="Annotation Mode",
    description="Annotate audio regions with labels, classificate media into categories, transcribe media or add notes",
)


@teams_type(
    "transcribe",
    title="Transcribe media or add notes",
    description="Add a free-form text input field that can be used to transcribe the audio or add other notes about the contents of the media file.",
    field_props={"rows": IntProps(title="Text field rows", min=1, max=10, step=1)},
)
@dataclass
class AVTranscription:
    rows: int = 3


@teams_type(
    "regions",
    title="Annotate audio regions",
    description="You'll be able to highlight overlapping regions in the audio waveform and assign labels to them",
    field_props={"label": props.label},
)
@dataclass
class AVRegions:
    label: List[str]


@teams_type(
    "classify",
    title="Annotate categories",
    description="Select one or more category labels that apply to the media file",
    field_props={"label": props.label, "labels_exclusive": props.labels_exclusive},
)
@dataclass
class AVClassification:
    label: List[str]
    labels_exclusive: bool = False


@task_recipe(
    title="Annotate Audio",
    description="Annotate regions, assign categories to audio content or transcribe audio files.",
    field_props={
        "dataset": props.dataset_choice,
        "mode": av_mode,
        "goal": props.goal,
        "exclude": props.exclude,
    },
)
def audio(
    *,
    dataset: Dataset[Literal["audio"]],
    input: Input,
    mode: Union[AVRegions, AVClassification, AVTranscription],
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    return audio_video(
        dataset,
        input,
        mode,
        exclude,
        goal,
    )


@task_recipe(
    title="Annotate Video",
    description="Annotate regions, assign categories to video content or transcribe video files.",
    field_props={
        "dataset": props.dataset_choice,
        "mode": av_mode,
        "goal": props.goal,
        "exclude": props.exclude,
    },
)
def video(
    *,
    dataset: Dataset[Literal["video"]],
    input: Input,
    mode: Union[AVRegions, AVClassification, AVTranscription],
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    return audio_video(
        dataset,
        input,
        mode,
        exclude,
        goal,
    )


def audio_video(
    dataset: Union[Dataset[Literal["video"]], Dataset[Literal["audio"]]],
    input: Input,
    mode: Union[AVRegions, AVClassification, AVTranscription],
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    stream = input.load(rehash=True, dedup=False)
    overlap = goal == "overlap"
    if isinstance(mode, AVClassification):
        labels = mode.label
        labels_exclusive = mode.labels_exclusive
        is_binary = len(labels) == 1
        stream = make_av_classification_tasks(stream, labels, is_binary)
        view_id = "classification" if is_binary else "choice"
        config = {
            "feed_overlap": overlap,
            "labels": labels,
            "choice_style": "single" if labels_exclusive else "multiple",
            "choice_auto_accept": labels_exclusive,
        }
    elif isinstance(mode, AVTranscription):
        rows = mode.rows or 3
        view_id = "blocks"
        blocks = [
            {"view_id": "audio"},
            {"view_id": "text_input", "field_rows": rows, "field_autofocus": True},
        ]
        config = {"feed_overlap": overlap, "blocks": blocks}
    else:
        view_id = "audio_manual"
        config = {"feed_overlap": overlap, "labels": mode.label}

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "view_id": view_id,
        "config": config,
        "exclude": exclude_names,
    }


def make_av_classification_tasks(
    stream: StreamType, labels: List[str], is_binary: bool = False
) -> StreamType:
    if is_binary:
        for eg in stream:
            eg["label"] = labels[0]
            yield eg
    else:
        # Add "options" to each outgoing task
        labels = labels or []
        options = [{"id": label, "text": label} for label in labels]
        for eg in stream:
            eg["options"] = options
            yield eg
