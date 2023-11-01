from typing import Callable, List, Literal, Optional, Tuple, Union

import prodigy.recipes.rel
from prodigy.models.matcher import PatternMatcher
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    BlankModel,
    BoolProps,
    ChoiceProps,
    Dataset,
    Goal,
    Input,
    InputDataset,
    ListProps,
    Patterns,
    UseModel,
    props,
    task_recipe,
    teams_type,
)
from spacy.tokens import Doc


def setup_matchers(
    pattern_matcher: PatternMatcher,
) -> Callable[[Doc], List[Tuple[int, int, int]]]:
    # Hacky way to access matcher and phrase matcher from loaded patterns
    # Possible refactor in future?
    def combined_matcher(doc: Doc) -> List[Tuple[int, int, int]]:
        matches = []
        for matcher in pattern_matcher.matchers:
            matches.extend(matcher(doc))
        return matches

    return combined_matcher


@teams_type(
    field_props={
        "add_ents": BoolProps(title="Add named entities predicted by the model"),
        "add_nps": BoolProps(title="Add noun phrases predicted by the model"),
    },
    exclude={"update"},
)
class RelationsModel(UseModel):
    add_ents: bool = False
    add_nps: bool = False


@task_recipe(
    title="Relation Extraction",
    description="Annotate relations between tokens and spans. Also supports joint span and relation annotation.",
    view_id="relations",
    field_props={
        # fmt: off
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "span_label": ListProps(title="Span label(s)", description="Comma-separated list of span labels to annotate", placeholder="Type labels here..."),
        "disable_patterns": ChoiceProps(title="Disable patterns", description="Use patterns to disable tokens. Disabled tokens are unselectable. This helps guide annotators towards considering only valid options. Can be uploaded to your cluster."),
        "goal": props.goal,
        "patterns": props.patterns,
        "exclude": props.exclude,
        # fmt: on
    },
    cli_names={
        "model-blank.lang": "model.lang",
        "model-relationsmodel.name": "model.name",
        "model-relationsmodel.add-ents": "model.add-ents",
        "model-relationsmodel.add-nps": "model.add-nps",
    },
)
def relations(
    *,
    dataset: Dataset[Literal["rel"]],
    model: Union[BlankModel, RelationsModel],
    input: Input,
    label: List[str],
    span_label: Optional[List[str]] = None,
    patterns: Optional[Patterns] = None,
    disable_patterns: Optional[Patterns] = None,
    exclude: Optional[List[InputDataset]] = None,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    add_nps = False
    add_ents = False
    if isinstance(model, RelationsModel):
        spacy_model = model.name
        assert spacy_model.path is not None
        nlp = spacy_model.load()
        add_ents = model.add_ents
        add_nps = model.add_nps
    else:
        nlp = model.load()
    stream = input.load(rehash=True, dedup=True, input_key="text")
    prodigy.recipes.rel.check_nlp(nlp, add_ents=add_ents, add_nps=add_nps)
    if add_nps and span_label and prodigy.recipes.rel.NP_LABEL not in span_label:
        # Add NP label if we know we need it and user hasn't set it
        span_label.append(prodigy.recipes.rel.NP_LABEL)
    # Set up combined token/phrase matchers with additional merge and disable patterns
    matcher = None
    disable_matcher = None
    if patterns:
        matcher = setup_matchers(patterns.load(nlp=nlp))
    if disable_patterns:
        disable_matcher = setup_matchers(disable_patterns.load(nlp=nlp))
    stream = prodigy.recipes.rel.preprocess_stream(
        stream,
        nlp,
        matcher=matcher,
        disable_matcher=disable_matcher,
        span_label=span_label,
        add_nps=add_nps,
        add_ents=add_ents,
    )

    exclude_names = [ds.name for ds in exclude] if exclude is not None else None

    return {
        "view_id": "relations",
        "dataset": dataset.name,
        "stream": stream,
        "exclude": exclude_names,
        "config": {
            "lang": nlp.lang,
            "labels": label,
            "relations_span_labels": span_label,
            "exclude_by": "input",
            "custom_theme": {"cardMaxWidth": "90%"},
            "feed_overlap": goal == "overlap",
        },
    }
