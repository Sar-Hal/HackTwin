import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";

interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

export const CountdownTimer = () => {
  const [timeLeft, setTimeLeft] = useState<TimeLeft>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  // Hackathon start date - you can modify this
  const hackathonStart = new Date("2024-03-15T09:00:00");

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const distance = hackathonStart.getTime() - now;

      if (distance > 0) {
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        setTimeLeft({ days, hours, minutes, seconds });
      } else {
        setTimeLeft({ days: 0, hours: 0, minutes: 0, seconds: 0 });
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [hackathonStart]);

  return (
    <section id="timeline" className="py-20 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-cyber-purple to-cyber-blue bg-clip-text text-transparent">
            Hackathon Starts In
          </span>
        </h2>
        <p className="text-muted-foreground mb-12">March 15, 2024 at 9:00 AM</p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Days", value: timeLeft.days },
            { label: "Hours", value: timeLeft.hours },
            { label: "Minutes", value: timeLeft.minutes },
            { label: "Seconds", value: timeLeft.seconds },
          ].map((item, index) => (
            <Card key={item.label} className="bg-gradient-to-br from-secondary to-accent border-border/50">
              <CardContent className="p-6">
                <div className="text-3xl md:text-4xl font-bold text-cyber-purple mb-2">
                  {String(item.value).padStart(2, "0")}
                </div>
                <div className="text-sm text-muted-foreground uppercase tracking-wider">
                  {item.label}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-16 space-y-8">
          <h3 className="text-2xl font-bold text-cyber-blue">Event Timeline</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-secondary border-cyber-purple/20">
              <CardContent className="p-6">
                <h4 className="font-bold text-cyber-purple mb-2">Registration</h4>
                <p className="text-sm text-muted-foreground">March 1-14, 2024</p>
                <p className="text-sm mt-2">Sign up and form your teams</p>
              </CardContent>
            </Card>
            <Card className="bg-secondary border-cyber-blue/20">
              <CardContent className="p-6">
                <h4 className="font-bold text-cyber-blue mb-2">Hackathon</h4>
                <p className="text-sm text-muted-foreground">March 15-17, 2024</p>
                <p className="text-sm mt-2">48 hours of intense coding</p>
              </CardContent>
            </Card>
            <Card className="bg-secondary border-cyber-green/20">
              <CardContent className="p-6">
                <h4 className="font-bold text-cyber-green mb-2">Results</h4>
                <p className="text-sm text-muted-foreground">March 17, 2024</p>
                <p className="text-sm mt-2">Winners announcement & prizes</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};