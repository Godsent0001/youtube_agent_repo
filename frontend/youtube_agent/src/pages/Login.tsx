import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Waves } from 'lucide-react';
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
      setTimeout(() => navigate('/'), 1500);
    } catch (err: any) {
      setError(err.message || 'Incorrect email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0F1115] flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md"
      >
        <div className="bg-white/[0.03] border border-white/5 rounded-[40px] p-12 shadow-2xl">
          <div className="text-center mb-10">
            <div className="flex justify-center mb-6">
                <div className="h-16 w-16 rounded-2xl bg-primary flex items-center justify-center shadow-[0_0_30px_rgba(59,130,246,0.3)]">
                    <Waves className="h-10 w-10 text-white" />
                </div>
            </div>
            <h1 className="text-3xl font-black text-white tracking-tight mb-2">MorphFlow</h1>
            <p className="text-white/40 font-medium">Log in to your creative suite</p>
          </div>

          {error && <p className="text-red-500 text-sm mb-6 text-center font-bold">{error}</p>}
          {success && <p className="text-green-500 text-sm mb-6 text-center font-bold">{success}</p>}

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-white/20 ml-1">Email Address</label>
              <input
                  type="email"
                  placeholder="name@example.com"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-white/[0.05] border border-white/10 rounded-2xl px-6 py-4 text-white placeholder:text-white/10 focus:outline-none focus:border-primary transition-colors font-bold"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center px-1">
                <label className="text-xs font-black uppercase tracking-widest text-white/20">Password</label>
                <Link to="/forgot-password" title="Forgot password?" className="text-[10px] font-black text-primary hover:text-white transition-colors uppercase tracking-widest">
                  Forgot?
                </Link>
              </div>
              <input
                  type="password"
                  placeholder="••••••••"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-white/[0.05] border border-white/10 rounded-2xl px-6 py-4 text-white placeholder:text-white/10 focus:outline-none focus:border-primary transition-colors font-bold"
              />
            </div>

            <Button
                type="submit"
                className="w-full py-8 rounded-2xl font-black text-lg bg-primary text-white hover:bg-primary/90 transition-all mt-4"
                disabled={loading}
            >
              {loading ? 'Processing...' : 'Enter MorphFlow'}
            </Button>
          </form>

          <p className="mt-10 text-center text-sm text-white/40 font-medium">
            New here?{' '}
            <Link to="/signup" className="text-primary hover:text-white font-black transition-colors">
              Create Account →
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};
