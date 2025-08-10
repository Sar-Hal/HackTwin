import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Brain, Leaf, Shield, Smartphone, Globe, Heart, Check } from "lucide-react";

const problemStatements = [
  {
    id: 1,
    title: "AI-Powered Healthcare Assistant",
    description: "Develop an AI-driven platform that can diagnose common health issues, provide medical recommendations, and connect patients with healthcare professionals.",
    category: "Healthcare",
    difficulty: "Hard",
    icon: Heart,
    tags: ["AI/ML", "Healthcare", "APIs"],
    details: "Build a comprehensive healthcare assistant that uses machine learning to analyze symptoms, provide preliminary diagnoses, and offer health recommendations. The solution should include patient data management, appointment scheduling, and telemedicine integration."
  },
  {
    id: 2,
    title: "Sustainable Smart City Dashboard",
    description: "Create a real-time dashboard for monitoring and optimizing resource usage in smart cities including energy, water, and waste management.",
    category: "Sustainability",
    difficulty: "Medium",
    icon: Leaf,
    tags: ["IoT", "Data Visualization", "Sustainability"],
    details: "Design an interactive dashboard that aggregates data from various city sensors and systems. Include features for energy consumption tracking, waste management optimization, water usage monitoring, and citizen engagement tools."
  },
  {
    id: 3,
    title: "Cybersecurity Threat Detection",
    description: "Build an advanced cybersecurity system that can detect, analyze, and respond to various types of cyber threats in real-time.",
    category: "Security",
    difficulty: "Hard",
    icon: Shield,
    tags: ["Cybersecurity", "Machine Learning", "Real-time"],
    details: "Develop a comprehensive threat detection system using machine learning algorithms to identify suspicious activities, malware, and potential security breaches. Include automated response mechanisms and detailed threat analysis reports."
  },
  {
    id: 4,
    title: "Education Technology Platform",
    description: "Design an innovative EdTech solution that personalizes learning experiences and makes education more accessible and engaging.",
    category: "Education",
    difficulty: "Medium",
    icon: Brain,
    tags: ["EdTech", "Personalization", "Mobile"],
    details: "Create a learning platform that adapts to individual student needs, provides personalized curriculum, includes gamification elements, and offers offline capabilities for students in remote areas."
  },
  {
    id: 5,
    title: "Blockchain-Based Supply Chain",
    description: "Develop a transparent and traceable supply chain management system using blockchain technology.",
    category: "Blockchain",
    difficulty: "Hard",
    icon: Globe,
    tags: ["Blockchain", "Supply Chain", "Transparency"],
    details: "Build a decentralized supply chain tracking system that ensures transparency, reduces fraud, and enables consumers to trace products from origin to delivery. Include smart contracts for automated transactions."
  },
  {
    id: 6,
    title: "Mental Health Support App",
    description: "Create a mobile application that provides mental health support, mood tracking, and connects users with mental health professionals.",
    category: "Healthcare",
    difficulty: "Easy",
    icon: Smartphone,
    tags: ["Mobile App", "Mental Health", "UI/UX"],
    details: "Design a user-friendly mobile app that offers mood tracking, meditation guidance, mental health resources, crisis support, and easy access to licensed therapists and counselors."
  }
];

interface ProblemSelectorProps {
  selectedProblemId?: number;
  onProblemSelect: (problemId: number) => void;
}

export const ProblemSelector = ({ selectedProblemId, onProblemSelect }: ProblemSelectorProps) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case "easy":
        return "bg-cyber-green/20 text-cyber-green border-cyber-green/30";
      case "medium":
        return "bg-cyber-blue/20 text-cyber-blue border-cyber-blue/30";
      case "hard":
        return "bg-cyber-pink/20 text-cyber-pink border-cyber-pink/30";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">
          <span className="bg-gradient-to-r from-cyber-purple to-cyber-blue bg-clip-text text-transparent">
            Select Problem Statement
          </span>
        </h2>
        <p className="text-muted-foreground">
          Choose a problem statement that interests you and your team
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {problemStatements.map((problem) => {
          const IconComponent = problem.icon;
          const isSelected = selectedProblemId === problem.id;
          
          return (
            <Card 
              key={problem.id} 
              className={`cursor-pointer transition-all duration-300 hover:scale-105 ${
                isSelected 
                  ? 'border-cyber-green bg-cyber-green/5 shadow-lg shadow-cyber-green/20' 
                  : 'hover:border-cyber-blue/50 hover:shadow-lg hover:shadow-cyber-blue/10'
              }`}
              onClick={() => onProblemSelect(problem.id)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="p-3 rounded-lg bg-gradient-to-br from-cyber-purple/20 to-cyber-blue/20">
                    <IconComponent className="w-6 h-6 text-cyber-purple" />
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <Badge className={getDifficultyColor(problem.difficulty)}>
                      {problem.difficulty}
                    </Badge>
                    {isSelected && (
                      <div className="flex items-center gap-1 text-cyber-green">
                        <Check className="w-4 h-4" />
                        <span className="text-xs font-medium">Selected</span>
                      </div>
                    )}
                  </div>
                </div>
                <CardTitle className="text-lg">{problem.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-sm mb-3 line-clamp-2">
                  {problem.description}
                </p>
                
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-1">
                    {problem.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {problem.tags.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{problem.tags.length - 3}
                      </Badge>
                    )}
                  </div>
                  
                  <div className="text-xs text-muted-foreground">
                    <strong className="text-cyber-purple">Category:</strong> {problem.category}
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};