import TitleSection from "@/components/TitleSection" 
import { Card } from "@/components/ui/card"
import { Link as LinkIcon } from "lucide-react"

function Anchor({children, to}) {
  return (
    <Card className="p-0 overflow-hidden" >
      <a target="_blank" 
        className="transition-colors duration-200 hover:bg-amber-200 flex items-center  justify-between gap-4 py-4 px-6 w-full" 
        href={to}>
        <span>{children}</span>
        <LinkIcon />
      </a>
    </Card>
  )
}

    

export default function SwitchAlarms() {
  
  return (
    <section>
      <TitleSection title="Acciones" subtitle="esta seccion es un portal a otras aplicaciones relacionadas a este proyecto" />

      <ul className="flex flex-col gap-3 my-4">
        <Anchor to="/controller/p2p/fiatexchangepair/">Tabla de Pares de monedas</Anchor>
        <Anchor to="/controller/p2p/traderequest/">Tabla de Operaciones</Anchor>
        <Anchor to="/controller/p2p/switchmodel/">Procesos en Segundo plano</Anchor>
      </ul>
    </section>
  )
}
