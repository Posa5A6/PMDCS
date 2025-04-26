import { LinkedinIcon, InstagramIcon, TwitterIcon } from 'lucide-react';
import React from 'react';
import { Link } from 'react-router';

const Footer: React.FC = () => {
  return (
    <footer className=" py-4 min-h-52">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="mb-4 md:mb-0">
          <Link to="/" className="text-xl font-bold">PMDCS</Link>
          <p>© 2025 Events. All rights reserved.</p>
        </div>
        <div className="flex space-x-4">
          <LinkedinIcon/>
          <InstagramIcon/>
          <TwitterIcon/>
        </div>
      </div>
    </footer>
  );
};

export default Footer;