from todo_backend import database, db_tests


def main() -> None:
    database.create_db_and_tables()
    db_tests.create_tasks()
    db_tests.select_tasks()


if __name__ == "__main__":
    main()
