import React from 'react';
import TaskItem from './TaskItem';
import EmptyState from './EmptyState';
import { Task } from '../../../../shared/types';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: (task: Task) => void;
  onTaskToggleStatus: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
  onAddTask: () => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdate, onTaskToggleStatus, onTaskDelete, onAddTask }) => {
  if (tasks.length === 0) {
    return <EmptyState onAddTask={onAddTask} />;
  }

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdate={onTaskUpdate}
          onTaskToggleStatus={onTaskToggleStatus}
          onTaskDelete={onTaskDelete}
        />
      ))}
    </ul>
  );
};

export default TaskList;