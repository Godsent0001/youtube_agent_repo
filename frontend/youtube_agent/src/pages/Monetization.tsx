
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Sparkles, Save, X } from 'lucide-react';

export const Monetization = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8">
      <div className="text-center sm:text-left">
        <h1 className="text-2xl sm:text-3xl font-bold text-white">Advertise & Monetize Your AI Agents</h1>
        <p className="text-sm sm:text-base text-secondary-foreground">Add products, affiliate links, or campaigns for your agents to promote.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader className="px-4 sm:px-6">
              <CardTitle className="text-lg sm:text-xl">Campaign Details</CardTitle>
              <CardDescription className="text-xs sm:text-sm">Configure how the AI should integrate your promotions.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 px-4 sm:px-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Select Agent</label>
                <Select required>
                  <option value="1">Daily AI Facts</option>
                  <option value="2">Wealth Wisdom</option>
                  <option value="3">Motivation Minute</option>
                </Select>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-white">Ad Type</label>
                  <Select defaultValue="affiliate">
                    <option value="affiliate">Affiliate Link</option>
                    <option value="product">Own Product</option>
                    <option value="brand">Brand Deal</option>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-white">Campaign Name</label>
                  <Input placeholder="e.g. Summer AI Tools Promo" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Product / Promo Link</label>
                <Input type="url" placeholder="https://your-link.com/ref=ai-agent" />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-white">Start Date</label>
                  <Input type="date" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-white">End Date (Optional)</label>
                  <Input type="date" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Optional Notes / Focus</label>
                <textarea
                  className="flex min-h-[100px] w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-white placeholder:text-neutral-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="e.g. Promote naturally in video script, focus on efficiency benefits"
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col sm:flex-row gap-3 sm:justify-between border-t border-border pt-6 px-4 sm:px-6">
              <Button variant="secondary" className="w-full sm:w-auto gap-2 py-6 sm:py-2 order-2 sm:order-1">
                <X className="h-4 w-4" />
                Cancel
              </Button>
              <Button className="w-full sm:w-auto gap-2 py-6 sm:py-2 order-1 sm:order-2">
                <Save className="h-4 w-4" />
                Save Campaign
              </Button>
            </CardFooter>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="bg-primary/5 border-primary/20">
            <CardHeader className="px-4 sm:px-6">
              <CardTitle className="flex items-center gap-2 text-lg">
                <Sparkles className="h-5 w-5 text-primary" />
                AI Preview
              </CardTitle>
            </CardHeader>
            <CardContent className="px-4 sm:px-6">
              <p className="text-sm text-secondary-foreground leading-relaxed">
                "Your agent will integrate the ad into upcoming videos naturally, staying on topic. Based on your niche (Facts), the AI will mention the product as a recommended tool for viewers interested in space technology."
              </p>
              <div className="mt-6 p-4 bg-black/40 rounded-lg border border-border">
                <div className="text-[10px] uppercase text-primary font-bold mb-2">Example Script Integration</div>
                <p className="text-xs italic text-neutral-400">
                  "...and that's why black holes are so fascinating. Speaking of efficiency, if you want to stay organized like a NASA scientist, check out the [Your Product Name] link in the description. Now, back to the event horizon..."
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="px-4 sm:px-6">
              <CardTitle className="text-lg">Active Campaigns</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 px-4 sm:px-6">
              <div className="p-3 bg-neutral-900 rounded-lg border border-border flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium text-white">Notion AI Promo</div>
                  <div className="text-[10px] text-secondary-foreground">Agent: Wealth Wisdom</div>
                </div>
                <div className="w-2 h-2 rounded-full bg-green-500" />
              </div>
              <div className="p-3 bg-neutral-900 rounded-lg border border-border flex justify-between items-center">
                <div>
                  <div className="text-sm font-medium text-white">Course Launch</div>
                  <div className="text-[10px] text-secondary-foreground">Agent: Daily AI Facts</div>
                </div>
                <div className="w-2 h-2 rounded-full bg-green-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
