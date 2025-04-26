import AppointmentsTable from '@/components/AppointmentTable'
import React from 'react'

const Dashboard = () => {
  return (
    <div className='pagePadding min-h-screen py-10'>
      Dashboard

        <AppointmentsTable/>
    </div>
  )
}

export default Dashboard