export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRegistration extends UserLogin {
  first_name?: string;
  last_name?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}