import { NavLink } from "react-router";
import { ArrowRightLeft, Bolt, Images } from "lucide-react"

export default function NavigationMenu() {
  
  const navItems = [
    { to: "/client/images", icon: <Images className="h-5 w-5" />, label: "Imagenes" },
    { to: "/client/changes", icon: <ArrowRightLeft  className="h-5 w-5" />, label: "Cambios" },
    { to: "/client/configuration", icon: <Bolt className="h-5 w-5" />, label: "Configuraciones" },
  ]

  return (
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
  )
}