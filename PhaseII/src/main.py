"""
Main CLI interface for the Todo Management Console Application.
Task ID: T003, T008, T009
"""

from task_manager import TaskManager, TaskValidationError


def display_menu():
    """
    Display the main menu options to the user.
    Task ID: T008
    """
    print("\n" + "="*40)
    print("Todo Management Application")
    print("="*40)
    print("Choose an option:")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Status")
    print("6. Exit")
    print("="*40)


def get_user_choice():
    """
    Get and validate the user's menu choice.
    Task ID: T008

    Returns:
        str: The user's choice
    """
    try:
        choice = input("Enter your choice (1-6): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\n\nExiting application...")
        return "6"


def add_task_ui(task_manager):
    """
    User interface for adding a new task.
    Task ID: T014, T015
    """
    try:
        title = input("Enter task title: ").strip()
        description = input("Enter task description (optional): ").strip()

        task = task_manager.add_task(title, description)
        print(f"Task added successfully with ID: {task.id}")
    except TaskValidationError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
    except Exception as e:
        print(f"An error occurred while adding the task: {e}")


def view_tasks_ui(task_manager):
    """
    User interface for viewing all tasks.
    Task ID: T019, T020
    """
    tasks = task_manager.list_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\nAll Tasks:")
    for task in tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} {task}")


def update_task_ui(task_manager):
    """
    User interface for updating a task.
    Task ID: T024, T025
    """
    try:
        task_id = int(input("Enter task ID to update: ").strip())

        # Check if task exists
        task = task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {task}")
        new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        new_description = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()

        # Prepare update parameters
        title_update = new_title if new_title else None
        description_update = new_description if new_description else None

        # Only update if there's something to update
        if title_update is not None or description_update is not None:
            success = task_manager.update_task(task_id, title_update, description_update)
            if success:
                print("Task updated successfully.")
            else:
                print("Error: Failed to update task.")
        else:
            print("No changes made to the task.")
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
    except Exception as e:
        print(f"An error occurred while updating the task: {e}")


def delete_task_ui(task_manager):
    """
    User interface for deleting a task.
    Task ID: T029, T030
    """
    try:
        task_id = int(input("Enter task ID to delete: ").strip())

        # Check if task exists before deletion
        task = task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        success = task_manager.delete_task(task_id)
        if success:
            print("Task deleted successfully.")
        else:
            print("Error: Failed to delete task.")
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
    except Exception as e:
        print(f"An error occurred while deleting the task: {e}")


def toggle_task_status_ui(task_manager):
    """
    User interface for toggling task completion status.
    Task ID: T034, T035
    """
    try:
        task_id = int(input("Enter task ID to toggle status: ").strip())

        # Check if task exists
        task = task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        success = task_manager.toggle_task_status(task_id)
        if success:
            task = task_manager.get_task_by_id(task_id)  # Get updated task to show new status
            new_status = "completed" if task.completed else "pending"
            print(f"Task status updated successfully. Task is now {new_status}.")
        else:
            print("Error: Failed to update task status.")
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
    except Exception as e:
        print(f"An error occurred while toggling task status: {e}")


def main():
    """
    Main application loop implementing the CLI menu structure.
    Task ID: T008, T036
    """
    task_manager = TaskManager()
    print("Welcome to the Todo Management Application!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            add_task_ui(task_manager)
        elif choice == "2":
            view_tasks_ui(task_manager)
        elif choice == "3":
            update_task_ui(task_manager)
        elif choice == "4":
            delete_task_ui(task_manager)
        elif choice == "5":
            toggle_task_status_ui(task_manager)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

        # Pause to let user see the result before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()