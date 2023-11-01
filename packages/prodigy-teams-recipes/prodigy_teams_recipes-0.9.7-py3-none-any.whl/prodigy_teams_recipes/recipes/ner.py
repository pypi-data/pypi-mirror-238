from typing import List, Literal, Optional, Union

import prodigy.recipes.ner
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    BlankModelSpans,
    Dataset,
    Goal,
    Input,
    InputDataset,
    Patterns,
    UseModel,
    props,
    task_recipe,
)


@task_recipe(
    title="Named Entity Recognition",
    description="Annotate labeled text spans representing real-world objects like names, persons, countries or products.",
    view_id="ner",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "segment": props.segment,
        "goal": props.goal,
        "patterns": props.patterns,
        "exclude": props.exclude,
    },
    cli_names={
        "model-blank-spans.lang": "model.lang",
        "model-blank-spans.highlight-chars": "model.highlight-chars",
        "model-use.name": "model.name",
        "model-use.update": "model.update",
    },
)
def ner(
    *,
    dataset: Dataset[Literal["ner"]],
    model: Union[BlankModelSpans, UseModel],
    input: Input,
    label: List[str],
    patterns: Optional[Patterns] = None,
    exclude: Optional[List[InputDataset]] = None,
    segment: bool = False,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    update_model = False
    spacy_model = None
    highlight_chars = False
    if isinstance(model, UseModel):
        spacy_model = model.name
        update_model = model.update
        nlp = spacy_model.load()
    else:
        nlp = model.load()
        highlight_chars = model.highlight_chars
    stream = input.load(rehash=True, dedup=True, input_key="text")
    labels, no_missing = prodigy.recipes.ner.get_ner_labels(nlp, label=label)
    if patterns:
        matcher = patterns.load(nlp=nlp, label=label)
        stream = (eg for _, eg in matcher(stream))
    stream = prodigy.recipes.ner.preprocess_stream(
        stream,
        nlp,
        labels=labels,
        unsegmented=not segment,
        set_annotations=spacy_model is not None,
    )

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "update": prodigy.recipes.ner.get_update(nlp, no_missing=no_missing)
        if update_model
        else None,
        "view_id": "ner_manual",
        "exclude": exclude_names,
        "config": {
            "labels": label,
            "lang": nlp.lang,
            "ner_manual_highlight_chars": highlight_chars,
            "feed_overlap": goal == "overlap",
        },
    }
