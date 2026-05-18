
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Plus, Play, Pause, ExternalLink, MoreVertical, Play as YoutubeIcon, Settings, Trash2 } from 'lucide-react';
import { apiRequest } from '../utils/api';
import { motion, AnimatePresence } from 'framer-motion';

export const Dashboard = () => {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await apiRequest('/agents');
        setAgents(data);
      } catch (err) {
        console.error('Failed to fetch agents:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const startAgent = async (agentId: string, youtubeConnected: boolean) => {
    if (!youtubeConnected) {
      const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com').replace(/\/+$/, "");
      window.location.href = `${API_BASE}/agents/${agentId}/youtube/connect`;
      return;
    }
    try {
        await apiRequest(`/agents/${agentId}`, {
            method: 'PUT',
            body: JSON.stringify({ is_active: true })
        });
        setAgents(agents.map(a => a.id === agentId ? { ...a, is_active: true } : a));
    } catch (err) {
        console.error('Failed to start agent:', err);
    }
  };

  const pauseAgent = async (agentId: string) => {
    try {
        await apiRequest(`/agents/${agentId}`, {
            method: 'PUT',
            body: JSON.stringify({ is_active: false })
        });
        setAgents(agents.map(a => a.id === agentId ? { ...a, is_active: false } : a));
    } catch (err) {
        console.error('Failed to pause agent:', err);
    }
  };

  const deleteAgent = async (agentId: string) => {
    try {
      await apiRequest(`/agents/${agentId}`, {
        method: 'DELETE'
      });
      setAgents(agents.filter(a => a.id !== agentId));
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Failed to delete agent:', err);
    }
  };
  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">Your AI Agents</h1>
          <p className="text-sm sm:text-base text-secondary-foreground">Monitor performance and manage your agents</p>
        </div>
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
          <Link to="/monetization" className="w-full sm:w-auto">
            <Button variant="outline" className="w-full sm:w-auto">Run Ads</Button>
          </Link>
          <Link to="/create-agent" className="w-full sm:w-auto">
            <Button className="w-full sm:w-auto gap-2">
              <Plus className="h-5 w-5" />
              Create Agent
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        {loading ? (
            <p className="text-white col-span-full text-center py-12">Loading agents...</p>
        ) : agents.map((agent) => (
          <Card key={agent.id} className="group relative">
            <CardHeader className="pb-4">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-xl">{agent.name}</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    {agent.niche} • {agent.content_type}
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={agent.is_active ? 'success' : 'warning'}>
                    {agent.is_active ? 'active' : 'paused'}
                  </Badge>
                  <div className="relative">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-8 w-8 p-0"
                      onClick={(e) => {
                        e.preventDefault();
                        setActiveMenu(activeMenu === agent.id ? null : agent.id);
                      }}
                    >
                      <MoreVertical className="h-4 w-4" />
                    </Button>

                    <AnimatePresence>
                      {activeMenu === agent.id && (
                        <>
                          <div
                            className="fixed inset-0 z-10"
                            onClick={() => setActiveMenu(null)}
                          />
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="absolute right-0 mt-2 w-48 bg-card border border-border rounded-md shadow-lg z-20 overflow-hidden"
                          >
                            <div className="py-1">
                              {!agent.youtube_connected && (
                                <button
                                  className="w-full text-left px-4 py-2 text-sm text-secondary-foreground hover:bg-neutral-800 flex items-center gap-2"
                                  onClick={() => {
                                    const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com').replace(/\/+$/, "");
                                    window.location.href = `${API_BASE}/agents/${agent.id}/youtube/connect`;
                                  }}
                                >
                                  <YoutubeIcon className="h-4 w-4 text-red-500" />
                                  Connect YouTube
                                </button>
                              )}
                              <button
                                className="w-full text-left px-4 py-2 text-sm text-secondary-foreground hover:bg-neutral-800 flex items-center gap-2"
                                onClick={() => navigate(`/edit-agent/${agent.id}`)}
                              >
                                <Settings className="h-4 w-4" />
                                Settings
                              </button>
                              <button
                                className="w-full text-left px-4 py-2 text-sm text-secondary-foreground hover:bg-neutral-800 flex items-center gap-2"
                                onClick={() => agent.is_active ? pauseAgent(agent.id) : startAgent(agent.id, agent.youtube_connected)}
                              >
                                {agent.is_active ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                                {agent.is_active ? 'Pause Agent' : 'Resume Agent'}
                              </button>
                              <button
                                className="w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-red-500/10 flex items-center gap-2"
                                onClick={() => {
                                  setDeleteConfirm(agent.id);
                                  setActiveMenu(null);
                                }}
                              >
                                <Trash2 className="h-4 w-4" />
                                Delete Agent
                              </button>
                            </div>
                          </motion.div>
                        </>
                      )}
                    </AnimatePresence>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-xs text-secondary-foreground">
                Last Video Posted: <span className="text-white">{agent.last_run_at || 'Never'}</span>
              </div>
              <div className="grid grid-cols-3 gap-4 border-y border-border py-4">
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{agent.total_videos_created || 0}</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Videos</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{agent.avg_retention || 0}%</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Retention</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-bold text-white">$0</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Earnings</div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="gap-2 bg-neutral-900/50 pt-4 px-4 sm:px-6">
              <Link to={`/agent/${agent.id}`} className="flex-1">
                <Button variant="secondary" className="w-full gap-2 text-xs py-5 sm:py-2">
                  <ExternalLink className="h-4 w-4 sm:h-3 sm:w-3" />
                  Details
                </Button>
              </Link>
              <div className="relative group/play">
                <Button
                  variant="ghost"
                  className="px-4 py-5 sm:px-3 sm:py-2"
                  onClick={() => agent.is_active ? pauseAgent(agent.id) : startAgent(agent.id, agent.youtube_connected)}
                >
                  {agent.is_active ? <Pause className="h-5 w-5 sm:h-4 sm:w-4" /> : <Play className="h-5 w-5 sm:h-4 sm:w-4" />}
                </Button>
                {/* Tooltip hidden on mobile via md:group-hover/play:opacity-100 */}
                <div className="hidden md:block absolute bottom-[110%] left-1/2 -translate-x-1/2 px-2 py-1 bg-black text-white text-[10px] rounded opacity-0 group-hover/play:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-[100] shadow-xl border border-white/10">
                  {agent.is_active ? 'Stop the agent from working' : 'Put the agent to actual work'}
                </div>
              </div>
            </CardFooter>
          </Card>
        ))}

        {/* Empty state / CTA card */}
        <Link to="/create-agent">
          <Card className="h-full border-dashed flex flex-col items-center justify-center p-8 hover:border-primary/50 transition-colors group">
            <div className="w-12 h-12 rounded-full bg-neutral-800 flex items-center justify-center mb-4 group-hover:bg-primary/10 transition-colors">
              <Plus className="h-6 w-6 text-secondary-foreground group-hover:text-primary" />
            </div>
            <p className="text-sm font-medium text-secondary-foreground group-hover:text-white">Add New Agent</p>
          </Card>
        </Link>
      </div>

      {/* Delete Confirmation Modal */}
      <AnimatePresence>
        {deleteConfirm && (
          <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="w-full max-w-sm"
            >
              <Card className="p-6 border-border shadow-2xl">
                <h3 className="text-xl font-bold text-white mb-2">Delete Agent?</h3>
                <p className="text-secondary-foreground mb-6">
                  Are you sure you want to delete this agent? This action cannot be undone and all data will be lost.
                </p>
                <div className="flex gap-3 justify-end">
                  <Button variant="ghost" onClick={() => setDeleteConfirm(null)}>
                    Cancel
                  </Button>
                  <Button variant="destructive" onClick={() => deleteAgent(deleteConfirm)}>
                    Delete
                  </Button>
                </div>
              </Card>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};
