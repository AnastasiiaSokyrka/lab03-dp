from row import Row


class Table:
    def __init__(self, name, columns, database=None):
        self.name = name
        self.columns = {column.name: column for column in columns}
        self.rows = []
        self.next_id = 1
        self.database = database

        if len(self.columns) != len(columns):
            raise ValueError("Duplicate column names")

        if not self.columns:
            raise ValueError("Table must have at least one column")

        primary_keys = [
            column for column in columns if column.primary_key
        ]

        if len(primary_keys) > 1:
            raise ValueError("Only one primary key is supported")

    def _validate_data(self, row_data, current_row=None):
        unknown_columns = set(row_data) - set(self.columns)

        if unknown_columns:
            raise ValueError(f"Unknown columns: {unknown_columns}")

        for name, column in self.columns.items():
            value = row_data.get(name)

            if not column.validate(value):
                raise ValueError(f"Invalid value for column {name}: {value}")

            if column.primary_key:
                if any(
                    row is not current_row and row[name] == value
                    for row in self.rows
                ):
                    raise ValueError(f"Duplicate primary key: {value}")

            if column.foreign_key is not None and value is not None:
                if self.database is None:
                    raise ValueError("Database is required for foreign keys")

                table_name, referenced_column = column.foreign_key

                if table_name not in self.database.tables:
                    raise ValueError(f"Referenced table {table_name} does not exist")

                referenced_table = self.database.tables[table_name]

                if referenced_column not in referenced_table.columns:
                    raise ValueError(
                        f"Referenced column {referenced_column} does not exist"
                    )

                if not any(
                    row[referenced_column] == value
                    for row in referenced_table.rows
                ):
                    raise ValueError(f"Foreign key violation: {value}")

    def insert(self, row_data):
        complete_data = {
            name: row_data.get(name)
            for name in self.columns
        }

        self._validate_data(complete_data)

        row = Row(complete_data, self.next_id)
        self.next_id += 1
        self.rows.append(row)

        return row

    def get_all(self):
        return list(self.rows)

    def get_by_id(self, row_id):
        for row in self.rows:
            if row.id == row_id:
                return row

        return None

    def update(self, row_id, new_data):
        row = self.get_by_id(row_id)

        if row is None:
            raise ValueError("Row not found")

        updated_data = row.data.copy()
        updated_data.update(new_data)

        self._validate_data(updated_data, current_row=row)
        row.data = updated_data

        return row

    def delete(self, row_id):
        row = self.get_by_id(row_id)

        if row is None:
            return False

        if self.database is not None:
            for table in self.database.tables.values():
                for column in table.columns.values():
                    if column.foreign_key == (self.name, next(
                        (
                            name for name, col in self.columns.items()
                            if col.primary_key
                        ),
                        None
                    )):
                        referenced_column = column.foreign_key[1]

                        if any(
                            item[referenced_column] == row[
                                column.foreign_key[1]
                            ]
                            for item in table.rows
                            if table is not self
                        ):
                            raise ValueError("Cannot delete referenced row")

        self.rows.remove(row)
        return True
