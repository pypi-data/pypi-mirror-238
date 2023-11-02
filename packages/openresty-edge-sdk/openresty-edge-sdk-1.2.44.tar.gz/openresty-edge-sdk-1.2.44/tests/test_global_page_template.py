# -*- coding: utf-8 -*-
# import io
import sdk_test
import string
import random

class TestGlobalPageTemplate(sdk_test.TestSdk):
    def test_global_page_template(self):
        content = """
<!doctype html>
<html>
<head>
  <title>404 NOT FOUND</title>
</head>
<body>
  ::CLIENT_IP::
</body>
</html>
"""
        name = ''.join([random.choice(string.ascii_letters) for n in range(10)])
        id = self.client.new_global_page_template(name=name, content=content)
        self.assertIs(type(id), int)

        data = self.client.get_global_page_template(id)
        self.assertEqual(data['name'], name)
        self.assertEqual(data['content'], content)

        ok = self.client.put_global_page_template(id, name='put'+name)
        self.assertTrue(ok)

        data = self.client.get_global_page_template(id)
        self.assertEqual(data['name'], 'put'+name)

        data = self.client.get_all_global_page_templates()
        self.assertGreaterEqual(len(data), 1)

        ok = self.client.del_global_page_template(id)
        self.assertTrue(ok)

        data = self.client.get_all_global_page_templates()
        self.assertGreaterEqual(len(data), 0)
