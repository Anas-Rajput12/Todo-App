import React, { useState } from 'react';
import { Task } from '../../../../shared/types';

interface TaskItemProps {
  task: Task;
  onTaskUpdate: (task: Task) => void;
  onTaskToggleStatus: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdate, onTaskToggleStatus, onTaskDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.title);
  const [editedDescription, setEditedDescription] = useState(task.description || '');
  const [editedDueDate, setEditedDueDate] = useState(task.due_date || '');

  const handleToggleComplete = () => {
    // Pass the original task to the parent - the parent will determine what to send to the API
    // and update the list with the response from the API
    onTaskToggleStatus(task);
  };

  const handleSaveEdit = () => {
    const updatedTask = {
      ...task,
      title: editedTitle,
      description: editedDescription,
      due_date: editedDueDate || undefined, // Use edited due date if available
      status: task.status  // Ensure status is preserved
    };

    // Call parent handler without try/catch to let parent handle errors
    onTaskUpdate(updatedTask);
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditedTitle(task.title);
    setEditedDescription(task.description || '');
    setEditedDueDate(task.due_date || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    onTaskDelete(task.id);
  };

  return (
    <li className="py-5 px-6 hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 transition-all duration-300 rounded-2xl group shadow-sm hover:shadow-md border border-gray-100">
      <div className="flex flex-col sm:flex-row sm:items-start gap-5">
        {!isEditing ? (
          <>
            <div className="flex items-start space-x-4 flex-1 min-w-0">
              <button
                onClick={handleToggleComplete}
                className={`flex-shrink-0 h-6 w-6 mt-1 rounded-full border-2 flex items-center justify-center transition-all duration-300 transform hover:scale-110 ${
                  task.status === 'completed'
                    ? 'bg-gradient-to-r from-green-500 to-emerald-500 border-green-500 shadow-md'
                    : 'border-gray-400 hover:border-indigo-500 bg-white'
                }`}
                aria-label={task.status === 'completed' ? 'Mark as pending' : 'Mark as completed'}
              >
                {task.status === 'completed' && (
                  <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </button>
              <div className="min-w-0 flex-1">
                <h3
                  className={`text-lg font-semibold ${
                    task.status === 'completed' ? 'text-gray-500 line-through opacity-75' : 'text-gray-900'
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-600 mt-2 bg-gray-50 rounded-lg px-3 py-2">{task.description}</p>
                )}
                {task.due_date && (() => {
                  try {
                    const dueDate = new Date(task.due_date);
                    const currentDate = new Date();
                    const isOverdue = dueDate < currentDate && task.status !== 'completed';

                    return (
                      <div className="flex items-center mt-3 p-2 bg-gray-50 rounded-lg w-fit">
                        <svg className="flex-shrink-0 mr-2 h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                        </svg>
                        <span className={`text-sm font-medium ${
                          isOverdue
                            ? 'text-red-600 bg-red-50 px-2 py-1 rounded'
                            : 'text-gray-600'
                        }`}>
                          Due: {isNaN(dueDate.getTime()) ? '' : dueDate.toLocaleDateString()}
                        </span>
                      </div>
                    );
                  } catch (error) {
                    console.error('Error processing due date:', error);
                    return null;
                  }
                })()}
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 w-full space-y-3">
            <input
              type="text"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
              className="block w-full px-4 py-3 text-base border-2 border-indigo-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
              placeholder="Task title"
              autoFocus
            />
            <textarea
              value={editedDescription}
              onChange={(e) => setEditedDescription(e.target.value)}
              className="block w-full px-4 py-3 text-base border-2 border-indigo-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
              rows={3}
              placeholder="Task description (optional)"
            />
            <input
              type="date"
              value={editedDueDate}
              onChange={(e) => setEditedDueDate(e.target.value)}
              className="block w-full px-4 py-3 text-base border-2 border-indigo-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
            />
          </div>
        )}

        <div className="flex flex-shrink-0 space-x-2 justify-end sm:justify-start">
          {isEditing ? (
            <>
              <button
                onClick={handleSaveEdit}
                className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200 transform hover:scale-105 shadow-md"
              >
                <svg className="mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Save
              </button>
              <button
                onClick={handleCancelEdit}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-base font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-100 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200 transform hover:scale-105 shadow-sm"
              >
                <svg className="mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                Cancel
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center p-2.5 border border-transparent rounded-xl text-gray-600 hover:text-indigo-600 hover:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-110 shadow-sm"
                aria-label="Edit task"
              >
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                onClick={handleDelete}
                className="inline-flex items-center p-2.5 border border-transparent rounded-xl text-gray-600 hover:text-red-600 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-200 transform hover:scale-110 shadow-sm"
                aria-label="Delete task"
              >
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </button>
            </>
          )}

          {/* Status Badge */}
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold shadow-sm ${
              task.status === 'completed'
                ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border border-green-200'
                : 'bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-800 border border-yellow-200'
            }`}
          >
            <span className={`mr-1.5 h-2 w-2 rounded-full ${
              task.status === 'completed' ? 'bg-green-500' : 'bg-yellow-500'
            }`}></span>
            {task.status === 'completed' ? 'COMPLETED' : 'PENDING'}
          </span>
        </div>
      </div>
    </li>
  );
};

export default TaskItem;