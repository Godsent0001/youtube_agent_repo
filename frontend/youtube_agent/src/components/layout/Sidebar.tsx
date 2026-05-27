
import { motion, AnimatePresence } from 'framer-motion';
import { Settings, CreditCard, User, LogOut, X, Waves } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  userEmail: string | null;
}

export const Sidebar = ({ isOpen, onClose, userEmail }: SidebarProps) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    onClose();
    navigate('/login');
  };

  const menuItems = [
    { name: 'Settings', icon: Settings, href: '/settings' },
    { name: 'Upgrade', icon: CreditCard, href: '/pricing' },
  ];

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
            className="fixed top-0 left-0 bottom-0 w-72 bg-card border-r border-border z-[70] flex flex-col"
          >
            <div className="p-6 flex items-center justify-between border-b border-border">
              <div className="flex items-center gap-2">
                <Waves className="h-8 w-8 text-primary" />
                <span className="text-xl font-bold text-white">MorphFlow</span>
              </div>
              <button onClick={onClose} className="text-secondary-foreground hover:text-white transition-colors">
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="flex-1 py-6 flex flex-col">
              <nav className="space-y-2 px-4 flex-1">
                {menuItems.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={onClose}
                    className="flex items-center gap-3 px-4 py-3 text-secondary-foreground hover:text-white hover:bg-white/5 rounded-lg transition-all"
                  >
                    <item.icon className="h-5 w-5" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                ))}

                {userEmail && (
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-3 px-4 py-3 text-red-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all"
                  >
                    <LogOut className="h-5 w-5" />
                    <span className="font-medium">Logout</span>
                  </button>
                )}
              </nav>

              {userEmail && (
                <div className="mx-4 mt-auto p-4 bg-white/5 rounded-2xl border border-border">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20 shrink-0">
                      <span className="text-primary font-bold text-sm">
                        {userEmail.substring(0, 2).toUpperCase()}
                      </span>
                    </div>
                    <div className="flex flex-col min-w-0">
                      <span className="text-sm font-bold text-white truncate">
                        {userEmail.split('@')[0]}
                      </span>
                      <span className="text-[10px] text-secondary-foreground truncate">
                        {userEmail}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
