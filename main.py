from database import Database
from builder import TableBuilder
from data_types import IntegerType, StringType, BooleanType, DateType
from query import SimpleQuery, JoinedTable
from datetime import date


def print_rows(rows):
    for row in rows:
        print(row)


def main():
    db = Database("mydb")

    db.reset()

    print("MINI DATABASE SYSTEM")

    users = (
        TableBuilder("users")
        .add_column("id", IntegerType(), nullable=False, primary_key=True)
        .add_column("name", StringType(50), nullable=False)
        .add_column("age", IntegerType(), nullable=False)
        .add_column("active", BooleanType(), nullable=False)
        .build(db)
    )

    orders = (
        TableBuilder("orders")
        .add_column("id", IntegerType(), nullable=False, primary_key=True)
        .add_column(
            "user_id",
            IntegerType(),
            nullable=False,
            foreign_key=("users", "id")
        )
        .add_column("product", StringType(100), nullable=False)
        .add_column("order_date", DateType(), nullable=False)
        .build(db)
    )

    print("\n1. INSERT")

    users.insert({
        "id": 1,
        "name": "Захар",
        "age": 20,
        "active": True
    })

    users.insert({
        "id": 2,
        "name": "Настя",
        "age": 19,
        "active": True
    })

    users.insert({
        "id": 3,
        "name": "Ася",
        "age": 21,
        "active": False
    })

    orders.insert({
        "id": 1,
        "user_id": 1,
        "product": "Laptop",
        "order_date": date(2026, 10, 1)
    })

    orders.insert({
        "id": 2,
        "user_id": 2,
        "product": "Keyboard",
        "order_date": date(2026, 10, 5)
    })

    orders.insert({
        "id": 3,
        "user_id": 1,
        "product": "Mouse",
        "order_date": date(2026, 10, 10)
    })

    print_rows(users.get_all())

    print("\n2. READ")

    print("User with ID 2:")
    print(users.get_by_id(2))

    print("\n3. UPDATE")

    users.update(3, {"age": 22})
    print(users.get_by_id(3))

    print("\n4. DELETE")

    print("Deleting order with ID 3:")
    orders.delete(3)
    print_rows(orders.get_all())

    print("\n5. FILTERING")

    query = SimpleQuery(users)

    results = (
        query
        .where("age", ">", 19)
        .execute()
    )

    print_rows(results)

    print("\n6. SELECT")

    results = (
        SimpleQuery(users)
        .select(["name", "age"])
        .execute()
    )

    print_rows(results)

    print("\n7. SORTING")

    results = (
        SimpleQuery(users)
        .order_by("age", ascending=False)
        .execute()
    )

    print_rows(results)

    print("\n8. INNER JOIN")

    joined = JoinedTable.inner_join(
        users,
        orders,
        "id",
        "user_id"
    )

    print_rows(joined)

    print("\n9. AGGREGATE FUNCTIONS")

    query = SimpleQuery(users)

    print("COUNT:", query.count())
    print("SUM of ages:", query.sum("age"))
    print("AVG of ages:", query.avg("age"))

    print("\n10. FOREIGN KEY VALIDATION")

    try:
        orders.insert({
            "id": 4,
            "user_id": 999,
            "product": "Monitor",
            "order_date": date(2026, 10, 15)
        })
    except ValueError as error:
        print("Error:", error)

    print("\n11. SINGLETON")

    db2 = Database("another_database")

    print("Same database object:", db is db2)

    print("\nDATABASE DEMONSTRATION FINISHED")


if __name__ == "__main__":
    main()
