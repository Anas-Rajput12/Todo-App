import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { User, UserLogin, UserRegistration, LoginResponse, Task, TaskCreateRequest, TaskUpdateRequest, TaskListResponse, TaskToggleCompleteRequest } from '../../../shared/types';

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL);

// const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || 'https://muhammadanasqadri-hackathon2.hf.space/v1').replace(/\/$/, '');

class ApiClient {
  private axiosClient: AxiosInstance;

  constructor() {
    this.axiosClient = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      // Add timeout to handle connection issues
      timeout: 10000, // 10 seconds
    });

    // Add request interceptor to include auth token
    this.axiosClient.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token expiration and provide better error reporting
    this.axiosClient.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token might be expired, clear it
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        // Log network errors for debugging
        if (error.message && error.message.includes('Network Error')) {
          console.error('Network error occurred:', error.config?.url, error.message);
        }
        return Promise.reject(error);
      }
    );

  }

  // Authentication methods
  async login(credentials: UserLogin): Promise<LoginResponse> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.post('/v1/auth/login', credentials);
      const loginData = response.data as LoginResponse;

      // Store token in localStorage
      if (loginData.access_token) {
        localStorage.setItem('access_token', loginData.access_token);
      }

      return loginData;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.post('/auth/login', credentials);
        const loginData = response.data as LoginResponse;

        // Store token in localStorage
        if (loginData.access_token) {
          localStorage.setItem('access_token', loginData.access_token);
        }

        return loginData;
      }
      throw error;
    }
  }

  async register(userData: UserRegistration): Promise<LoginResponse> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.post('/v1/auth/signup', userData);
      const loginData = response.data as LoginResponse;

      // Store token in localStorage
      if (loginData.access_token) {
        localStorage.setItem('access_token', loginData.access_token);
      }

      return loginData;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.post('/auth/signup', userData);
        const loginData = response.data as LoginResponse;

        // Store token in localStorage
        if (loginData.access_token) {
          localStorage.setItem('access_token', loginData.access_token);
        }

        return loginData;
      }
      throw error;
    }
  }

  async logout(): Promise<void> {
    // Remove token from localStorage
    localStorage.removeItem('access_token');
  }

  async getProfile(): Promise<User> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.get('/v1/auth/profile');
      return response.data as User;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.get('/auth/profile');
        return response.data as User;
      }
      throw error;
    }
  }

  // Task methods
  async getTasks(): Promise<TaskListResponse> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.get('/v1/tasks/'); // note the trailing slash
      return response.data as TaskListResponse;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.get('/tasks');
        return response.data as TaskListResponse;
      }
      throw error;
    }
  }

  async createTask(taskData: TaskCreateRequest): Promise<Task> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.post('/v1/tasks/', taskData);
      return response.data as Task;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.post('/tasks', taskData);
        return response.data as Task;
      }
      throw error;
    }
  }

  async updateTask(id: string, taskData: TaskUpdateRequest): Promise<Task> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.put(`/v1/tasks/${id}`, taskData);
      return response.data as Task;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.put(`/tasks/${id}`, taskData);
        return response.data as Task;
      }
      throw error;
    }
  }

  async deleteTask(id: string): Promise<void> {
    try {
      // Try v1 prefix first, then fall back to direct route
      await this.axiosClient.delete(`/v1/tasks/${id}`);
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        await this.axiosClient.delete(`/tasks/${id}`);
        return;
      }
      throw error;
    }
  }

  async toggleTaskComplete(id: string, completeData: TaskToggleCompleteRequest): Promise<Task> {
    try {
      // Try v1 prefix first, then fall back to direct route
      const response = await this.axiosClient.patch(`/v1/tasks/${id}/complete`, completeData);
      return response.data as Task;
    } catch (error) {
      // If v1 prefix fails, try without it
      if (error.response?.status === 404) {
        const response = await this.axiosClient.patch(`/tasks/${id}/complete`, completeData);
        return response.data as Task;
      }
      throw error;
    }
  }
}

export const apiClient = new ApiClient();

export default ApiClient;