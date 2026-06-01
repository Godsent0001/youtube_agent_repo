import { Outlet } from 'react-router-dom';

export const DashboardLayout = () => {
  return (
    <div className="min-h-screen bg-[#0F1115]">
      <Outlet />
    </div>
  );
};
