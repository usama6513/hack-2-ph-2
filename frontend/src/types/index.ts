export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface Todo {
  id: number;
  description: string;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Token {
  sub: string;
  email: string;
  exp: number;
}