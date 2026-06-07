import React, { useState, useEffect } from 'react';
import { apiRequest } from '../utils/api';

export const Settings = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      // In a real app, we'd have a /auth/me or similar
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const handleSave = () => {
    setMessage('Settings saved successfully!');
    setTimeout(() => setMessage(''), 3000);
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="p-4 md:p-12 max-w-4xl mx-auto">
      <header className="mb-12">
        <h1 className="font-hanken text-3xl font-semibold text-primary">Settings</h1>
        <p className="text-on-surface-variant text-sm">Manage your account and preferences</p>
      </header>

      <div className="space-y-8 bg-white p-8 rounded-[32px] border border-outline-variant/30">
        <section className="space-y-4">
          <h2 className="font-hanken text-xl font-medium text-primary">Account Profile</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Email Address</label>
              <input
                type="text"
                readOnly
                value={user?.email || ''}
                className="w-full p-3 bg-surface-container-low rounded-xl text-on-surface-variant border-none cursor-not-allowed"
              />
            </div>
            <div className="space-y-1">
              <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Subscription Tier</label>
              <div className="w-full p-3 bg-primary/5 text-primary rounded-xl font-medium flex items-center justify-between">
                 <span>{user?.tier || 'Free Plan'}</span>
                 <button className="text-[10px] underline uppercase tracking-widest hover:opacity-70">Upgrade</button>
              </div>
            </div>
          </div>
        </section>

        <section className="space-y-4 pt-8 border-t border-outline-variant/10">
          <h2 className="font-hanken text-xl font-medium text-primary">Preferences</h2>
          <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-on-surface-variant">dark_mode</span>
              <div>
                <p className="font-geist text-sm font-medium">Dark Mode</p>
                <p className="text-[10px] text-on-surface-variant uppercase">Switch interface theme</p>
              </div>
            </div>
            <div className="w-12 h-6 bg-outline-variant/30 rounded-full relative cursor-pointer">
              <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full"></div>
            </div>
          </div>
        </section>

        <div className="flex items-center justify-between pt-8">
           {message && <span className="text-emerald-500 font-geist text-xs">{message}</span>}
           <div className="flex-grow"></div>
           <button
             className="px-8 py-2 bg-primary text-on-primary rounded-full font-geist text-xs font-medium active:scale-95 transition-all"
             onClick={handleSave}
           >
             Save Changes
           </button>
        </div>
      </div>
    </div>
  );
};
