from enum import Enum
import json
from datetime import date
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DataLoaderFsEventHandler(FileSystemEventHandler):
    def __init__(self, manager, data_dir):
        super().__init__()
        self.manager = manager
        self.data_dir = data_dir

    def on_any_event(self, event):
        if not event.is_directory:
            self.manager.load_data(event.src_path)


class TaskType(Enum):
    TASK = 'task'
    NOTE = 'note'


@dataclass
class JacketTask:
    task_type: TaskType
    is_completed: bool
    is_cancelled: bool
    is_migrated_fwd: bool
    is_migrated_bwd: bool
    text: str


@dataclass
class JacketPage:
    date: date
    tasks: List[JacketTask]

    def date_str(self) -> str:
        return self.date.strftime('%a %d %b')


class JacketData:
    pages: List[JacketPage] = []
    pages_by_year: Dict[int, List[JacketPage]] = {}

    def add_page(self, page: JacketPage):
        self.pages.append(page)
        if page.date.year not in self.pages_by_year.keys():
            self.pages_by_year[page.date.year] = []

        self.pages_by_year[page.date.year].append(page)

    def sorted_pages(self) -> List[JacketPage]:
        return sorted(self.pages, reverse=True, key=lambda i: i.date)

    def get_years(self):
        return self.pages_by_year.keys()

    def pages_by_month(self, year):
        if year not in self.pages_by_year.keys():
            return None

        result = {}
        for page in self.pages_by_year[year]:
            month = page.date.month
            if month not in result.keys():
                result[month] = []

            result[month].append(page)

        return result


class DataManager():

    jacket_data: JacketData = None

    def load_data(self, file_path):
        with open(file_path) as file:
            json_data = file.read()
            self.convert_data(json.loads(json_data))

    def convert_data(self, loaded_data):
        self.jacket_data = JacketData()
        for data_page in loaded_data["pages"]:
            tasks = []
            for data_task in data_page["tasks"]:
                tasks.append(JacketTask(
                    task_type=TaskType(data_task["type"]),
                    is_completed=data_task["isCompleted"],
                    is_cancelled=data_task["isCancelled"],
                    is_migrated_fwd=False,
                    is_migrated_bwd=False,
                    text=data_task["text"]
                ))

            page = JacketPage(
                date=date.fromisoformat(data_page["date"]),
                tasks=tasks)
            self.jacket_data.add_page(page)


DATA_DIR = './data'

observer = Observer()
manager = DataManager()
fs_handler = DataLoaderFsEventHandler(manager, DATA_DIR)


class DataAccessor:

    data_manager: DataManager

    def __init__(self) -> None:
        self.data_manager = manager

    def get_data(self) -> JacketData:
        return self.data_manager.jacket_data


def start():
    dirpath = Path(DATA_DIR)
    for file_path in dirpath.iterdir():
        manager.load_data(str(file_path))

    observer.schedule(fs_handler, DATA_DIR)
    observer.start()


def stop():
    observer.stop()
    observer.join()
