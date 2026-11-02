class Row:
    def __init__(self, data, row_id=None):
        self.data = data.copy()
        self.id = row_id

    def __getitem__(self, column):
        return self.data[column]

    def __setitem__(self, column, value):
        self.data[column] = value

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def __repr__(self):
        return f"Row(id={self.id}, data={self.data})"
