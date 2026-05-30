
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Waves, Menu, Download, Play, ChevronDown } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Sidebar } from '../components/layout/Sidebar';
import { apiRequest } from '../utils/api';

export const LandingPage = () => {
  const [prompt, setPrompt] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [aspectRatio, setAspectRatio] = useState<'shorts' | 'long'>('long');
  const [duration, setDuration] = useState(60);
  const [showAspectMenu, setShowAspectMenu] = useState(false);
  const [showDurationMenu, setShowDurationMenu] = useState(false);
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
      try {
        const { prompt, aspectRatio, duration } = JSON.parse(storedPrompt);
        setPrompt(prompt);
        setAspectRatio(aspectRatio);
        setDuration(duration);
        localStorage.removeItem('pending_prompt');
        handleGenerate(prompt, aspectRatio, duration);
      } catch (e) {
        localStorage.removeItem('pending_prompt');
      }
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
    <div className="min-h-screen bg-[#0F1115] text-white selection:bg-primary/30 relative overflow-x-hidden">
      {/* Background Image - Studio Theme */}
      <div
        className="fixed inset-0 z-0 pointer-events-none opacity-40"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?q=80&w=2070&auto=format&fit=crop")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'grayscale(20%) brightness(50%) contrast(120%)'
        }}
      />

      {/* Header - Pill Shape / Glassmorphic */}
      <header className="fixed top-6 left-6 right-6 z-50 flex justify-center pointer-events-none">
        <div className="w-full max-w-6xl h-20 bg-white/5 backdrop-blur-xl border border-white/10 rounded-[32px] px-8 flex items-center justify-between shadow-2xl pointer-events-auto">
          <div className="flex items-center gap-6">
            {isLoggedIn && (
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="p-2.5 hover:bg-white/5 rounded-2xl transition-colors"
              >
                <Menu className="h-6 w-6 text-white" />
              </button>
            )}
            <Link to="/" className="flex items-center gap-3">
              <Waves className="h-8 w-8 text-primary" />
              <span className="text-2xl font-black tracking-tight text-white">MorphFlow</span>
            </Link>
          </div>

          <div className="flex items-center gap-4">
            {!isLoggedIn ? (
              <Link to="/login">
                <Button variant="ghost" className="text-white hover:text-primary font-bold">Login</Button>
              </Link>
            ) : (
              <div className="hidden sm:flex items-center gap-3 px-5 py-2 bg-white/5 rounded-2xl border border-white/5">
                <div className="h-2 w-2 rounded-full bg-blue-500 animate-pulse" />
                <span className="text-sm font-bold text-white/80">{userEmail}</span>
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
      <main className="pt-44 pb-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl sm:text-7xl font-black tracking-tight mb-6"
          >
            Imagine. <span className="text-primary">Generate.</span> Viral.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-xl text-white/60 font-medium"
          >
            Transform any idea into a high-quality video in seconds.
          </motion.p>
        </div>

        {/* Prompt Section */}
        <section className="relative">
          <div className="bg-white/5 border border-white/10 rounded-[40px] p-2 shadow-2xl overflow-hidden backdrop-blur-xl">
            <div className="relative">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value.slice(0, 2000))}
                placeholder="What are we creating today?"
                className="w-full bg-transparent border-none focus:ring-0 text-2xl p-10 min-h-[300px] resize-none text-white placeholder:text-white/20 font-bold"
              />
              <div className="absolute bottom-6 right-10 text-sm text-white/10 font-mono">
                {prompt.length}/2000
              </div>
            </div>

            <div className="flex flex-col md:flex-row items-center justify-between p-8 gap-6 border-t border-white/5 bg-white/[0.02]">
              <div className="flex flex-wrap items-center gap-4">

                {/* Aspect Ratio */}
                <div className="relative">
                    <button
                        onClick={() => setShowAspectMenu(!showAspectMenu)}
                        className="flex items-center gap-3 px-6 py-4 bg-white/5 hover:bg-white/10 rounded-2xl border border-white/10 transition-all font-bold min-w-[180px]"
                    >
                        <span className="text-white/40 uppercase text-[10px] tracking-widest">Ratio</span>
                        <span className="text-white capitalize">{aspectRatio}</span>
                        <ChevronDown className={`h-4 w-4 ml-auto transition-transform ${showAspectMenu ? 'rotate-180' : ''}`} />
                    </button>

                    <AnimatePresence>
                        {showAspectMenu && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: 10 }}
                                className="absolute bottom-full mb-3 left-0 w-full bg-[#1a1d23] border border-white/10 rounded-2xl overflow-hidden shadow-2xl z-20"
                            >
                                <button
                                    onClick={() => { setAspectRatio('shorts'); setShowAspectMenu(false); }}
                                    className="w-full text-left px-6 py-4 hover:bg-primary/20 transition-colors font-bold text-white border-b border-white/5"
                                >
                                    Shorts (9:16)
                                </button>
                                <button
                                    onClick={() => { setAspectRatio('long'); setShowAspectMenu(false); }}
                                    className="w-full text-left px-6 py-4 hover:bg-primary/20 transition-colors font-bold text-white"
                                >
                                    Long (16:9)
                                </button>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Duration */}
                <div className="relative">
                    <button
                        onClick={() => setShowDurationMenu(!showDurationMenu)}
                        className="flex items-center gap-3 px-6 py-4 bg-white/5 hover:bg-white/10 rounded-2xl border border-white/10 transition-all font-bold min-w-[180px]"
                    >
                        <span className="text-white/40 uppercase text-[10px] tracking-widest">Length</span>
                        <span className="text-white">{duration}s</span>
                        <ChevronDown className={`h-4 w-4 ml-auto transition-transform ${showDurationMenu ? 'rotate-180' : ''}`} />
                    </button>

                    <AnimatePresence>
                        {showDurationMenu && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: 10 }}
                                className="absolute bottom-full mb-3 left-0 w-full bg-[#1a1d23] border border-white/10 rounded-2xl overflow-hidden shadow-2xl z-20"
                            >
                                {[15, 30, 60].map((s) => (
                                    <button
                                        key={s}
                                        onClick={() => { setDuration(s); setShowDurationMenu(false); }}
                                        className="w-full text-left px-6 py-4 hover:bg-primary/20 transition-colors font-bold text-white border-b border-white/5 last:border-0"
                                    >
                                        {s} Seconds
                                    </button>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

              </div>

              <Button
                  size="lg"
                  className="bg-primary text-white hover:bg-primary/90 rounded-[24px] px-12 py-8 text-xl font-black shadow-[0_0_40px_rgba(59,130,246,0.3)] transition-all hover:scale-105 active:scale-95"
                  onClick={() => handleGenerate()}
                  disabled={isGenerating || !prompt.trim()}
              >
                  Create Video
              </Button>
            </div>
          </div>
        </section>

        {/* Generation Overlay */}
        <AnimatePresence>
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-[100] bg-[#0F1115]/60 backdrop-blur-3xl flex items-center justify-center p-8 text-center"
            >
              <div className="max-w-md w-full">
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0]
                    }}
                    transition={{ repeat: Infinity, duration: 4 }}
                    className="mb-12"
                  >
                    <Waves className="h-24 w-24 text-primary mx-auto drop-shadow-[0_0_25px_rgba(59,130,246,0.5)]" />
                  </motion.div>

                  <h3 className="text-4xl font-black mb-4 tracking-tight">Morphing...</h3>
                  <p className="text-white/60 mb-12 text-lg font-medium">
                      {jobStatus?.activities?.[jobStatus.activities.length - 1]?.step || 'Starting the creative engine...'}
                  </p>

                  <div className="w-full bg-white/5 h-3 rounded-full overflow-hidden border border-white/5">
                      <motion.div
                          className="bg-primary h-full rounded-full shadow-[0_0_20px_rgba(59,130,246,0.6)]"
                          initial={{ width: 0 }}
                          animate={{ width: `${jobStatus?.progress || 0}%` }}
                      />
                  </div>
                  <div className="mt-4 flex justify-between items-center px-1">
                      <span className="text-[10px] uppercase tracking-widest font-black text-white/30">Neural Synthesis</span>
                      <span className="text-sm font-mono font-bold text-primary">
                          {jobStatus?.progress || 0}%
                      </span>
                  </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Video Result */}
        <AnimatePresence>
          {generatedVideo && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-16"
            >
              <div className="bg-white/5 border border-white/10 rounded-[40px] overflow-hidden shadow-2xl backdrop-blur-sm">
                <div className="p-8 border-b border-white/5 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-black text-white">{generatedVideo.topic}</h2>
                        <p className="text-white/40 font-medium">Generation Complete</p>
                    </div>
                    <Button
                        variant="outline"
                        size="lg"
                        className="gap-3 rounded-2xl border-white/10 hover:bg-white/5 text-white"
                        onClick={() => downloadVideo(generatedVideo.video_url)}
                    >
                        <Download className="h-5 w-5" />
                        Download
                    </Button>
                </div>

                <div className="aspect-video bg-black relative group">
                    <video
                        src={(import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com').replace(/\/+$/, "") + generatedVideo.video_url}
                        className="w-full h-full object-contain"
                        controls
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center pointer-events-none">
                        <div className="h-24 w-24 rounded-full bg-primary/20 backdrop-blur-md border border-primary/40 flex items-center justify-center">
                            <Play className="h-12 w-12 text-white fill-white" />
                        </div>
                    </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="py-12 border-t border-white/5 relative z-10">
        <div className="mx-auto max-w-7xl px-8 text-center text-white/20 text-sm font-medium">
          <p>© {new Date().getFullYear()} MorphFlow AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
