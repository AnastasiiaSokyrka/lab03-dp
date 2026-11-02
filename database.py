class Database:
    _instance = None

    def __new__(cls, name="mydb"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self, name="mydb"):
        if self._initialized:
            return

        self.name = name
        self.tables = {}
        self._initialized = True

    def create_table(self, table):
        from table import Table

        if not isinstance(table, Table):
            raise TypeError("Expected a Table object")

        if table.name in self.tables:
            raise ValueError(f"Table {table.name} already exists")

        for column in table.columns.values():
            if column.foreign_key is not None:
                table_name, column_name = column.foreign_key

                if table_name not in self.tables:
                    raise ValueError(
                        f"Referenced table {table_name} does not exist"
                    )

                if column_name not in self.tables[table_name].columns:
                    raise ValueError(
                        f"Referenced column {column_name} does not exist"
                    )

        table.database = self
        self.tables[table.name] = table

        return table

    def create_table_with_builder(self, table):
        return self.create_table(table)

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist")

        return self.tables[name]

    def drop_table(self, name):
        if name not in self.tables:
            return False

        for table in self.tables.values():
            if table.name == name:
                continue

            for column in table.columns.values():
                if column.foreign_key is not None:
                    if column.foreign_key[0] == name:
                        raise ValueError(
                            f"Table {name} is referenced by {table.name}"
                        )

        del self.tables[name]
        return True

    def reset(self):
        self.tables.clear()
