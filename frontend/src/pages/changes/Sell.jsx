import { useState } from "react"

import Calculator from "@/components/Calculator"
import { Separator } from "@/components/ui/separator"
import { AlertCircle } from "lucide-react"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"


import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

import RequestList from "@/components/RequestList"

import { useChanges } from "@/contexts/ChangeContext"
import { useTradeRequest } from "@/contexts/TradeRequestContext"
import { toast } from "sonner"
import axios from "@/lib/axios"


export default function Sell() {
  const [selectedPair, setSelectedPair] = useState(0)
  const {sellPairs} = useChanges()
  const {sellRequests, updateTradeRequest} = useTradeRequest()

  async function onSubmit(formData, trade_request_id, side_operation) {
    const body = {
      ...formData,
      trade_request_id,
      side_operation,
    }

    const resp = await axios.post("/api/trade-requests/register-exchange", body)
    if (resp.status === 201) {
      toast(
          "You submitted the following values:", {
          description: JSON.stringify(formData, null, 2),
          action: {
              label: "cerrar",
              onClick: () => console.log("Undo"),
          },
      })

      updateTradeRequest(resp.data.id, resp.data)
    }
  }
  

  

  
  return (
    <section>

      <div className="text-slate-900 flex flex-col items-center justify-center text-center gap-4 my-4">
        <p className="text-xl font-medium">Calculadora de Cambios</p>
        {sellPairs.length > 0 ? (
          <Select onValueChange={(value) => setSelectedPair(value)} defaultValue={selectedPair}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar cambio" />
          </SelectTrigger>
          <SelectContent>
            {sellPairs.map((pair, index) => (
              <SelectItem key={index} value={index}>{pair.currencyFrom.code} a {pair.currencyTo.code}</SelectItem>
            ))}
          </SelectContent>
        </Select>)
        : (
          <div className="text-sm">
            <p>No hay operaciones para mostrar</p>
          </div>
        )  
      }
      {sellPairs[selectedPair] && <Calculator data={sellPairs[selectedPair]} />}
      </div>

      <Separator className="my-4" />

      {sellPairs[selectedPair] &&
        <Alert className="bg-red-100" variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Importante!!</AlertTitle>
        <AlertDescription>
          Vender USDT por menos de {sellPairs[selectedPair]?.rateInfo.sell_price_limit} produce perdidas 
        </AlertDescription>
      </Alert>}

      <Separator className="my-4" />

      {sellRequests &&  
        <RequestList
          onSubmit={onSubmit}
          data={sellRequests} 
          titleSection="Peticiones de cambios" />}

    </section>
    
  )
}
