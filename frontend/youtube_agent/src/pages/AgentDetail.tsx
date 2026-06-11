import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiRequest } from '../utils/api';
import { motion } from 'framer-motion';

export const AgentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [video, setVideo] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchVideo();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [id]);

  const fetchVideo = async () => {
    try {
      const data = await apiRequest(`/videos/${id}`);

      // Fix for hardcoded URLs from previous environments
      if (data.video_url && data.video_url.includes('onrender.com')) {
        const urlParts = data.video_url.split('/storage/');
        if (urlParts.length > 1) {
          const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
          data.video_url = `${API_BASE_URL}/storage/${urlParts[1]}`;
        }
      }

      setVideo(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

  const fetchStatus = async () => {
    try {
      const data = await apiRequest(`/videos/${id}/status`);
      setStatus(data);
      if (data.status === 'completed' && !video?.video_url) {
        fetchVideo();
      }
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const handleDownload = () => {
    if (video?.video_url) {
      window.open(video.video_url, '_blank');
    }
  };

  const handleShare = () => {
     const url = window.location.href;
     navigator.clipboard.writeText(url);
     alert('Link copied to clipboard!');
  };

  if (loading && !status) {
    return (
      <div className="h-full flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <main className="min-h-full pt-12 pb-24 px-4 md:px-12 max-w-[1440px] mx-auto w-full">
      {!video && status && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
           <div className="w-full max-w-md space-y-6 text-center">
              <div className="text-primary font-hanken text-2xl font-semibold mb-8">
                {status?.activities?.length > 0 ? `${status.activities[status.activities.length - 1].step} ${status.progress || 0}%` : 'Initializing...'}
              </div>
              <div className="w-full bg-surface-container h-3 rounded-full overflow-hidden shadow-inner">
                 <motion.div
                  className="bg-primary h-full shadow-[0_0_15px_rgba(59,130,246,0.5)]"
                  initial={{ width: 0 }}
                  animate={{ width: `${status?.progress || 0}%` }}
                  transition={{ duration: 0.5 }}
                 />
              </div>
              <div className="space-y-3 max-h-60 overflow-y-auto hide-scrollbar text-left bg-surface/50 p-6 rounded-2xl border border-outline-variant/20">
                 {status?.activities?.slice().reverse().map((act: any, i: number) => (
                   <div key={i} className={`flex items-center gap-3 text-sm ${i === 0 ? 'text-primary font-medium' : 'text-on-surface-variant opacity-60'}`}>
                      <span className="material-symbols-outlined text-[18px] text-emerald-500">
                        {i === 0 && status.status !== 'completed' ? 'sync' : 'check_circle'}
                      </span>
                      <span>{act.step}</span>
                   </div>
                 ))}
              </div>
           </div>
        </div>
      )}

      <header className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className={`flex h-2.5 w-2.5 rounded-full ${video.status === 'completed' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.4)]' : video.status === 'failed' ? 'bg-error' : 'bg-primary animate-pulse'}`}></span>
            <span className="font-geist text-[10px] text-on-surface-variant tracking-wider uppercase">
              {video.status}
            </span>
          </div>
          <h1 className="font-hanken text-3xl font-semibold text-primary tracking-tight">
            {video.title || 'Generating Video...'}
          </h1>
          <p className="font-hanken text-sm text-on-surface-variant">
            Generated on {new Date(video.created_at).toLocaleDateString()} • {video.aspect_ratio}
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            className="flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-3 border border-outline-variant bg-surface hover:bg-surface-container-low transition-colors rounded-xl font-geist text-xs active:scale-95"
            onClick={handleShare}
          >
            <span className="material-symbols-outlined text-[20px]">share</span>
            Share
          </button>
          <button
            className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-geist text-xs active:scale-95 transition-all ${video.status === 'completed' ? 'bg-primary text-on-primary hover:opacity-90' : 'bg-surface-container text-outline cursor-not-allowed'}`}
            disabled={video.status !== 'completed'}
            onClick={handleDownload}
          >
            <span className="material-symbols-outlined text-[20px]">download</span>
            Download
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8 space-y-8">
          {/* Video Player Area */}
          <div className={`relative group bg-surface-container-lowest rounded-[24px] overflow-hidden border border-outline-variant/30 shadow-[0_20px_50px_rgba(0,0,0,0.08)] ${video.aspect_ratio === '9:16' ? 'aspect-[9/16] max-h-[70vh] mx-auto' : 'aspect-video'}`}>
            {video.status === 'completed' && video.video_url ? (
              <video
                src={video.video_url}
                controls
                className="w-full h-full object-contain"
                poster={video.thumbnail_url}
              />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center">
                 <div className="w-full max-w-md space-y-6">
                    <div className="text-primary font-hanken text-xl font-medium">
                      {status?.activities?.length > 0 ? `${status.activities[status.activities.length - 1].step} ${status.progress || 0}%` : 'Initializing...'}
                    </div>
                    <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                       <motion.div
                        className="bg-primary h-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${status?.progress || 0}%` }}
                       />
                    </div>
                    <div className="space-y-2 max-h-40 overflow-y-auto hide-scrollbar text-left">
                       {status?.activities?.map((act: any, i: number) => (
                         <div key={i} className="flex items-center gap-3 text-xs text-on-surface-variant">
                            <span className="material-symbols-outlined text-[14px] text-emerald-500">check_circle</span>
                            <span>{act.step}</span>
                         </div>
                       ))}
                    </div>
                 </div>
              </div>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <button
              className="flex items-center gap-2 px-5 py-2.5 border border-outline-variant rounded-full font-geist text-xs hover:bg-surface-container-low transition-all active:scale-95"
              onClick={() => navigate(`/edit-agent/${id}`)}
            >
              <span className="material-symbols-outlined text-[18px]">edit</span>
              Edit / Regenerate
            </button>
            <div className="flex-grow"></div>
            <button
              className="flex items-center gap-2 px-5 py-2.5 border border-error/20 text-error rounded-full font-geist text-xs hover:bg-error/5 transition-all active:scale-95"
              onClick={async () => {
                if(confirm('Delete this video?')) {
                  await apiRequest(`/videos/${id}`, { method: 'DELETE' });
                  navigate('/dashboard');
                }
              }}
            >
              <span className="material-symbols-outlined text-[18px]">delete</span>
              Delete Project
            </button>
          </div>
        </div>

        <aside className="lg:col-span-4 space-y-6">
          <div className="bg-surface-container-low p-8 rounded-[24px] border border-outline-variant/20">
            <h3 className="font-hanken text-xl font-semibold text-primary mb-6">Video Details</h3>
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Original Prompt</label>
                <div className="bg-surface p-4 rounded-xl border border-outline-variant/30 font-hanken text-sm text-on-surface leading-relaxed">
                  "{video.prompt}"
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Aspect Ratio</label>
                  <p className="font-hanken text-base text-primary font-medium">{video.aspect_ratio}</p>
                </div>
                <div className="space-y-1">
                  <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Duration</label>
                  <p className="font-hanken text-base text-primary font-medium">{video.duration_seconds}s</p>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
};
