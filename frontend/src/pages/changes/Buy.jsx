import { useState } from "react"
import Calculator from "@/components/Calculator"
import { FormRegisterOperation } from "@/components/FormRegisterOperation"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { AlertCircle } from "lucide-react"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"

import { Link } from "react-router"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

import { useChanges } from "@/contexts/ChangeContext"
import { useTradeRequest } from "@/contexts/TradeRequestContext"
import RequestList from "@/components/RequestList"
import axios from "@/lib/axios"

export default function Buy() {
  const [selectedPair, setSelectedPair] = useState(0)
  const {buyPairs} = useChanges()
  const {buyRequests, updateTradeRequest} = useTradeRequest()

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
      console.log(resp.data)
      updateTradeRequest(trade_request_id, resp.data)
    }
  }

  if (!buyPairs) {
    return (<p className="text-4xl">Cargando...</p>)
  }
  

  return (
    <section>
       <div className="text-slate-900 flex flex-col items-center justify-center text-center gap-4 my-4">
        <p className="text-xl font-medium">Calculadora de Cambios</p>
        {buyPairs?.length > 0 ? (
        <Select onValueChange={(value) => setSelectedPair(value)} defaultValue={selectedPair}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar cambio" />
          </SelectTrigger>
          <SelectContent>
            {buyPairs?.map((pair, index) => (
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
      {buyPairs[selectedPair] && <Calculator data={buyPairs[selectedPair]} />}
      </div>

      <Separator className="my-4" />
      
      {buyPairs[selectedPair] &&
        <Alert className="bg-red-100" variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Importante!!</AlertTitle>
        <AlertDescription>
          Comprar USDT por más de {buyPairs[selectedPair].rateInfo.buy_price_limit} produce perdidas 
        </AlertDescription>
      </Alert>}

      <Separator className="my-4" />

      {buyRequests &&  
      <RequestList 
        data={buyRequests} 
        titleSection="Peticiones de cambios"
        onSubmit={onSubmit}
      />}

    </section>
  )
}
