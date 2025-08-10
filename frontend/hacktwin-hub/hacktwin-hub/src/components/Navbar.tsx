import { Button } from "@/components/ui/button";
import { Code, Menu, X } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate("/")}>
            <div className="p-2 rounded-lg bg-gradient-to-r from-cyber-purple to-cyber-blue">
              <Code className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-cyber-purple to-cyber-blue bg-clip-text text-transparent">
              HackTwin
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#problems" className="text-foreground hover:text-cyber-blue transition-colors">
              Problems
            </a>
            <a href="#timeline" className="text-foreground hover:text-cyber-blue transition-colors">
              Timeline
            </a>
            <a href="#rules" className="text-foreground hover:text-cyber-blue transition-colors">
              Rules
            </a>
            <a href="#sponsors" className="text-foreground hover:text-cyber-blue transition-colors">
              Sponsors
            </a>
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate("/login")}
              className="hover:text-cyber-blue"
            >
              Login
            </Button>
            <Button 
              onClick={() => navigate("/login")}
              className="bg-gradient-to-r from-cyber-purple to-cyber-blue hover:opacity-90"
            >
              Register
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden bg-background/95 backdrop-blur-md border-b border-border">
          <div className="px-4 py-6 space-y-4">
            <a href="#problems" className="block text-foreground hover:text-cyber-blue transition-colors">
              Problems
            </a>
            <a href="#timeline" className="block text-foreground hover:text-cyber-blue transition-colors">
              Timeline
            </a>
            <a href="#rules" className="block text-foreground hover:text-cyber-blue transition-colors">
              Rules
            </a>
            <a href="#sponsors" className="block text-foreground hover:text-cyber-blue transition-colors">
              Sponsors
            </a>
            <div className="pt-4 space-y-2">
              <Button 
                variant="ghost" 
                className="w-full justify-start hover:text-cyber-blue"
                onClick={() => navigate("/login")}
              >
                Login
              </Button>
              <Button 
                className="w-full bg-gradient-to-r from-cyber-purple to-cyber-blue hover:opacity-90"
                onClick={() => navigate("/login")}
              >
                Register
              </Button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};