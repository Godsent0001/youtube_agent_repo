import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiRequest } from '../utils/api';

export const SignUp = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await apiRequest('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password, full_name: 'User' })
      });
      // After signup, login
      const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_id', response.user_id);
      localStorage.setItem('user', JSON.stringify({ email, id: response.user_id }));

      const pendingVideo = localStorage.getItem('pending_video');
      if (pendingVideo) {
        localStorage.removeItem('pending_video');
        const videoResponse = await apiRequest('/videos', {
          method: 'POST',
          body: pendingVideo
        });
        navigate(`/video/${videoResponse.video_id}`);
      } else {
        // Redirection updated: Go to Home page by default
        navigate('/');
      }
    } catch (err: any) {
      setError(err.message || 'Signup failed');
    }
  };

  return (
    <div className="min-h-full flex flex-col items-center justify-center p-6 bg-background">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="font-hanken text-4xl font-black text-primary mb-2">MorphFlow</h1>
          <p className="text-on-surface-variant font-geist text-xs uppercase tracking-widest">Create your account</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-[32px] border border-outline-variant/30 shadow-sm space-y-6">
          {error && <div className="p-3 bg-error/10 text-error rounded-xl text-xs font-geist">{error}</div>}

          <div className="space-y-1">
            <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Email Address</label>
            <input
              type="email"
              required
              className="w-full p-4 bg-surface-container-low rounded-2xl border border-transparent focus:border-primary/20 focus:bg-white transition-all text-sm"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="space-y-1">
            <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Password</label>
            <input
              type="password"
              required
              className="w-full p-4 bg-surface-container-low rounded-2xl border border-transparent focus:border-primary/20 focus:bg-white transition-all text-sm"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-4 bg-primary text-on-primary rounded-2xl font-geist text-sm font-bold active:scale-[0.98] transition-all"
          >
            Get Started
          </button>

          <p className="text-center text-on-surface-variant text-xs pt-4">
            Already have an account? <Link to="/login" className="text-primary font-bold hover:underline">Sign in</Link>
          </p>
        </form>
      </div>
    </div>
  );
};
