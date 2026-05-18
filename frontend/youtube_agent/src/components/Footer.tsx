import { Link } from 'react-router-dom';

export const Footer = () => {
  return (
    <footer className="border-t border-border bg-card/50 py-8 sm:py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
          <div className="sm:col-span-2 md:col-span-1">
            <h3 className="text-lg font-bold text-white mb-4">AI YouTube Agents</h3>
            <p className="text-sm text-secondary-foreground">
              Automate your content creation and channel management with cutting-edge AI.
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Product</h4>
            <ul className="space-y-2">
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Features</Link></li>
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Pricing</Link></li>
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">API</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Company</h4>
            <ul className="space-y-2">
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">About</Link></li>
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Blog</Link></li>
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Legal</h4>
            <ul className="space-y-2">
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Privacy</Link></li>
              <li><Link to="#" className="text-sm text-secondary-foreground hover:text-primary transition-colors">Terms</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-border pt-8 text-center sm:mt-12">
          <p className="text-sm text-secondary-foreground">
            © {new Date().getFullYear()} AI YouTube Agents. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
