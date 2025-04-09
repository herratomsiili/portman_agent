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

// Provider component that wraps the app and makes auth available
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is already logged in on initial load
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error parsing stored user:', error);
        localStorage.removeItem('user');
      }
    }
  }, []);

  // Login function
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // TODO: Implement real authentication
      // For development, use these test accounts:
      // admin@portman.com / admin123
      // user@portman.com / user123
      // viewer@portman.com / viewer123
      
      if (email === 'admin@portman.com' && password === 'admin123') {
        const user = {
          id: '1',
          username: 'Admin User',
          email: 'admin@portman.com',
          role: 'admin' as const
        };
        setUser(user);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(user));
        return true;
      }
      
      if (email === 'user@portman.com' && password === 'user123') {
        const user = {
          id: '2',
          username: 'Regular User',
          email: 'user@portman.com',
          role: 'user' as const
        };
        setUser(user);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(user));
        return true;
      }
      
      if (email === 'viewer@portman.com' && password === 'viewer123') {
        const user = {
          id: '3',
          username: 'Viewer User',
          email: 'viewer@portman.com',
          role: 'viewer' as const
        };
        setUser(user);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(user));
        return true;
      }

      throw new Error('Invalid credentials');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  // Logout function
  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
  };

  // Register function
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
    isAuthenticated,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
