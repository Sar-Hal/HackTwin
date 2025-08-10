import { Button } from "@/components/ui/button";
import { Clock, Users, Trophy } from "lucide-react";

export const HeroSection = () => {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-secondary to-accent">
        <div className="absolute inset-0 opacity-30" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>
      
      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
        <div className="space-y-6">
          <div className="inline-block p-1 rounded-full bg-gradient-to-r from-cyber-purple to-cyber-blue">
            <div className="px-6 py-2 rounded-full bg-background">
              <span className="text-sm font-medium bg-gradient-to-r from-cyber-purple to-cyber-blue bg-clip-text text-transparent">
                HackTwin 2024
              </span>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-cyber-purple via-cyber-blue to-cyber-green bg-clip-text text-transparent">
              Code. Create. Compete.
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto mb-8">
            Join the ultimate 48-hour hackathon where innovation meets collaboration. 
            Build solutions that matter.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button size="lg" className="bg-gradient-to-r from-cyber-purple to-cyber-blue hover:opacity-90 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-cyber-purple/25">
              Register Now
            </Button>
            <Button variant="outline" size="lg" className="border-cyber-blue text-cyber-blue hover:bg-cyber-blue/10">
              Learn More
            </Button>
          </div>
          
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 pt-16 border-t border-border">
            <div className="text-center">
              <Clock className="w-8 h-8 text-cyber-purple mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-cyber-purple">48</h3>
              <p className="text-muted-foreground">Hours of Coding</p>
            </div>
            <div className="text-center">
              <Users className="w-8 h-8 text-cyber-blue mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-cyber-blue">500+</h3>
              <p className="text-muted-foreground">Participants</p>
            </div>
            <div className="text-center">
              <Trophy className="w-8 h-8 text-cyber-green mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-cyber-green">₹1L+</h3>
              <p className="text-muted-foreground">Prize Pool</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};