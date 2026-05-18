
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { User as UserIcon, Bell, Key, Shield, Trash2, Play, Save } from 'lucide-react';
import { apiRequest } from '../utils/api';

export const Settings = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await apiRequest('/auth/me');
        setUser(data);
      } catch (err) {
        console.error('Failed to fetch user:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) return <p className="text-white text-center py-12">Loading settings...</p>;

  return (
    <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8">
      <div className="text-center sm:text-left">
        <h1 className="text-2xl sm:text-3xl font-bold text-white">Settings</h1>
        <p className="text-sm sm:text-base text-secondary-foreground">Manage your account and preferences</p>
      </div>

      <div className="space-y-6">
        {/* Account Settings */}
        <Card>
          <CardHeader className="px-4 sm:px-6">
            <div className="flex items-center gap-2">
              <UserIcon className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg sm:text-xl">Account Settings</CardTitle>
            </div>
            <CardDescription className="text-xs sm:text-sm">Update your personal information and profile settings.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 px-4 sm:px-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Full Name</label>
                <Input defaultValue={user?.full_name || ''} className="py-5 sm:py-2" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Email Address</label>
                <Input type="email" defaultValue={user?.email || ''} readOnly className="py-5 sm:py-2 opacity-70" />
              </div>
            </div>
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 bg-neutral-900 rounded-lg border border-border gap-4">
              <div className="flex items-center gap-3">
                <Play className="h-6 w-6 text-red-600" />
                <div>
                  <div className="text-sm font-bold text-white">YouTube OAuth</div>
                  <div className="text-xs text-secondary-foreground">
                    {user?.youtube_refresh_token ? 'Connected' : 'Not Connected'}
                  </div>
                </div>
              </div>
              <Button variant="outline" size="sm" className="w-full sm:w-auto py-5 sm:py-2">
                  {user?.youtube_refresh_token ? 'Reconnect' : 'Connect'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader className="px-4 sm:px-6">
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg sm:text-xl">Notification Settings</CardTitle>
            </div>
            <CardDescription className="text-xs sm:text-sm">Choose what updates you want to receive.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 px-4 sm:px-6">
            {[
              { label: 'Email Notifications for New Videos', description: 'Get an email every time an agent posts a video.' },
              { label: 'Campaign Performance Updates', description: 'Weekly reports on your monetization campaigns.' },
              { label: 'Agent Status Alerts', description: 'Immediate alerts if an agent is paused or encounters an error.' },
            ].map((notif, i) => (
              <div key={i} className="flex items-start justify-between">
                <div>
                  <div className="text-sm font-medium text-white">{notif.label}</div>
                  <div className="text-xs text-secondary-foreground">{notif.description}</div>
                </div>
                <input type="checkbox" className="mt-1 h-4 w-4 rounded border-border bg-card text-primary focus:ring-primary" />
              </div>
            ))}
          </CardContent>
        </Card>

        {/* API Keys */}
        <Card>
          <CardHeader className="px-4 sm:px-6">
            <div className="flex items-center gap-2">
              <Key className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg sm:text-xl">API & Integration</CardTitle>
            </div>
            <CardDescription className="text-xs sm:text-sm">Access keys for advanced integrations and developer tools.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 px-4 sm:px-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">YouTube API Key</label>
              <div className="flex flex-col sm:flex-row gap-2">
                <Input type="password" value="********************************" readOnly className="py-5 sm:py-2" />
                <Button variant="outline" className="w-full sm:w-auto py-5 sm:py-2">Edit</Button>
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">AI Engine API Key</label>
              <div className="flex flex-col sm:flex-row gap-2">
                <Input type="password" value="********************************" readOnly className="py-5 sm:py-2" />
                <Button variant="outline" className="w-full sm:w-auto py-5 sm:py-2">Edit</Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Preferences */}
        <Card>
          <CardHeader className="px-4 sm:px-6">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg sm:text-xl">Default Preferences</CardTitle>
            </div>
            <CardDescription className="text-xs sm:text-sm">Set defaults for newly created agents.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4 px-4 sm:px-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Video Length</label>
              <Select defaultValue="30s">
                <option value="30s">30 Seconds</option>
                <option value="60s">60 Seconds</option>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Content Type</label>
              <Select defaultValue="shorts">
                <option value="shorts">Shorts</option>
                <option value="long">Long-form</option>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Language</label>
              <Select defaultValue="en">
                <option value="en">English (US)</option>
                <option value="ng">English (NG)</option>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-red-900/50">
          <CardHeader className="px-4 sm:px-6">
            <div className="flex items-center gap-2">
              <Trash2 className="h-5 w-5 text-red-500" />
              <CardTitle className="text-red-500 text-lg sm:text-xl">Danger Zone</CardTitle>
            </div>
            <CardDescription className="text-xs sm:text-sm">Irreversible actions for your account and agents.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col sm:flex-row gap-3 sm:gap-4 px-4 sm:px-6">
            <Button variant="outline" className="w-full sm:w-auto border-red-900 text-red-500 hover:bg-red-950/30 py-6 sm:py-2">
              Disconnect All Agents
            </Button>
            <Button variant="outline" className="w-full sm:w-auto border-red-900 text-red-500 hover:bg-red-950/30 py-6 sm:py-2">
              Delete Account
            </Button>
          </CardContent>
        </Card>

        <div className="flex justify-end pt-6">
          <Button size="lg" className="w-full sm:w-auto sm:px-12 gap-2 py-6 sm:py-2">
            <Save className="h-5 w-5" />
            Save Changes
          </Button>
        </div>
      </div>
    </div>
  );
};
