import unittest

from database import Database
from builder import TableBuilder
from data_types import IntegerType, StringType
from query import SimpleQuery


class DatabaseTests(unittest.TestCase):

    def setUp(self):
        self.db = Database("test_db")
        self.db.reset()

        self.users = (
            TableBuilder("users")
            .add_column(
                "id",
                IntegerType(),
                nullable=False,
                primary_key=True
            )
            .add_column("name", StringType(50), nullable=False)
            .add_column("age", IntegerType(), nullable=False)
            .build(self.db)
        )

        self.orders = (
            TableBuilder("orders")
            .add_column(
                "id",
                IntegerType(),
                nullable=False,
                primary_key=True
            )
            .add_column(
                "user_id",
                IntegerType(),
                nullable=False,
                foreign_key=("users", "id")
            )
            .build(self.db)
        )

    def test_insert(self):
        row = self.users.insert({
            "id": 1,
            "name": "Настя",
            "age": 19
        })

        self.assertEqual(row["name"], "Настя")
        self.assertEqual(row.id, 1)

    def test_read(self):
        self.users.insert({
            "id": 1,
            "name": "Захар",
            "age": 20
        })

        row = self.users.get_by_id(1)

        self.assertEqual(row["name"], "Захар")

    def test_update(self):
        self.users.insert({
            "id": 1,
            "name": "Ася",
            "age": 21
        })

        self.users.update(1, {"age": 22})

        self.assertEqual(
            self.users.get_by_id(1)["age"],
            22
        )

    def test_delete(self):
        self.users.insert({
            "id": 1,
            "name": "Настя",
            "age": 19
        })

        self.assertTrue(self.users.delete(1))
        self.assertEqual(len(self.users.rows), 0)

    def test_duplicate_primary_key(self):
        self.users.insert({
            "id": 1,
            "name": "Захар",
            "age": 20
        })

        with self.assertRaises(ValueError):
            self.users.insert({
                "id": 1,
                "name": "Ася",
                "age": 21
            })

    def test_foreign_key(self):
        with self.assertRaises(ValueError):
            self.orders.insert({
                "id": 1,
                "user_id": 999
            })

    def test_valid_foreign_key(self):
        self.users.insert({
            "id": 1,
            "name": "Настя",
            "age": 19
        })

        order = self.orders.insert({
            "id": 1,
            "user_id": 1
        })

        self.assertEqual(order["user_id"], 1)

    def test_not_nullable(self):
        with self.assertRaises(ValueError):
            self.users.insert({
                "id": 1,
                "name": None,
                "age": 19
            })

    def test_filtering(self):
        self.users.insert({
            "id": 1,
            "name": "Захар",
            "age": 20
        })

        self.users.insert({
            "id": 2,
            "name": "Настя",
            "age": 18
        })

        results = (
            SimpleQuery(self.users)
            .where("age", ">", 19)
            .execute()
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Захар")

    def test_singleton(self):
        db1 = Database("first")
        db2 = Database("second")

        self.assertIs(db1, db2)

    def test_invalid_foreign_key_definition(self):
        invalid_table = (
            TableBuilder("invalid")
            .add_column(
                "id",
                IntegerType(),
                nullable=False,
                primary_key=True
            )
            .add_column(
                "user_id",
                IntegerType(),
                foreign_key=("unknown", "id")
            )
            .build()
        )

        with self.assertRaises(ValueError):
            self.db.create_table(invalid_table)


if __name__ == "__main__":
    unittest.main()
