import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiRequest } from '../utils/api';

export const CreateAgent = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [video, setVideo] = useState<any>(null);
  const [editPrompt, setEditPrompt] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchVideo();
    }
  }, [id]);

  const fetchVideo = async () => {
    try {
      const data = await apiRequest(`/videos/${id}`);
      setVideo(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

  const handleRegenerate = async () => {
    try {
      const response = await apiRequest('/videos', {
        method: 'POST',
        body: JSON.stringify({
          prompt: video.prompt,
          aspect_ratio: video.aspect_ratio,
          duration_seconds: video.duration_seconds,
          edit_prompt: editPrompt,
          original_video_id: id
        })
      });
      navigate(`/video/${response.video_id}`);
    } catch (error) {
      console.error('Error regenerating video:', error);
      alert('Failed to start regeneration.');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="h-full flex flex-col items-center justify-center px-4 bg-surface-container-lowest">
      <div className="text-center mb-8 max-w-2xl">
        <h1 className="font-hanken text-4xl font-semibold text-primary mb-4">Edit Workspace</h1>
        <p className="font-hanken text-lg text-on-surface-variant">
          Provide instructions to refine your video. MorphFlow will use your previous generation as context.
        </p>
      </div>

      <div className="w-full max-w-[800px] bg-white rounded-[32px] border border-outline-variant/40 shadow-[0_20px_50px_rgba(0,0,0,0.02)] p-8 flex flex-col gap-6">
        <div className="space-y-2">
           <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest">Original Prompt</label>
           <div className="p-4 bg-surface-container-low rounded-xl text-on-surface-variant text-sm">
             {video.prompt}
           </div>
        </div>

        <div className="relative">
          <label className="font-geist text-[10px] text-on-surface-variant uppercase tracking-widest block mb-2">Refinement Instructions</label>
          <textarea
            className="w-full h-32 border border-outline-variant/30 rounded-2xl focus:ring-1 focus:ring-primary font-hanken text-lg p-4 placeholder:text-outline text-on-surface"
            placeholder="e.g., 'Make the lighting more dramatic' or 'Change the voice to be more energetic'..."
            value={editPrompt}
            onChange={(e) => setEditPrompt(e.target.value)}
          ></textarea>
        </div>

        <div className="flex justify-end gap-4">
           <button
             className="px-6 py-2 rounded-full border border-outline-variant text-on-surface font-geist text-xs"
             onClick={() => navigate(-1)}
           >
             Cancel
           </button>
           <button
             className="px-8 py-2 rounded-full bg-primary text-on-primary font-geist text-xs font-medium active:scale-95 transition-all"
             onClick={handleRegenerate}
           >
             Regenerate Video
           </button>
        </div>
      </div>
    </div>
  );
};
