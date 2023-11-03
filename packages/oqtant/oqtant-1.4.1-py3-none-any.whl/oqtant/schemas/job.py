# Copyright 2023 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from bert_schemas import job as job_schema
from dateutil import parser as date_parser
from dateutil import tz
from pydantic import computed_field, conlist

SIG_ABS = 0.297


def print_keys(subject: Any, indent: int = 0, drill_lists=False):
    """
    Print the keys of a nested dictionary or list.

    Args:
        subject (Any): The subject to print the keys of.
        indent (int, optional): The number of spaces to indent. Defaults to 0.
        drill_lists (bool, optional): Whether to drill into lists. Defaults to False.

    Returns:
        None
    """
    if isinstance(subject, dict):
        for key, value in subject.items():
            print(f"{' ' * indent}- {key}")
            if isinstance(value, dict):
                print_keys(value, indent=indent + 2, drill_lists=drill_lists)
            if isinstance(value, list) and drill_lists:
                for list_value in value:
                    if isinstance(list_value, dict):
                        print_keys(
                            list_value, indent=indent + 2, drill_lists=drill_lists
                        )


class OqtantJob(job_schema.JobBase):
    active_run: int = 1
    external_id: UUID | None = None
    time_submit: str | datetime | None = None
    input_count: int | None = None
    run: int | None = None
    inputs: conlist(
        job_schema.Input,
        min_length=1,
        max_length=30,
    )

    @computed_field
    @property
    def job_type(self) -> job_schema.JobType:
        if self.inputs[0].values.optical_landscape:
            return job_schema.JobType.PAINT_1D
        elif (
            self.inputs[0].values.optical_barriers
            or self.inputs[0].values.image_type == job_schema.ImageType.IN_TRAP
        ):
            return job_schema.JobType.BARRIER
        else:
            return job_schema.JobType.BEC

    @property
    def truncated_name(self):
        if len(self.name) > 40:
            return f"{self.name[:37]}..."
        return self.name

    @property
    def id(self):
        return self.external_id

    @property
    def formatted_time_submit(self):
        return self.format_datetime(self.time_submit)

    @staticmethod
    def format_datetime(datetime_value: str | datetime):
        try:
            parsed_datetime = date_parser.parse(datetime_value)
            parsed_datetime = parsed_datetime.replace(tzinfo=tz.tzutc())
            parsed_datetime = parsed_datetime.astimezone(tz.tzlocal())
        except Exception:
            parsed_datetime = datetime_value
        return parsed_datetime.strftime("%d %b %Y, %H:%M:%S")

    @property
    def input_fields(self):
        print_keys(self.input.dict(), drill_lists=True)

    @property
    def input(self):
        return self.inputs[self.active_run - 1].values

    @property
    def lifetime(self):
        return self.input.end_time_ms

    def add_notes_to_input(self, notes: str):
        self.inputs[self.active_run - 1].notes = notes
