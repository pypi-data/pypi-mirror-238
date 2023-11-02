from datetime import timedelta, datetime
from quantit_snapshot.base import SnapshotProfile, task, BaseSM


class SM(BaseSM):
    @classmethod
    def profile(cls) -> SnapshotProfile:
        return SnapshotProfile(
            dag_name="sample_sm",
            owner=["dksung"],
            start_date=datetime(2021, 1, 1),
            retries=3,
            retry_delay=timedelta(minutes=5),
            depends_on_past=False,
            schedule_interval="0 0 * * *",

        )

    @task(task_id="taskA", upstream_dependencies=[])
    def task_A(self):
        return "bash -c 'sleep 3 && echo Task A is executed"

    @task(task_id="taskB", upstream_dependencies=["taskA"])
    def task_B(self):
        return "bash -c 'sleep 3 && echo Task B is executed"

    @task(task_id="taskC", upstream_dependencies=["taskB"])
    def task_C(self):
        return "bash -c 'sleep 3 && echo Task C is executed"


def test_parse_task():
    tasks = SM.parse_task()
    print(tasks)
    assert len(tasks) == 3, "SampleSM should have 3 tasks"


def test_tasks_execution(capsys):
    sample_sm = SM()
    sample_sm.task_A()
    sample_sm.task_B()
    sample_sm.task_C()


def test_profile():
    profile = SM.profile()
    assert isinstance(profile, SnapshotProfile), "SampleSM profile should return SnapshotProfile"


def test_has_cycle():
    has_cycle = SM._has_cycle()
    assert has_cycle is False, "SampleSM should not have a cycle"
