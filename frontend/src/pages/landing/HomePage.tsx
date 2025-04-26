import React from 'react';
import HeroSection from './HeroSection';
import ExploreSection from './ExploreSection';

const HomePage: React.FC = () => {
  return (
    <div>
      <HeroSection/>
      <div id="exploreSection">
      <ExploreSection />
      </div>
    </div>
  );
}

export default HomePage;