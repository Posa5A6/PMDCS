// UserContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { User, UserContextType } from '@/types';

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const URL = import.meta.env.VITE_BACKEND_URL;

  const register = async (username: string, email: string, password: string, role:string) => {
    try {
      const response = await fetch(`${URL}/api/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, role }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Registration error:', errorData);
        return {
          status: response.status,
          message: errorData.message,
        }

      }
      const data: { user: User; token: string, message: string } = await response.json();
      console.log(data)
      setUser(data.user);
      setToken(data.token);
      localStorage.setItem('token', data.token);
       return {
        status: response.status,
        message: data.message,
      };

    } catch (error) {
      console.error('Error registering user:', error);
      return {
        status: 400, 
        message: 'Registration failed. Please try again.',
      };
    }
  };

  const login = async (email: string, password: string) => {
    console.log("loginrew");
    console.log(email, password)
    try {
      const response = await fetch(`${URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      console.log(response)

      if (!response.ok) {
        const errorData = await response.json();
        return {
          status: response.status,
          message: errorData.message,
        };
      }

      const data: { user: User; token: string } = await response.json();
      setUser(data.user);
      setToken(data.token);
      localStorage.setItem('token', data.token);
      return {
        status: response.status,
        message: 'Login successful',
      };
    } catch (error) {
      console.error('Error logging in:', error);
      return {
        status: 400,
        message: 'Login failed. Please check your credentials.',
      };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <UserContext.Provider value={{ user, token, register, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

// Custom hook to use the UserContext
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};