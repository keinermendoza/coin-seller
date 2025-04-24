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

import { useChanges } from "@/contexts/ChangeContext"
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
  const {changes:data} = useChanges()

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
    <div>
      <div className="text-slate-900 text-center my-4">
        <p className="text-xl font-medium">Calculadora de Cambios</p>
        <p className=" text-3xl font-bold">R$ <span className="font-medium text-xl">a</span> Bs</p>
      </div>
      {data?.sell && <Calculator data={data.sell} />}

      <Separator className="my-4" />

      {data?.sell.sell_price_limit &&
        <Alert className="bg-red-100" variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Importante!!</AlertTitle>
        <AlertDescription>
          Vender USDT por menos de {data.sell.sell_price_limit} produce perdidas 
        </AlertDescription>
      </Alert>}
      
      <Separator className="my-4" />


      <div className="text-slate-900 text-center my-4">
        <p className="text-xl font-medium">Registro de Ventas en Binance</p>
      </div>
      <FormRegisterOperation onSubmit={onSubmit} price={price} amount={amount} />
      
    </div>
    
  )
}
