import React from 'react';

interface EmptyStateProps {
  onAddTask: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onAddTask }) => {
  return (
    <div className="text-center py-16">
      <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100">
        <svg
          className="h-8 w-8 text-indigo-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
          />
        </svg>
      </div>
      <h3 className="mt-4 text-lg font-semibold text-gray-900">No tasks yet</h3>
      <p className="mt-2 text-sm text-gray-500 max-w-md mx-auto">
        Get started by creating your first task. Organize your work and boost your productivity.
      </p>
      <div className="mt-8">
        <button
          type="button"
          onClick={onAddTask}
          className="inline-flex items-center px-5 py-2.5 border border-transparent text-sm font-medium rounded-xl shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105"
        >
          <svg
            className="-ml-1 mr-2 h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clipRule="evenodd"
            />
          </svg>
          Create your first task
        </button>
      </div>
      <div className="mt-10 grid grid-cols-3 gap-8 max-w-lg mx-auto">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-gray-100">
            <svg className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <dt className="mt-3 text-sm font-medium text-gray-900">Organize</dt>
        </div>
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-gray-100">
            <svg className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <dt className="mt-3 text-sm font-medium text-gray-900">Track</dt>
        </div>
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-gray-100">
            <svg className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <dt className="mt-3 text-sm font-medium text-gray-900">Achieve</dt>
        </div>
      </div>
    </div>
  );
};

export default EmptyState;