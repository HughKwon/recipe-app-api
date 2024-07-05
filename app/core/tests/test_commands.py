"""
Test custom Djangogo management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError

from django.test import SimpleTestCase


# the command that we'll be mocking
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the database when getting OperationalError."""
        # Through trial and error, the lecturer found out
        # there are two stages of error:
        # 1. Psycopg2Error --> Postgres application hasn't started yet,
        #  and cannot accept connections
        # 2. OperationalError --> Postgres is ready to accept connections,
        #  but the database is not ready yet

        # 1. Psycopg2Error
        # 2. Psycopg2Error
        # 3. OperationalError
        # 4. OperationalError
        # 5. OperationalError
        # 6. True

        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
