
import { motion } from 'framer-motion';
import { Check, Waves } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

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
    features: ['100 videos per month', '4K resolution', 'All premium voices', 'Priority rendering'],
    cta: 'Go Pro',
    highlighted: false
  }
];

export const Pricing = () => {
  return (
    <div className="py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-black mb-4">Choose Your Plan</h1>
        <p className="text-secondary-foreground max-w-2xl mx-auto">
          Scale your content creation with MorphFlow. Choose the plan that fits your needs.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {PLANS.map((plan, idx) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card className={`relative p-8 h-full flex flex-col ${plan.highlighted ? 'border-primary shadow-2xl blue-glow' : 'border-border'}`}>
              {plan.highlighted && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                  Most Popular
                </div>
              )}

              <div className="mb-8">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-black">{plan.price}</span>
                  <span className="text-secondary-foreground">/mo</span>
                </div>
                <p className="mt-4 text-secondary-foreground text-sm">{plan.description}</p>
              </div>

              <div className="flex-1 space-y-4 mb-8">
                {plan.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-3">
                    <div className="h-5 w-5 rounded-full bg-primary/10 flex items-center justify-center">
                      <Check className="h-3 w-3 text-primary" />
                    </div>
                    <span className="text-sm text-secondary-foreground">{feature}</span>
                  </div>
                ))}
              </div>

              <Button
                variant={plan.highlighted ? 'primary' : 'outline'}
                className="w-full py-6 rounded-xl font-bold"
              >
                {plan.cta}
              </Button>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
