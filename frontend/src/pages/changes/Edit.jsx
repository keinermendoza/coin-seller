import { useParams, Link, Navigate, useNavigate } from "react-router"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import { toast } from "sonner"

import {buttonVariants} from "@/components/ui/button"

import useFetch from "@/hooks/useFetch"
import axios from "@/lib/axios"
import { useTradeRequest } from "@/contexts/TradeRequestContext"
import { FormRegisterOperation } from "@/components/FormRegisterOperation"

function ErrorPage() {
    return (
        <section className="grid place-content-center">
        <Card>
            <CardHeader>
                <CardTitle>Error</CardTitle>
                <CardDescription>Algo salio mal con la petición</CardDescription>
            </CardHeader>
            <CardContent>
                Ah ocurrido un error al intentar obtener los datos del cambio que seleccionaste.
                Intenta recargar la página, si el error persiste por favor contacte con soporte técnico
            </CardContent>
            <CardFooter>
                <Link className={buttonVariants({ variant: "link" })} to="../">Volver a la sección de Cambios</Link>
            </CardFooter>
            </Card>
        </section>
    )
}

export default function Edit() {
    const {id} = useParams()
    const navigate = useNavigate()
    const endpoint = "/api/trade-requests/update-exchange/" + id
    const {data, error} = useFetch(endpoint)
    const {refetchTradeRequests} = useTradeRequest()



  async function onSubmit(formData, trade_request_id=null, side_operation=null) {
    const body = {
      ...formData
    }

    const resp = await axios.patch(endpoint, body)
    if (resp.status === 200) {
      toast(
          "You submitted the following values:", {
          description: JSON.stringify(formData, null, 2),
          action: {
              label: "cerrar",
              onClick: () => console.log("Undo"),
          },
      })
      refetchTradeRequests()
      navigate("../")
    }
    console.log(resp.data)

  }
    
    if (error) {
       return (
        <ErrorPage />
       ) 
    }

    const price = {
        label: `Precio expresado en Fiat de 1 USDT`,
        placeholder: "Ejemplo: 100",
        helpText: `El precio expresado en Fiat al que se canjeo cada USDT en binance.`,
        value: data?.price,
    }
      
      const amount = {
        label: `Cantidad de USDT canjeados`,
        placeholder: "Ejemplo: 100",
        helpText: `Cuantos USDT canjeaste en binance`,
        value: data?.amount,
      }

    return (
    <section className="grid place-content-center ">
        <Card>
            
            <CardHeader>
                <CardTitle>Editar registro</CardTitle>
                <CardDescription>Estas a punto de editar el registro de lo que hiciste en binance para esta operacion</CardDescription>
            </CardHeader>
            <CardContent>
                {data && 
                <FormRegisterOperation 
                    onSubmit={onSubmit} 
                    price={price} 
                    amount={amount} 
                    />
                }
            </CardContent>
            <CardFooter>
                <p>Si entraste aqui por error puedes volver atras sin problemas</p>
                <Link className={buttonVariants({ variant: "link" })} to="../">Volver a la sección de Cambios</Link>
            </CardFooter>
        </Card>

    </section>
  )
}
