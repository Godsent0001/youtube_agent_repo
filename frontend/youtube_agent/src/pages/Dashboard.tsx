
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Plus, Play, Pause, ExternalLink, MessageSquare, ThumbsUp } from 'lucide-react';

const AGENTS = [
  {
    id: '1',
    name: 'Daily AI Facts',
    niche: 'Facts',
    type: 'Shorts',
    status: 'active',
    lastPosted: '2 hours ago',
    metrics: {
      views: '12.4K',
      retention: '75%',
      likes: '320',
      comments: '12',
      earnings: '$45',
    },
  },
  {
    id: '2',
    name: 'Wealth Wisdom',
    niche: 'Finance',
    type: 'Long-form',
    status: 'active',
    lastPosted: '5 hours ago',
    metrics: {
      views: '8.2K',
      retention: '45%',
      likes: '150',
      comments: '45',
      earnings: '$120',
    },
  },
  {
    id: '3',
    name: 'Motivation Minute',
    niche: 'Motivation',
    type: 'Shorts',
    status: 'paused',
    lastPosted: '1 day ago',
    metrics: {
      views: '45K',
      retention: '82%',
      likes: '1.2K',
      comments: '88',
      earnings: '$210',
    },
  },
];

export const Dashboard = () => {
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
        {AGENTS.map((agent) => (
          <Card key={agent.id} className="group overflow-hidden">
            <CardHeader className="pb-4">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-xl">{agent.name}</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    {agent.niche} • {agent.type}
                  </CardDescription>
                </div>
                <Badge variant={agent.status === 'active' ? 'success' : 'warning'}>
                  {agent.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-xs text-secondary-foreground">
                Last Video Posted: <span className="text-white">{agent.lastPosted}</span>
              </div>
              <div className="grid grid-cols-3 gap-4 border-y border-border py-4">
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{agent.metrics.views}</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Views</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{agent.metrics.retention}</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Retention</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{agent.metrics.earnings}</div>
                  <div className="text-[10px] text-secondary-foreground uppercase">Earnings</div>
                </div>
              </div>
              <div className="flex justify-between items-center text-xs text-secondary-foreground pt-2">
                <div className="flex items-center gap-1">
                  <ThumbsUp className="h-3 w-3" /> {agent.metrics.likes}
                </div>
                <div className="flex items-center gap-1">
                  <MessageSquare className="h-3 w-3" /> {agent.metrics.comments}
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
              <Button variant="ghost" className="px-3">
                {agent.status === 'active' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
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
