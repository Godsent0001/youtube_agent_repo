import { motion } from 'framer-motion';
import { User, Bell, Shield, Wallet, Globe, Mail } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const Settings = () => {
  const sections = [
    {
      title: 'Profile Settings',
      icon: User,
      fields: [
        { label: 'Display Name', value: 'John Doe', type: 'text' },
        { label: 'Email Address', value: 'john@example.com', type: 'email' },
      ]
    },
    {
      title: 'Preferences',
      icon: Bell,
      fields: [
        { label: 'Email Notifications', value: true, type: 'switch' },
        { label: 'Weekly Reports', value: false, type: 'switch' },
        { label: 'Activity Alerts', value: true, type: 'switch' },
      ]
    }
  ];

  return (
    <div className="py-20 px-8 max-w-4xl mx-auto">
      <div className="mb-12">
        <h1 className="text-4xl font-black text-white mb-4">Settings</h1>
        <p className="text-white/40 font-medium">Manage your MorphFlow account and preferences.</p>
      </div>

      <div className="space-y-10">
        {sections.map((section) => (
          <motion.div
            key={section.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/[0.03] border border-white/5 rounded-[40px] p-10 overflow-hidden shadow-2xl"
          >
            <div className="flex items-center gap-4 mb-10 pb-6 border-b border-white/5">
              <div className="h-12 w-12 rounded-2xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
                <section.icon className="h-6 w-6" />
              </div>
              <h2 className="text-xl font-black text-white">{section.title}</h2>
            </div>

            <div className="space-y-8">
              {section.fields.map((field) => (
                <div key={field.label} className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <p className="text-sm font-black text-white uppercase tracking-widest">{field.label}</p>
                    {typeof field.value !== 'boolean' && (
                       <p className="text-white/40 text-sm font-medium">{field.value}</p>
                    )}
                  </div>

                  {field.type === 'switch' ? (
                    <button className={`w-14 h-7 rounded-full transition-colors relative ${field.value ? 'bg-primary' : 'bg-white/10'}`}>
                      <div className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-all ${field.value ? 'right-1' : 'left-1'}`} />
                    </button>
                  ) : (
                    <Button variant="outline" size="sm" className="rounded-xl border-white/10 text-white font-bold px-6">
                      Edit
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        ))}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-500/5 border border-red-500/10 rounded-[40px] p-10 shadow-2xl"
        >
          <h2 className="text-xl font-black text-red-500 mb-6">Danger Zone</h2>
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-sm font-black text-white uppercase tracking-widest">Delete Account</p>
              <p className="text-white/40 text-sm font-medium">Permanently remove all your data and videos.</p>
            </div>
            <Button variant="ghost" className="text-red-500 hover:bg-red-500/10 font-black rounded-xl">
              Delete Forever
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
