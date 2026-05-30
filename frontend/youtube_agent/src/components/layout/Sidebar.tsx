import { motion, AnimatePresence } from 'framer-motion';
import {
  Settings,
  CreditCard,
  LogOut,
  X,
  Zap
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  userEmail: string | null;
}

export const Sidebar = ({ isOpen, onClose, userEmail }: SidebarProps) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
    onClose();
  };

  const menuItems = [
    { icon: Settings, label: 'Settings', path: '/settings' },
    { icon: CreditCard, label: 'Upgrade', path: '/pricing' },
  ];

  const initials = userEmail ? userEmail.substring(0, 2).toUpperCase() : 'MF';

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60]"
          />
          <motion.div
            initial={{ x: '-100%' }}
            animate={{ x: 0 }}
            exit={{ x: '-100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed left-0 top-0 bottom-0 w-[320px] bg-[#16191f] z-[70] border-r border-white/5 flex flex-col"
          >
            <div className="p-8 flex items-center justify-between border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-primary flex items-center justify-center text-white font-black text-lg shadow-lg">
                  {initials}
                </div>
                <div>
                  <p className="text-sm font-black text-white truncate max-w-[160px]">
                    {userEmail || 'User'}
                  </p>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <Zap className="h-3 w-3 text-primary fill-primary" />
                    <span className="text-[10px] font-black uppercase tracking-widest text-primary">Free Plan</span>
                  </div>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/5 rounded-full transition-colors text-white/40 hover:text-white"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="flex-1 py-8 px-4 space-y-2">
              {menuItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={onClose}
                  className="flex items-center gap-4 px-6 py-4 rounded-2xl text-white/60 hover:text-white hover:bg-white/5 transition-all font-bold group"
                >
                  <item.icon className="h-5 w-5 group-hover:text-primary transition-colors" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>

            <div className="p-8 border-t border-white/5">
              <button
                onClick={handleLogout}
                className="flex items-center gap-4 w-full px-6 py-4 rounded-2xl text-red-400 hover:text-red-300 hover:bg-red-400/5 transition-all font-bold group"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
