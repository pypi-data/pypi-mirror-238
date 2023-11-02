# -*- coding: utf-8 -*-
import os
import string
import random
import time
import subprocess
import sdk_test

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestDosLogs(sdk_test.TestSdk):

    def test_get_dos_logs(self):
        init_waf_log_script = os.path.join(CURPATH, 'tests', 'data', 'init-dos-logs.sh')

        app_id = 1

        command = "/usr/bin/bash {}".format(init_waf_log_script)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        self.assertEqual(result.returncode, 0)

        data, count = self.client.get_dos_logs(app_id)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), count)

        data, count = self.client.get_dos_logs(app_id, page=1, pagesize=2)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), 2)

        data, count = self.client.get_dos_logs(app_id, page=2, pagesize=2)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), 2)

        data, count = self.client.get_dos_logs(app_id, page=4, pagesize=3)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), 1)

        # 2023-09-21 15:00:00
        current_time = 1695279610
        # current_time = time.time()

        # 9 ~ 21
        start_time = current_time - 3600 * 6
        end_time = current_time + 3600 * 6
        data, count = self.client.get_dos_logs(app_id, start_time=start_time, end_time=end_time)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), 10)

        start_time = current_time - 3600 * 6
        end_time = current_time - 3600 * 5
        data, count = self.client.get_dos_logs(app_id, start_time=start_time, end_time=end_time)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        start_time = current_time + 3600 * 5
        end_time = current_time + 3600 * 6
        data, count = self.client.get_dos_logs(app_id, start_time=start_time, end_time=end_time)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        # 11 ~ 12
        start_time = current_time - 3600 * 4
        end_time = current_time - 3600 * 3
        data, count = self.client.get_dos_logs(app_id, start_time=start_time, end_time=end_time)
        self.assertEqual(count, 5)
        self.assertEqual(len(data), 5)

        # 12 ~ 13
        start_time = current_time - 3600 * 3
        end_time = current_time - 3600 * 2
        data, count = self.client.get_dos_logs(app_id, start_time=start_time, end_time=end_time)
        self.assertEqual(count, 4)
        self.assertEqual(len(data), 4)

        host="test.com"
        data, count = self.client.get_dos_logs(app_id, host=host)
        self.assertEqual(count, 9)
        self.assertEqual(len(data), 9)

        host="test2.com"
        data, count = self.client.get_dos_logs(app_id, host=host)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        host="test3.com"
        data, count = self.client.get_dos_logs(app_id, host=host)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        uri="/"
        data, count = self.client.get_dos_logs(app_id, uri=uri)
        self.assertEqual(count, 10)
        self.assertEqual(len(data), 10)

        uri="/foo"
        data, count = self.client.get_dos_logs(app_id, uri=uri)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        uri="/bar"
        data, count = self.client.get_dos_logs(app_id, uri=uri)
        self.assertEqual(count, 2)
        self.assertEqual(len(data), 2)

        uri="/bar2"
        data, count = self.client.get_dos_logs(app_id, uri=uri)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)


        ua="curl"
        data, count = self.client.get_dos_logs(app_id, user_agent=ua)
        self.assertEqual(count, 9)
        self.assertEqual(len(data), 9)

        ua="curl2"
        data, count = self.client.get_dos_logs(app_id, user_agent=ua)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        ua="Mozilla"
        data, count = self.client.get_dos_logs(app_id, user_agent=ua)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        remote_addr = "127.0.0.1"
        data, count = self.client.get_dos_logs(app_id, remote_addr=remote_addr)
        self.assertEqual(count, 8)
        self.assertEqual(len(data), 8)

        remote_addr = "127.0.0.2"
        data, count = self.client.get_dos_logs(app_id, remote_addr=remote_addr)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        remote_addr = "127.0.0.255"
        data, count = self.client.get_dos_logs(app_id, remote_addr=remote_addr)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        action = "error_page"
        data, count = self.client.get_dos_logs(app_id, action=action)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        action = "js_challenge"
        data, count = self.client.get_dos_logs(app_id, action=action)
        self.assertEqual(count, 5)
        self.assertEqual(len(data), 5)

        try:
            action = "bad_action"
            data, count = self.client.get_dos_logs(app_id, action=action)
        except Exception as e:
            self.assertEqual(e.args[0], 'unknown action: {}'.format(action))

        request_id = "0000008000045611bdc0001a"
        data, count = self.client.get_dos_logs(app_id, request_id=request_id)
        self.assertEqual(count, 1)
        self.assertEqual(len(data), 1)

        request_id = "00000580000455aad5e00000"
        data, count = self.client.get_dos_logs(app_id, request_id=request_id)
        self.assertEqual(count, 0)
        self.assertEqual(data, None)

        try:
            app_id = 2
            request_id = "0000008000045611bdc0001a"
            data, count = self.client.get_dos_logs(app_id, request_id=request_id)
        except Exception as e:
            self.assertEqual(e.args[0], 'request id 0000008000045611bdc0001a does not belong to app {}, but belongs to 1'.format(app_id))
