from typing import List, Union

import prodigy.components.db
from prodigy.util import set_hashes
from prodigy_teams_recipes_sdk import (
    ChoiceProps,
    Dataset,
    Input,
    InputDataset,
    Props,
    action_recipe,
    teams_type,
)


@teams_type(
    "merge",
    title="Merge multiple datasets",
    field_props={
        "in_sets": Props(title="Datasets to merge", exists=True),
        "out_set": Props(title="New dataset", exists=False),
    },
)
class DatasetMerge:
    in_sets: List[InputDataset]
    out_set: Dataset

    def merge(self, db: prodigy.components.db.Database) -> None:
        data = []
        for dataset in self.in_sets:
            data.extend(dataset.load())
        db.add_dataset(str(self.out_set.id))
        db.add_examples(data, [str(self.out_set.id)])


@teams_type(
    "copy",
    title="Copy a dataset",
    field_props={
        # fmt: off
        "in_data": Props(title="Input data", description="Name of the resource to copy", exists=True),
        "out_set": Props(title="New dataset", description="Name of the new dataset to copy to", exists=False)
        # fmt: on
    },
)
class DatasetCopy:
    in_data: Union[InputDataset, Input]
    out_set: Dataset

    def copy(self, db: prodigy.components.db.Database) -> None:
        if isinstance(self.in_data, Input):
            data = []
            for eg in self.in_data.load():
                eg = set_hashes(eg)
                if "answer" not in eg:
                    eg["answer"] = "accept"
                data.append(eg)
        else:
            data = list(self.in_data.load())
        db.add_dataset(str(self.out_set.id))
        db.add_examples(data, [str(self.out_set.id)])


@action_recipe(
    title="Dataset operations",
    description="Merge, copy and export annotated data",
    field_props={"mode": ChoiceProps(title="Operation")},
    cli_names={
        "mode-copy.in-data-input-dataset": "copy.in-dataset",
        "mode-copy.in-data-input": "copy.in-asset",
        "mode-copy.out-set": "copy.out-set",
        "mode-merge.in-sets": "merge.in-sets",
        "mode-merge.out-sets": "merge.out-sets",
    },
)
def db_actions(*, mode: Union[DatasetCopy, DatasetMerge]) -> None:
    db = prodigy.components.db.connect()
    if isinstance(mode, DatasetCopy):
        mode.copy(db)
    elif isinstance(mode, DatasetMerge):
        mode.merge(db)
