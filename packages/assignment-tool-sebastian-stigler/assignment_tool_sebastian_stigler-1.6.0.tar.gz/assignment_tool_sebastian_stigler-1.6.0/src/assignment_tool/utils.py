import os.path
from base64 import b64decode
from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Assignment:
    name: str = ""
    path: str = ""
    base_filename: str = ""
    download_source: bool = False
    course_path: str = ""

    @property
    def assignment_path(self):
        return os.path.join(self.course_path, self.path)


@dataclass
class Url:
    lms: str
    compiler: str


@dataclass_json
@dataclass
class CheckResult:
    basename: str = ""
    tmp_name: str = ""
    disp_cmd: str = ""
    base64_output: List[str] = field(default_factory=list)
    rc: int = -1
    filename_format_ok: bool = True
    status_code: int = 0
    msg: str = ""

    @property
    def failed(self):
        return len(self.base64_output) > 0 or self.rc != 0

    @property
    def output(self):
        result = []
        for line in self.base64_output:
            result.append(b64decode(line.encode()).decode())
        return "\n".join(result)
