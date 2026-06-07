import React from 'react';
import { useNavigate } from 'react-router-dom';

interface TopNavBarProps {
  onMenuClick: () => void;
  user: any;
}

export const TopNavBar: React.FC<TopNavBarProps> = ({ onMenuClick, user }) => {
  const navigate = useNavigate();

  return (
    <header className="fixed top-0 left-1/2 -translate-x-1/2 z-50 flex items-center rounded-full mt-4 mx-auto px-6 py-2 bg-surface/80 backdrop-blur-xl border border-outline-variant/30 shadow-[0_10px_30px_rgba(0,0,0,0.04)] w-[calc(100%-2rem)] max-w-4xl justify-between">
      <div className="flex items-center gap-4">
        {user && (
          <button
            className="p-2 hover:bg-surface-container rounded-full transition-colors"
            onClick={onMenuClick}
          >
            <span className="material-symbols-outlined text-primary">menu</span>
          </button>
        )}
        <span
          className="font-hanken text-xl font-bold text-primary cursor-pointer"
          onClick={() => navigate('/')}
        >
          MorphFlow
        </span>
      </div>

      <div className="flex items-center gap-4">
        {user ? (
          <div className="w-8 h-8 rounded-full overflow-hidden border border-outline-variant bg-secondary-container flex items-center justify-center cursor-pointer" onClick={() => navigate('/settings')}>
            <span className="text-on-secondary-container font-geist text-[12px] font-bold">
              {user.email?.substring(0, 2).toUpperCase() || 'US'}
            </span>
          </div>
        ) : (
          <button
            className="bg-primary text-on-primary px-4 py-1.5 rounded-full font-geist text-xs font-medium active:scale-95 transition-transform"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        )}
      </div>
    </header>
  );
};
