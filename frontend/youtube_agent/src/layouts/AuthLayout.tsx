import { Outlet, Link } from 'react-router-dom';
import { Waves } from 'lucide-react';
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
          <Link to="/" className="flex items-center gap-3 mb-4">
            <div className="h-12 w-12 bg-primary/20 rounded-xl flex items-center justify-center neo-out">
              <Waves className="h-7 w-7 text-primary" />
            </div>
            <span className="text-3xl font-black tracking-tight text-white">MorphFlow</span>
          </Link>
        </div>
        <div className="bg-card p-6 sm:p-8 rounded-2xl border border-border shadow-xl">
          <Outlet />
        </div>
      </motion.div>
    </div>
  );
};
