import { useChanges } from "@/contexts/ChangeContext"
import timeFormat from "@/lib/timeFormat"
import { Button } from "@/components/ui/button"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { Info } from "lucide-react"
import { Separator } from "@/components/ui/separator"
import axios from "@/lib/axios";

import { toast } from "sonner"


export default function Update() {
  const {changes, refetchChanges} = useChanges()

  const handleAutoupdateChanges = async () => {
    try {
      const resp = await axios.post("/api/rates/autoupdate");
      if (resp.status === 201) {
        refetchChanges();
        toast("Tipos de cambio actualizados", {
          description: timeFormat(changes.now, true),
          action: {
            label: "Cerrar",
            onClick: () => console.log("Undo"),
          },
        })
      }
    } catch (error) {
      console.error("Error al hacer autoupdate:", error);
    }
  }
  return (
    <section className="text-slate-900 text-center mt-4 space-y-4">


      <div className="space-y-2">
        <p className="text-xl font-medium">Ultima consulta</p>
        <p className="font-semibold">{timeFormat(changes.now, true)}</p>
        <Button className="cursor-pointer" onClick={refetchChanges}>Consultar Nuevamente</Button>
      </div>

      <Separator className="my-4" />

      <div className="space-y-2">
        <p className="text-xl font-medium">Valor de cambio VES/BRL</p>
        <p className="font-bold text-4xl">{changes.buy.rate}</p>
        <p className="text-sm italic">Actualizado el {timeFormat(changes.buy.created)}</p>
      </div>

      <Separator className="my-4" />

      <div className="space-y-2">
        <p className="text-xl font-medium">Valor de cambio BRL/VES</p>
        <p className="font-bold text-4xl">{changes.sell.rate}</p>
        <p className="text-sm italic">Actualizado el {timeFormat(changes.sell.created)}</p>
      </div>

      <Separator className="my-4" />
      
        <div className="space-y-2">
          <p className="text-xl font-medium">Actualizar cambios</p>
          <p>Preciona este boton para actualizar los tipo de cambios en el sistema</p>
          <Alert className="bg-blue-200" variant="">
            <span className="text-blue-950"><Info className=" h-4 w-4" /></span>
            <AlertTitle className="text-blue-950">Nota importante</AlertTitle>
            <AlertDescription>
            los cambios se calcularan usando los mejores valores de compra y venta en el mercado y los margenes de ganancia que escogiste en la seccion de configuración para cada par de monedas 
            </AlertDescription>
          </Alert>

          <Button className="cursor-pointer" onClick={handleAutoupdateChanges}>Actualizar tipos automaticamente</Button>
        </div>

    </section>
  )
}
