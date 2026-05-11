import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { motion } from 'framer-motion';

export const ForgotPassword = () => {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
    >
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-white">Forgot Your Password?</h1>
        <p className="text-secondary-foreground">Enter your email to reset</p>
      </div>

      {!submitted ? (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-secondary-foreground">Email</label>
            <Input type="email" placeholder="name@example.com" required />
          </div>
          <Button type="submit" className="w-full">
            Send Reset Link
          </Button>
        </form>
      ) : (
        <div className="p-4 bg-green-950/20 border border-green-900 rounded-lg text-center">
          <p className="text-green-500 text-sm">Check your email for the reset link</p>
        </div>
      )}

      <p className="mt-8 text-center text-sm text-secondary-foreground">
        <Link to="/login" className="text-primary hover:underline font-medium">
          Back to Login →
        </Link>
      </p>
    </motion.div>
  );
};
