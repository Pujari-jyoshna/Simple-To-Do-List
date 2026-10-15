"""A simple to-do list program for beginners."""

import json
from pathlib import Path

TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    """Load saved tasks, or start with an empty list."""
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read the saved tasks. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save tasks so they are available next time."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def show_tasks(tasks):
    """Print all tasks with their completion status."""
    if not tasks:
        print("\nYour list is empty.")
        return

    print("\nYour tasks:")
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"{number}. [{mark}] {task['title']}")


def get_task_number(tasks, action):
    """Ask which task the user wants to change or delete."""
    if not tasks:
        print("There are no tasks.")
        return None

    show_tasks(tasks)
    answer = input(f"Enter the task number to {action}: ").strip()

    if not answer.isdigit():
        print("Please enter a number.")
        return None

    number = int(answer)

    if number < 1 or number > len(tasks):
        print("That task number does not exist.")
        return None

    return number - 1


def main():
    tasks = load_tasks()
    print("Welcome to the Simple To-Do List!")

    while True:
        print("\n--- Menu ---")
        print("1. Show tasks")
        print("2. Add a task")
        print("3. Mark a task complete")
        print("4. Delete a task")
        print("5. Quit")

        choice = input("Choose 1-5: ").strip()

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            title = input("Enter a task: ").strip()

            if title:
                tasks.append({"title": title, "done": False})
                save_tasks(tasks)
                print("Task added.")
            else:
                print("The task cannot be empty.")

        elif choice == "3":
            index = get_task_number(tasks, "complete")

            if index is not None:
                tasks[index]["done"] = True
                save_tasks(tasks)
                print("Task marked complete.")

        elif choice == "4":
            index = get_task_number(tasks, "delete")

            if index is not None:
                deleted_task = tasks.pop(index)
                save_tasks(tasks)
                print(f"Deleted: {deleted_task['title']}")

        elif choice == "5":
            print("Your tasks are saved. Goodbye!")
            break

        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()