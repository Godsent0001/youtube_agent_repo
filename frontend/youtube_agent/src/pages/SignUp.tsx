import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Play } from 'lucide-react';
import { motion } from 'framer-motion';

export const SignUp = () => {
  const navigate = useNavigate();

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
    >
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-white">Create Your Account</h1>
        <p className="text-secondary-foreground">Start building AI channels</p>
      </div>

      <div className="space-y-4">
        <Button variant="outline" className="w-full gap-2 bg-white text-black hover:bg-neutral-200 border-none">
          <Play className="h-5 w-5 text-red-600" />
          Sign up with YouTube
        </Button>
      </div>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-card px-2 text-secondary-foreground">Or sign up with email</span>
        </div>
      </div>

      <form onSubmit={handleSignUp} className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-foreground">Email</label>
          <Input type="email" placeholder="name@example.com" required />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-foreground">Password</label>
          <Input type="password" placeholder="••••••••" required />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-foreground">Confirm Password</label>
          <Input type="password" placeholder="••••••••" required />
        </div>
        <Button type="submit" className="w-full">
          Sign Up
        </Button>
      </form>
    </motion.div>
  );
};
