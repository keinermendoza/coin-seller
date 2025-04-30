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
  import TitleSection from "@/components/TitleSection"

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
const neomorphisem = {
    "boxShadow": "inset -5px -5px 9px rgba(255,255,255,0.45), inset 5px 5px 9px rgba(94,104,121,0.3)"
  }

function RequestResolved({exchange, side, fiatCode}) {
  const sideWordAcusativePast = side === "S" ? "Vendiste" : "Compraste"  
  return (
    <div style={neomorphisem} className="text-lg w-full p-4 rounded-xl text-black/60 bg-gray-100">
      <div className="flex gap-4 mb-2">
        <p>{sideWordAcusativePast} {parseFloat(exchange.amount)} USDT a {parseFloat(exchange.price)} {fiatCode} </p>
      </div>
      <p className="text-sm">Operación registrada el {timeFormat(exchange.created)}</p>
    </div>
  )
}


function RequestDialogue({pair, onSubmit, tradeRequestId}) {
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
                    <FormRegisterOperation onSubmit={onSubmit} 
                    price={price} 
                    amount={amount} 
                    extraParamsSubmit={{
                      trade_request_id: tradeRequestId,
                      side_operation: pair.side,
                    }}
                    />
                </div>
            </DialogDescription>
            </DialogHeader>
        </DialogContent>
    </Dialog>
    )

}

function RequestItem({data}) {
    const {getFiatPair} = useTradeRequest()
    const pair = getFiatPair(data.pair)
  return (
    <li>
        <Card>
        <CardHeader>
            <CardTitle>Cambio de {pair.currencyFrom} a {pair.currencyTo}</CardTitle>
        </CardHeader>
        <CardContent>
            <p>{data.exchange_buy.amount}</p>
            <p>{data.exchange_buy.price}</p>
            <p className="mb-1 text-sm text-black/60">{timeFormat(data.exchange_buy.created)}</p>
            <Badge>{data.status_text}</Badge>
        </CardContent>
        <CardFooter>
            formato
        </CardFooter>
        </Card>

    </li>
  )
}


export default function RequestCompletedList({data}) {
  return (
    <ul className="space-y-4">

        {data.map((item) => (
            <RequestItem key={item.id} data={item} />
        ))}
    </ul>
  )
}

