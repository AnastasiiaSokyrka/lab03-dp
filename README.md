
# Mini Database System

## Description

A simplified in-memory relational database implemented in Python.

The project demonstrates object-oriented programming principles
and design patterns.

## Features

- Data types: Integer, String, Boolean, Date
- Table and Row management
- CRUD operations
- Primary Key and Foreign Key constraints
- Data validation
- Simple queries: SELECT, WHERE, ORDER BY
- INNER JOIN
- Aggregate functions: COUNT, SUM, AVG
- Singleton design pattern
- Builder design pattern
- Unit tests

## Architecture

- data_types.py - data type classes
- column.py - column definition and validation
- row.py - table row representation
- table.py - table management and CRUD
- query.py - queries, sorting, filtering and JOIN
- database.py - database management using Singleton
- builder.py - table creation using Builder
- main.py - demonstration of the system
- tests/test_database.py - unit tests

## Design Patterns

### Singleton

Ensures that only one Database instance exists.

### Builder

Allows step-by-step construction of tables by adding columns.

## Running the program

```bash
python main.py
```

## Running tests

```bash
python -m unittest discover -s tests -v
```
