from typing import List, Literal, Optional, Union

import prodigy.recipes.spans
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

# TODO: figure out how to support suggesters


@task_recipe(
    title="Span Categorization",
    description="Annotate potentially overlapping and nested spans in the data.",
    view_id="spans_manual",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
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
def spans(
    *,
    dataset: Dataset[Literal["spans"]],
    model: Union[BlankModelSpans, UseModel],
    input: Input,
    label: List[str],
    patterns: Optional[Patterns] = None,
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    update_model = False
    spacy_model = None
    highlight_chars = False
    labels = label
    key = ""
    set_annotations = isinstance(model, UseModel)
    if set_annotations:
        spacy_model = model.name
        update_model = model.update
        assert spacy_model.path is not None
        nlp = spacy_model.load()
        labels, key = prodigy.recipes.spans.get_span_labels(nlp, label=label)
    else:
        nlp = model.load()
        highlight_chars = model.highlight_chars
    assert input.path is not None
    stream = input.load(rehash=True, dedup=True, input_key="text")
    if patterns:
        matcher = patterns.load(nlp=nlp, label=label, allow_overlap=True)
        stream = (eg for _, eg in matcher(stream))

    if set_annotations:
        stream = prodigy.recipes.spans.preprocess_stream(
            stream, nlp, labels=labels, key=key, set_annotations=set_annotations
        )
    else:
        stream = prodigy.recipes.spans.add_tokens(
            nlp, stream, use_chars=highlight_chars
        )

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "dataset": dataset.name,
        "stream": stream,
        "update": prodigy.recipes.spans.get_update(nlp, key=key)
        if update_model
        else None,
        "view_id": "spans_manual",
        "exclude": exclude_names,
        "config": {
            "labels": label,
            "lang": nlp.lang,
            "ner_manual_highlight_chars": highlight_chars,
            "feed_overlap": goal == "overlap",
        },
    }
