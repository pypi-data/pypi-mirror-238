from typing import List, Literal, Optional

import prodigy.recipes.sent
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    Dataset,
    Goal,
    Input,
    InputDataset,
    Model,
    props,
    task_recipe,
)


@task_recipe(
    title="Sentence Segmentation",
    description="Create gold data for sentence boundaries by correcting a model's predictions",
    view_id="pos_manual",
    field_props={
        "dataset": props.dataset_choice,
        "model": props.model,
        "goal": props.goal,
        "exclude": props.exclude,
    },
    cli_names={
        "model": "model.name",  # Usability: make it consistent with the other recipes
    },
)
def sent(
    *,
    dataset: Dataset[Literal["sent"]],
    model: Model,
    input: Input,
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    nlp = model.load()
    stream = input.load(rehash=True, dedup=True, input_key="text")
    stream = prodigy.recipes.sent.preprocess_stream(stream, nlp)
    exclude_names = [ds.name for ds in exclude] if exclude is not None else None
    return {
        "dataset": dataset.name,
        "stream": stream,
        "view_id": "pos_manual",
        "exclude": exclude_names,
        "config": {
            "lang": nlp.lang,
            "labels": [prodigy.recipes.sent.SENT_START_LABEL],
            "exclude_by": "input",
            "allow_newline_highlight": True,
            "feed_overlap": goal == "overlap",
        },
    }
