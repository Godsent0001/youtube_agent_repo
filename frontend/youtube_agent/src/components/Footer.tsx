import { motion } from 'framer-motion';
import { Waves, Github, Twitter, Linkedin, Youtube } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer = () => {
  return (
    <footer className="bg-[#0F1115] border-t border-white/5 pt-20 pb-10">
      <div className="mx-auto max-w-7xl px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-20">
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center gap-3 mb-6">
              <Waves className="h-8 w-8 text-primary" />
              <span className="text-2xl font-black text-white">MorphFlow</span>
            </Link>
            <p className="text-white/40 max-w-sm mb-8 font-medium">
              Revolutionizing digital content with state-of-the-art AI. Generate viral videos in seconds.
            </p>
            <div className="flex gap-4">
              {[Twitter, Github, Linkedin, Youtube].map((Icon, i) => (
                <a key={i} href="#" className="h-10 w-10 rounded-xl bg-white/5 flex items-center justify-center text-white/40 hover:text-primary hover:bg-primary/10 transition-all border border-white/5">
                  <Icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-white font-black uppercase text-xs tracking-widest mb-6">Product</h4>
            <ul className="space-y-4">
              {['Pricing', 'Features', 'Showcase', 'Updates'].map(item => (
                <li key={item}>
                  <a href="#" className="text-white/40 hover:text-white transition-colors font-medium text-sm">{item}</a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white font-black uppercase text-xs tracking-widest mb-6">Legal</h4>
            <ul className="space-y-4">
              {['Privacy Policy', 'Terms of Service', 'Cookie Policy'].map(item => (
                <li key={item}>
                  <a href="#" className="text-white/40 hover:text-white transition-colors font-medium text-sm">{item}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="text-center pt-10 border-t border-white/5">
          <p className="text-white/20 text-xs font-black uppercase tracking-widest">
            © {new Date().getFullYear()} MorphFlow AI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
