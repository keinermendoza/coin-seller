import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"

  import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog"
  
  import { Badge } from "@/components/ui/badge"
  import { Button } from "@/components/ui/button"
import { FormRegisterOperation } from "./FormRegisterOperation"
import timeFormat from "@/lib/timeFormat"
  import { useTradeRequest } from "@/contexts/TradeRequestContext"
// "id": 7,
// "created": "2025-04-27T22:20:16.082596-04:00",
// "edited": "2025-04-27T22:20:16.082635-04:00",
// "requested_amount": "10.000",
// "rate": null,
// "result": null,
// "status": 1,
// "created_by": 1,
// "pair": 2,
// "exchange_buy": null,
// "exchange_sell": null


function RequestDialogue({data, pair, onSubmit}) {
    const sideWord =  pair.side === "S" ? "venta" : "compra";
    const sideWordPast =  pair.side === "S" ? "vendió" : "compró";
    const sideWordVerb =  pair.side === "S" ? "vender" : "comprar";
    const sideWordPastPerfect =  pair.side === "S" ? "vendidos" : "comprados";

    const fiatCode =  pair.side === "S" ? pair.currencyTo : pair.currencyFrom;

    const price = {
        label: `Precio de ${sideWordVerb} 1 USDT`,
        placeholder: "Ejemplo: 100",
        helpText: `El precio en ${fiatCode} al que ${sideWordPast} cada USDT en binance.`,
      }
      
      const amount = {
        label: `Cantidad de USDT ${sideWordPastPerfect}`,
        placeholder: "Ejemplo: 100",
        helpText: `Cuantos USDT ${sideWordPast} en binance`,
      }
    
    return (

    <Dialog>
        <Button className="w-full bg-gradient-to-b from-blue-500 to-cyan-600 cursor-pointer opacity-90 hover:opacity-100" asChild>
            <DialogTrigger>Resolver</DialogTrigger>
        </Button>
        <DialogContent>
            <DialogHeader>
            <DialogTitle className="mb-2">Usa este formulario para registrar tu {sideWord}</DialogTitle>
            <DialogDescription asChild>
                <div>
                    <FormRegisterOperation onSubmit={onSubmit} price={price} amount={amount} />
                </div>
            </DialogDescription>
            </DialogHeader>
        </DialogContent>
    </Dialog>
    )

}

function RequestItem({data, onSubmit}) {
    const {getFiatPair} = useTradeRequest()
    const pair = getFiatPair(data.pair)
  return (
    <li>
        <Card>
        <CardHeader>
            <CardTitle>Cambio de {pair.currencyFrom} a {pair.currencyTo}</CardTitle>
            <CardDescription>Cliente desea transferir {parseFloat(data.requested_amount)} {pair.currencyFrom} </CardDescription>
        </CardHeader>
        <CardContent>
            <p className="mb-1 text-sm text-black/60">Creado el {timeFormat(data.created)}</p>
            <Badge>{data.status}</Badge>
        </CardContent>
        <CardFooter>
            <RequestDialogue data={data} pair={pair} onSubmit={onSubmit} />
        </CardFooter>
        </Card>

    </li>
  )
}


export default function RequestList({data, titleSection, onSubmit}) {
  return (
    <ul className="space-y-4">
        <div className="space-y-2 text-center">
            <p className="text-xl font-medium">{titleSection}</p>
            <p className="italic">los clientes aguardan por que resolvamos las siguientes operaciones</p>
        </div>

        {data.map((item) => (
            <RequestItem key={item.id} data={item} onSubmi={onSubmit}/>
        ))}
    </ul>
  )
}

