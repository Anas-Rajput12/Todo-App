# Quickstart Guide: Todo Management Console Application

## Getting Started

### Prerequisites
- Python 3.13+ installed on your system

### Running the Application

1. Navigate to the project directory:
   ```bash
   cd /path/to/Todo_app
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```

3. The application will start and display a menu with available options:
   - Add a new task
   - View all tasks
   - Update a task
   - Delete a task
   - Mark task as complete/incomplete
   - Exit

### Basic Usage

1. **Adding a Task**:
   - Select option 1 from the menu
   - Enter the task title when prompted
   - Optionally enter a description
   - The system will assign a unique ID and confirm creation

2. **Viewing Tasks**:
   - Select option 2 from the menu
   - All tasks will be displayed with their ID, title, description, and completion status

3. **Updating a Task**:
   - Select option 3 from the menu
   - Enter the task ID you want to update
   - Enter the new title and/or description
   - The system will confirm the update

4. **Deleting a Task**:
   - Select option 4 from the menu
   - Enter the task ID you want to delete
   - The system will confirm deletion

5. **Marking Task Status**:
   - Select option 5 from the menu
   - Enter the task ID you want to update
   - Enter 'complete' or 'incomplete' to set the status
   - The system will confirm the status change

6. **Exiting**:
   - Select option 6 from the menu
   - The application will terminate gracefully

### Example Workflow

```
Welcome to the Todo Management Application!

Choose an option:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Status
6. Exit

> 1
Enter task title: Buy groceries
Enter task description (optional): Need to buy milk and bread
Task added successfully with ID: 1

> 2
All Tasks:
ID: 1 | Title: Buy groceries | Description: Need to buy milk and bread | Status: Pending

> 5
Enter task ID: 1
Enter status (complete/incomplete): complete
Task status updated successfully

> 2
All Tasks:
ID: 1 | Title: Buy groceries | Description: Need to buy milk and bread | Status: Complete

> 6
Goodbye!
```