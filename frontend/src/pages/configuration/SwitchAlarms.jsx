import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import axios from "@/lib/axios"
import { useState } from "react"

const MyTooltip = ({children, tooltipText}) => {
  return (
  <TooltipProvider>
    <Tooltip>
      <TooltipTrigger>
        {children}
      </TooltipTrigger>
      <TooltipContent>
        <p className="text-sm w-fit max-w-md text-center">{tooltipText}</p>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
  )

}


export default function SwitchAlarms() {
  const [switches, setSwitches] = useState({
    requestP2P: false,
    performDummy: false,
    emailAlert: false,
  })

  const handleToggle = async (key, value) => {
    setSwitches((prev) => ({ ...prev, [key]: value }))
    
    try {
      await axios.post("/api/update-actions/", {
      "action": key,
      "isActive": value
    })
    } catch (error) {
      console.error("Error al hacer la petición:", error)
      setSwitches((prev) => ({ ...prev, [key]: !value }))
    }
  }

  return (
    <section className="space-y-4">
      <p>Acciones</p>

      <div className="flex flex-col gap-4 w-fit">

        <MyTooltip
          tooltipText="almacena precios de binance sobre las monedas en la base de datos"
        >
          <div className="flex items-center space-x-2">
            <Switch id="request-p2p-data" 
               checked={switches.requestP2P}
               onCheckedChange={(value) => handleToggle("requestP2P", value)}
            />
            <Label htmlFor="request-p2p-data">Recolectar Informacion de Precios</Label>
          </div>
        </MyTooltip>
        
        
        <MyTooltip
          tooltipText="Calcula y guarda tipos de cambio hipoteticos en la base de datos"
        >
          <div className="flex items-center space-x-2">
            <Switch id="perform-dummy-changes"
             checked={switches.requestP2P}
             onCheckedChange={(value) => handleToggle("requestP2P", value)}
            />
            <Label htmlFor="perform-dummy-changes">Crear Cambios Hipoteticos</Label>
          </div>
        </MyTooltip>
        
        <MyTooltip
          tooltipText="Envía un email cada vez que los tipos de cambio sobrepasen el margen de seguridad"
        >
          <div className="flex items-center space-x-2">
            <Switch id="email-alert" 
             checked={switches.requestP2P}
             onCheckedChange={(value) => handleToggle("requestP2P", value)}
            />
            <Label htmlFor="email-alert">Activar Alerta por Email</Label>
          </div>
        </MyTooltip>
        
      </div>
    </section>
  )
}
