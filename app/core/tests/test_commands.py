from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') \
                as get_item_mock:
            get_item_mock.return_value = True
            call_command('wait_for_db')
            self.assertEqual(get_item_mock.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, time_sleep_mock):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') \
                as get_item_mock:
            get_item_mock.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(get_item_mock.call_count, 6)
