import { Outlet, NavLink } from "react-router";

export default function TopButtonNavigationLayout({navItems, title}) {
  return (
    <section>
      <h1 className="text-3xl font-medium mb-4">{title}</h1>

      <div className="mb-4 bg-muted text-muted-foreground inline-flex h-9 w-fit items-center justify-center rounded-lg p-[3px]">
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({isActive}) => 
          ` text-foreground dark:text-muted-foreground inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-md border border-transparent px-2 py-1 text-sm font-medium whitespace-nowrap transition-[color,box-shadow] focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:outline-ring focus-visible:ring-[3px] focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4
            ${
              isActive ? "bg-background shadow-sm dark:text-foreground dark:border-input dark:bg-input/30" : ""
            }`
          }
        >{item.text}</NavLink>
      ))}
      </div>
      <Outlet />
    </section>
        
  )
}
