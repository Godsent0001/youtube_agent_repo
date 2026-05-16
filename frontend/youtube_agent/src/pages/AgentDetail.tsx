
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/Tabs';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  TrendingUp,
  Users,
  DollarSign,
  MessageSquare,
  ThumbsUp,
  Eye,
  Pause,
  Play,
  Clock,
  Globe,
  Play as YoutubeIcon
} from 'lucide-react';
import { apiRequest } from '../utils/api';

export const AgentDetail = () => {
  const { id } = useParams();
  const [agentData, setAgentData] = useState<any>(null);
  const [videos, setVideos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [agent, allVideos] = await Promise.all([
          apiRequest(`/agents/${id}`),
          apiRequest(`/videos`)
        ]);
        setAgentData(agent);
        setVideos(allVideos.filter((v: any) => v.agent_id === id));
      } catch (err) {
        console.error("Failed to fetch agent data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const startAgent = async () => {
    if (!agentData.youtube_connected) {
      handleConnectYouTube();
      return;
    }
    try {
        await apiRequest(`/agents/${id}/generate`, {
            method: 'POST'
        });
        setAgentData({ ...agentData, is_active: true });
    } catch (err) {
        console.error('Failed to start agent:', err);
    }
  };

  const pauseAgent = async () => {
    try {
        const updated = await apiRequest(`/agents/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ is_active: false })
        });
        setAgentData(updated);
    } catch (err) {
        console.error('Failed to pause agent:', err);
    }
  };

  const toggleAgentStatus = () => {
    if (agentData.is_active) {
      pauseAgent();
    } else {
      startAgent();
    }
  };

  const handleConnectYouTube = () => {
    // Redirect to backend OAuth initiation endpoint
    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://youtube-backend-agent-repo.onrender.com';
    window.location.href = `${API_BASE}/agents/${id}/youtube/connect/`;
  };

  if (loading) return <div className="p-8 text-white">Loading agent...</div>;
  if (!agentData) return <div className="p-8 text-white">Agent not found.</div>;

  const agent = {
    name: agentData.name,
    niche: agentData.niche,
    type: agentData.content_type === 'shorts' ? 'Shorts' : 'Long-form',
    status: agentData.is_active ? 'active' : 'paused',
    youtube_connected: agentData.youtube_connected,
    lastPosted: agentData.last_run_at ? new Date(agentData.last_run_at).toLocaleString() : 'Never',
    is_active: agentData.is_active,
    metrics: [
      { label: 'Views', value: videos.reduce((acc, v) => acc + (v.views || 0), 0).toLocaleString(), icon: Eye, color: 'text-blue-500' },
      { label: 'Avg Watch Time', value: agentData.avg_watch_time ? `${agentData.avg_watch_time}s` : '0s', icon: Clock, color: 'text-green-500' },
      { label: 'Retention Rate', value: `${agentData.avg_retention || 0}%`, icon: TrendingUp, color: 'text-primary' },
      { label: 'Likes', value: videos.reduce((acc, v) => acc + (v.likes || 0), 0).toLocaleString(), icon: ThumbsUp, color: 'text-red-500' },
      { label: 'Comments', value: videos.reduce((acc, v) => acc + (v.comments || 0), 0).toLocaleString(), icon: MessageSquare, color: 'text-purple-500' },
      { label: 'Estimated Earnings', value: `$${(videos.length * 2)}`, icon: DollarSign, color: 'text-emerald-500' },
    ],
    videoHistory: videos.map(v => ({
      id: v.id,
      title: v.title || 'Untitled Video',
      date: new Date(v.created_at).toLocaleDateString(),
      views: v.views || 0,
      retention: `${v.retention_rate || 0}%`,
      earnings: `$${(v.views || 0) * 0.002}`
    })),
    audience: {
      age: [
        { range: '18–24', percentage: 45 },
        { range: '25–34', percentage: 30 },
        { range: '35–44', percentage: 15 },
        { range: '45+', percentage: 10 },
      ],
      regions: [
        { name: 'United States', percentage: 35 },
        { name: 'Nigeria', percentage: 30 },
        { name: 'India', percentage: 20 },
        { name: 'Other', percentage: 15 },
      ]
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-4">
        <Link to="/dashboard">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-white">{agent.name}</h1>
          <p className="text-secondary-foreground">{agent.niche} • {agent.type}</p>
        </div>
        <div className="flex gap-2">
          {agent.youtube_connected ? (
            <Button variant="outline" size="sm" className="gap-2 text-green-500 border-green-500/50 bg-green-500/10 hover:bg-green-500/20">
              <YoutubeIcon className="h-4 w-4" />
              Connected
            </Button>
          ) : (
            <Button variant="outline" size="sm" className="gap-2 text-primary border-primary/50 bg-primary/10 hover:bg-primary/20" onClick={handleConnectYouTube}>
              <YoutubeIcon className="h-4 w-4" />
              Connect YouTube
            </Button>
          )}
          <Button
            size="sm"
            className={`gap-2 ${agent.is_active ? 'bg-amber-600 hover:bg-amber-700' : 'bg-primary'}`}
            onClick={toggleAgentStatus}
          >
            {agent.is_active ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            {agent.is_active ? 'Pause Agent' : 'Start Agent'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {agent.metrics.map((metric, idx) => (
          <Card key={idx} className="p-4">
            <div className="flex items-center gap-2 text-secondary-foreground mb-2 text-xs font-medium uppercase tracking-wider">
              <metric.icon className={`h-3 w-3 ${metric.color}`} />
              {metric.label}
            </div>
            <div className="text-2xl font-bold text-white">{metric.value}</div>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="history">Video History</TabsTrigger>
          <TabsTrigger value="audience">Audience</TabsTrigger>
          <TabsTrigger value="revenue">Revenue</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Views Trend (Last 7 Days)</CardTitle>
                <CardDescription>Visual trend of your agent performance</CardDescription>
              </CardHeader>
              <CardContent className="h-64 flex items-end gap-2 px-6">
                {[40, 60, 45, 90, 65, 80, 100].map((height, i) => (
                  <div key={i} className="flex-1 bg-primary/20 rounded-t-sm relative group">
                    <motion.div
                      className="absolute bottom-0 w-full bg-primary rounded-t-sm"
                      initial={{ height: 0 }}
                      animate={{ height: `${height}%` }}
                      transition={{ duration: 1, delay: i * 0.1 }}
                    />
                    <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 -translate-x-1/2 bg-white text-black text-[10px] py-1 px-2 rounded transition-opacity whitespace-nowrap">
                      {height * 100} views
                    </div>
                  </div>
                ))}
              </CardContent>
              <div className="flex justify-between px-6 pb-6 text-[10px] text-secondary-foreground uppercase">
                <span>Mon</span>
                <span>Tue</span>
                <span>Wed</span>
                <span>Thu</span>
                <span>Fri</span>
                <span>Sat</span>
                <span>Sun</span>
              </div>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Agent Activity</CardTitle>
                <CardDescription>Recent actions taken by your AI agent</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {videos.length > 0 ? videos.slice(0, 5).map((v, i) => (
                  <div key={i} className="flex items-center gap-4 text-sm">
                    <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(255,0,0,0.5)]" />
                    <div className="flex-1">
                      <div className="text-white font-medium">Video Created & Posted</div>
                      <div className="text-secondary-foreground text-xs">{v.title || v.topic}</div>
                    </div>
                    <div className="text-xs text-secondary-foreground">{new Date(v.created_at).toLocaleDateString()}</div>
                  </div>
                )) : (
                  <div className="text-center py-8 text-secondary-foreground text-sm italic">
                    No recent activity recorded.
                  </div>
                )}
                {agentData.created_at && (
                  <div className="flex items-center gap-4 text-sm">
                    <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
                    <div className="flex-1">
                      <div className="text-white font-medium">Agent Initialized</div>
                      <div className="text-secondary-foreground text-xs">System ready</div>
                    </div>
                    <div className="text-xs text-secondary-foreground">{new Date(agentData.created_at).toLocaleDateString()}</div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="history">
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-border bg-neutral-900/50">
                    <th className="p-4 text-xs font-semibold text-secondary-foreground uppercase">Date</th>
                    <th className="p-4 text-xs font-semibold text-secondary-foreground uppercase">Video Title</th>
                    <th className="p-4 text-xs font-semibold text-secondary-foreground uppercase">Views</th>
                    <th className="p-4 text-xs font-semibold text-secondary-foreground uppercase">Retention</th>
                    <th className="p-4 text-xs font-semibold text-secondary-foreground uppercase">Earnings</th>
                  </tr>
                </thead>
                <tbody>
                  {agent.videoHistory.map((video) => (
                    <tr key={video.id} className="border-b border-border hover:bg-neutral-800/50 transition-colors">
                      <td className="p-4 text-sm">{video.date}</td>
                      <td className="p-4 text-sm font-medium text-white">{video.title}</td>
                      <td className="p-4 text-sm">{video.views}</td>
                      <td className="p-4 text-sm">{video.retention}</td>
                      <td className="p-4 text-sm text-primary font-semibold">{video.earnings}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="p-4 border-t border-border flex justify-center">
              <Button variant="ghost" size="sm">View All History</Button>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="audience">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-primary" />
                  Age Breakdown
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {agent.audience.age.map((item, i) => (
                  <div key={i} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-secondary-foreground">{item.range}</span>
                      <span className="text-white font-medium">{item.percentage}%</span>
                    </div>
                    <div className="h-2 w-full bg-neutral-800 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-primary"
                        initial={{ width: 0 }}
                        animate={{ width: `${item.percentage}%` }}
                        transition={{ duration: 1, delay: i * 0.1 }}
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-primary" />
                  Top Regions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {agent.audience.regions.map((item, i) => (
                  <div key={i} className="flex items-center gap-4">
                    <div className="text-sm font-medium text-white w-24">{item.name}</div>
                    <div className="flex-1 h-2 bg-neutral-800 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-primary"
                        initial={{ width: 0 }}
                        animate={{ width: `${item.percentage}%` }}
                        transition={{ duration: 1, delay: i * 0.1 }}
                      />
                    </div>
                    <div className="text-sm text-secondary-foreground w-8 text-right">{item.percentage}%</div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="revenue">
          <Card className="p-8">
            <div className="flex flex-col md:flex-row items-center justify-center gap-12">
              <div className="relative w-48 h-48">
                {/* Simplified Pie Chart Representation */}
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="96"
                    cy="96"
                    r="80"
                    stroke="#333"
                    strokeWidth="20"
                    fill="transparent"
                  />
                  <motion.circle
                    cx="96"
                    cy="96"
                    r="80"
                    stroke="#FF0000"
                    strokeWidth="20"
                    fill="transparent"
                    strokeDasharray="502.4"
                    initial={{ strokeDashoffset: 502.4 }}
                    animate={{ strokeDashoffset: 502.4 * (1 - 0.55) }}
                    transition={{ duration: 1.5 }}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <div className="text-2xl font-bold">$45</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Total</div>
                </div>
              </div>

              <div className="space-y-6 flex-1 max-w-sm w-full">
                <div className="flex justify-between items-center p-4 rounded-xl bg-neutral-900 border border-border">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-primary" />
                    <div>
                      <div className="text-sm font-bold text-white">Ad Revenue</div>
                      <div className="text-xs text-secondary-foreground">YouTube Adsense</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-white">$25</div>
                    <div className="text-xs text-primary">55%</div>
                  </div>
                </div>

                <div className="flex justify-between items-center p-4 rounded-xl bg-neutral-900 border border-border">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-neutral-700" />
                    <div>
                      <div className="text-sm font-bold text-white">Affiliate Revenue</div>
                      <div className="text-xs text-secondary-foreground">Product promos</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-white">$20</div>
                    <div className="text-xs text-secondary-foreground">45%</div>
                  </div>
                </div>

                <Button className="w-full">Manage Payouts</Button>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
