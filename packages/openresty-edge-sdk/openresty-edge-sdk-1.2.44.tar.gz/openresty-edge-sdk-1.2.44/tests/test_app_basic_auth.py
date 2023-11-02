# -*- coding: utf-8 -*-
# import io
import sdk_test


class TestAppBasicAuth(sdk_test.TestSdk):
    def test_app_basic_auth(self):
        app_id = self.app_id

        data = self.client.get_all_app_basic_auth_user_groups()
        self.assertEqual(len(data), 0)

        data = self.client.get_all_app_basic_auth_user_groups(app_id)
        self.assertEqual(len(data), 0)

        ug_id1 = self.client.new_app_basic_auth_user_group("test1")
        ug_id2 = self.client.new_app_basic_auth_user_group("test2", app_id=app_id)
        data = self.client.get_all_app_basic_auth_user_groups()
        self.assertEqual(len(data), 2)

        ok = self.client.del_app_basic_auth_user_group(ug_id2)
        self.assertEqual(ok, True)

        data = self.client.get_all_app_basic_auth_user_groups()
        self.assertEqual(len(data), 1)

        ok = self.client.put_app_basic_auth_user_group(ug_id1, name="new-test1", label="new-test1-label")
        self.assertEqual(ok, True)

        ok = self.client.put_app_basic_auth_user_group(ug_id1, name="new-test1", label="new-test1-label", app_id=app_id)
        self.assertEqual(ok, True)

        data = self.client.get_app_basic_auth_user_group(ug_id1)
        self.assertEqual(data['name'], "new-test1")
        self.assertEqual(data['label'], "new-test1-label")

        data = self.client.get_app_basic_auth_user_group(ug_id1, app_id)
        self.assertEqual(data['name'], "new-test1")
        self.assertEqual(data['label'], "new-test1-label")

        # test cases fro basic auth user
        data = self.client.get_app_basic_auth_users_in_group(ug_id1)
        self.assertEqual(len(data), 0)

        data = self.client.get_app_basic_auth_users_in_group(ug_id1, app_id)
        self.assertEqual(len(data), 0)

        user1 = self.client.new_app_basic_auth_user(ug_id1, "user1", "ORTest&123")
        user2 = self.client.new_app_basic_auth_user(ug_id1, "user2", "ORTest&123", app_id=app_id)
        data = self.client.get_app_basic_auth_users_in_group(ug_id1)
        self.assertEqual(len(data), 2)

        ok = self.client.del_app_basic_auth_user(user2, ug_id1)
        self.assertEqual(ok, True)

        data = self.client.get_app_basic_auth_users_in_group(ug_id1)
        self.assertEqual(len(data), 1)

        ok = self.client.put_app_basic_auth_user(user1, ug_id1, "new-user1", "ORTest&123")
        self.assertEqual(ok, True)

        ok = self.client.put_app_basic_auth_user(user1, ug_id1, "new-user1", "ORTest&123", app_id=app_id)
        self.assertEqual(ok, True)

        data = self.client.get_app_basic_auth_user(user1, ug_id1)
        self.assertEqual(data['username'], "new-user1")
        self.assertEqual(data['password'], None)

        data = self.client.get_app_basic_auth_user(user1, ug_id1, app_id)
        self.assertEqual(data['username'], "new-user1")
        self.assertEqual(data['password'], None)
