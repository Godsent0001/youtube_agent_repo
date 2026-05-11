
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
  Download,
  Pause,
  Clock,
  Globe
} from 'lucide-react';

export const AgentDetail = () => {
  const { id } = useParams();
  console.log("Agent ID:", id);

  // Mock data for a single agent
  const agent = {
    name: 'Daily AI Facts',
    niche: 'Facts',
    type: 'Shorts',
    status: 'active',
    lastPosted: '2 hours ago',
    metrics: [
      { label: 'Views', value: '12,430', icon: Eye, color: 'text-blue-500' },
      { label: 'Avg Watch Time', value: '18s', icon: Clock, color: 'text-green-500' },
      { label: 'Retention Rate', value: '75%', icon: TrendingUp, color: 'text-primary' },
      { label: 'Likes', value: '320', icon: ThumbsUp, color: 'text-red-500' },
      { label: 'Comments', value: '12', icon: MessageSquare, color: 'text-purple-500' },
      { label: 'Estimated Earnings', value: '$45', icon: DollarSign, color: 'text-emerald-500' },
    ],
    videoHistory: [
      { id: 1, title: 'Black Holes Explained', date: '04/09', views: '2,340', retention: '70%', earnings: '$8' },
      { id: 2, title: 'Solar System Facts', date: '04/08', views: '1,980', retention: '72%', earnings: '$6' },
      { id: 3, title: 'Mars Facts', date: '04/07', views: '3,210', retention: '80%', earnings: '$12' },
      { id: 4, title: 'Jupiter Great Red Spot', date: '04/06', views: '1,100', retention: '65%', earnings: '$4' },
      { id: 5, title: 'Moon Landing Secrets', date: '04/05', views: '4,500', retention: '85%', earnings: '$20' },
    ],
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
          <Button variant="outline" size="sm" className="gap-2">
            <Download className="h-4 w-4" />
            Export
          </Button>
          <Button size="sm" className="gap-2">
            <Pause className="h-4 w-4" />
            Pause Agent
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
                {[
                  { action: 'Video Posted', detail: 'Black Holes Explained', time: '2 hours ago' },
                  { action: 'Script Generated', detail: 'Neutron Stars (Upcoming)', time: '4 hours ago' },
                  { action: 'Ad Integrated', detail: 'Summer AI Tools Promo', time: '6 hours ago' },
                  { action: 'Analytics Synced', detail: 'Success', time: '12 hours ago' },
                ].map((log, i) => (
                  <div key={i} className="flex items-center gap-4 text-sm">
                    <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(255,0,0,0.5)]" />
                    <div className="flex-1">
                      <div className="text-white font-medium">{log.action}</div>
                      <div className="text-secondary-foreground text-xs">{log.detail}</div>
                    </div>
                    <div className="text-xs text-secondary-foreground">{log.time}</div>
                  </div>
                ))}
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
