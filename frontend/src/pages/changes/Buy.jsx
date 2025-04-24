import Calculator from "@/components/Calculator"
import { FormRegisterOperation } from "@/components/FormRegisterOperation"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { AlertCircle } from "lucide-react"
import useFetch from "@/hooks/useFetch"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"


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
  const {data} = useFetch('/api/buy')
  
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
      <div className="text-slate-900 text-center my-4">
        <p className="text-xl font-medium">Calculadora de Cambios</p>
        <p className=" text-3xl font-bold">Bs <span className="font-medium text-xl">a</span> R$</p>
      </div>
      {data && <Calculator data={data} />}

      <Separator className="my-4" />
      
      {data?.buy_price_limit &&
        <Alert className="bg-red-100" variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Importante!!</AlertTitle>
        <AlertDescription>
          Comprar USDT por más de {data.buy_price_limit} produce perdidas 
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
