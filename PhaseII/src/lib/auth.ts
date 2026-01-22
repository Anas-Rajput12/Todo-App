import { User } from '../../../shared/types';

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('access_token');
  return !!token;
};

// Get the current user from localStorage or return null
export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('current_user');
  if (!userStr) return null;

  try {
    return JSON.parse(userStr);
  } catch (error) {
    console.error('Error parsing current user from localStorage:', error);
    return null;
  }
};

// Save the current user to localStorage
export const setCurrentUser = (user: User): void => {
  localStorage.setItem('current_user', JSON.stringify(user));
};

// Clear authentication data
export const clearAuthData = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('current_user');
};

// Get the authentication token
export const getToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// Set the authentication token
export const setToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

// Check if token is expired (helper function)
export const isTokenExpired = (token: string): boolean => {
  try {
    const payload = token.split('.')[1];
    const decodedPayload = atob(payload);
    const parsedPayload = JSON.parse(decodedPayload);
    const currentTime = Math.floor(Date.now() / 1000);

    return parsedPayload.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true; // If we can't decode, assume expired
  }
};