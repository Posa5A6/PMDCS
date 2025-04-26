import React from 'react'
import { OurTeam } from './OurTeam'
import { GoalGrid } from './GoalGrid'

const AboutUs : React.FC = () => {
  return (
    <div className='pagePadding my-10'>
      <div className='flex flex-wrap gap-4 justify-center items-center text-center w-full py-10'>
        
        <img src="/ladyDoctor.jpg" alt="About Us" className='w-1/2 h-auto w-96  rounded-lg shadow-lg ' />
        <div className='md:w-1/2 w-full '>
          <h1>Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis, laudantium suscipit. Dolorem a doloribus earum ea cum dolorum dignissimos necessitatibus, numquam consequatur enim? Assumenda corrupti adipisci in quo dolorem laboriosam.</h1>
        </div>
      </div>

      <div>

        <GoalGrid/>
      </div>

      <OurTeam/>
      
    </div>
  )
}

export default AboutUs


