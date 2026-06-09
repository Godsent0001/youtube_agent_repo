import { useState, useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { TopNavBar } from '../components/TopNavBar';
import { SideNavBar } from '../components/SideNavBar';
import { motion, AnimatePresence } from 'framer-motion';
import heroBg from '../assets/hero-bg.png';

export const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isBgLoaded, setIsBgLoaded] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const isLandingPage = location.pathname === '/';

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    // Preload background image for landing page
    if (isLandingPage) {
      const img = new Image();
      img.src = heroBg;
      img.onload = () => setIsBgLoaded(true);
      img.onerror = () => {
        console.error("Failed to load background image");
        setIsBgLoaded(true); // Proceed anyway to avoid blank screen
      };
    } else {
      setIsBgLoaded(true);
    }
  }, [isLandingPage]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  return (
    <div className={`h-screen flex flex-col ${isLandingPage ? 'bg-transparent' : 'bg-surface-container-lowest'} overflow-hidden relative`}>
      <AnimatePresence mode="wait">
        {isLandingPage && isBgLoaded && (
          <motion.div
            key="hero-background"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            className="fixed inset-0 -z-10 overflow-hidden"
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

      {(!isLandingPage || isBgLoaded) && (
        <motion.div
          key="main-content"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: isLandingPage ? 0.2 : 0 }}
          className="flex flex-col h-full"
        >
        <TopNavBar
          onMenuClick={() => setIsSidebarOpen(true)}
          user={user}
          isLandingPage={isLandingPage}
        />

          <main className="flex-1 overflow-y-auto pt-20">
            <div className="h-full">
              <Outlet />
            </div>
          </main>
        </motion.div>
      )}

      <SideNavBar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        user={user}
        onLogout={handleLogout}
      />
    </div>
  );
};
