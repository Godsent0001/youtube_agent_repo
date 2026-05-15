import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, LayoutDashboard, PlusCircle, Megaphone, Settings, Menu, X, LogOut } from 'lucide-react';
import { Button } from './ui/Button';
import { Card } from './ui/Card';

const NAV_ITEMS = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Create Agent', href: '/create-agent', icon: PlusCircle },
  { name: 'Monetization', href: '/monetization', icon: Megaphone },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const isAuthPage = ['/login', '/signup', '/forgot-password'].includes(location.pathname);
  const isLandingPage = location.pathname === '/';
  const isLoggedIn = !!localStorage.getItem('access_token');

  if (isAuthPage) return null;

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    setShowLogoutConfirm(false);
    navigate('/login');
  };

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
              {isLandingPage && !isLoggedIn ? (
                <>
                  <a href="#features" className="px-3 py-2 text-sm font-medium text-secondary-foreground hover:text-primary transition-colors">Features</a>
                  <Link to="/login">
                    <Button variant="outline" size="sm">Login</Button>
                  </Link>
                  <Link to="/signup">
                    <Button size="sm">Sign Up</Button>
                  </Link>
                </>
              ) : (
                <>
                  {isLandingPage && (
                    <>
                      <a href="#features" className="px-3 py-2 text-sm font-medium text-secondary-foreground hover:text-primary transition-colors mr-2">Features</a>
                      <Link to="/dashboard">
                        <Button variant="ghost" size="sm" className="text-secondary-foreground hover:text-primary">Dashboard</Button>
                      </Link>
                    </>
                  )}
                  {(isLandingPage || location.pathname === '/settings') && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="gap-2 text-secondary-foreground hover:text-primary"
                      onClick={() => setShowLogoutConfirm(true)}
                    >
                      <LogOut className="h-4 w-4" />
                      Logout
                    </Button>
                  )}
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20 ml-2">
                    <span className="text-xs font-bold text-primary">
                      {localStorage.getItem('user_email')?.substring(0, 2).toUpperCase() || 'AI'}
                    </span>
                  </div>
                </>
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

      {/* Logout Confirmation Modal */}
      <AnimatePresence>
        {showLogoutConfirm && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="w-full max-w-sm"
            >
              <Card className="p-6 border-border shadow-2xl bg-card">
                <h3 className="text-xl font-bold text-white mb-4 text-center">Are you sure you want to logout?</h3>
                <div className="flex gap-3 justify-center">
                  <Button variant="ghost" onClick={() => setShowLogoutConfirm(false)}>
                    Cancel
                  </Button>
                  <Button variant="destructive" onClick={handleLogout}>
                    Logout
                  </Button>
                </div>
              </Card>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

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
              {isLandingPage && !isLoggedIn ? (
                <>
                  <Link to="/login" className="block px-3 py-2 text-base font-medium text-secondary-foreground hover:text-primary">Login</Link>
                  <Link to="/signup" className="block px-3 py-2 text-base font-medium text-primary">Sign Up</Link>
                </>
              ) : isLoggedIn ? (
                <>
                  {isLandingPage && (
                    <Link
                      to="/dashboard"
                      onClick={() => setIsOpen(false)}
                      className="flex items-center gap-3 px-3 py-2 text-base font-medium text-secondary-foreground hover:text-primary"
                    >
                      <LayoutDashboard className="h-5 w-5" />
                      Dashboard
                    </Link>
                  )}
                  {NAV_ITEMS.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsOpen(false)}
                      className="flex items-center gap-3 px-3 py-2 text-base font-medium text-secondary-foreground hover:text-primary"
                    >
                      <item.icon className="h-5 w-5" />
                      {item.name}
                    </Link>
                  ))}
                  {(isLandingPage || location.pathname === '/settings') && (
                    <button
                      onClick={() => {
                        setIsOpen(false);
                        setShowLogoutConfirm(true);
                      }}
                      className="flex w-full items-center gap-3 px-3 py-2 text-base font-medium text-secondary-foreground hover:text-red-500"
                    >
                      <LogOut className="h-5 w-5" />
                      Logout
                    </button>
                  )}
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
