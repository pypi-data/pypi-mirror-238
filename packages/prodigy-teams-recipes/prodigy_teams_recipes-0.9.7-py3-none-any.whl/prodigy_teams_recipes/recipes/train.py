import dataclasses
from typing import Dict, List, Optional, Tuple

import prodigy.recipes.train
from prodigy.errors import RecipeError
from prodigy_teams_recipes_sdk import (
    BoolProps,
    FloatProps,
    InputDataset,
    IntProps,
    ListProps,
    OptionalProps,
    action_recipe,
    props,
    teams_type,
)

# TODO: allow custom config
# TODO: save to cluster


@teams_type(
    title="Training data",
    description="Annotated data for the differnt components to train",
    field_props={
        # fmt: off
        "training": ListProps(title="Training datasets", exists=True, min=1),
        "evaluation": ListProps(title="Optional datasets to evaluate on", description="If no datasets are provided, a portion of the training data (defined as the eval split) is held back for evaluation", exists=True, min=0),
        # fmt: on
    },
)
@dataclasses.dataclass
class ComponentData:
    training: List[InputDataset]
    evaluation: Optional[List[InputDataset]] = None

    def load(self) -> Tuple[List[str], List[str]]:
        return (
            [str(d.name) for d in self.training],
            [str(d.name) for d in self.evaluation]
            if self.evaluation is not None
            else [],
        )


@teams_type(
    field_props={
        # fmt: off
        "ner": OptionalProps(title="Named Entity Recognizer datasets", optional_title="Train a Named Entity Recognizer"),
        "spancat": OptionalProps(title="Span Categorizer datasets", optional_title="Train a Span Categorizer"),
        "textcat": OptionalProps(title="Text Classifier (exclusive categories) datasets", optional_title="Train a Text Classifier (exclusive categories)"),
        "textcat_multilabel": OptionalProps(title="Text Classifier (non-exclusive categories) datasets", optional_title="Train a Text Classifier (non-exclusive categories)"),
        "tagger": OptionalProps(title="Part-of-speech Tagger datasets", optional_title="Train a Part-of-speech Tagger"),
        "parser": OptionalProps(title="Dependency Parser datasets", optional_title="Train a Dependency Parser"),
        "senter": OptionalProps(title="Sentence Segmenter datasets", optional_title="Train a Sentence Segmenter"),
        "coref": OptionalProps(title="Coreference Resolution datasets", optional_title="Train a Coreference Resolution component"),
        # fmt: on
    }
)
@dataclasses.dataclass
class Data:
    ner: Optional[ComponentData] = None
    spancat: Optional[ComponentData] = None
    textcat: Optional[ComponentData] = None
    textcat_multilabel: Optional[ComponentData] = None
    tagger: Optional[ComponentData] = None
    parser: Optional[ComponentData] = None
    senter: Optional[ComponentData] = None
    coref: Optional[ComponentData] = None

    def load(self) -> Dict[str, Tuple[List[str], List[str]]]:
        pipes = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if value is not None:
                pipes[field.name] = value.load()
        return pipes


@teams_type(
    title="Train Curve mode",
    field_props={
        # fmt: off
        "n_samples": IntProps(title="Number of samples to take", description="For example, 4 samples to train with 25, 50 and 100%", min=1, step=1),
        "show_plot": BoolProps(title="Show a visual plot of the curve in the logs"),
        # fmt: on
    },
)
class TrainCurve:
    n_samples: int = 1
    show_plot: bool = False


COMPONENTS = [f.name for f in dataclasses.fields(Data)]


@action_recipe(
    title="Train a spaCy pipeline",
    description="Train a spaCy model with one or more components on annotated data",
    field_props={
        # fmt: off
        "lang": props.lang,
        "eval_split": FloatProps(title="Portion of examples to split off for evaluation", description="This is applied if no dedicated evaluation datasets are provided for a component.", min=0.0, max=1.0, step=0.05),
        "label_stats": BoolProps(title="Show per-label scores", description="Will output an additional table for each component with scores for the individual labels"),
        "verbose": BoolProps(title="Enable verbose logging"),
        "train_curve": OptionalProps(title="Train curve", description="Train with different portions of the data to simulate how the model improves with more data", optional_title="Enable train curve diagnostics")
        # fmt: on
    },
    cli_names={
        **{f"data.{c}.training": f"{c}.train" for c in COMPONENTS},
        **{f"data.{c}.evaluation": f"{c}.eval" for c in COMPONENTS},
    },
)
def train(
    *,
    data: Data,
    lang: str = "en",
    eval_split: float = 0.2,
    label_stats: bool = False,
    verbose: bool = False,
    train_curve: Optional[TrainCurve] = None,
) -> None:
    """
    Train a spaCy pipeline from one or more datasets for different components
    or run training diagnostics to check if more annotations improve the model.
    """
    prodigy.recipes.train.set_log_level(verbose=verbose)
    pipes = data.load()
    if not pipes:
        raise RecipeError("No components to train")
    elif train_curve is not None and train_curve.n_samples > 1:
        prodigy.recipes.train._train_curve(
            pipes,
            eval_split=eval_split,
            n_samples=train_curve.n_samples,
            show_plot=train_curve.show_plot,
        )
    else:
        train_config = prodigy.recipes.train._prodigy_config(
            pipes, None, lang=lang, eval_split=eval_split, verbose=verbose
        )
        prodigy.recipes.train._train(
            train_config, overrides={}, gpu_id=-1, show_label_stats=label_stats
        )
