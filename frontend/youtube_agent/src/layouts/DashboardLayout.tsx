import { useState, useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { TopNavBar } from '../components/TopNavBar';
import { SideNavBar } from '../components/SideNavBar';
import { motion, AnimatePresence } from 'framer-motion';
import heroBg from '../assets/hero-bg.png';

export const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [user, setUser] = useState<any>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const isLandingPage = location.pathname === '/';

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  return (
    <div className={`h-screen flex flex-col ${isLandingPage ? 'bg-transparent' : 'bg-surface-container-lowest'} overflow-hidden relative`}>
      <AnimatePresence>
        {isLandingPage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
            className="fixed inset-0 -z-10 overflow-hidden bg-black"
          >
            <div
              className="absolute inset-0 bg-center bg-cover"
              style={{ backgroundImage: `url(${heroBg})` }}
            >
            </div>

            {/* Overlay for UI Legibility */}
            <div className="absolute inset-0 bg-black/20 backdrop-blur-[2px]"></div>
          </motion.div>
        )}
      </AnimatePresence>

      <TopNavBar
        onMenuClick={() => setIsSidebarOpen(true)}
        user={user}
        isLandingPage={isLandingPage}
      />

      <SideNavBar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        user={user}
        onLogout={handleLogout}
      />

      <main className="flex-1 overflow-y-auto pt-20">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="h-full"
        >
          <Outlet />
        </motion.div>
      </main>
    </div>
  );
};
