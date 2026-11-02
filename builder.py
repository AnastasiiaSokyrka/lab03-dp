from table import Table


class TableBuilder:
    def __init__(self, name):
        self.name = name
        self.columns = []

    def add_column(
        self,
        name,
        data_type,
        nullable=True,
        primary_key=False,
        foreign_key=None
    ):
        from column import Column

        column = Column(
            name=name,
            data_type=data_type,
            nullable=nullable,
            primary_key=primary_key,
            foreign_key=foreign_key
        )

        self.columns.append(column)
        return self

    def build(self, db=None):
        table = Table(self.name, self.columns, database=db)

        if db is not None:
            return db.create_table(table)

        return table
