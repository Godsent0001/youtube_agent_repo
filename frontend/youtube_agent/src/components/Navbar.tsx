import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, LayoutDashboard, PlusCircle, Megaphone, Settings, Menu, X } from 'lucide-react';
import { Button } from './ui/Button';

const NAV_ITEMS = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Create Agent', href: '/create-agent', icon: PlusCircle },
  { name: 'Monetization', href: '/monetization', icon: Megaphone },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const isAuthPage = ['/login', '/signup', '/forgot-password'].includes(location.pathname);
  const isLandingPage = location.pathname === '/';

  if (isAuthPage) return null;

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2 group">
              <Play className="h-8 w-8 text-primary fill-primary group-hover:scale-110 transition-transform" />
              <span className="text-xl font-bold tracking-tight text-white">AI Agents</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="flex items-center gap-4">
              {!isLandingPage && NAV_ITEMS.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center gap-2 px-3 py-2 text-sm font-medium transition-colors hover:text-primary ${
                      isActive ? 'text-primary' : 'text-secondary-foreground'
                    }`}
                  >
                    <item.icon className="h-4 w-4" />
                    {item.name}
                  </Link>
                );
              })}
              {isLandingPage ? (
                <>
                  <a href="#features" className="px-3 py-2 text-sm font-medium text-secondary-foreground hover:text-primary transition-colors">Features</a>
                  <Link to="/dashboard">
                    <Button variant="ghost" size="sm">Dashboard</Button>
                  </Link>
                  <Link to="/login">
                    <Button variant="outline" size="sm">Login</Button>
                  </Link>
                  <Link to="/signup">
                    <Button size="sm">Sign Up</Button>
                  </Link>
                </>
              ) : (
                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                  <span className="text-xs font-bold text-primary">GE</span>
                </div>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-secondary-foreground hover:text-white hover:bg-card focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-card border-b border-border overflow-hidden"
          >
            <div className="space-y-1 px-4 pb-3 pt-2">
              {isLandingPage ? (
                <>
                  <Link to="/login" className="block px-3 py-2 text-base font-medium text-secondary-foreground hover:text-primary">Login</Link>
                  <Link to="/signup" className="block px-3 py-2 text-base font-medium text-primary">Sign Up</Link>
                </>
              ) : (
                NAV_ITEMS.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 px-3 py-2 text-base font-medium text-secondary-foreground hover:text-primary"
                  >
                    <item.icon className="h-5 w-5" />
                    {item.name}
                  </Link>
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};
