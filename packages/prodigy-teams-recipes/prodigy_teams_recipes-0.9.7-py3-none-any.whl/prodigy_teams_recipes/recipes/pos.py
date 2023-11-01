from typing import List, Literal, Optional

import prodigy.recipes.pos
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    Dataset,
    Goal,
    Input,
    InputDataset,
    UseModel,
    props,
    task_recipe,
)


@task_recipe(
    title="Part of Speech tagging recipe",
    description="Annotate word types.",
    view_id="ner",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "segment": props.segment,
        "goal": props.goal,
        "exclude": props.exclude,
    },
)
def pos(
    *,
    dataset: Dataset[Literal["pos"]],
    input: Input,
    label: List[str],
    model: UseModel,
    exclude: Optional[List[InputDataset]] = None,
    segment: bool = False,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    spacy_model = model.name
    # update_model = model.update_model
    assert spacy_model.path is not None
    nlp = spacy_model.load()
    labels = prodigy.recipes.pos.get_pos_labels(nlp, label)
    stream = input.load(rehash=True, dedup=True, input_key="text")
    stream = prodigy.recipes.pos.preprocess_stream(
        stream, nlp, labels=labels, unsegmented=not segment
    )

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        # TODO: add update callback for active learning
        "view_id": "pos_manual",
        "exclude": exclude_names,
        "config": {
            "lang": nlp.lang,
            "labels": label,
            "feed_overlap": goal == "nooverlap",
        },
    }
