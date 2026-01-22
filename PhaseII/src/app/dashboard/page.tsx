'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Task, TaskCreateRequest, User } from '@/shared/types';

import { apiClient } from '../../lib/api-client';
import { isAuthenticated, clearAuthData } from '../../lib/auth';
import TaskList from '../../components/tasks/TaskList';
import TaskForm from '../../components/tasks/TaskForm';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

 useEffect(() => {
  if (!isAuthenticated()) {
    router.push('/login');
    return;
  }

  fetchTasks();
}, [router]); // add router as dependency


  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTasks();
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return task.status === 'pending';
    if (filter === 'completed') return task.status === 'completed';
    return true; // 'all' filter
  });

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.status === 'completed').length;
  const pendingTasks = tasks.filter(task => task.status === 'pending').length;

  const handleCreateTask = async (taskData: TaskCreateRequest) => {
    try {
      setError(null); // Clear any previous errors
      console.log('Attempting to create task:', taskData);

      const newTask = await apiClient.createTask(taskData);
      console.log('Task created successfully:', newTask);

      setTasks([...tasks, newTask]);
      setShowForm(false);

      // Show success message
      setSuccess('Task created successfully!');
      setTimeout(() => setSuccess(null), 3000);
    } catch (error: any) {
      console.error('Failed to create task:', error);

      // More detailed error handling for network errors
      let errorMessage = 'Failed to create task. Please try again.';

      if (error.code === 'NETWORK_ERROR' || error.message?.includes('Network Error') || !error.response) {
        errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection and make sure the backend server is running.';
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      // Show error for a few seconds
      setTimeout(() => setError(null), 5000);
    }
  };

  const handleUpdateTask = async (updatedTask: Task) => {
    try {
      setError(null); // Clear any previous errors
      const response = await apiClient.updateTask(updatedTask.id, {
        title: updatedTask.title,
        description: updatedTask.description || undefined,
        due_date: updatedTask.due_date || undefined,
        status: updatedTask.status
      });

      // Update the task in the list
      setTasks(tasks.map(task =>
        task.id === updatedTask.id ? response : task
      ));

      // Show success message
      setSuccess('Task updated successfully!');
      setTimeout(() => setSuccess(null), 3000);
    } catch (error: any) {
      console.error('Failed to update task:', error);
      let errorMessage = 'An unexpected error occurred while updating the task. Please try again.';

      if (error?.response?.status === 401) {
        errorMessage = 'Unauthorized: Please log in again.';
        // Redirect to login after a delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else if (error?.response?.status === 403) {
        errorMessage = 'Forbidden: You do not have permission to update this task.';
      } else if (error?.response?.status === 404) {
        errorMessage = 'Task not found. It may have been deleted.';
      } else if (error?.response?.status >= 500) {
        errorMessage = 'Server error: Unable to update task. Please try again later.';
      } else if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error?.message?.includes('Network Error') || error?.code === 'NETWORK_ERROR') {
        errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
      } else if (error?.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      setTimeout(() => setError(null), 5000);
    }
  };

  const handleToggleTaskStatus = async (task: Task) => {
    try {
      setError(null); // Clear any previous errors
      const response = await apiClient.toggleTaskComplete(task.id, {
        completed: task.status !== 'completed'
      });

      // Update the task in the list
      setTasks(tasks.map(t =>
        t.id === task.id ? response : t
      ));

      // Show success message
      const newStatusText = response.status === 'completed' ? 'marked as completed' : 'marked as pending';
      setSuccess(`Task ${newStatusText} successfully!`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (error: any) {
      console.error('Failed to update task status:', error);
      let errorMessage = 'An unexpected error occurred while updating task status. Please try again.';

      if (error?.response?.status === 401) {
        errorMessage = 'Unauthorized: Please log in again.';
        // Redirect to login after a delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else if (error?.response?.status === 403) {
        errorMessage = 'Forbidden: You do not have permission to update this task.';
      } else if (error?.response?.status === 404) {
        errorMessage = 'Task not found. It may have been deleted.';
      } else if (error?.response?.status >= 500) {
        errorMessage = 'Server error: Unable to update task status. Please try again later.';
      } else if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error?.message?.includes('Network Error') || error?.code === 'NETWORK_ERROR') {
        errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
      } else if (error?.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      setTimeout(() => setError(null), 5000);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      setError(null); // Clear any previous errors
      await apiClient.deleteTask(taskId);

      // Update the task list by removing the deleted task
      setTasks(tasks.filter(task => task.id !== taskId));

      // Show success message
      setSuccess('Task deleted successfully!');
      setTimeout(() => setSuccess(null), 3000);
    } catch (error: any) {
      console.error('Failed to delete task:', error);
      let errorMessage = 'An unexpected error occurred while deleting the task. Please try again.';

      if (error?.response?.status === 401) {
        errorMessage = 'Unauthorized: Please log in again.';
        // Redirect to login after a delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else if (error?.response?.status === 403) {
        errorMessage = 'Forbidden: You do not have permission to delete this task.';
      } else if (error?.response?.status === 404) {
        errorMessage = 'Task not found. It may have already been deleted.';
      } else if (error?.response?.status >= 500) {
        errorMessage = 'Server error: Unable to delete task. Please try again later.';
      } else if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error?.message?.includes('Network Error') || error?.code === 'NETWORK_ERROR') {
        errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
      } else if (error?.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      setTimeout(() => setError(null), 5000);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600 font-medium">Loading your tasks...</p>
          <p className="text-sm text-gray-500">Preparing your personalized workspace</p>
        </div>
      </div>
    );
  }

  const handleLogout = () => {
    clearAuthData();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Sidebar for desktop */}
      <div className="hidden md:block md:w-64 md:fixed md:inset-y-0 md:flex md:flex-col bg-white border-r border-gray-200 z-10 shadow-lg">
        <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <div className="flex items-center flex-shrink-0 px-4">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg">
              <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <span className="ml-3 text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">TaskFlow</span>
          </div>
          <nav className="mt-8 flex-1 px-2 space-y-1">
            <div className="p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl m-2 shadow-sm border border-indigo-100">
              <h3 className="text-xs font-semibold text-indigo-600 uppercase tracking-wider mb-3">Overview</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600 font-medium">Total</span>
                  <span className="font-bold text-gray-900 text-lg">{totalTasks}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-yellow-600 font-medium">Pending</span>
                  <span className="font-bold text-yellow-700 text-lg">{pendingTasks}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-green-600 font-medium">Completed</span>
                  <span className="font-bold text-green-700 text-lg">{completedTasks}</span>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="px-2 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Filters</h3>
              <div className="space-y-1">
                <button
                  onClick={() => setFilter('all')}
                  className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    filter === 'all'
                      ? 'bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 shadow-md border border-indigo-200'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-indigo-600 hover:translate-x-1'
                  }`}
                >
                  <div className="h-8 w-8 rounded-lg bg-indigo-100 flex items-center justify-center mr-3">
                    <svg className="h-4 w-4 text-indigo-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000 16zM8 8a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1zm1 4a1 1 0 100 2h2a1 1 0 100-2H9z" clipRule="evenodd" />
                    </svg>
                  </div>
                  All Tasks
                </button>
                <button
                  onClick={() => setFilter('pending')}
                  className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    filter === 'pending'
                      ? 'bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-700 shadow-md border border-yellow-200'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-yellow-600 hover:translate-x-1'
                  }`}
                >
                  <div className="h-8 w-8 rounded-lg bg-yellow-100 flex items-center justify-center mr-3">
                    <svg className="h-4 w-4 text-yellow-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Pending
                </button>
                <button
                  onClick={() => setFilter('completed')}
                  className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    filter === 'completed'
                      ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 shadow-md border border-green-200'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-green-600 hover:translate-x-1'
                  }`}
                >
                  <div className="h-8 w-8 rounded-lg bg-green-100 flex items-center justify-center mr-3">
                    <svg className="h-4 w-4 text-green-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Completed
                </button>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-200">
              <button
                onClick={handleLogout}
                className="w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl text-gray-600 hover:bg-red-50 hover:text-red-600 hover:translate-x-1 transition-all duration-200"
              >
                <div className="h-8 w-8 rounded-lg bg-red-100 flex items-center justify-center mr-3">
                  <svg className="h-4 w-4 text-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                  </svg>
                </div>
                Sign out
              </button>
            </div>
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="md:pl-64">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Mobile header with sidebar toggle */}
          <div className="md:hidden flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">My Tasks</h1>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="inline-flex items-center p-3 rounded-xl text-gray-400 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 bg-white shadow-md"
            >
              <span className="sr-only">Open sidebar</span>
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>

          {/* Mobile sidebar overlay */}
          {sidebarOpen && (
            <div className="md:hidden fixed inset-0 z-40 flex">
              <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)}></div>
              <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white shadow-xl">
                <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
                  <div className="flex-shrink-0 flex items-center px-4">
                    <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg">
                      <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                      </svg>
                    </div>
                    <span className="ml-3 text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">TaskFlow</span>
                  </div>
                  <nav className="mt-8 flex-1 px-2 space-y-1">
                    <div className="p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl m-2 shadow-sm border border-indigo-100">
                      <h3 className="text-xs font-semibold text-indigo-600 uppercase tracking-wider mb-3">Overview</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-gray-600 font-medium">Total</span>
                          <span className="font-bold text-gray-900 text-lg">{totalTasks}</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-yellow-600 font-medium">Pending</span>
                          <span className="font-bold text-yellow-700 text-lg">{pendingTasks}</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-green-600 font-medium">Completed</span>
                          <span className="font-bold text-green-700 text-lg">{completedTasks}</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-6">
                      <h3 className="px-2 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Filters</h3>
                      <div className="space-y-1">
                        <button
                          onClick={() => {
                            setFilter('all');
                            setSidebarOpen(false);
                          }}
                          className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                            filter === 'all'
                              ? 'bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 shadow-md border border-indigo-200'
                              : 'text-gray-600 hover:bg-gray-50 hover:text-indigo-600 hover:translate-x-1'
                          }`}
                        >
                          <div className="h-8 w-8 rounded-lg bg-indigo-100 flex items-center justify-center mr-3">
                            <svg className="h-4 w-4 text-indigo-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000 16zM8 8a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1zm1 4a1 1 0 100 2h2a1 1 0 100-2H9z" clipRule="evenodd" />
                            </svg>
                          </div>
                          All Tasks
                        </button>
                        <button
                          onClick={() => {
                            setFilter('pending');
                            setSidebarOpen(false);
                          }}
                          className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                            filter === 'pending'
                              ? 'bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-700 shadow-md border border-yellow-200'
                              : 'text-gray-600 hover:bg-gray-50 hover:text-yellow-600 hover:translate-x-1'
                          }`}
                        >
                          <div className="h-8 w-8 rounded-lg bg-yellow-100 flex items-center justify-center mr-3">
                            <svg className="h-4 w-4 text-yellow-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                          </div>
                          Pending
                        </button>
                        <button
                          onClick={() => {
                            setFilter('completed');
                            setSidebarOpen(false);
                          }}
                          className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                            filter === 'completed'
                              ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 shadow-md border border-green-200'
                              : 'text-gray-600 hover:bg-gray-50 hover:text-green-600 hover:translate-x-1'
                          }`}
                        >
                          <div className="h-8 w-8 rounded-lg bg-green-100 flex items-center justify-center mr-3">
                            <svg className="h-4 w-4 text-green-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                          </div>
                          Completed
                        </button>
                      </div>
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-200">
                      <button
                        onClick={() => {
                          handleLogout();
                          setSidebarOpen(false);
                        }}
                        className="w-full flex items-center px-3 py-3 text-sm font-medium rounded-xl text-gray-600 hover:bg-red-50 hover:text-red-600 hover:translate-x-1 transition-all duration-200"
                      >
                        <div className="h-8 w-8 rounded-lg bg-red-100 flex items-center justify-center mr-3">
                          <svg className="h-4 w-4 text-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                          </svg>
                        </div>
                        Sign out
                      </button>
                    </div>
                  </nav>
                </div>
              </div>
            </div>
          )}

          {/* Success message display */}
          {success && (
            <div className="mb-6 rounded-2xl bg-gradient-to-r from-green-50 to-emerald-50 p-5 border border-green-200 shadow-sm">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center">
                    <svg className="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-sm font-semibold text-green-800">{success}</h3>
                </div>
              </div>
            </div>
          )}

          {/* Error message display */}
          {error && (
            <div className="mb-6 rounded-2xl bg-gradient-to-r from-red-50 to-pink-50 p-5 border border-red-200 shadow-sm">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center">
                    <svg className="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-sm font-semibold text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">My Tasks</h1>
              <p className="mt-2 text-sm text-gray-500">Manage your daily tasks efficiently</p>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-semibold rounded-2xl shadow-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 hover:shadow-xl"
            >
              <svg className="-ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              {showForm ? 'Cancel' : 'Add New Task'}
            </button>
          </div>

          {showForm && (
            <div className="mb-8 bg-white p-8 rounded-3xl shadow-xl border border-gray-100 transition-all duration-500 backdrop-blur-sm bg-opacity-80">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Task</h2>
              <TaskForm
                onTaskSubmit={handleCreateTask}
                onCancel={() => setShowForm(false)}
              />
            </div>
          )}

          {/* Task Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl p-6 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-12 w-12 rounded-2xl bg-white bg-opacity-20 flex items-center justify-center backdrop-blur-sm">
                    <svg className="h-7 w-7 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium opacity-90">Total Tasks</p>
                  <p className="text-3xl font-bold">{totalTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-3xl p-6 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-12 w-12 rounded-2xl bg-white bg-opacity-20 flex items-center justify-center backdrop-blur-sm">
                    <svg className="h-7 w-7 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium opacity-90">Pending</p>
                  <p className="text-3xl font-bold">{pendingTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-3xl p-6 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-12 w-12 rounded-2xl bg-white bg-opacity-20 flex items-center justify-center backdrop-blur-sm">
                    <svg className="h-7 w-7 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium opacity-90">Completed</p>
                  <p className="text-3xl font-bold">{completedTasks}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Task List */}
          <div className="bg-white/70 backdrop-blur-sm bg-opacity-80 shadow-xl rounded-3xl border border-gray-100 overflow-hidden">
            <div className="sm:rounded-3xl">
              <TaskList
                tasks={filteredTasks}
                onTaskUpdate={(task) => {
                  // Handle updates to task details (title, description, due date)
                  handleUpdateTask(task);
                }}
                onTaskToggleStatus={(task) => {
                  // Handle toggling of task status (completed/pending)
                  handleToggleTaskStatus(task);
                }}
                onTaskDelete={handleDeleteTask}
                onAddTask={() => setShowForm(true)}
              />
            </div>
          </div>

          {/* Floating action button for mobile */}
          <button
            onClick={() => setShowForm(true)}
            className="fixed bottom-8 right-6 md:hidden inline-flex items-center justify-center p-5 border border-transparent text-base font-semibold rounded-full shadow-2xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-110 z-10 animate-pulse"
            aria-label="Add new task"
          >
            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
