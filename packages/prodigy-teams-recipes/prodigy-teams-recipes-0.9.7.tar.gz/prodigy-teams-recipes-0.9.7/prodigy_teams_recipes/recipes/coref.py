from typing import List, Literal, Optional

import prodigy.recipes.coref
import prodigy.recipes.rel
from prodigy.errors import RecipeError
from prodigy.models.matcher import PatternMatcher, PatternType
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    BoolProps,
    Dataset,
    Goal,
    Input,
    InputDataset,
    ListProps,
    UseModel,
    props,
    task_recipe,
    teams_type,
)

from .rel import setup_matchers


@teams_type(
    field_props={
        "add_ents": BoolProps(title="Add named entities predicted by the model"),
        "add_nps": BoolProps(title="Add noun phrases predicted by the model"),
    },
    exclude={"update"},
)
class CorefModel(UseModel):
    add_ents: bool = False
    add_nps: bool = False


@task_recipe(
    title="Coreference Resolution",
    description='Annotate coreference, i.e. links of ambiguous mentions like "her" or "the woman" back to an antecedent providing more context about the entity in question',
    view_id="relations",
    field_props={
        # fmt: off
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "pos_tags": ListProps(title="Part-of-speech tags", description="List of coarse-grained POS tags to enable for annotation", placeholder="Type labels here..."),
        "poss_pron_tags": ListProps(title="Possessive pronoun tags", description="List of fine-grained tag values for possessive pronoun to use in patterns", placeholder="Type labels here..."),
        "ner_labels": ListProps(title="Named entity labels", description="List of NER labels to use if model has entity recognizer"),
        "show_arrow_heads": BoolProps(title="Show the arrow heads visually", description="If disabled, relations will be shown as lines instead of directional arrows"),
        "goal": props.goal,
        "exclude": props.exclude,
        # fmt: on
    },
)
def coref(
    *,
    dataset: Dataset[Literal["rel"]],
    model: CorefModel,
    input: Input,
    label: List[str] = prodigy.recipes.coref.DEFAULT_LABELS,
    pos_tags: List[str] = prodigy.recipes.coref.DEFAULT_POS,
    poss_pron_tags: List[str] = prodigy.recipes.coref.DEFAULT_POSS_PRON,
    ner_labels: List[str] = prodigy.recipes.coref.DEFAULT_NER_LABELS,
    exclude: Optional[List[InputDataset]] = None,
    show_arrow_heads: bool = False,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    """Create training data for coreference resolution. Coreference resolution
    is the challenge of linking ambiguous mentions such as "her" or "that woman"
    back to an antecedent providing more context about the entity in question.

    This recipe allows you to focus on nouns, proper nouns and pronouns
    specifically, by disabling all other tokens. You can customize the labels
    used to extract those using the recipe arguments.
    """
    spacy_model = model.name
    nlp = spacy_model.load()
    add_ents = model.add_ents
    add_nps = model.add_nps
    if "tagger" not in nlp.pipe_names:
        raise RecipeError(
            "No tagger found in pipeline",
            "The provided model should have a 'tagger' component to allow "
            "pattern matching on the POS tags for efficient coreference annotation.",
        )
    stream = input.load(rehash=True, dedup=True, input_key="text")
    prodigy.recipes.rel.check_nlp(nlp, add_ents=add_ents, add_nps=add_nps)
    patterns: list[PatternType] = [
        {
            "label": prodigy.recipes.coref.NP_LABEL,
            "pattern": [
                {"POS": "DET", "TAG": {"NOT_IN": poss_pron_tags}, "OP": "?"},
                {"POS": "ADJ", "OP": "*"},
                # Proper nouns but no entities, otherwise this custom pattern
                # would overwrite them
                {
                    "POS": {"IN": ["PROPN", "NOUN"]},
                    "OP": "+",
                    "ENT_TYPE": {"NOT_IN": ner_labels},
                },
            ],
            "id": None,
        }
    ]
    # Other POS tags but no tokens in our previously matched NPs
    disable_token = {
        "POS": {"NOT_IN": pos_tags},
        "_": {"label": {"NOT_IN": [prodigy.recipes.coref.NP_LABEL]}},
    }
    # Set up combined token/phrase matchers with additional merge and disable patterns
    matcher = PatternMatcher(nlp, combine_matches=True, all_examples=True)
    matcher.add_patterns(patterns)
    disable_matcher = PatternMatcher(nlp, combine_matches=True, all_examples=True)
    disable_matcher.add_patterns(
        [{"pattern": [disable_token], "label": "", "id": None}]
    )
    stream = prodigy.recipes.rel.preprocess_stream(
        stream,
        nlp,
        matcher=setup_matchers(matcher),
        disable_matcher=setup_matchers(disable_matcher),
        span_label=None,
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
            "exclude_by": "input",
            "custom_theme": {"cardMaxWidth": "90%"},
            "hide_relation_arrow": not show_arrow_heads,
            "feed_overlap": goal == "overlap",
            "wrap_relations": True,
        },
    }
