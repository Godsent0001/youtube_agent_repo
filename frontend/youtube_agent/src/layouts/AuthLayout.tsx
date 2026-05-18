import { Outlet, Link } from 'react-router-dom';
import { Play } from 'lucide-react';
import { motion } from 'framer-motion';

export const AuthLayout = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md"
      >
        <div className="flex flex-col items-center mb-8">
          <Link to="/" className="flex items-center gap-2 mb-4">
            <Play className="h-10 w-10 text-primary" />
            <span className="text-2xl font-bold tracking-tight">AI Agents</span>
          </Link>
        </div>
        <div className="bg-card p-6 sm:p-8 rounded-2xl border border-border shadow-xl">
          <Outlet />
        </div>
      </motion.div>
    </div>
  );
};
