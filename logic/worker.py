from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool


class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)


class Worker(QRunnable):
    def __init__(self, loader_func):
        super().__init__()
        self.loader_func = loader_func
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        try:
            result = self.loader_func()
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))


def start_worker_task(task_function, finished_slot, error_slot):
    worker = Worker(task_function)
    worker.signals.finished.connect(finished_slot)
    worker.signals.error.connect(error_slot)

    thread_pool = QThreadPool.globalInstance()
    thread_pool.start(worker)
