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
import React from "react"

const price = {
  label: "Precio de comprar 1 USDT",
  placeholder: "Ejemplo: 98700",
  helpText: "Esto es para registrar el precio que usted pagó por cada USDT.",
}

const amount = {
  label: "Cantidad de USDT comprados",
  placeholder: "Ejemplo: 10",
  helpText: "Esto es para registrar la cantidad de USDT usted compró",
}


export default function Buy() {
  const [selectedPair, setSelectedPair] = useState(0)
  const {buyPairs} = useChanges()
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
      <div className="text-slate-900 flex flex-col items-center justify-center text-center gap-4 my-4">
        <p className="text-xl font-medium">Calculadora de Cambios</p>
        {buyPairs.length > 0 ? (
        <Select onValueChange={(value) => setSelectedPair(value)} defaultValue={selectedPair}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar cambio" />
          </SelectTrigger>
          <SelectContent>
            {buyPairs.map((pair, index) => (
              <SelectItem key={index} value={index}>{pair.currencyFrom.code} a {pair.currencyTo.code}</SelectItem>
            ))}
          </SelectContent>
        </Select>)
        : (
          <div className="text-sm">
            <p>No estás suscrito a ningun cambio como comprador</p>
            <p>Para suscribirte a un cambio ve a <Link to="#suscription">suscribirse</Link></p>
          </div>
        )  
      }
        

      </div>

      {buyPairs[selectedPair] && <Calculator data={buyPairs[selectedPair]} />}

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

      <div className="text-slate-900 text-center my-4">
        <p className="text-xl font-medium">Registro de Compras en Binance</p>
      </div>
      <FormRegisterOperation onSubmit={onSubmit} price={price} amount={amount}  />
    </section>
  )
}
