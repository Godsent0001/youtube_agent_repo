import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiRequest } from '../utils/api';
import { motion } from 'framer-motion';

export const Dashboard = () => {
  const [videos, setVideos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const data = await apiRequest('/dashboard/videos');
      setVideos(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching videos:', error);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="p-4 md:p-12 max-w-[1440px] mx-auto">
      <header className="flex justify-between items-center mb-12">
        <div>
           <h1 className="font-hanken text-3xl font-semibold text-primary">Library</h1>
           <p className="text-on-surface-variant text-sm">Your generated video collection</p>
        </div>
        <button
          className="bg-primary text-on-primary px-6 py-2 rounded-full font-geist text-xs font-medium"
          onClick={() => navigate('/')}
        >
          Create New
        </button>
      </header>

      {videos.length === 0 ? (
        <div className="text-center py-20 bg-surface-container-low rounded-[32px] border border-dashed border-outline-variant">
           <span className="material-symbols-outlined text-5xl text-outline mb-4">video_library</span>
           <p className="text-on-surface-variant">No projects yet. Start your first generation!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {videos.map((video) => (
            <motion.div
              key={video.id}
              whileHover={{ y: -4 }}
              className="group relative bg-surface border border-outline-variant/30 rounded-2xl overflow-hidden aspect-square cursor-pointer shadow-sm hover:shadow-xl transition-all"
              onClick={() => navigate(`/video/${video.id}`)}
            >
              {video.thumbnail_url ? (
                <img src={video.thumbnail_url} alt={video.title} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full bg-surface-container flex items-center justify-center">
                  <span className="material-symbols-outlined text-4xl text-outline-variant">movie</span>
                </div>
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
                <p className="text-white font-geist text-xs font-bold mb-1 truncate">{video.title || 'Untitled Project'}</p>
                <p className="text-white/60 text-[10px] uppercase">{video.aspect_ratio} • {video.status}</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};
