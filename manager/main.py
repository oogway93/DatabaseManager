import sqlite3
from abc import ABC, abstractmethod


class CRUD(ABC):
    @abstractmethod
    def _execute(self):
        raise NotImplementedError()

    @abstractmethod
    def create_table(self):
        raise NotImplementedError()

    @abstractmethod
    def add(self):
        raise NotImplementedError()

    @abstractmethod
    def update_data(self):
        raise NotImplementedError()

    @abstractmethod
    def add_new_column(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_table(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_column(self):
        raise NotImplementedError()


class SQLiteManager(ABC, RUD):
    def __init__(self, database_filename: str, table_name: str):
        self.connection = sqlite3.connect(database_filename)
        self.table_name = table_name

    def _execute(self, statement: str, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor  # returns a cursor that has stored data

    def create_table(self, columns: dict):
        columns_with_types = [f"{column_name} {data_type}" for column_name, data_type in columns.items()]
        self._execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name}
        ({', '.join(columns_with_types)});
        ''')

    def add(self, data: dict):
        placeholders = ', '.join('?' * len(data))
        names = ', '.join(data.keys())
        values = tuple(data.values())

        self._execute(f'''
        INSERT INTO {self.table_name}({names})
        VALUES ({placeholders});
        ''', values)

    def update_data(self, _id: int, data: dict):
        columns_with_values = [f"{column_name} = '{value}'" for column_name, value in data.items()]

        self._execute(f"""
        UPDATE {self.table_name}
        SET {', '.join(columns_with_values)}
        WHERE id = {_id};
        """)

    def add_new_column(self, column: dict):
        column_with_type = [f"{name} {data_type}" for name, data_type in column.items()]

        self._execute(f"""
        ALTER TABLE {self.table_name}
        ADD {''.join(column_with_type)}; 
        """)

    def delete_table(self):
        self._execute(f"""DROP TABLE {self.table_name};""")

    def delete_column(self, column: str):
        self._execute(f"""
        ALTER TABLE {self.table_name}
        DROP COLUMN {column};
        """)
