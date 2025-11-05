from todo_backend import db_tests


def main() -> None:
    db_tests.create_tasks()


if __name__ == "__main__":
    main()
