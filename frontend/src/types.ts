
export interface User {
  id: string;
  username: string;
  email: string;
  role: string;

}

export interface UserContextType {
  user: User | null; 
  token: string | null;
  register: (username: string, email: string, password: string, role : string) => Promise<void>;
  login: (username: string, password: string) => Promise<void>; // identifier can be username or email
  logout: () => void;
}