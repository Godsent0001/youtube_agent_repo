import { createContext, useContext, useState, ReactNode } from 'react';
import { cn } from '../../utils/cn';

const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (id: string) => void;
} | null>(null);

export const Tabs = ({ children, defaultValue, className }: { children: ReactNode, defaultValue: string, className?: string }) => {
  const [activeTab, setActiveTab] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={cn('w-full', className)}>{children}</div>
    </TabsContext.Provider>
  );
};

export const TabsList = ({ children, className }: { children: ReactNode, className?: string }) => (
  <div className={cn('inline-flex h-10 items-center justify-center rounded-md bg-neutral-900 p-1 text-secondary-foreground', className)}>
    {children}
  </div>
);

export const TabsTrigger = ({ children, value, className }: { children: ReactNode, value: string, className?: string }) => {
  const context = useContext(TabsContext);
  if (!context) return null;
  const isActive = context.activeTab === value;
  return (
    <button
      onClick={() => context.setActiveTab(value)}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50',
        isActive ? 'bg-card text-white shadow-sm' : 'hover:text-white',
        className
      )}
    >
      {children}
    </button>
  );
};

export const TabsContent = ({ children, value }: { children: ReactNode, value: string }) => {
  const context = useContext(TabsContext);
  if (!context || context.activeTab !== value) return null;
  return <div className="mt-2 outline-none">{children}</div>;
};
