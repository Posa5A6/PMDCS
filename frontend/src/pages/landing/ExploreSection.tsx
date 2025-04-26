import React from 'react'
import {  Calendar } from 'lucide-react';
import { Link } from 'react-router';

const ExploreSection : React.FC = () => {
  return (
    <div className='pagePadding min-h-96 py-10'>
      <div className='text-center mb-10'>

        <span className='text-xl'>Get your </span>
        <span className='text-3xl font-bold'>Treatment done</span>
        <p className='text-foreground/80 w-1/2 mx-auto my-1'>We have a wide range of services to help you get the treatment you need.</p>
      </div>

        <Link to={'/events'}>
          <button className='bg-[#7F56D9] hover:bg-[#6941c6] px-6 py-3 rounded-md text-lg text-white font-semibold transition-all ease-in-out duration-150 flex items-center justify-center mx-auto'>
            <Calendar className='mr-2' />
            Book an appointment
          </button>
        </Link>
    </div>
  )
}

export default ExploreSection