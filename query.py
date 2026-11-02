from row import Row


class SimpleQuery:
    def __init__(self, table):
        self.table = table
        self.selected_columns = None
        self.filter_conditions = []
        self.sort_column = None
        self.sort_ascending = True

    def select(self, columns):
        self.selected_columns = columns
        return self

    def where(self, column, operator, value):
        if column not in self.table.columns:
            raise ValueError(f"Unknown column: {column}")

        if operator not in ("=", "!=", ">", "<", ">=", "<="):
            raise ValueError("Unsupported operator")

        self.filter_conditions.append((column, operator, value))
        return self

    def order_by(self, column, ascending=True):
        if column not in self.table.columns:
            raise ValueError(f"Unknown column: {column}")

        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def execute(self):
        results = []

        for row in self.table.rows:
            matches = True

            for column, operator, value in self.filter_conditions:
                row_value = row[column]

                if row_value is None:
                    matches = False
                    break

                if operator == "=":
                    matches = row_value == value
                elif operator == "!=":
                    matches = row_value != value
                elif operator == ">":
                    matches = row_value > value
                elif operator == "<":
                    matches = row_value < value
                elif operator == ">=":
                    matches = row_value >= value
                elif operator == "<=":
                    matches = row_value <= value

                if not matches:
                    break

            if matches:
                results.append(row)

        if self.sort_column:
            results.sort(
                key=lambda row: (
                    row[self.sort_column] is None,
                    row[self.sort_column]
                    if row[self.sort_column] is not None
                    else 0
                ),
                reverse=not self.sort_ascending
            )

        if self.selected_columns is not None:
            for column in self.selected_columns:
                if column not in self.table.columns:
                    raise ValueError(f"Unknown column: {column}")

            results = [
                Row(
                    {
                        column: row[column]
                        for column in self.selected_columns
                    },
                    row.id
                )
                for row in results
            ]

        return results

    def count(self):
        return len(self.execute())

    def sum(self, column):
        values = [
            row[column]
            for row in self.execute()
            if row[column] is not None
        ]
        return sum(values)

    def avg(self, column):
        values = [
            row[column]
            for row in self.execute()
            if row[column] is not None
        ]

        if not values:
            return 0

        return sum(values) / len(values)


class JoinedTable:
    @staticmethod
    def inner_join(table1, table2, column1, column2):
        if column1 not in table1.columns:
            raise ValueError(f"Unknown column: {column1}")

        if column2 not in table2.columns:
            raise ValueError(f"Unknown column: {column2}")

        results = []

        for row1 in table1.rows:
            for row2 in table2.rows:
                if (
                    row1[column1] is not None
                    and row1[column1] == row2[column2]
                ):
                    joined_data = {
                        f"{table1.name}.{key}": value
                        for key, value in row1.items()
                    }

                    joined_data.update({
                        f"{table2.name}.{key}": value
                        for key, value in row2.items()
                    })

                    results.append(joined_data)

        return results
