# Task Management API Contract

## Overview
This contract defines the operations available in the Todo Management Console Application.

## Operations

### Add Task
- **Operation**: Add a new task to the system
- **Input**:
  - title (string, required): The task title
  - description (string, optional): Additional task details
- **Output**:
  - task_id (integer): The unique ID assigned to the task
  - message (string): Confirmation message
- **Success**: Task is added to the in-memory store with a unique ID
- **Error**: If title is empty, return error message

### List Tasks
- **Operation**: Retrieve all tasks in the system
- **Input**: None
- **Output**:
  - tasks (array): List of all tasks with id, title, description, and completion status
- **Success**: Returns all tasks in the system
- **Error**: None (returns empty list if no tasks exist)

### Update Task
- **Operation**: Modify an existing task's title and/or description
- **Input**:
  - task_id (integer, required): ID of the task to update
  - title (string, optional): New task title
  - description (string, optional): New task description
- **Output**:
  - message (string): Confirmation message
- **Success**: Task is updated with new information
- **Error**: If task_id doesn't exist, return error message

### Delete Task
- **Operation**: Remove a task from the system
- **Input**:
  - task_id (integer, required): ID of the task to delete
- **Output**:
  - message (string): Confirmation message
- **Success**: Task is removed from the system
- **Error**: If task_id doesn't exist, return error message

### Toggle Task Status
- **Operation**: Change a task's completion status
- **Input**:
  - task_id (integer, required): ID of the task to update
- **Output**:
  - message (string): Confirmation message
- **Success**: Task completion status is toggled (completed ↔ pending)
- **Error**: If task_id doesn't exist, return error message

### Exit Application
- **Operation**: Gracefully terminate the application
- **Input**: None
- **Output**: None
- **Success**: Application terminates without error
- **Error**: None