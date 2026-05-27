
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Waves, Menu, Download, Loader2 } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Sidebar } from '../components/layout/Sidebar';
import { apiRequest } from '../utils/api';

export const LandingPage = () => {
  const [prompt, setPrompt] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [aspectRatio, setAspectRatio] = useState<'shorts' | 'long'>('shorts');
  const [duration, setDuration] = useState(60);
  const [isGenerating, setIsGenerating] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<any>(null);
  const [generatedVideo, setGeneratedVideo] = useState<any>(null);

  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('access_token');
  const userEmail = localStorage.getItem('user_email');

  // Handle stored prompt from redirection
  useEffect(() => {
    const storedPrompt = localStorage.getItem('pending_prompt');
    if (storedPrompt && isLoggedIn) {
      const { prompt, aspectRatio, duration } = JSON.parse(storedPrompt);
      setPrompt(prompt);
      setAspectRatio(aspectRatio);
      setDuration(duration);
      localStorage.removeItem('pending_prompt');
      // Trigger generation automatically if desired
      handleGenerate(prompt, aspectRatio, duration);
    }
  }, [isLoggedIn]);

  // Polling for job status
  useEffect(() => {
    let interval: any;
    if (isGenerating && jobId) {
      interval = setInterval(async () => {
        try {
          const status = await apiRequest(`/jobs/${jobId}`);
          setJobStatus(status);

          if (status.status === 'completed') {
            setIsGenerating(false);
            setJobId(null);
            // Fetch the latest video for this user
            const videos = await apiRequest('/videos');
            if (videos && videos.length > 0) {
                setGeneratedVideo(videos[0]);
            }
          } else if (status.status === 'failed') {
            setIsGenerating(false);
            setJobId(null);
            alert('Generation failed: ' + (status.error || 'Unknown error'));
          }
        } catch (err) {
          console.error('Status poll error:', err);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [isGenerating, jobId]);

  const handleGenerate = async (p = prompt, ar = aspectRatio, d = duration) => {
    if (!p.trim()) return;

    if (!isLoggedIn) {
      localStorage.setItem('pending_prompt', JSON.stringify({ prompt: p, aspectRatio: ar, duration: d }));
      navigate('/login');
      return;
    }

    setIsGenerating(true);
    setGeneratedVideo(null);
    setJobStatus(null);

    try {
      const response = await apiRequest('/videos/generate', {
        method: 'POST',
        body: JSON.stringify({
          prompt: p,
          content_type: ar,
          video_length: d
        })
      });
      setJobId(response.job_id);
    } catch (err) {
      console.error('Generation failed:', err);
      setIsGenerating(false);
      alert('Failed to start generation');
    }
  };

  const downloadVideo = (url: string) => {
    const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com').replace(/\/+$/, "");
    const fullUrl = url.startsWith('http') ? url : `${API_BASE}${url}`;
    window.open(fullUrl, '_blank');
  };

  return (
    <div className="min-h-screen bg-background text-white selection:bg-primary/30 relative">
      {/* Background Image */}
      <div
        className="fixed inset-0 z-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?q=80&w=2070&auto=format&fit=crop")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'grayscale(100%) brightness(50%)'
        }}
      />
      {/* Header */}
      <header className="fixed top-4 left-4 right-4 z-50 flex justify-center">
        <div className="w-full max-w-7xl glass-pill h-16 flex items-center justify-between px-6 shadow-2xl">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 hover:bg-white/10 rounded-full transition-colors"
            >
              <Menu className="h-6 w-6 text-white" />
            </button>
            <Link to="/" className="flex items-center gap-2">
              <Waves className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold tracking-tight text-white">MorphFlow</span>
            </Link>
          </div>

          <div className="flex items-center gap-4">
            {!isLoggedIn ? (
              <Link to="/login">
                <Button variant="ghost" size="sm" className="text-white hover:text-primary">Login</Button>
              </Link>
            ) : (
              <div className="hidden sm:flex items-center gap-2 px-4 py-1.5 bg-white/10 rounded-full border border-white/10">
                <div className="h-2 w-2 rounded-full bg-blue-500 animate-pulse" />
                <span className="text-xs font-medium text-white/80">{userEmail}</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        userEmail={userEmail}
      />

      {/* Main Content */}
      <main className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl sm:text-6xl font-black tracking-tight mb-4"
          >
            Imagine. <span className="text-primary">Generate.</span> Viral.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-lg text-secondary-foreground"
          >
            Transform any idea into a high-quality video in seconds.
          </motion.p>
        </div>

        {/* Prompt Section */}
        <section className="relative z-10">
          <div className="neo-out rounded-[40px] p-2 blue-glow">
            <div className="relative">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value.slice(0, 2000))}
                placeholder="What video are you creating today?"
                className="w-full bg-transparent border-none focus:ring-0 text-xl p-8 min-h-[200px] resize-none text-white placeholder:text-white/20"
              />
              <div className="absolute bottom-6 right-8 text-xs text-white/30 font-mono">
                {prompt.length}/2000
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-between p-6 gap-6 border-t border-white/5">
              <div className="flex items-center gap-6">
                {/* Aspect Ratio Selector */}
                <div className="flex items-center gap-2 bg-black/40 p-1.5 rounded-2xl neo-in">
                  <button
                    onClick={() => setAspectRatio('shorts')}
                    className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold transition-all ${aspectRatio === 'shorts' ? 'bg-primary text-white shadow-lg' : 'text-white/40 hover:text-white'}`}
                  >
                    Shorts
                  </button>
                  <button
                    onClick={() => setAspectRatio('long')}
                    className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold transition-all ${aspectRatio === 'long' ? 'bg-primary text-white shadow-lg' : 'text-white/40 hover:text-white'}`}
                  >
                    Long
                  </button>
                </div>

                {/* Duration Selector */}
                <div className="flex items-center gap-2 bg-black/40 p-1.5 rounded-2xl neo-in">
                  {[15, 30, 60].map((s) => (
                    <button
                      key={s}
                      onClick={() => setDuration(s)}
                      className={`px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${duration === s ? 'bg-white text-black' : 'text-white/40 hover:text-white'}`}
                    >
                      {s}s
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-4">
                <Button
                    size="lg"
                    className="neo-btn rounded-2xl px-12 py-7 text-xl font-black text-primary hover:text-white"
                    onClick={() => handleGenerate()}
                    disabled={isGenerating || !prompt.trim()}
                >
                    Create
                </Button>
              </div>
            </div>
          </div>

          {/* Blur Overlay for Generation */}
          <AnimatePresence>
            {isGenerating && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 z-10 bg-background/40 backdrop-blur-md rounded-3xl flex items-center justify-center p-8 text-center"
              >
                <div className="max-w-md w-full">
                    <Loader2 className="h-12 w-12 text-primary animate-spin mx-auto mb-6" />
                    <h3 className="text-2xl font-bold mb-2">Morphing your idea...</h3>
                    <p className="text-secondary-foreground mb-8">
                        {jobStatus?.activities?.[jobStatus.activities.length - 1]?.step || 'Starting the creative engine...'}
                    </p>

                    {/* Progress Bar */}
                    <div className="w-full bg-white/10 h-2 rounded-full overflow-hidden">
                        <motion.div
                            className="bg-primary h-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${jobStatus?.progress || 0}%` }}
                        />
                    </div>
                    <div className="mt-2 text-right text-xs text-secondary-foreground font-mono">
                        {jobStatus?.progress || 0}%
                    </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>

        {/* Video Output Display */}
        <AnimatePresence>
          {generatedVideo && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-12"
            >
              <div className="bg-card border border-border rounded-3xl overflow-hidden shadow-2xl">
                <div className="p-6 border-b border-border flex items-center justify-between">
                    <div>
                        <h2 className="text-xl font-bold text-white">{generatedVideo.topic}</h2>
                        <p className="text-sm text-secondary-foreground">Generated successfully</p>
                    </div>
                    <Button
                        variant="outline"
                        size="sm"
                        className="gap-2"
                        onClick={() => downloadVideo(generatedVideo.video_url)}
                    >
                        <Download className="h-4 w-4" />
                        Download
                    </Button>
                </div>

                <div className="aspect-video bg-black relative group">
                    <video
                        src={(import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com').replace(/\/+$/, "") + generatedVideo.video_url}
                        className="w-full h-full object-contain"
                        controls
                    />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="py-10 border-t border-border">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center text-secondary-foreground text-sm">
          <p>© {new Date().getFullYear()} MorphFlow AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
