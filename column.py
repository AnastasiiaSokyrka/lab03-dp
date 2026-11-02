class Column:
    def __init__(
        self,
        name,
        data_type,
        nullable=True,
        primary_key=False,
        foreign_key=None
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.foreign_key = foreign_key

        if primary_key and nullable:
            self.nullable = False

        if not isinstance(data_type, object):
            raise TypeError("Invalid data type")

    def validate(self, value):
        if value is None:
            return self.nullable

        return self.data_type.validate(value)
