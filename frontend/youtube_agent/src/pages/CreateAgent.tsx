import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { motion } from 'framer-motion';
import { apiRequest } from '../utils/api';

const NICHES = ['Facts', 'Motivation', 'Tech', 'AI', 'Finance', 'Health', 'Stories', 'Business', 'Self-Improvement'];

export const CreateAgent = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // For edit mode
  const isEdit = !!id;

  const [name, setName] = useState('Daily AI Facts');
  const [niche, setNiche] = useState('');
  const [contentType, setContentType] = useState('shorts');
  const [videoLength, setVideoLength] = useState('30');
  const [customPrompt, setCustomPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(isEdit);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      const fetchAgent = async () => {
        try {
          const data = await apiRequest(`/agents/${id}`);
          setName(data.name);
          setNiche(data.niche);
          setContentType(data.content_type);
          setVideoLength(data.video_length?.toString() || (data.content_type === 'shorts' ? '30' : '180'));
          setCustomPrompt(data.custom_prompt || '');
        } catch (err: any) {
          setError('Failed to fetch agent settings');
        } finally {
          setFetching(false);
        }
      };
      fetchAgent();
    }
  }, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (isEdit) {
        await apiRequest(`/agents/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              name,
              niche,
              content_type: contentType,
              video_length: parseInt(videoLength),
              custom_prompt: customPrompt,
          }),
        });
      } else {
        await apiRequest('/agents', {
          method: 'POST',
          body: JSON.stringify({
              name,
              niche,
              content_type: contentType,
              video_length: parseInt(videoLength),
              custom_prompt: customPrompt,
              posting_frequency: 'daily'
          }),
        });
      }
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (fetching) return <div className="p-8 text-white text-center">Loading agent settings...</div>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto py-8"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">
          {isEdit ? `Edit Agent: ${name}` : 'Create New AI Channel Agent'}
        </h1>
        <p className="text-secondary-foreground">
          {isEdit ? 'Update your agent configuration' : 'Set up your AI agent with minimal inputs'}
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Agent Configuration</CardTitle>
            <CardDescription>Configure how your AI agent will generate and post content.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Channel Name</label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Niche</label>
                <Select
                    required
                    value={niche}
                    onChange={(e) => setNiche(e.target.value)}
                >
                  <option value="" disabled>Select a niche</option>
                  {NICHES.map((n) => (
                    <option key={n} value={n.toLowerCase()}>{n}</option>
                  ))}
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Content Type</label>
                <Select
                    value={contentType}
                    onChange={(e) => setContentType(e.target.value)}
                >
                  <option value="shorts">YouTube Shorts</option>
                  <option value="long">Long-form</option>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Video Length</label>
              <Select
                value={videoLength}
                onChange={(e) => setVideoLength(e.target.value)}
              >
                <option value="15" disabled={contentType === 'long'}>15 seconds</option>
                <option value="30" disabled={contentType === 'long'}>30 seconds</option>
                <option value="60" disabled={contentType === 'long'}>60 seconds</option>
                <option value="180" disabled={contentType === 'shorts'}>3-5 minutes (Long-form)</option>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Custom Instructions (Optional)</label>
              <textarea
                className="flex min-h-[100px] w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                placeholder="e.g. Make it humorous, focus on students"
                maxLength={200}
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
              />
            </div>
          </CardContent>
          <CardFooter className="flex gap-4 justify-end border-t border-border pt-6">
            <Button variant="secondary" type="button" onClick={() => navigate('/dashboard')}>
              Cancel
            </Button>
            <Button type="submit" className="px-8" disabled={loading}>
              {loading ? (isEdit ? 'Updating...' : 'Creating...') : 'Done'}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </motion.div>
  );
};
