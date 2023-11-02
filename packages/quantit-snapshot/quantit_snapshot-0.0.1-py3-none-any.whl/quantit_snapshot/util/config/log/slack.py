import json
import sys
import requests
import traceback

from quantit_snapshot.base.setting.settings import (
    SNAPSHOT_S3_BUCKET_CONFIG,
    SNAPSHOT_AWS_S3_KEY,
    SNAPSHOT_AWS_S3_SECRET_KEY
)
from quantit_snapshot.util.cloud.aws.s3_quanda_ex import S3QuandaEx

SPLIT_LENGTH = 4000
F_NAME = "slack.json"
CHANNEL_MON_PROD_SM = "mon_prod_sm"


def _get_webhook_addr():
    data = S3QuandaEx.get_data(
        F_NAME,
        SNAPSHOT_S3_BUCKET_CONFIG,
        SNAPSHOT_AWS_S3_KEY,
        SNAPSHOT_AWS_S3_SECRET_KEY
    )
    if data is None:
        return {}
    slack_info = json.loads(data)
    return slack_info


def get_webhook_addr(workspace: str, receiver: str):
    return _get_webhook_addr()[workspace][receiver]


def register_webhook_addr(workspace: str, receiver: str, webhook_addr: str):
    webhook_addr = {workspace: {receiver: webhook_addr}}
    all_webhook_addr = _get_webhook_addr()
    try:
        assert receiver not in all_webhook_addr[workspace].keys(), f"workspace {workspace} already exist."
    except KeyError:  # newly registered
        all_webhook_addr.update(webhook_addr)

    all_webhook_addr[workspace].update(
        webhook_addr[workspace]
    )
    S3QuandaEx.put_data(
        json.dumps(all_webhook_addr),
        F_NAME,
        SNAPSHOT_S3_BUCKET_CONFIG,
        SNAPSHOT_AWS_S3_KEY,
        SNAPSHOT_AWS_S3_SECRET_KEY
    )


def send_error(receiver=None, title=sys.argv[0], workspace="quantit"):
    def wrapper(f):
        def inner_wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except Exception as e:
                if receiver is not None:
                    send_slack(
                        receiver=receiver, title=title, text=traceback.format_exc(),
                        workspace=workspace, codeblock=True
                    )
                send_slack(
                    receiver=CHANNEL_MON_PROD_SM, title=title, text=traceback.format_exc(),
                    workspace=workspace, codeblock=True
                )
                raise e

        return inner_wrapper

    return wrapper


def split2len(s, n):
    def _f(s, n):
        if not s:
            yield ""
        while s:
            try:
                if len(s) <= n:
                    split_index = n
                else:
                    split_index = s[:n].rindex("\n") + 1
            except ValueError:  # if not exist \n in splited text
                split_index = n
            yield s[:split_index]
            s = s[split_index:]

    return list(_f(s, n))


def send_slack(
        receiver,
        title,
        text,
        workspace="quantit",
        codeblock=False,
        textmode=False,
        color="#36a64f",
):
    text_list = split2len(text, SPLIT_LENGTH)
    for i, split_text in enumerate(text_list):
        new_title = f"{title}" if i == 0 else f"{title} ({i})"
        new_text = f"```{split_text}```" if codeblock else split_text
        slack_msg = {"channel": receiver}
        if textmode:
            slack_msg["title"] = new_title
            slack_msg["text"] = new_text
        else:
            slack_msg["attachments"] = [
                {
                    "color": "#36a64f",
                    "title": new_title,
                    "text": new_text,
                    "mrkdwn": "true"
                }
            ]
            slack_msg["mrkdwn"] = "true"
        try:
            response = requests.post(
                get_webhook_addr(workspace, receiver),
                json.dumps(slack_msg),
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 200:
                raise ValueError(
                    "Request to slack returned an error %s, the response is:\n%s"
                    % (response.status_code, response.text)
                )
        except Exception as e:
            print(e)

