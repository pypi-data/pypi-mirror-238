import enum
from datetime import datetime, timedelta
from typing import Optional
from typing import List
import inspect
from abc import abstractmethod
from functools import wraps
import pydantic


class SnapshotProfile(pydantic.BaseModel):
    dag_name: str
    owner: List[str]
    start_date: datetime
    retries: int
    retry_delay: timedelta
    depends_on_past: bool = False
    schedule_interval: str
    container_name: str = 'default'



class Task(pydantic.BaseModel):
    task_id: str
    upstream_dependencies: List[str]  # upstream dependency task ids
    method_name: str


def task(task_id, upstream_dependencies,):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not isinstance(result, str):
                raise TypeError("task function should return string")
            return result

        task_obj = Task(
            task_id=task_id,
            upstream_dependencies=upstream_dependencies,
            method_name=f.__name__,
        )
        wrapper.task = task_obj
        return wrapper
    return decorator


class BaseSM:
    @classmethod
    def parse_task(
            cls,
    ) -> List[Task]:
        tasks = []
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        task_methods = [
            method for _, method in methods if hasattr(method, "task")
        ]
        tasks = [method.task for method in task_methods]
        return tasks

    @classmethod
    @abstractmethod
    def profile(cls) -> SnapshotProfile:
        pass

    @classmethod
    def _has_cycle(cls):
        tasks = cls.parse_task()
        visited = set()
        stack = set()

        def dfs(
                node: Task,
        ):
            task_id = node.task_id
            visited.add(task_id)
            stack.add(task_id)

            for dependency in node.upstream_dependencies:
                if dependency not in visited:
                    if dfs(
                            next(filter(lambda x: x.task_id == dependency, tasks)),
                    ):
                        return True
                elif dependency in stack:
                    return True
            stack.remove(task_id)
            return False

        for t in tasks:
            if t.task_id not in visited:
                if dfs(t):
                    return True
        return False
