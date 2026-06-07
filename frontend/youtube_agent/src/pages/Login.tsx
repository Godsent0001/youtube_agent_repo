import { useNavigate, Link } from 'react-router-dom';
import { apiRequest } from '../utils/api';
import React, { useState } from 'react';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
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
        // Always redirect to video detail page after processing pending video
        navigate(`/video/${videoResponse.video_id}`, { replace: true });
      } else {
        // Redirection updated: Go to Home page by default
        navigate('/');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed');
    }
  };

  return (
    <div className="w-full space-y-8">
        <div className="text-center">
          <h1 className="font-hanken text-4xl md:text-5xl font-black text-primary mb-2">MorphFlow</h1>
          <p className="text-on-surface-variant font-geist text-xs uppercase tracking-widest">Sign in to continue</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && <div className="p-3 bg-error/10 text-error rounded-xl text-xs font-geist">{error}</div>}

          <div className="space-y-2">
            <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest px-1">Email Address</label>
            <input
              type="email"
              required
              className="w-full p-5 bg-surface-container-low rounded-2xl border border-transparent focus:border-primary/20 focus:bg-white transition-all text-base md:text-sm"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center px-1">
              <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Password</label>
            </div>
            <input
              type="password"
              required
              className="w-full p-5 bg-surface-container-low rounded-2xl border border-transparent focus:border-primary/20 focus:bg-white transition-all text-base md:text-sm"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-5 bg-primary text-on-primary rounded-2xl font-geist text-base font-bold active:scale-[0.98] transition-all shadow-lg"
          >
            Sign In
          </button>

          <p className="text-center text-on-surface-variant text-xs pt-4">
            Don't have an account? <Link to="/signup" className="text-primary font-bold hover:underline">Sign up</Link>
          </p>
        </form>
    </div>
  );
};
