import argparse
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


class Args(argparse.Namespace, metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @abstractmethod
    def parse(
            cls,
            default=datetime.today() - timedelta(days=1)
    ) -> argparse.Namespace:
        return


class SnapshotArgs(Args):
    @classmethod
    def parse(
            cls,
            default=datetime.today() - timedelta(days=1),
            default_item=None
    ) -> argparse.Namespace:
        default = datetime(default.year, default.month, default.day)
        parser = argparse.ArgumentParser()
        parser.add_argument("--item", default=default_item, nargs="*")
        parser.add_argument(
            "--date",
            default=default,
            type=lambda x: datetime.strptime(x, "%Y%m%d")
        )
        parser.add_argument("--from_valid", action="store_true")
        parser.add_argument("--dry", action="store_true")
        return parser.parse_args()
