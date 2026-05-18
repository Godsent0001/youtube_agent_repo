import React, { useState } from "react";

import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Play, Mail } from 'lucide-react';
import { motion } from 'framer-motion';
import { apiRequest } from '../utils/api';

export const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('user_email', email);
      setSuccess('Login successful! Redirecting...');
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (err: any) {
      if (err.message.includes('401') || err.message.toLowerCase().includes('invalid')) {
        setError('Incorrect email or password, please try again.');
      } else {
        setError(err.message || 'An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
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
        <Button variant="outline" className="w-full gap-2 bg-white text-black hover:bg-neutral-200 border-none py-6 sm:py-2">
          <Play className="h-5 w-5 text-red-600" />
          Continue with YouTube
        </Button>
        <Button variant="outline" className="w-full gap-2 py-6 sm:py-2">
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

      {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
      {success && <p className="text-green-500 text-sm mb-4 text-center">{success}</p>}
      <form onSubmit={handleLogin} className="space-y-4">
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
        <Button type="submit" className="w-full py-6 sm:py-2" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
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
