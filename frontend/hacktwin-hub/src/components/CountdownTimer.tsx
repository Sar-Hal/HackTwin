import { useEffect, useState } from "react";

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

  // Hackathon start date - August 10th, 2025 at 18:30
  const hackathonStart = new Date("2025-08-10T18:30:00");

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

  const padNumber = (num: number): string => num.toString().padStart(2, '0');

  return (
    <section id="timeline" className="py-20 px-4 bg-black/95">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="bg-gradient-to-r from-[#9333EA] via-[#3B82F6] to-[#06B6D4] bg-clip-text text-transparent">
            Hackathon Starts In
          </span>
        </h2>
        <p className="text-gray-400 mb-12 text-lg">August 10, 2025 at 6:30 PM</p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 shadow-2xl">
            <div className="text-5xl md:text-6xl font-bold bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent mb-2">
              {padNumber(timeLeft.days)}
            </div>
            <div className="text-sm uppercase tracking-widest text-gray-400 font-medium">
              Days
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 shadow-2xl">
            <div className="text-5xl md:text-6xl font-bold bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent mb-2">
              {padNumber(timeLeft.hours)}
            </div>
            <div className="text-sm uppercase tracking-widest text-gray-400 font-medium">
              Hours
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 shadow-2xl">
            <div className="text-5xl md:text-6xl font-bold bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent mb-2">
              {padNumber(timeLeft.minutes)}
            </div>
            <div className="text-sm uppercase tracking-widest text-gray-400 font-medium">
              Minutes
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 shadow-2xl">
            <div className="text-5xl md:text-6xl font-bold bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent mb-2">
              {padNumber(timeLeft.seconds)}
            </div>
            <div className="text-sm uppercase tracking-widest text-gray-400 font-medium">
              Seconds
            </div>
          </div>
        </div>

      </div>
    </section>
  );
};