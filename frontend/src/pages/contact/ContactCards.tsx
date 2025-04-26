import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { MagicCard } from "@/components/magicui/magic-card";
import { useTheme } from "@/components/theme-provider"
import { Logos } from "@/utils/Logos";
import {BlurFade} from '@/components/magicui/blur-fade';

const cardsData = [
  {
    "title":"Chat to sales",
    "description":"Speak to our friendly team.",
    "link":"mailto:",
    "linkText":"",
    "img":Logos.ChatSalesIcon
  },
  {
    "title":"Chat to support",
    "description":"We're here to help",
    "link":"mailto:",
    "linkText":"",
    "img":Logos.ChatSupportIcon
  },
  {
    "title":"Follow us",
    "description":"Visit our website",
    "link":"",
    "linkText":"",
    "img":Logos.LocationIcon
  },
  {
    "title":"Call us",
    "description":"Mon-Fri from 8am to 5pm.",
    "link":"tel:+",
    "linkText":"+",
    "img":Logos.CallIcon
  },
  

]

interface ContactCardProps {
    title: string;
    description: string;
    link: string;
    linkText: string;
    img: React.FC<React.SVGProps<SVGSVGElement>>;
    }

    function ContactCard({ title, description, link, linkText, img: Img }: ContactCardProps) {
        const { theme } = useTheme();
      
        return (
          <Card className="p-0 w-sm w-full shadow-none border text-start min-h-56">
            <MagicCard
              gradientColor={theme === "dark" ? "" : "#D9D9D955"}
              className="p-0"
            >
              <CardHeader className="p-6 space-y-4 ">
                {/* Logo on top */}
                <div className="w-12 h-12">
                  <Img />
                </div>
      
                {/* Title and description */}
                <div>
                  <CardTitle className="text-lg">{title}</CardTitle>
                  <CardDescription className="text-sm mt-2">{description}</CardDescription>
                </div>
      
                {/* Link at the bottom */}
                {link && (
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-3 text-sm font-medium text-primary underline hover:text-primary/80 transition"
                  >
                    {linkText || "Learn more"}
                  </a>
                )}
              </CardHeader>
            </MagicCard>
          </Card>
        );
      }
      


const ContactCards = () => {
  return (
    <div className="pagePadding my-10">
      <div className="grid grid-cols-4 gap-5">
        {cardsData.map((card, index) => (
            <BlurFade key={index} className="w-full max-w-sm"
                delay={0.25+(index/2)}
                inView 
            >
                <ContactCard
                    title={card.title}
                    description={card.description}
                    link={card.link}
                    linkText={card.linkText}
                    img={card.img}
                />
          </BlurFade>
        ))}

        </div>
    </div>
  )
}

export default ContactCards