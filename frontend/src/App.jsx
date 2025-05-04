import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { BaseLayout, TopButtonNavigationLayout} from "./layouts";
import {  Profile, SwitchAlarms } from "@/pages/configuration";
import { History, Sell, Buy, Requests, Edit } from "@/pages/changes"
import { ArrowRightLeft, Bolt } from "lucide-react"

const BaseNavItems = [
  { to: "/client/cambios", icon: <ArrowRightLeft  className="h-5 w-5" />, label: "Cambios" },
  { to: "/client/general", icon: <Bolt className="h-5 w-5" />, label: "General" },
]

const changesNavItems =  [
  { to: "recibir", text: "Recibir" },
  { to: "enviar", text: "Enviar" },
  { to: "nuevo", text: "Nuevo" },
]

const configurationNavItems = [
  { to: "historial", text: "Historial" },
  { to: "acciones", text: "Acciones" },
  { to: "perfil", text: "Perfil" },
]

function App() {
  
  return (

  <BrowserRouter>
    <Routes>
      <Route path="client" element={<BaseLayout navItems={BaseNavItems} />} >
        <Route index element={<Navigate to="cambios" replace />} /> 
        
        <Route path="cambios" element={<TopButtonNavigationLayout title="Cambios" navItems={changesNavItems} />} >
          <Route index element={<Navigate to="recibir" replace />} /> 
          <Route path="enviar" element={<Buy />} />
          <Route path="recibir" element={<Sell />} /> 
          <Route path="nuevo" element={<Requests />} /> 
          <Route path=":id" element={<Edit />} /> 
        </Route>

        <Route path="general" element={<TopButtonNavigationLayout title="General" navItems={configurationNavItems} />} >
          <Route index element={<Navigate to="historial" replace />} /> 
          <Route path="historial" element={<History />} />
          <Route path="perfil" element={<Profile />} /> 
          <Route path="acciones" element={<SwitchAlarms />} /> 
        </Route>

      </Route>
    </Routes>
  </BrowserRouter>
  )
}

export default App
