import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/layout/Sidebar';
import { Footer } from '../components/Footer';
import { motion } from 'framer-motion';
import { Menu, Waves } from 'lucide-react';
import { Link } from 'react-router-dom';

export const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const userEmail = localStorage.getItem('user_email');

  return (
    <div className="min-h-screen flex flex-col">
      <header className="fixed top-4 left-4 right-4 z-50 flex justify-center">
        <div className="w-full max-w-7xl glass-pill h-16 flex items-center justify-between px-6 shadow-2xl">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 hover:bg-white/10 rounded-full transition-colors"
            >
              <Menu className="h-6 w-6 text-white" />
            </button>
            <Link to="/" className="flex items-center gap-2">
              <Waves className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold tracking-tight text-white">MorphFlow</span>
            </Link>
          </div>
        </div>
      </header>

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        userEmail={userEmail}
      />

      <main className="flex-1 overflow-x-hidden overflow-y-auto pt-16">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
          className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 sm:py-8"
        >
          <Outlet />
        </motion.div>
      </main>
      <Footer />
    </div>
  );
};
