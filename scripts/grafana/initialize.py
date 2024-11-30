#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import json
import glob


class Main(object):
    def __init__(self, address=None, username="admin", password="admin"):
        self.address = address
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.auth = requests.auth.HTTPBasicAuth(
            username, password
        )

    def initialize(self):
        self.address = os.environ.get("GRAFANA_URL")
        if self.address is None:
            return

        print("token: {0}".format(self.get_token()))
        if self.get_token() is None:
            return

        data_source_url = os.environ.get("DATA_SOURCE_URL")
        if data_source_url is not None:
            print("add data source: {0}".format(self.add_data_source(data_source_url)))

        self.walk_dashboard_path()

    def get_orgs(self):
        request = requests.get("{0}/api/orgs".format(self.address), auth=self.auth, timeout=5)
        response_data = json.loads(request.text)
        print(json.dumps(response_data, indent=4))

    def get_current_user(self):
        request = requests.get("{0}/api/user".format(self.address), auth=self.auth, timeout=5)
        response_data = json.loads(request.text)
        print(json.dumps(response_data, indent=4))

    def get_token(self):
        token_file = "{0}/token.json".format(self.current_path)
        if os.path.exists(token_file) is False:
            self.create_token()

        if os.path.exists(token_file) is True:
            token_json = json.loads(open(token_file, "r").read())
            return token_json.get("key")
        return None

    def create_token(self):
        request_headers = {"Content-Type": "application/json"}
        request_data = json.dumps({"name": "token", "role": "Admin"})
        request = requests.post("{0}/api/auth/keys".format(self.address),
                                auth=self.auth, headers=request_headers, data=request_data, timeout=5)
        response_data = json.loads(request.text)
        with open("{0}/token.json".format(self.current_path), "w") as f:
            f.write(json.dumps(response_data))
        print("create token done")

    def get_user_list(self, login=None):
        request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.get_token())
        }
        request = requests.get("{0}/api/users".format(self.address),
                               auth=self.auth, headers=request_headers, timeout=5)
        response_data = json.loads(request.text)
        if login is not None and login != "":
            for v in response_data:
                if v["login"] == login:
                    return v
            return None
        for v in response_data:
            print(v)

    def modify_user_is_admin(self, name=None):
        user = self.get_user_list(login=name)
        if user is not None:
            request_headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(self.get_token())
            }
            request_data = json.dumps({"role": "Admin"})
            request = requests.patch("{0}/api/orgs/1/users/{1}".format(self.address, user["id"]),
                                     auth=self.auth, headers=request_headers, data=request_data, timeout=5)
            return request.text
        return None

    def add_data_source(self, url):
        request_headers = {"Content-Type": "application/json"}
        request_data = json.dumps({
            "name": "Prometheus",
            "type": "prometheus",
            "url": url,
            "isDefault": True,
            "access": "proxy"
        })
        request = requests.post("{0}/api/datasources".format(self.address),
                                auth=self.auth, headers=request_headers, data=request_data, timeout=5)
        return request.text

    def get_dashboard(self, uid):
        request_headers = {"Content-Type": "application/json"}
        request = requests.get("{0}/api/dashboards/uid/{1}".format(self.address, uid),
                               auth=self.auth, headers=request_headers, timeout=5)
        request_data = json.loads(request.text)
        print(json.dumps(request_data, indent=4))

    def walk_dashboard_path(self, home_file_name="home.json"):
        dashboard_path = "{0}/dashboard".format(self.current_path)
        if os.path.exists(dashboard_path):
            json_files = glob.glob(os.path.join(dashboard_path, "*.json"))
            for json_file in json_files:
                response_data = self.create_dashboard(open(json_file, "r").read())
                print("create dashboard: {0}".format(response_data))
                if os.path.basename(json_file) == home_file_name and response_data.get("id") is not None:
                    print("preferences: {0}".format(self.preferences(response_data["id"])))

    def create_dashboard(self, json_content):
        request_headers = {"Content-Type": "application/json"}
        request = requests.post("{0}/api/dashboards/db".format(self.address),
                                    auth=self.auth, headers=request_headers, data=json_content, timeout=5)
        response_data = json.loads(request.text)
        return response_data

    def preferences(self, home_id):
        request_headers = {"Content-Type": "application/json"}
        request_data = json.dumps({
            "homeDashboardId": home_id,
            "timezone": "Asia/Shanghai",
            "weekStart": "monday"
        })
        request = requests.patch("{0}/api/org/preferences".format(self.address),
                                 auth=self.auth, headers=request_headers, data=request_data, timeout=5)
        response_data = json.loads(request.text)
        return response_data


if __name__ == "__main__":
    Main().initialize()
