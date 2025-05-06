import TitleSection from "@/components/TitleSection" 
import Anchor from "@/components/Anchor"

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
