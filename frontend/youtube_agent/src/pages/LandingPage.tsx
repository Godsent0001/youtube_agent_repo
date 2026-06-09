import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiRequest } from '../utils/api';

export const LandingPage = () => {
  const [prompt, setPrompt] = useState('');
  const [aspectRatio, setAspectRatio] = useState<'16:9' | '9:16'>('16:9');
  const [duration, setDuration] = useState<number>(30);
  const [isAspectOpen, setIsAspectOpen] = useState(false);
  const [isDurationOpen, setIsDurationOpen] = useState(false);
  const navigate = useNavigate();

  const handleCreate = async () => {
    const token = localStorage.getItem('access_token');
    const userId = localStorage.getItem('user_id');

    const videoData = {
      prompt,
      aspect_ratio: aspectRatio,
      duration_seconds: duration
    };

    if (!token || !userId) {
      localStorage.setItem('pending_video', JSON.stringify(videoData));
      navigate('/login', { state: { from: '/' } });
      return;
    }

    try {
      const response = await apiRequest('/videos', {
        method: 'POST',
        body: JSON.stringify(videoData)
      });
      navigate(`/video/${response.video_id}`);
    } catch (error) {
      console.error('Error creating video:', error);
      alert('Failed to start video generation.');
    }
  };

  return (
    <div className="relative h-full flex flex-col items-center justify-center px-4 py-12 overflow-y-auto">
        {/* Hero Section */}
      <div className="text-center mb-8 max-w-2xl">
        <h1 className="font-hanken text-3xl md:text-5xl font-semibold text-primary mb-4 leading-tight">
          Create Professional Videos in Minutes
        </h1>
        <p className="font-hanken text-lg text-on-surface-variant">
          Transform ideas into polished videos using intelligent video assembly and editing.
        </p>
      </div>

      {/* Prompt Workspace */}
      <div className="w-full max-w-[800px] bg-white rounded-[32px] border border-outline-variant/40 shadow-[0_20px_50px_rgba(0,0,0,0.02)] p-4 md:p-8 flex flex-col gap-4">
        <div className="relative">
          <textarea
            className="w-full min-h-[160px] md:h-40 border-none focus:ring-0 resize-none font-hanken text-lg p-0 placeholder:text-outline text-on-surface"
            placeholder="What do you want to create today? Describe your vision, style, and tone..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          ></textarea>
        </div>

        <div className="flex flex-wrap items-center justify-between pt-4 border-t border-outline-variant/20">
          <div className="flex items-center gap-3">
            {/* Aspect Ratio Dropdown */}
            <div className="relative">
              <button
                className="flex items-center gap-2 px-3 py-1.5 bg-surface-container-low rounded-full hover:bg-surface-container transition-colors font-geist text-xs border border-outline-variant/10"
                onClick={() => setIsAspectOpen(!isAspectOpen)}
              >
                <span className="material-symbols-outlined text-[18px]">aspect_ratio</span>
                <span>{aspectRatio}</span>
                <span className="material-symbols-outlined text-[16px]">expand_more</span>
              </button>
              {isAspectOpen && (
                <div className="absolute top-full left-0 mt-2 w-32 bg-white border border-outline-variant/20 rounded-xl shadow-lg z-10 overflow-hidden">
                  {['16:9', '9:16'].map((ratio) => (
                    <button
                      key={ratio}
                      className="w-full text-left px-4 py-2 hover:bg-surface-container font-geist text-xs"
                      onClick={() => { setAspectRatio(ratio as any); setIsAspectOpen(false); }}
                    >
                      {ratio}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Duration Dropdown */}
            <div className="relative">
              <button
                className="flex items-center gap-2 px-3 py-1.5 bg-surface-container-low rounded-full hover:bg-surface-container transition-colors font-geist text-xs border border-outline-variant/10"
                onClick={() => setIsDurationOpen(!isDurationOpen)}
              >
                <span className="material-symbols-outlined text-[18px]">schedule</span>
                <span>{duration}s</span>
                <span className="material-symbols-outlined text-[16px]">expand_more</span>
              </button>
              {isDurationOpen && (
                <div className="absolute top-full left-0 mt-2 w-32 bg-white border border-outline-variant/20 rounded-xl shadow-lg z-10 overflow-hidden">
                  {[15, 30, 60, 120].map((d) => (
                    <button
                      key={d}
                      className="w-full text-left px-4 py-2 hover:bg-surface-container font-geist text-xs"
                      onClick={() => { setDuration(d); setIsDurationOpen(false); }}
                    >
                      {d}s
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          <button
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-lg ${prompt.trim() ? 'bg-primary text-on-primary hover:scale-105 active:scale-95' : 'bg-surface-container text-outline cursor-not-allowed'}`}
            disabled={!prompt.trim()}
            onClick={handleCreate}
          >
            <span className="material-symbols-outlined">arrow_forward</span>
          </button>
        </div>
      </div>

      {/* Atmospheric Footer Indicator */}
      <div className="absolute bottom-8 flex items-center gap-2 text-outline-variant font-geist text-[10px] uppercase tracking-widest">
        <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
        MorphFlow Core v3.0 Ready
      </div>
    </div>
  );
};
