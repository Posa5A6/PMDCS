import React from 'react'
import { AuroraText } from "@/components/magicui/aurora-text";
import { InteractiveHoverButton } from '@/components/magicui/interactive-hover-button';


const HeroSection : React.FC = () => {
  return (
    <div className='pagePadding py-20 mb-10 flex w-full items-center '>
      <div className='max-w-2xl  flex flex-col gap-4 md:px-10'>

      <h1 className="text-4xl font-bold md:text-5xl lg:text-7xl tracking-normal">
        Welcome to <br/> <AuroraText className='tracking-wider'>PMDCS</AuroraText>
      </h1>
        <p className='mt-2 text-lg text-foreground/60 w-4/5'>PMDCS is a revolutionary healthcare platform designed to centralize patient data and enhance collaboration between healthcare providers and patients. Our goal is to improve healthcare delivery by leveraging the latest in technology.</p>

        
        <InteractiveHoverButton className='w-fit' 
        onClick={() => {
            const el = document.getElementById('exploreSection');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
          }}
        >
            Explore Now
        </InteractiveHoverButton>
        
        
        
      </div>

      <div>
        <img src="doctor_1.svg" alt="Landing Image" className='hidden md:block w-full h-full object-cover' />
      </div>

      
    </div>
  )
}

export default HeroSection