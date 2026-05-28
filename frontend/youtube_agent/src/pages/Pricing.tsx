
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Button } from '../components/ui/Button';

const PLANS = [
  {
    name: 'Free',
    price: '$0',
    description: 'Perfect for getting started',
    features: ['10 videos per month', '720p resolution', 'Basic AI voiceover'],
    cta: 'Current Plan',
    highlighted: false
  },
  {
    name: 'Elite',
    price: '$15.99',
    description: 'For serious creators',
    features: ['30 videos per month', '1080p resolution', 'Premium AI voices', 'No watermark'],
    cta: 'Upgrade to Elite',
    highlighted: true
  },
  {
    name: 'Pro',
    price: '$35',
    description: 'Full automation power',
    features: ['Unlimited videos', '4K resolution', 'All premium voices', 'Priority rendering'],
    cta: 'Go Pro',
    highlighted: false
  }
];

export const Pricing = () => {
  return (
    <div className="py-12 px-4">
      <div className="text-center mb-12 sm:mb-16">
        <h1 className="text-3xl sm:text-4xl font-black mb-4">Choose Your Plan</h1>
        <p className="text-secondary-foreground max-w-2xl mx-auto text-sm sm:text-base">
          Scale your content creation with MorphFlow. Choose the plan that fits your needs.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 sm:gap-12 max-w-6xl mx-auto">
        {PLANS.map((plan, idx) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <div className={`relative p-8 h-full flex flex-col rounded-[32px] ${plan.highlighted ? 'neo-out border border-primary/20 shadow-primary/10' : 'neo-out border border-white/5'} blue-glow transition-all hover:scale-[1.02]`}>
              {plan.highlighted && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-white text-[10px] font-black px-4 py-1.5 rounded-full uppercase tracking-widest shadow-lg">
                  Most Popular
                </div>
              )}

              <div className="mb-8">
                <h3 className="text-xl sm:text-2xl font-black mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-3xl sm:text-4xl font-black">{plan.price}</span>
                  <span className="text-secondary-foreground text-sm">/mo</span>
                </div>
                <p className="mt-4 text-secondary-foreground text-xs sm:text-sm font-medium leading-relaxed">{plan.description}</p>
              </div>

              <div className="flex-1 space-y-4 mb-10">
                {plan.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-3">
                    <div className="h-5 w-5 rounded-full bg-primary/10 flex items-center justify-center neo-in border border-primary/20">
                      <Check className="h-2.5 w-2.5 text-primary" />
                    </div>
                    <span className="text-sm text-secondary-foreground font-medium">{feature}</span>
                  </div>
                ))}
              </div>

              <Button
                variant="primary"
                className={`w-full py-5 sm:py-6 rounded-2xl font-black text-sm uppercase tracking-wider neo-btn ${plan.highlighted ? 'text-white' : 'text-primary'}`}
              >
                {plan.cta}
              </Button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
