import React from "react";

import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Play, Mail } from 'lucide-react';
import { motion } from 'framer-motion';

export const Login = () => {
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
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
        <h1 className="text-2xl font-bold text-white">Welcome Back!</h1>
        <p className="text-secondary-foreground">Login to manage your AI agents</p>
      </div>

      <div className="space-y-4">
        <Button variant="outline" className="w-full gap-2 bg-white text-black hover:bg-neutral-200 border-none">
          <Play className="h-5 w-5 text-red-600" />
          Continue with YouTube
        </Button>
        <Button variant="outline" className="w-full gap-2">
          <Mail className="h-5 w-5" />
          Continue with Google
        </Button>
      </div>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-card px-2 text-secondary-foreground">Or continue with</span>
        </div>
      </div>

      <form onSubmit={handleLogin} className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-foreground">Email</label>
          <Input type="email" placeholder="name@example.com" required />
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <label className="text-sm font-medium text-secondary-foreground">Password</label>
            <Link to="/forgot-password" className="text-xs text-primary hover:underline">
              Forgot password?
            </Link>
          </div>
          <Input type="password" placeholder="••••••••" required />
        </div>
        <Button type="submit" className="w-full">
          Login
        </Button>
      </form>

      <p className="mt-8 text-center text-sm text-secondary-foreground">
        Don't have an account?{' '}
        <Link to="/signup" className="text-primary hover:underline font-medium">
          Create Account →
        </Link>
      </p>
    </motion.div>
  );
};
