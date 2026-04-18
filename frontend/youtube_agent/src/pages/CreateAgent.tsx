import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { motion } from 'framer-motion';

const NICHES = ['Facts', 'Motivation', 'AI / Tech', 'Finance', 'Health', 'Stories', 'Business', 'Self-Improvement'];

export const CreateAgent = () => {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto py-8"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Create New AI Channel Agent</h1>
        <p className="text-secondary-foreground">Set up your AI agent with minimal inputs</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Agent Configuration</CardTitle>
            <CardDescription>Configure how your AI agent will generate and post content.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Channel Name</label>
              <Input defaultValue="Daily AI Facts" required />
              <p className="text-[10px] text-secondary-foreground italic">Prefilled by AI based on potential niche, but editable.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Niche</label>
                <Select required defaultValue="">
                  <option value="" disabled>Select a niche</option>
                  {NICHES.map((niche) => (
                    <option key={niche} value={niche.toLowerCase()}>{niche}</option>
                  ))}
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Content Type</label>
                <Select defaultValue="shorts">
                  <option value="shorts">YouTube Shorts</option>
                  <option value="long">Long-form</option>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Video Length</label>
              <Select defaultValue="30">
                <option value="15">15 seconds</option>
                <option value="30">30 seconds</option>
                <option value="60">60 seconds</option>
                <option value="180">3-5 minutes (Long-form)</option>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Custom Instructions (Optional)</label>
              <textarea
                className="flex min-h-[100px] w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                placeholder="e.g. Make it humorous, focus on students"
                maxLength={200}
              />
            </div>
          </CardContent>
          <CardFooter className="flex gap-4 justify-end border-t border-border pt-6">
            <Button variant="secondary" type="button" onClick={() => navigate('/dashboard')}>
              Cancel
            </Button>
            <Button type="submit" className="px-8">
              Done
            </Button>
          </CardFooter>
        </form>
      </Card>
    </motion.div>
  );
};
