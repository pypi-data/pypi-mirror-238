from typing import List, Literal, Optional

import prodigy.recipes.review
from prodigy.components.db import connect
from prodigy.types import RecipeSettingsType
from prodigy.util import log
from prodigy_teams_recipes_sdk import (
    BoolProps,
    Dataset,
    InputDataset,
    ListProps,
    props,
    task_recipe,
)


@task_recipe(
    title="Review Annotations",
    description="Review existing annotations created by multiple annotators and resolve potential conflicts by creating one final annotation.",
    view_id="review",
    field_props={
        # fmt: off
        "dataset": props.dataset_choice,
        "datasets": ListProps(title="Review Datasets", description="Examples from all the datasets will be combined, and you'll review them one-by-one with conflicting examples being combined so you can pick the correct answer.", exists=True),
        "label": props.label,
        "show_skipped": BoolProps(title="Include skipped answers", description="e.g. if annotator hit ignore or rejected manual annotation"),
        "auto_accept": BoolProps(title="Auto accept annotations", description="Automatically accept annotations with no conflicts and add them to the dataset"),
        # fmt: on
    },
)
def review(
    *,
    dataset: Dataset[Literal["review"]],
    datasets: List[InputDataset],
    label: Optional[List[str]] = None,
    show_skipped: bool = False,
    auto_accept: bool = False,
) -> RecipeSettingsType:
    log("RECIPE: Starting recipe review", locals())
    all_examples = {}
    stream = None
    for ds in datasets:
        all_examples[ds.name] = list(ds.load())
    stream = prodigy.recipes.review.get_review_stream(
        all_examples, show_skipped=show_skipped
    )
    if auto_accept:
        DB = connect()
        stream = prodigy.recipes.review.filter_auto_accept_stream(
            stream, DB, dataset.name
        )
    return {
        "view_id": "review",
        "dataset": dataset.name,
        "stream": stream,
        "config": {"labels": label} if label is not None else {},
    }
