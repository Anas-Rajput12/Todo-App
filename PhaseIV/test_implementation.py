#!/usr/bin/env python3
"""
Test script to validate the Todo Management Console Application functionality.
"""

from src.models import Task
from src.task_manager import TaskManager, TaskValidationError

def test_task_creation():
    """Test Task model creation."""
    print("Testing Task creation...")
    task = Task(1, "Test Task", "Test Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    print("✓ Task creation successful")

def test_task_manager():
    """Test TaskManager functionality."""
    print("Testing TaskManager...")
    tm = TaskManager()

    # Test adding a task
    task = tm.add_task("Test Task", "Test Description")
    assert task.id == 1
    assert len(tm.list_tasks()) == 1
    print("✓ Add task successful")

    # Test listing tasks
    tasks = tm.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    print("✓ List tasks successful")

    # Test toggling status
    result = tm.toggle_task_status(1)
    assert result == True
    assert tm.list_tasks()[0].completed == True
    print("✓ Toggle task status successful")

    # Test updating task
    result = tm.update_task(1, "Updated Task", "Updated Description")
    assert result == True
    assert tm.list_tasks()[0].title == "Updated Task"
    assert tm.list_tasks()[0].description == "Updated Description"
    print("✓ Update task successful")

    # Test deleting task
    result = tm.delete_task(1)
    assert result == True
    assert len(tm.list_tasks()) == 0
    print("✓ Delete task successful")

    # Test validation
    try:
        tm.add_task("")  # Should raise exception
        assert False, "Should have raised validation error"
    except TaskValidationError:
        print("✓ Validation error handling successful")

def test_error_handling():
    """Test error handling functionality."""
    print("Testing error handling...")
    tm = TaskManager()

    # Test operations on non-existent task
    result = tm.update_task(999, "Title")
    assert result == False

    result = tm.delete_task(999)
    assert result == False

    result = tm.toggle_task_status(999)
    assert result == False

    print("✓ Error handling for non-existent tasks successful")

if __name__ == "__main__":
    print("Starting validation tests...")
    test_task_creation()
    test_task_manager()
    test_error_handling()
    print("\\n✓ All validation tests passed! The implementation is working correctly.")