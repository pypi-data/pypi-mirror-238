from typing import Union

from prodigy.types import RecipeSettingsType, ViewId
from prodigy_teams_recipes_sdk import (
    Dataset,
    Goal,
    Input,
    InputDataset,
    props,
    task_recipe,
)


@task_recipe(
    title="Curate and Explore",
    description="View what's in your data and accept or reject examples",
    view_id="text",  # not correct but we need to use somthing
    field_props={
        "dataset": props.dataset_choice,
        "input": props.asset_or_dataset,
        "view_id": props.view_id,
        "goal": props.goal,
    },
)
def curate(
    *,
    dataset: Dataset,
    input: Union[Input, InputDataset],
    view_id: ViewId,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    stream = input.load()
    return {
        "view_id": view_id,
        "dataset": dataset.name,
        "stream": stream,
        "config": {"exclude_by": "input", "feed_overlap": goal == "overlap"},
    }
