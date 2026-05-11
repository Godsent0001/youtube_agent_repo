
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Plus, Play, Pause, ExternalLink } from 'lucide-react';
import { apiRequest } from '../utils/api';

export const Dashboard = () => {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

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

  const toggleAgentStatus = async (agentId: string, currentStatus: boolean) => {
    try {
        await apiRequest(`/agents/${agentId}`, {
            method: 'PUT',
            body: JSON.stringify({ is_active: !currentStatus })
        });
        setAgents(agents.map(a => a.id === agentId ? { ...a, is_active: !currentStatus } : a));
    } catch (err) {
        console.error('Failed to toggle status:', err);
    }
  };
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Your AI Agents</h1>
          <p className="text-secondary-foreground">Monitor performance and manage your agents</p>
        </div>
        <div className="flex gap-3">
          <Link to="/monetization">
            <Button variant="outline">Run Ads</Button>
          </Link>
          <Link to="/create-agent">
            <Button className="gap-2">
              <Plus className="h-5 w-5" />
              Create Agent
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
            <p className="text-white col-span-full text-center py-12">Loading agents...</p>
        ) : agents.map((agent) => (
          <Card key={agent.id} className="group overflow-hidden">
            <CardHeader className="pb-4">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-xl">{agent.name}</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    {agent.niche} • {agent.content_type}
                  </CardDescription>
                </div>
                <Badge variant={agent.is_active ? 'success' : 'warning'}>
                  {agent.is_active ? 'active' : 'paused'}
                </Badge>
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
            <CardFooter className="gap-2 bg-neutral-900/50 pt-4">
              <Link to={`/agent/${agent.id}`} className="flex-1">
                <Button variant="secondary" className="w-full gap-2 text-xs">
                  <ExternalLink className="h-3 w-3" />
                  Details
                </Button>
              </Link>
              <Button
                variant="ghost"
                className="px-3"
                onClick={() => toggleAgentStatus(agent.id, agent.is_active)}
              >
                {agent.is_active ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </Button>
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
    </div>
  );
};
