import { useState, useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { TopNavBar } from '../components/TopNavBar';
import { SideNavBar } from '../components/SideNavBar';
import { motion } from 'framer-motion';

export const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [user, setUser] = useState<any>(null);
  const navigate = useNavigate();

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
    <div className="h-screen flex flex-col bg-surface-container-lowest overflow-hidden">
      <TopNavBar
        onMenuClick={() => setIsSidebarOpen(true)}
        user={user}
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
