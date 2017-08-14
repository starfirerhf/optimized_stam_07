import unittest
from sqlite import create_table


class CreateTableTestCase(unittest.TestCase):
    """Tests for create_table.py."""

    def test_create_with_def(self):
        """Testing simple author table creation"""
        sqlite_file = 'my_first_db.sqlite'  # name of the sqlite database file

        table_def = [{"AUTHOR_ID": "TEXT PRIMARY KEY"}, \
                     {"AUTHOR_NM": "TEXT"}, \
                     {"TWEET_COUNT": "INTEGER"}]

        print(table_def)
        table_created = create_table.Sqlite_Table(sqlite_file, 'VALID_AUTHORS', table_def)
        self.assertTrue(table_created, True)


unittest.main()