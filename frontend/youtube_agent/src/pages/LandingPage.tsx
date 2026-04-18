
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Play, Zap, DollarSign, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="lg:flex lg:items-center lg:gap-x-16">
            <motion.div
              className="mx-auto max-w-2xl lg:mx-0 lg:flex-auto"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="flex items-center gap-x-2 mb-6">
                <div className="rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold leading-6 text-primary ring-1 ring-inset ring-primary/20">
                  New: AI Shorts Agent
                </div>
              </div>
              <h1 className="text-4xl font-bold tracking-tight sm:text-6xl text-white">
                Automate Your YouTube Channel with <span className="text-primary">AI</span>
              </h1>
              <p className="mt-6 text-lg leading-8 text-secondary-foreground">
                Create AI-powered channels that post daily videos, generate trending content, and even run affiliate ads—without lifting a finger.
              </p>
              <div className="mt-10 flex items-center gap-x-6">
                <Link to="/signup">
                  <Button size="lg" className="gap-2">
                    Create Your First Agent <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="ghost" size="lg">
                    Learn How It Works
                  </Button>
                </Link>
              </div>
            </motion.div>
            <motion.div
              className="mt-16 sm:mt-24 lg:mt-0 lg:flex-shrink-0 lg:flex-grow"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2 }}
            >
              <div className="relative mx-auto max-w-[500px] aspect-square bg-gradient-to-br from-primary/20 to-transparent rounded-full flex items-center justify-center p-8">
                <div className="absolute inset-0 bg-primary/5 blur-3xl rounded-full animate-pulse" />
                <div className="relative z-10 w-full h-full bg-card rounded-2xl border border-border overflow-hidden shadow-2xl flex flex-col p-4">
                  <div className="flex items-center justify-between mb-4 border-b border-border pb-2">
                    <div className="flex gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-red-500" />
                      <div className="w-3 h-3 rounded-full bg-yellow-500" />
                      <div className="w-3 h-3 rounded-full bg-green-500" />
                    </div>
                    <div className="text-xs text-secondary-foreground font-mono">Agent: Active</div>
                  </div>
                  <div className="flex-1 space-y-4">
                    <div className="h-4 bg-neutral-800 rounded w-3/4 animate-pulse" />
                    <div className="h-32 bg-neutral-800 rounded w-full animate-pulse" />
                    <div className="grid grid-cols-2 gap-4">
                      <div className="h-16 bg-neutral-800 rounded animate-pulse" />
                      <div className="h-16 bg-neutral-800 rounded animate-pulse" />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
        {/* Background Decorative Element */}
        <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl -z-10" />
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32 bg-card/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-base font-semibold leading-7 text-primary">How It Works</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl text-white">Everything you need to scale</p>
          </div>
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {[
              {
                title: 'Create AI Agent',
                description: 'Set up your YouTube agent in seconds with minimal inputs and clear goals.',
                icon: Zap,
              },
              {
                title: 'Automatic Content',
                description: 'Agent fetches trending topics, generates scripts, and posts daily videos.',
                icon: Play,
              },
              {
                title: 'Monetize Effortlessly',
                description: 'Add affiliate links or promotions; agent integrates them naturally into videos.',
                icon: DollarSign,
              },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                variants={itemVariants}
                className="bg-card p-8 rounded-2xl border border-border hover:border-primary/50 transition-colors group"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-6 group-hover:bg-primary transition-colors">
                  <feature.icon className="h-6 w-6 text-primary group-hover:text-white" />
                </div>
                <h3 className="text-xl font-bold mb-2 text-white">{feature.title}</h3>
                <p className="text-secondary-foreground">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 sm:py-32 overflow-hidden">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            className="relative isolate overflow-hidden bg-card px-6 py-24 text-center shadow-2xl rounded-3xl sm:px-16"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to start your AI channel?
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-secondary-foreground">
              Join thousands of creators who are automating their content creation workflow with AI.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link to="/signup">
                <Button size="lg">Create Your First Agent</Button>
              </Link>
            </div>
            {/* Background pattern */}
            <svg
              viewBox="0 0 1024 1024"
              className="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-x-1/2 [mask-image:radial-gradient(closest-side,white,transparent)]"
              aria-hidden="true"
            >
              <circle cx="512" cy="512" r="512" fill="url(#827591b1-ce8c-4110-b064-7cb85a0b1217)" fillOpacity="0.7" />
              <defs>
                <radialGradient id="827591b1-ce8c-4110-b064-7cb85a0b1217">
                  <stop stopColor="#FF0000" />
                  <stop offset={1} stopColor="#1E1E1E" />
                </radialGradient>
              </defs>
            </svg>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
};
