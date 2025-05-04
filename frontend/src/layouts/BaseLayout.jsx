import { Outlet, NavLink } from "react-router";
import { Toaster } from "@/components/ui/sonner"

export default function BaseLayout({navItems}) {
  return (
    <div className="w-full mx-auto max-w-3xl min-h-screen pb-16 px-4 pt-4 bg-gray-100">
      <Outlet />
      <Toaster />

      <div className="fixed bottom-0 left-0 w-full border-t bg-white shadow z-50">
        <nav className="flex justify-around w-full">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center py-2 ${
                  isActive ? "text-blue-600" : "text-gray-500"
                }`
              }
            >
              {item.icon}
              <span className="text-xs">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>
  </div>
  )
}