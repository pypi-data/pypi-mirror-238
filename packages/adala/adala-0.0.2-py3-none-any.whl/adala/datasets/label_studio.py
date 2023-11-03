import json
import label_studio_sdk

from pprint import pprint
from .base import Dataset, InternalDataFrame
from pydantic import model_validator, SkipValidation
from label_studio_sdk.project import LabelStudioException, Project
from typing import Optional, List, Dict


class LabelStudioFormatMixin:

    def _tasks_to_df(
        self,
        tasks,
        include_annotations: bool = True,
        only_annotated: bool = False,
        ground_truth_column: str = 'ground_truth'
    ):
        indices, records = [], []
        for task in tasks:
            record = task['data']
            if only_annotated and not task['annotations']:
                continue

            if (only_annotated or include_annotations) and task['annotations']:
                # TODO: expand more complex annotations
                if len(task['annotations']) > 1:
                    raise NotImplementedError('Multiple annotations are not supported yet')
                annotation = task['annotations'][0]
                annotation_type = annotation['result'][0]['type']
                if annotation_type == 'textarea':
                    annotation_type = 'text'
                if len(annotation['result']) > 1:
                    raise NotImplementedError('Multiple results per annotation are not supported yet')
                label = annotation['result'][0]['value'][annotation_type]
                if isinstance(label, list):
                    if len(label) == 1:
                        label = label[0]
                    else:
                        label = ','.join(sorted(label))
                else:
                    label = str(label)
                record[ground_truth_column] = label

            index = task['id']
            records.append(record)
            indices.append(index)
        return InternalDataFrame(records, index=indices)


class LabelStudioDataset(Dataset, LabelStudioFormatMixin):

    label_studio_url: str
    label_studio_api_key: str
    label_studio_project_id: int

    ground_truth_column: str = 'ground_truth'

    _project_client: SkipValidation[Project] = None

    @model_validator(mode='after')
    def init_client(self):
        if self._project_client is None:
            client = label_studio_sdk.Client(
                url=self.label_studio_url,
                api_key=self.label_studio_api_key
            )
            self._project_client = client.get_project(id=self.label_studio_project_id)
        return self

    def get_project_info(self):
        return self._project_client.get_params()

    def info(self) -> None:
        pprint(self.get_project_info())

    def __len__(self):
        info = self.get_project_info()
        return info['task_number']

    def batch_iterator(self, batch_size: int = 100) -> InternalDataFrame:
        page = 1
        while True:
            try:
                data = self._project_client.get_paginated_tasks(page=page, page_size=batch_size)
                yield self._tasks_to_df(data['tasks'], include_annotations=False)
                page += 1
            # we'll get 404 from API on empty page
            except LabelStudioException as e:
                break

    def get_ground_truth(self, batch: Optional[InternalDataFrame] = None) -> InternalDataFrame:
        if batch is None:
            labeled_tasks = self._project_client.get_labeled_tasks()
            gt = self._tasks_to_df(labeled_tasks, only_annotated=True, ground_truth_column='ground_truth')
            return gt
        else:
            # TODO: not the most effective method - better to send subset of indices to LS API
            labeled_tasks = self._project_client.get_labeled_tasks()
            gt = self._tasks_to_df(labeled_tasks, only_annotated=True, ground_truth_column='ground_truth')
            return gt[gt.index.isin(batch.index)]


class LabelStudioFileDataset(Dataset, LabelStudioFormatMixin):
    label_studio_file: str
    ground_truth_column: str = 'ground_truth'

    _data: List[Dict] = None

    @model_validator(mode='after')
    def load_data(self):
        with open(self.label_studio_file) as f:
            self._data = json.load(f)
        return self

    def batch_iterator(self, batch_size: int = 100) -> InternalDataFrame:
        for i in range(0, len(self._data), batch_size):
            batch = self._data[i:i+batch_size]
            yield self._tasks_to_df(batch, include_annotations=False)

    def get_ground_truth(self, batch: Optional[InternalDataFrame]) -> InternalDataFrame:
        return self._tasks_to_df(self._data, only_annotated=True, ground_truth_column='ground_truth')

    def __len__(self):
        return len(self._data)

    def info(self) -> None:
        print(f'Total Label Studio tasks loaded: {len(self)}')
