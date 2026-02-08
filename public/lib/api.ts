// frontend/lib/api.ts
// API client for interacting with the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// Define types
export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  category?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  category?: string;
  tags?: string[];
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  category?: string;
  tags?: string[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserRegistration {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// Helper function to make API requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'An error occurred');
    }

    return data;
  } catch (error: any) {
    return {
      success: false,
      error: error.message || 'Network error',
    };
  }
}

// Authentication functions
export const auth = {
  register: async (userData: UserRegistration): Promise<ApiResponse<AuthResponse>> => {
    return apiRequest<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  login: async (credentials: UserCredentials): Promise<ApiResponse<AuthResponse>> => {
    return apiRequest<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  logout: async (): Promise<ApiResponse<void>> => {
    return apiRequest<void>('/auth/logout', {
      method: 'POST',
    });
  },
};

// Todo functions
export const todos = {
  getAll: async (
    params?: {
      status?: string;
      priority?: string;
      category?: string;
      search?: string;
      sort?: string;
      order?: string;
      page?: number;
      limit?: number;
    }
  ): Promise<ApiResponse<{ todos: Todo[]; pagination: any }>> => {
    const queryParams = new URLSearchParams(params as Record<string, string>);
    return apiRequest<{ todos: Todo[]; pagination: any }>(`/todos?${queryParams}`);
  },

  getById: async (id: string): Promise<ApiResponse<{ todo: Todo }>> => {
    return apiRequest<{ todo: Todo }>(`/todos/${id}`);
  },

  create: async (todoData: TodoCreate): Promise<ApiResponse<{ todo: Todo }>> => {
    return apiRequest<{ todo: Todo }>('/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  },

  update: async (id: string, todoData: TodoUpdate): Promise<ApiResponse<{ todo: Todo }>> => {
    return apiRequest<{ todo: Todo }>(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  },

  toggle: async (id: string): Promise<ApiResponse<{ todo: Todo }>> => {
    return apiRequest<{ todo: Todo }>(`/todos/${id}/toggle`, {
      method: 'PATCH',
    });
  },

  delete: async (id: string): Promise<ApiResponse<void>> => {
    return apiRequest<void>(`/todos/${id}`, {
      method: 'DELETE',
    });
  },
};

// Categories functions
export const categories = {
  getAll: async (): Promise<ApiResponse<any>> => {
    return apiRequest('/categories');
  },

  create: async (categoryData: any): Promise<ApiResponse<any>> => {
    return apiRequest('/categories', {
      method: 'POST',
      body: JSON.stringify(categoryData),
    });
  },
};