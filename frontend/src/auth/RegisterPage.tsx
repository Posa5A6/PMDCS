import React, { useState } from 'react'
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useId } from "react";
import { Button } from "@/components/ui/button";
import { useUser } from '@/context/UserContext';
import { useNavigate } from 'react-router';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"


const RegisterPage : React.FC = () => {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [role, setRole] = useState("")

  const{ register }= useUser()
  const navigate = useNavigate();
  const handleRegister = async (e : React.FormEvent) => {
    e.preventDefault();
    try {
      console.log("registering");
      console.log(username, email, password, role);
      await register(username, email, password,role);
      navigate('/');
    } catch (error) {
      console.error(error);
    }
  }
  const id = useId();
  return (
    <div className="h-screen w-screen  flex justify-center items-center">
      <div className="w-72 mx-auto border  px-3 py-6 rounded-md">
        <h1 className="text-xl text-center font-semibold">Register</h1>
      <form className="space-y-5" onSubmit={handleRegister}>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor={`${id}-username`}>Username</Label>
            <Input
              id={`${id}-username`}
              placeholder="username"
              type="username"
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor={`${id}-email`}>Email</Label>
            <Input
              id={`${id}-email`}
              placeholder="example@mail.com"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor={`${id}-password`}>Password</Label>
            <Input
              id={`${id}-password`}
              placeholder="Enter your password"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor={`${id}-role`}>Role</Label>
          <Select onValueChange={(value) => setRole(value)} required>
            <SelectTrigger className="w-full ">
              <SelectValue placeholder="You are" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="patient">Patient</SelectItem>
              <SelectItem value="doctor">Doctor</SelectItem>
            </SelectContent>
          </Select>
          </div>
        </div>
        
        <div className="flex justify-between gap-2">
          {/* <a className="text-sm underline hover:no-underline" href="#">
              Forgot password?
            </a> */}
            <p className="text-sm text-gray-400">Already have an account?<a href="/login" className="text-[#7F56D9] underline px-1">Login</a></p>
        </div>
        <Button type="submit" className="w-full">
          Sign in
        </Button>
      </form>
      </div>
    </div>
  )
}

export default RegisterPage