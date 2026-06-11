import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { apiRequest } from '../utils/api';

interface SideNavBarProps {
  isOpen: boolean;
  onClose: () => void;
  user: any;
  onLogout: () => void;
}

export const SideNavBar: React.FC<SideNavBarProps> = ({ isOpen, onClose, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [recentVideos, setRecentVideos] = useState<any[]>([]);

  useEffect(() => {
    if (isOpen) {
      fetchRecentVideos();
    }
  }, [isOpen, location.pathname]);

  const fetchRecentVideos = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        console.warn('SideNavBar: user_id not found in localStorage');
        return;
      }
      const data = await apiRequest(`/videos?user_id=${userId}`);

      if (Array.isArray(data)) {
        // Sort by created_at descending just in case the API doesn't
        const sorted = data.sort((a: any, b: any) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setRecentVideos(sorted.slice(0, 5));
      }
    } catch (error) {
      console.error('Error fetching recent videos:', error);
    }
  };

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

            {recentVideos.length > 0 && (
              <div className="mt-4">
                <p className="px-3 py-2 text-[10px] font-bold text-outline uppercase tracking-wider">Recent Videos</p>
                <div className="flex flex-col gap-1">
                  {recentVideos.map((video) => (
                    <button
                      key={video.id}
                      className="flex items-center gap-3 p-3 rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-all text-left"
                      onClick={() => { navigate(`/video/${video.id}`); onClose(); }}
                    >
                      <span className="material-symbols-outlined text-[20px]">movie</span>
                      <span className="font-geist text-xs truncate">{video.title || 'Untitled Project'}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
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
