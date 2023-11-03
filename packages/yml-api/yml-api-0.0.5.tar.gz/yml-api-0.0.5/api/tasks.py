import traceback
import time
import datetime
from threading import Thread
from django.core.cache import cache
from uuid import uuid1
from .utils import to_csv_temp_file, to_xls_temp_file


class Task:

    def __init__(self):
        self.total = 0
        self.partial = 0
        self.progress = 0
        self.error = None
        self.file_path = None
        self.key = uuid1().hex
        self.save()
        self.sleep(1)

    def save(self):
        cache.set(self.key, dict(progress=self.progress, error=self.error, file_path=self.file_path), timeout=30)

    def next(self):
        self.partial += 1
        self.progress = int(self.partial / self.total * 100) if self.total else 0
        if self.progress == 100:
            self.progress = 99
        self.save()

    def iterate(self, iterable):
        self.total = len(iterable)
        for obj in iterable:
            self.next()
            yield obj

    def run(self):
        raise NotImplemented()

    def sleep(self, secs=1):
        time.sleep(secs)

    def to_xls_file(self, **sheets):
        return to_xls_temp_file(sheets)

    def to_csv_file(self, rows):
        return to_csv_temp_file(rows)


class TaskRunner(Thread):

    def __init__(self, task, *args, **kwargs):
        self.task = task
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            self.task.file_path = self.task.run()
            self.task.progress = 100
            self.task.save()
        except Exception as e:
            traceback.print_exc()
            self.task.error = 'Ocorreu um erro: {}'.format(str(e))
            self.task.save()
