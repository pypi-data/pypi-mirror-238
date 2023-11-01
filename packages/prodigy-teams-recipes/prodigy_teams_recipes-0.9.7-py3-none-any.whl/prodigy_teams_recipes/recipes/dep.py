from typing import List, Literal, Optional

import prodigy.recipes.dep
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
    title="Dependency Parsing",
    description="Annotate syntactic dependencies.",
    view_id="relations",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "segment": props.segment,
        "goal": props.goal,
        "exclude": props.exclude,
    },
)
def dep(
    *,
    dataset: Dataset[Literal["dep"]],
    model: UseModel,
    input: Input,
    label: List[str],
    exclude: Optional[List[InputDataset]] = None,
    segment: bool = False,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    if isinstance(model, UseModel):
        spacy_model = model.name
        update_model = model.update
    else:
        spacy_model = model.lang
        update_model = False
    assert spacy_model.path is not None
    nlp = spacy_model.load()
    stream = input.load(rehash=True, dedup=True, input_key="text")
    labels = prodigy.recipes.dep.get_dep_labels(nlp, label)
    stream = prodigy.recipes.dep.preprocess_stream(
        stream, nlp, unsegmented=not segment, labels=labels
    )

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "update": prodigy.recipes.dep.get_update(nlp) if update_model else None,
        "view_id": "relations",
        "exclude": exclude_names,
        "config": {
            "lang": nlp.lang,
            "labels": label,
            "feed_overlap": goal == "overlap",
            "custom_theme": {"cardMaxWidth": "90%", "relationHeight": 150},
        },
    }
