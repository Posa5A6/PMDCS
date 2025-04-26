import './App.css'
import { BrowserRouter, Routes, Route } from "react-router";
import Layout from './layout';
import HomePage from '@/pages/landing/HomePage';
import ProtectedRoute from "./auth/ProtectedRoute"
import RegisterPage from './auth/RegisterPage';
import LoginPage from './auth/LoginPage';
import AboutUs from './pages/about/AboutUs';
import ContactUs from './pages/contact/ContactUs';
import Dashboard from './pages/dashboard/Dashboard';

function App() {
  

  return (
    <BrowserRouter>
    <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage/>} />
          <Route path="/about" element={<AboutUs/>} /> 
          <Route path="/contact" element={<ContactUs/>} /> 
          <Route path="/dashboard" element={<Dashboard/>} /> 
          <Route element={<ProtectedRoute />}>
            {/* <Route path="/event/:eventId" element={<EventRoom />} />
            <Route path="/create-event" element={<CreateEvent />} />
            <Route path="/edit-event/:id" element={<EditEvent />} /> */}
          </Route>
        </Route>
        <Route path='/register' element={<RegisterPage />}/>
        <Route path='/login' element={<LoginPage/>}/>
    </Routes>
  </BrowserRouter>
  )
}

export default App