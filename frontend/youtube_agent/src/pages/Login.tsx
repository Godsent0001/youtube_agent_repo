import React, { useState } from "react";

import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Play, Mail } from 'lucide-react';
import { motion } from 'framer-motion';
import { api } from '../utils/api';

export const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await api.post<{ user_id: string; access_token: string }>('/auth/login', {
        email,
        password,
      });

      localStorage.setItem('user_id', response.user_id);
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_email', email);

      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
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
        {error && (
          <div className="p-3 text-sm text-red-500 bg-red-500/10 border border-red-500/20 rounded-md">
            {error}
          </div>
        )}
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-foreground">Email</label>
          <Input
            type="email"
            placeholder="name@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <label className="text-sm font-medium text-secondary-foreground">Password</label>
            <Link to="/forgot-password" className="text-xs text-primary hover:underline">
              Forgot password?
            </Link>
          </div>
          <Input
            type="password"
            placeholder="••••••••"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
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
