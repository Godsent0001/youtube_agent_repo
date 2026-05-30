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
    <div className="py-20 px-8 bg-[#0F1115] min-h-screen">
      <div className="text-center mb-20">
        <h1 className="text-5xl font-black mb-6 text-white tracking-tight">Choose Your Plan</h1>
        <p className="text-white/40 max-w-2xl mx-auto text-lg font-medium">
          Scale your content creation with MorphFlow. Choose the plan that fits your needs.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10 max-w-7xl mx-auto">
        {PLANS.map((plan, idx) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="flex"
          >
            <div className={`relative p-10 w-full flex flex-col rounded-[40px] bg-white/[0.03] border ${plan.highlighted ? 'border-primary shadow-[0_0_50px_rgba(59,130,246,0.1)]' : 'border-white/5'} transition-all hover:translate-y-[-8px]`}>
              {plan.highlighted && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-white text-xs font-black px-6 py-2 rounded-full uppercase tracking-widest shadow-xl">
                  Most Popular
                </div>
              )}

              <div className="mb-10">
                <h3 className="text-3xl font-black mb-3 text-white">{plan.name}</h3>
                <div className="flex items-baseline gap-2">
                  <span className="text-5xl font-black text-white">{plan.price}</span>
                  <span className="text-white/40 text-sm font-bold">/mo</span>
                </div>
                <p className="mt-6 text-white/60 font-medium leading-relaxed">{plan.description}</p>
              </div>

              <div className="flex-1 space-y-5 mb-12">
                {plan.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-4">
                    <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                      <Check className="h-3 w-3 text-primary" />
                    </div>
                    <span className="text-white/80 font-medium">{feature}</span>
                  </div>
                ))}
              </div>

              <Button
                variant={plan.highlighted ? 'primary' : 'outline'}
                className={`w-full py-8 rounded-[20px] font-black text-lg uppercase tracking-widest ${!plan.highlighted ? 'border-white/10 text-white hover:bg-white/5' : ''}`}
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
