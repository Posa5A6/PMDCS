
export interface User {
  id: string;
  username: string;
  email: string;
  role: string;

}

export interface UserContextType {
  user: User | null; 
  token: string | null;
  register: (username: string, email: string, password: string, role : string) => Promise<{ status:number, message:string }>;
  login: (mail: string, password: string) => Promise<{ status:number, message:string }>; 
  logout: () => void;
}