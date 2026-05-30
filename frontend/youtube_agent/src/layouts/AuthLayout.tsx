import { Outlet } from 'react-router-dom';

export const AuthLayout = () => {
  return (
    <div className="min-h-screen bg-[#0F1115]">
      <Outlet />
    </div>
  );
};
