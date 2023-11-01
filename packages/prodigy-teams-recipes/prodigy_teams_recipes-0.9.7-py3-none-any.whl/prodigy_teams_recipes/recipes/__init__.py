# isort: skip_file
# The import order determines the order of recipes shown in the UI
from . import (
    # Annotation recipes
    ner,
    spans,
    textcat,
    rel,
    coref,
    dep,
    pos,
    terms,
    image,
    audio,
    curate,
    review,
    sent,
    test_task,
    # Action recipes
    db_actions,
    example_computations,
    train,
)

__all__ = [
    "audio",
    "dep",
    "image",
    "test_task",
    "ner",
    "pos",
    "rel",
    "coref",
    "review",
    "terms",
    "textcat",
    "sent",
    "spans",
    "curate",
    "db_actions",
    "example_computations",
    "train",
]
