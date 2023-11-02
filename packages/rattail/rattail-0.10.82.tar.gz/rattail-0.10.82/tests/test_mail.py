# -*- coding: utf-8; -*-

import unittest

from rattail import mail
from rattail.config import RattailConfig


class TestEmail(unittest.TestCase):

    def test_template_lookup_paths(self):

        # empty (no paths) by default
        config = RattailConfig()
        email = mail.Email(config, 'testing')
        self.assertEqual(email.html_templates.directories, [])
        
        # config may specify paths
        config = RattailConfig()
        config.set('rattail.mail', 'templates', '/tmp/foo /tmp/bar')
        email = mail.Email(config, 'testing')
        self.assertEqual(email.html_templates.directories, ['/tmp/foo', '/tmp/bar'])
