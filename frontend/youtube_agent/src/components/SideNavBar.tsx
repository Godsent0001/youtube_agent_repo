import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

interface SideNavBarProps {
  isOpen: boolean;
  onClose: () => void;
  user: any;
  onLogout: () => void;
}

export const SideNavBar: React.FC<SideNavBarProps> = ({ isOpen, onClose, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { label: 'Home', icon: 'home', path: '/' },
    { label: 'Projects', icon: 'video_library', path: '/dashboard' },
    { label: 'Settings', icon: 'settings', path: '/settings' },
  ];

  return (
    <>
      <aside
        className={`fixed left-0 top-0 bottom-0 flex flex-col p-4 gap-4 z-[60] h-screen w-64 bg-surface border-r border-outline-variant/30 sidebar-transition ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex flex-col gap-6 h-full">
          <div className="px-2 pt-4">
            <span className="font-hanken text-2xl font-black text-primary">MorphFlow</span>
            <p className="text-on-surface-variant font-geist text-xs">AI Video Creator</p>
          </div>

          <button
            className="flex items-center gap-3 w-full bg-primary text-on-primary p-3 rounded-lg font-medium active:scale-[0.98] transition-all"
            onClick={() => { navigate('/'); onClose(); }}
          >
            <span className="material-symbols-outlined">add</span>
            <span>New Project</span>
          </button>

          <nav className="flex flex-col gap-1 flex-grow">
            {navItems.map((item) => (
              <button
                key={item.path}
                className={`flex items-center gap-3 p-3 rounded-lg transition-all active:scale-[0.98] ${
                  location.pathname === item.path
                    ? 'bg-secondary-container text-on-secondary-container font-medium'
                    : 'text-on-surface-variant hover:bg-surface-container-high'
                }`}
                onClick={() => { navigate(item.path); onClose(); }}
              >
                <span className="material-symbols-outlined">{item.icon}</span>
                <span className="font-geist text-sm">{item.label}</span>
              </button>
            ))}
          </nav>

          <div className="mt-auto border-t border-outline-variant/20 pt-4 flex flex-col gap-1">
            <button
              className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-surface-container-high rounded-lg transition-all text-error"
              onClick={onLogout}
            >
              <span className="material-symbols-outlined">logout</span>
              <span className="font-geist text-sm">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/10 backdrop-blur-[2px] z-50 transition-opacity"
          onClick={onClose}
        ></div>
      )}
    </>
  );
};
