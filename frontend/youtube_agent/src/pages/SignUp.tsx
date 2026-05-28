import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Waves } from 'lucide-react';
import { motion } from 'framer-motion';
import { apiRequest } from '../utils/api';

export const SignUp = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // Background items for depth
  const bgItems = Array.from({ length: 6 }).map((_, i) => ({
    id: i,
    size: Math.random() * 300 + 100,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 10 + 10
  }));

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      const data = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, username: email.split('@')[0] }),
      });
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('user_email', email);
      setSuccess('Account created successfully! Welcome aboard.');
      setTimeout(() => navigate('/'), 1500);
    } catch (err: any) {
      if (err.message.toLowerCase().includes('already exists')) {
        setError('An account with this email already exists.');
      } else {
        setError(err.message || 'Could not create account. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden flex items-center justify-center px-4">
      {/* Dynamic Background */}
      {bgItems.map(item => (
        <motion.div
          key={item.id}
          className="absolute rounded-full bg-primary/5 blur-[100px]"
          style={{
            width: item.size,
            height: item.size,
            left: `${item.x}%`,
            top: `${item.y}%`,
          }}
          animate={{
            x: [0, 50, -50, 0],
            y: [0, -50, 50, 0],
          }}
          transition={{
            duration: item.duration,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      ))}

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md z-10 py-10"
      >
        <div className="neo-out rounded-[40px] p-8 sm:p-12 blue-glow border border-white/5">
          <div className="text-center mb-10">
            <div className="flex justify-center mb-6">
                <motion.div
                    whileHover={{ rotate: 180 }}
                    transition={{ duration: 0.5 }}
                    className="h-16 w-16 rounded-2xl bg-primary flex items-center justify-center shadow-[0_0_30px_rgba(59,130,246,0.4)]"
                >
                    <Waves className="h-10 w-10 text-white" />
                </motion.div>
            </div>
            <h1 className="text-3xl font-black text-white tracking-tight mb-2">Join MorphFlow</h1>
            <p className="text-secondary-foreground font-medium">Start your viral journey today</p>
          </div>

          {error && <p className="text-red-500 text-sm mb-6 text-center font-bold">{error}</p>}
          {success && <p className="text-green-500 text-sm mb-6 text-center font-bold">{success}</p>}

          <form onSubmit={handleSignUp} className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-white/40 ml-1">Email Address</label>
              <div className="neo-in rounded-2xl p-1">
                <input
                    type="email"
                    placeholder="name@example.com"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-transparent border-none focus:ring-0 px-5 py-4 text-white placeholder:text-white/10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-white/40 ml-1">Password</label>
              <div className="neo-in rounded-2xl p-1">
                <input
                    type="password"
                    placeholder="••••••••"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-transparent border-none focus:ring-0 px-5 py-4 text-white placeholder:text-white/10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-white/40 ml-1">Confirm Password</label>
              <div className="neo-in rounded-2xl p-1">
                <input
                    type="password"
                    placeholder="••••••••"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-transparent border-none focus:ring-0 px-5 py-4 text-white placeholder:text-white/10"
                />
              </div>
            </div>

            <Button
                type="submit"
                className="w-full py-7 rounded-2xl font-black text-lg neo-btn text-primary hover:text-white transition-all mt-4"
                disabled={loading}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>
          </form>

          <p className="mt-10 text-center text-sm text-secondary-foreground font-medium">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:text-white font-black transition-colors">
              Log In →
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};
