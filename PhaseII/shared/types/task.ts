export type TaskStatus = 'pending' | 'completed';

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  due_date?: string; // ISO date string (optional)
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  due_date?: string; // ISO date string (optional)
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  due_date?: string; // ISO date string (optional)
}

export interface TaskToggleCompleteRequest {
  completed: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
}