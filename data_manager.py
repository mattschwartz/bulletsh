import json
from pathlib import Path
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


class DataManager():
    def load_data(self, file_path):
        with open(file_path) as file:
            json_data = file.read()
            self.loaded_data = json.loads(json_data)


DATA_DIR = './data'

observer = Observer()
manager = DataManager()
fs_handler = DataLoaderFsEventHandler(manager, DATA_DIR)


def get_data():
    return manager.loaded_data


def start():
    dirpath = Path(DATA_DIR)
    for file_path in dirpath.iterdir():
        manager.load_data(str(file_path))

    observer.schedule(fs_handler, DATA_DIR)
    observer.start()


def stop():
    observer.stop()
    observer.join()
