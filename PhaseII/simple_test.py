#!/usr/bin/env python3
"""
Simple test to validate the Todo Management Console Application functionality.
"""

def run_tests():
    print("Starting validation tests...")

    try:
        # Import the modules
        from src.models import Task
        from src.task_manager import TaskManager, TaskValidationError
        print("[PASS] Modules imported successfully")

        # Test Task creation
        task = Task(1, "Test Task", "Test Description")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed == False
        print("[PASS] Task creation successful")

        # Test TaskManager
        tm = TaskManager()
        print("[PASS] TaskManager created successfully")

        # Test adding a task
        task = tm.add_task("Test Task", "Test Description")
        assert task.id == 1
        assert len(tm.list_tasks()) == 1
        print("[PASS] Add task successful")

        # Test listing tasks
        tasks = tm.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        print("[PASS] List tasks successful")

        # Test toggling status
        result = tm.toggle_task_status(1)
        assert result == True
        assert tm.list_tasks()[0].completed == True
        print("[PASS] Toggle task status successful")

        # Test updating task
        result = tm.update_task(1, "Updated Task", "Updated Description")
        assert result == True
        assert tm.list_tasks()[0].title == "Updated Task"
        assert tm.list_tasks()[0].description == "Updated Description"
        print("[PASS] Update task successful")

        # Test deleting task
        result = tm.delete_task(1)
        assert result == True
        assert len(tm.list_tasks()) == 0
        print("[PASS] Delete task successful")

        # Test validation
        try:
            tm.add_task("")  # Should raise exception
            assert False, "Should have raised validation error"
        except TaskValidationError:
            print("[PASS] Validation error handling successful")

        # Test operations on non-existent task
        result = tm.update_task(999, "Title")
        assert result == False
        result = tm.delete_task(999)
        assert result == False
        result = tm.toggle_task_status(999)
        assert result == False
        print("[PASS] Error handling for non-existent tasks successful")

        print("\n[SUCCESS] All validation tests passed! The implementation is working correctly.")

    except Exception as e:
        print(f"[FAIL] Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_tests()