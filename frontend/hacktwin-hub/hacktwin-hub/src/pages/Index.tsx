import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import { CountdownTimer } from "@/components/CountdownTimer";
import { ProblemStatements } from "@/components/ProblemStatements";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <HeroSection />
      <CountdownTimer />
      <ProblemStatements />
    </div>
  );
};

export default Index;
