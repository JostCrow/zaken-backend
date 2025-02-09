import json
import logging
from itertools import chain

import requests
from api.case import Case
from api.events import CaseEvent, CitizenReportEvent

logger = logging.getLogger(__name__)


class Client:
    authenticated = False
    headers = None

    def __init__(self, config):
        self.host = config["host"]
        if "://api.wonen.zaken.amsterdam.nl/" in self.host:
            raise Exception(f"Host ({self.host}) not allowed")

    def request(self, verb, url, headers=None, json=None, task_name="SYSTEM"):
        url = f"{self.host}{url}"
        logger.info(
            f"{verb.upper()} on '{url}' with headers:\n{headers}\nand json:\n{json}\n"
        )

        res = requests.request(verb, url=url, headers=headers, json=json)

        logger.info(
            f"Response {task_name} api status:{res.status_code} with text:\n{res.text[:5000]}\n"
        )

        if not res.ok:
            raise Exception(
                f"Error {task_name}: status: {res.status_code} on url: {url} with data: {json}"
            )

        return res.json()

    def call(self, verb, url, json=None, task_name="SYSTEM"):
        if not self.authenticated:
            response = self.request(
                "post",
                "/oidc-authenticate/",
                json={"code": "string"},
                task_name=task_name,
            )
            self.headers = {"Authorization": f"Bearer {response['access']}"}
            self.authenticated = True
        return self.request(
            verb, url, headers=self.headers, json=json, task_name=task_name
        )

    def get_case_tasks(self, case_id):
        response = self.call("get", f"/cases/{case_id}/tasks/")
        lists = map(lambda x: x["tasks"], response["results"])
        flat_list = list(chain.from_iterable(lists))

        logging.info(f"Open tasks for case id {case_id}:")
        logging.info(f"{json.dumps(flat_list, sort_keys=True, indent=4)}\n\n")

        return flat_list

    def get_case_events(self, case_id):
        return self.call("get", f"/cases/{case_id}/events/")

    def get_close_reasons(self, theme):
        return self.call("get", f"/themes/{theme}/case-close-reasons/")["results"]

    def get_names_from_tasks(self, tasks):
        return list(map(lambda task: task["task_name"], tasks))

    def create_case(self, data):
        events = [CaseEvent]

        if "citizen_reports" in data and data["citizen_reports"]:
            events.append(CitizenReportEvent)

        return Case(
            self.call("post", "/cases/", data, task_name="create_case"), self, events
        )
