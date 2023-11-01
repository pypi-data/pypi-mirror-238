from typing import Dict, List, Literal

from prodigy.components.db import connect
from prodigy.components.sorters import Probability
from prodigy.types import ScoredStreamType, TaskType
from prodigy.util import log, set_hashes
from prodigy_teams_recipes_sdk import (
    Dataset,
    ListProps,
    Model,
    Props,
    props,
    task_recipe,
)
from spacy.lexeme import Lexeme
from spacy.tokens import Doc
from spacy.vocab import Vocab


@task_recipe(
    title="Terminology List",
    description="Bootstrap a terminology list from word vectors. Terminology lists can be converted into patterns to help pre-select entity spans during annotation.",
    view_id="text",
    field_props={
        # fmt: off
        "dataset": props.dataset_choice,
        "seeds": ListProps(title="Seed Terms", description="Comma-separated list of 3 or more terms", min=3),
        "vectors": Props(title="Word Vectors", description="Loadable spaCy model with word vectors. If you have custom models, you can add them to your cluster."),
        # fmt: on
    },
)
def terms(
    *,
    dataset: Dataset[Literal["terms"]],
    seeds: List[str],
    vectors: Model,
) -> Dict:
    dataset_name = dataset.name
    unique_seeds = list(set(t.strip() for t in seeds if t != ""))
    seed_tasks = [set_hashes({"text": s, "answer": "accept"}) for s in unique_seeds]
    DB = connect()
    DB.add_examples(seed_tasks, datasets=[dataset_name])
    nlp = vectors.load()
    # add all words with vectors to lexeme cache
    for s in nlp.vocab.vectors:
        nlp.vocab[s]
    accept_words = unique_seeds
    reject_words = list()
    accept_doc = Doc(nlp.vocab, words=accept_words)
    reject_doc = Doc(nlp.vocab, words=reject_words)
    score = 0

    def predict(term: Lexeme) -> float:
        nonlocal accept_doc, reject_doc
        if len(accept_doc) == 0 and len(reject_doc) == 0:
            return 0.5
        if len(accept_doc) and accept_doc.vector_norm != 0.0:
            accept_score = max(term.similarity(accept_doc), 0.0)
        else:
            accept_score = 0.0
        if len(reject_doc) and reject_doc.vector_norm != 0:
            reject_score = max(term.similarity(reject_doc), 0.0)
        else:
            reject_score = 0.0
        score = accept_score / (accept_score + reject_score + 0.2)
        return max(score, 0.0)

    def update(answers: List[TaskType]) -> None:
        nonlocal accept_doc, reject_doc, score
        log(f"RECIPE: Update predictions with {len(answers)} answers", answers)
        accept_words = [t.text for t in accept_doc]
        reject_words = [t.text for t in reject_doc]
        for answer in answers:
            if answer["answer"] == "accept":
                score += 1
                accept_words.append(answer["text"])
            elif answer["answer"] == "reject":
                score -= 1
                reject_words.append(answer["text"])
        accept_doc = Doc(nlp.vocab, words=accept_words)
        reject_doc = Doc(nlp.vocab, words=reject_words)

    def stream_scored(stream: Vocab) -> ScoredStreamType:
        # We only want to use lowercase-only for languages that have case
        has_case = nlp.Defaults.writing_system.get("has_case", True)
        lexemes = [
            lex for lex in stream if lex.is_alpha and not has_case or lex.is_lower
        ]
        while True:
            seen = set(w.orth for w in accept_doc)
            seen.update(set(w.orth for w in reject_doc))
            lexemes = [
                w
                for w in lexemes
                # TODO: unignore this once spaCy is updated
                if w.orth not in seen and w.vector_norm  # pyright: ignore
            ]
            by_score = [(predict(lex), lex) for lex in lexemes]
            by_score.sort(reverse=True)
            for _, term in by_score:  # Need to predict in loop, as model changes
                score = predict(term)
                yield score, {"text": term.text, "meta": {"score": score}}

    stream = Probability(stream_scored(nlp.vocab))

    return {
        "dataset": dataset_name,
        "view_id": "text",
        "stream": stream,
        "update": update,
    }
