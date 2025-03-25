import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import { User } from '../types';

// Define the shape of our auth context
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (name: string, email: string, password: string, role: string) => Promise<boolean>;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  login: async () => false,
  logout: () => {},
  register: async () => false,
});

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

interface AuthProviderProps {
  children: ReactNode;
}

// Mock user data for demonstration
const mockUsers = [
  {
    id: '1',
    username: 'admin',
    email: 'admin@example.com',
    role: 'admin' as const,
  },
  {
    id: '2',
    username: 'user',
    email: 'user@example.com',
    role: 'user' as const,
  },
];

// Default user for auto-login
const defaultUser = mockUsers[0];

// Provider component that wraps the app and makes auth available
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(defaultUser); // Set default user immediately

  // Auto-login on initial load
  useEffect(() => {
    // Set the default user in localStorage for persistence
    if (!localStorage.getItem('portmanUser')) {
      localStorage.setItem('portmanUser', JSON.stringify(defaultUser));
    }
  }, []);

  // Login function (kept for future use)
  const login = async (email: string, password: string): Promise<boolean> => {
    // In a real app, this would call an API
    // For demo purposes, we'll just check against our mock users
    const foundUser = mockUsers.find(u => u.email === email);

    if (foundUser) {
      // In a real app, we would verify the password here
      setUser(foundUser);
      localStorage.setItem('portmanUser', JSON.stringify(foundUser));
      return true;
    }

    return false;
  };

  // Logout function (kept for future use)
  const logout = () => {
    // Instead of logging out completely, we'll just switch back to the default user
    setUser(defaultUser);
    localStorage.setItem('portmanUser', JSON.stringify(defaultUser));
  };

  // Register function (kept for future use)
  const register = async (name: string, email: string, password: string, role: string): Promise<boolean> => {
    // In a real app, this would call an API to create a new user
    // For demo purposes, we'll just pretend it worked
    const newUser = {
      id: `${mockUsers.length + 1}`,
      username: name,
      email,
      role: role as 'admin' | 'user' | 'viewer',
    };

    // In a real app, we would add the user to the database
    // For demo purposes, we'll just return success
    return true;
  };

  // Value object that will be passed to consumers
  const value = {
    user,
    isAuthenticated: true, // Always authenticated
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
