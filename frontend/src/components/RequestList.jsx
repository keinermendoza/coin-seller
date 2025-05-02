import { Link } from "react-router"

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
  import { Button, buttonVariants } from "@/components/ui/button"
import { FormRegisterOperation } from "./FormRegisterOperation"
import timeFormat from "@/lib/timeFormat"
  import { useTradeRequest } from "@/contexts/TradeRequestContext"
  import TitleSection from "@/components/TitleSection"

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
      <div className="mt-2 flex justify-end items-center">
        <Link className={buttonVariants({variant:  "destructive", size: "sm" })} 
        to={"./" + exchange.id}
        >Editar</Link>
      </div>
    </div>
  )
}


function RequestDialogue({pair, onSubmit, tradeRequestId}) {
    const sideWord =  pair.side === "S" ? "VENTA" : "COMPRA";
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
            <DialogTitle className="mb-2"><span className="font-normal">Usa este formulario para registrar tu</span> {sideWord}</DialogTitle>
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

function RequestItem({data, onSubmit}) {
    const {getFiatPair} = useTradeRequest()
    const pair = getFiatPair(data.pair)

 

    const actionSide = pair.side === "S" ? "exchange_sell" : "exchange_buy";
    const fiatCode =  pair.side === "S" ? pair.currencyTo : pair.currencyFrom;
  return (
    <li>
        <Card>
        <CardHeader>
            <CardTitle>Cambio de {pair.currencyFrom} a {pair.currencyTo}</CardTitle>
            <CardDescription>Cliente desea transferir <b className="text-slate-800">{parseFloat(data.requested_amount)} {pair.currencyFrom} </b></CardDescription>
        </CardHeader>
        <CardContent>
            {data.message && <>
            <p className="text-lg">Inforamcion del destinatario</p>
            <p className="mb-4">{data.message}</p>
            </>}

            <p className="mb-1 text-sm text-black/60">Creado el {timeFormat(data.created)}</p>
            <Badge>{data.status_text}</Badge>
        </CardContent>
        <CardFooter>
            {data[actionSide] ?
            (
              <RequestResolved exchange={data[actionSide]} side={pair.side} fiatCode={fiatCode} />
            ) : (
            <RequestDialogue pair={pair} onSubmit={onSubmit} tradeRequestId={data.id} />
            )}
        </CardFooter>
        </Card>

    </li>
  )
}


export default function RequestList({data, titleSection, onSubmit}) {
  return (
    <ul className="space-y-4">
      <TitleSection 
        title={titleSection}
        subtitle="los clientes aguardan por que resolvamos las siguientes operaciones"  
      />

        {data.map((item) => (
            <RequestItem key={item.id} data={item} onSubmit={onSubmit} />
        ))}
    </ul>
  )
}

