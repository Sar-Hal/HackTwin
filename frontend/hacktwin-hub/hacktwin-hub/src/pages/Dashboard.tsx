import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  User, 
  Users, 
  Trophy, 
  Clock, 
  Code, 
  Star, 
  Calendar,
  MapPin,
  Mail,
  Phone,
  LogOut,
  FileText,
  Upload
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { ProblemSelector } from "@/components/ProblemSelector";

// Mock user data
const userData = {
  id: "USR001",
  name: "Satya Aman",
  email: "satya.aman@email.com",
  phone: "+91 98765 43210",
  college: "IIT Delhi",
  year: "3rd Year",
  branch: "Computer Science",
  experience: "Intermediate",
  skills: ["React", "Node.js", "Python", "AI/ML", "Blockchain"],
  teamStatus: "Team Leader",
  teamName: "Code Crusaders",
  teamMembers: [
    { name: "Satya Aman", role: "Team Leader", skills: ["React", "Node.js"] },
    { name: "Arka Roy", role: "Frontend Dev", skills: ["React", "TypeScript"] },
    { name: "Shalo", role: "Designer", skills: ["UI/UX", "Figma"] },
    { name: "Sarthakbrata Halder", role: "Backend Dev", skills: ["Python", "Django"] },
    { name: "Sarthak H", role: "Full Stack", skills: ["MERN", "DevOps"] },
    { name: "Arkabrata Roy", role: "AI Specialist", skills: ["ML", "TensorFlow"] },
    { name: "Carol Williams", role: "Data Analyst", skills: ["Python", "SQL"] },
    { name: "Bob Chen", role: "Mobile Dev", skills: ["React Native", "Flutter"] },
    { name: "Alice Johnson", role: "QA Engineer", skills: ["Testing", "Automation"] }
  ],
  selectedProblem: {
    id: 1,
    title: "AI-Powered Healthcare Assistant",
    category: "Healthcare",
    difficulty: "Hard"
  },
  submissions: [],
  achievements: [
    { title: "Early Bird", description: "Registered in first week", icon: "🐦" },
    { title: "Team Player", description: "Formed complete team", icon: "👥" },
    { title: "Problem Solver", description: "Selected problem statement", icon: "🧩" }
  ]
};

export default function Dashboard() {
  const navigate = useNavigate();
  const [selectedProblemId, setSelectedProblemId] = useState<number>(userData.selectedProblem.id);
  const [showProblemSelector, setShowProblemSelector] = useState<boolean>(false);

  const handleLogout = () => {
    navigate("/");
  };

  const handleProblemSelect = (problemId: number) => {
    setSelectedProblemId(problemId);
    setShowProblemSelector(false);
    // Here you would update the user data in your backend
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-2 rounded-lg bg-gradient-to-r from-cyber-purple to-cyber-blue">
                <Code className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyber-purple to-cyber-blue bg-clip-text text-transparent">
                  HackTwin Dashboard
                </h1>
                <p className="text-sm text-muted-foreground">Welcome back, {userData.name}!</p>
              </div>
            </div>
            <Button onClick={handleLogout} variant="ghost" size="sm">
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="profile">Profile</TabsTrigger>
            <TabsTrigger value="team">Team</TabsTrigger>
            <TabsTrigger value="problem">Problem</TabsTrigger>
            <TabsTrigger value="submissions">Submissions</TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="space-y-6">
            {/* Profile Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="w-5 h-5 text-cyber-purple" />
                    Profile Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <Avatar className="w-20 h-20">
                      <AvatarImage src="" />
                      <AvatarFallback className="text-lg bg-gradient-to-r from-cyber-purple to-cyber-blue text-white">
                        {userData.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="text-xl font-bold">{userData.name}</h3>
                      <p className="text-muted-foreground">{userData.college}</p>
                      <Badge variant="secondary">{userData.experience}</Badge>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">{userData.email}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Phone className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">{userData.phone}</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">{userData.branch}, {userData.year}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">ID: {userData.id}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-3">Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {userData.skills.map((skill) => (
                        <Badge key={skill} variant="outline" className="border-cyber-blue text-cyber-blue">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-3 flex items-center gap-2">
                      <FileText className="w-4 h-4 text-cyber-purple" />
                      Resume
                    </h4>
                    <div className="p-4 border border-border rounded-lg bg-secondary/30">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="p-2 rounded-lg bg-gradient-to-r from-cyber-purple/20 to-cyber-blue/20">
                            <FileText className="w-5 h-5 text-cyber-purple" />
                          </div>
                          <div>
                            <p className="font-medium text-sm">Resume.pdf</p>
                            <p className="text-xs text-muted-foreground">Uploaded 2 days ago</p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            View
                          </Button>
                          <Button variant="outline" size="sm">
                            <Upload className="w-4 h-4 mr-1" />
                            Update
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="space-y-6">
                {/* Achievements */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Trophy className="w-5 h-5 text-cyber-green" />
                      Achievements
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {userData.achievements.map((achievement, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-secondary/50">
                        <span className="text-2xl">{achievement.icon}</span>
                        <div>
                          <h5 className="font-semibold text-sm">{achievement.title}</h5>
                          <p className="text-xs text-muted-foreground">{achievement.description}</p>
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>

                {/* Quick Stats */}
                <Card>
                  <CardHeader>
                    <CardTitle>Quick Stats</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Team Status</span>
                      <Badge className="bg-cyber-green/20 text-cyber-green border-cyber-green/30">
                        {userData.teamStatus}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Problem Selected</span>
                      <Badge className="bg-cyber-blue/20 text-cyber-blue border-cyber-blue/30">
                        Yes
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Submissions</span>
                      <span className="text-sm font-semibold">{userData.submissions.length}</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="team" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-cyber-blue" />
                  Team: {userData.teamName}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {userData.teamMembers.map((member, index) => (
                    <div key={index} className="p-4 rounded-lg border border-border bg-secondary/30">
                      <div className="flex items-center gap-3 mb-3">
                        <Avatar>
                          <AvatarFallback className="bg-gradient-to-r from-cyber-purple to-cyber-blue text-white">
                            {member.name.split(' ').map(n => n[0]).join('')}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <h4 className="font-semibold">{member.name}</h4>
                          <p className="text-sm text-muted-foreground">{member.role}</p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {member.skills.map((skill) => (
                          <Badge key={skill} variant="secondary" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="problem" className="space-y-6">
            {showProblemSelector ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Star className="w-5 h-5 text-cyber-green" />
                      Problem Selection
                    </CardTitle>
                    <Button 
                      variant="outline" 
                      onClick={() => setShowProblemSelector(false)}
                      size="sm"
                    >
                      Back to Selected
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <ProblemSelector 
                    selectedProblemId={selectedProblemId}
                    onProblemSelect={handleProblemSelect}
                  />
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Star className="w-5 h-5 text-cyber-green" />
                      Selected Problem Statement
                    </CardTitle>
                    <Button 
                      variant="outline" 
                      onClick={() => setShowProblemSelector(true)}
                      size="sm"
                    >
                      Change Problem
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-xl font-bold">{userData.selectedProblem.title}</h3>
                      <div className="flex gap-2">
                        <Badge className="bg-cyber-green/20 text-cyber-green border-cyber-green/30">
                          {userData.selectedProblem.category}
                        </Badge>
                        <Badge className="bg-cyber-pink/20 text-cyber-pink border-cyber-pink/30">
                          {userData.selectedProblem.difficulty}
                        </Badge>
                      </div>
                    </div>
                    <p className="text-muted-foreground">
                      Develop an AI-driven platform that can diagnose common health issues, provide medical 
                      recommendations, and connect patients with healthcare professionals. Build a comprehensive 
                      healthcare assistant that uses machine learning to analyze symptoms.
                    </p>
                    <div className="flex gap-4 pt-4">
                      <Button className="bg-gradient-to-r from-cyber-purple to-cyber-blue hover:opacity-90">
                        View Full Details
                      </Button>
                      <Button variant="outline" className="border-cyber-green text-cyber-green hover:bg-cyber-green/10">
                        Start Working
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="submissions" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-cyber-purple" />
                  Submissions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12">
                  <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-r from-cyber-purple to-cyber-blue opacity-20 flex items-center justify-center">
                    <Code className="w-10 h-10 text-cyber-purple" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">No submissions yet</h3>
                  <p className="text-muted-foreground mb-6">
                    Start working on your project and submit your progress here.
                  </p>
                  <Button className="bg-gradient-to-r from-cyber-purple to-cyber-blue hover:opacity-90">
                    Make Your First Submission
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}