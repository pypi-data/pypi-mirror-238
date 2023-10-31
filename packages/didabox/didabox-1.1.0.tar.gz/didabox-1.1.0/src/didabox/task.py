# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : task.py
@Date    : 2023/10/31 13:42:42
@Author  : zhchen
@Desc    : 
"""
import requests

from src.didabox import DidaBox


class TaskBox(DidaBox):

    def _task_api(self, data: dict):
        response = requests.post(
            'https://api.dida365.com/api/v2/batch/task',
            cookies=self.cookies, headers=self.headers, json=data)
        return response

    def add_reminders_task(self, project_id: str, title: str, content: str, trigger_time: str):
        trigger_time = self.str2utc(trigger_time)
        json_data = {
            'add': [
                {
                    'items': [],
                    'reminders': [
                        {
                            'id': self.random_int(),
                            'trigger': 'TRIGGER:PT0S',
                        },
                    ],
                    'exDate': [],
                    'dueDate': None,
                    'priority': 0,
                    'isAllDay': False,
                    'repeatFlag': None,
                    'progress': 0,
                    'assignee': None,
                    'sortOrder': -self.random_int(),
                    'startDate': self.shanghai2utc(trigger_time),
                    'isFloating': False,
                    'status': 0,
                    'projectId': project_id,
                    'kind': None,
                    'createdTime': self.shanghai2utc(self.now()),
                    'modifiedTime': self.shanghai2utc(self.now()),
                    'title': title,
                    'tags': [],
                    'timeZone': self.tz,
                    'content': content,
                    'id': self.random_str(),
                },
            ],
            'update': [],
            'delete': [],
            'addAttachments': [],
            'updateAttachments': [],
            'deleteAttachments': [],
        }
        return self._task_api(json_data)
