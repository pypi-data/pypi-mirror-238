#!/usr/bin/env python

__author__ = "Svein Tore Eikeskog"
__email__ = "st@eikeskog.com"

import json
import requests
import calendar
from datetime import datetime


########################################################################################################################


class Github_repos(object):
    def __init__(self, token):
        self.repo_url = "https://api.github.com/repos"
        self.headers = {
             'Accept': 'application/vnd.github+json',
             'Authorization': f'Bearer {token}',
             'X-GitHub-Api-Version': '2022-11-28'
             }
        self.pull_number = None
        self.pr_state = "unknown"

    def get_pr(self, url):
        if not isinstance(self.pull_number, int):
            return

        url = f"{self.repo_url}/{url}/pulls/{self.pull_number}"
        r = requests.get(url,headers=self.headers)
        self.pr_state = r.json().get("state")

    def get_pr_state(self, url, pull_number):
        self.pr_state = "unknown"
        self.pull_number = pull_number

        self.get_pr(url)
        return self.pr_state

    def get_milestones(self, url):
        result = None
        r = requests.get(url, headers=self.headers)
        if r:
            try:
                result = r.json()
            except:
                pass
        return result

    def get_duedate(self, t):
        try:
            year, month, period = t.split("-")
        except:
            return

        if int(period) == 1:
            return f"{year}-{month}-14T23:59:59Z"

        dt = datetime(int(year), int(month), int(period))
        res = calendar.monthrange(dt.year, dt.month)
        day = res[1]
        return f"{year}-{month}-{day}T23:59:59Z"

    def create_milestone(self, url, title):
        result = None
        due_date = self.get_duedate(title)
        if not due_date:
            return

        payload = {"title": title, "state": "open", "due_on": due_date}

        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if not r:
            # Creating milestone for repo failed.
            # Probably exists.
            return

        try:
            result = r.json()
        except:
            # Creating milestone for repo failed.
            # Unknown error.
            pass

        return result
