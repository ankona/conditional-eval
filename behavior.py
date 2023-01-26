import typing as t

class Behavior(t.Protocol):
    def execute(self) -> None:
        ...

    def __call__(self, *args: t.Any, **kwds: t.Any) -> t.Any:
        self.execute()


class PrintBehavior(Behavior):
    def __init__(self, msg: str) -> None:
        self._msg = msg

    def execute(self) -> None:
        print(f"\tExecuting mock action: {self._msg}")


class PublishBehavior(Behavior):
    def __init__(self, queue_name: str) -> None:
        self._queue_name = queue_name

    def execute(self) -> None:
        print(f"\tPublishing mock message to celery queue: {self._queue_name}")
