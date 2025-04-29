import { useState } from "react"

import Calculator from "@/components/Calculator"
import { FormRegisterOperation } from "@/components/FormRegisterOperation"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { AlertCircle } from "lucide-react"
import { Link } from "react-router"
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

// const data = {
//   currencyTo: {
//       image: "",
//       name: "Bolivar",
//       symbol: "Bs",
//       code: "VES"
//   },
//   currencyFrom: {
//       image: "",
//       name: "Real",
//       symbol: "R$",
//       code: "BRL"
//   },
//   rate: 15.670,
//   sell_price_limit: 98.000, 
//   created: "14/04/25 13:45"
// }

const price = {
  label: "Precio de vender 1 USDT",
  placeholder: "Ejemplo: 95670",
  helpText: "Esto es para registrar el precio al que vendió los USDT en binance.",
}

const amount = {
  label: "Cantidad de USDT vendidos",
  placeholder: "Ejemplo: 10",
  helpText: "Esto es para registrar la cantidad de USDT que le compraron en binance",
}

export default function Sell() {
  const [selectedPair, setSelectedPair] = useState(0)
  const {sellPairs} = useChanges()
  const {sellRequests} = useTradeRequest()
  

  function onSubmit(data) {
    toast(
        "You submitted the following values:", {
        description: JSON.stringify(data, null, 2),
        action: {
            label: "cerrar",
            onClick: () => console.log("Undo"),
        },
    })
  }
  
  return (
    <section>
      {sellRequests &&  <RequestList data={sellRequests} titleSection="Peticiones de cambios" />}

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
            <p>No estás suscrito a ningun cambio como vendedor</p>
            <p>Para suscribirte a un cambio ve a <Link to="#suscription">suscribirse</Link></p>
          </div>
        )  
      }
        

      </div>


      {sellPairs[selectedPair] && <Calculator data={sellPairs[selectedPair]} />}
      


      
      {/* <Separator className="my-4" /> */}


      {/* <div className="text-slate-900 text-center my-4">
        <p className="text-xl font-medium">Registro de Ventas en Binance</p>
      </div>
      <FormRegisterOperation onSubmit={onSubmit} price={price} amount={amount} /> */}
      
    </section>
    
  )
}
