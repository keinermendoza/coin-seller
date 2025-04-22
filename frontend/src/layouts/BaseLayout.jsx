import { Outlet } from "react-router";
import { Toaster } from "@/components/ui/sonner"

import NavigationMenu from "@/components/NavigationMenu";
export default function BaseLayout() {
  return (
    <div className="w-full mx-auto max-w-3xl min-h-screen pb-16 px-4 pt-4 bg-gray-100">
        <Outlet />
        <Toaster />
        <NavigationMenu />
  </div>
  )
}