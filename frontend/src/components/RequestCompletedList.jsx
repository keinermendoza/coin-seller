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

  import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
  } from "@/components/ui/accordion"
  
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


// esults": [
  // at_suscriptions": [
  //   {
  //       "id": 1,
  //       "side": "S",
  //       "currencyFrom": "VES",
  //       "currencyTo": "BRL",
  //       "currencyFromSymbol": "Bs"
  //   },


//   {
//       "id": 1,
//       "status_text": "Dinero entregado al destinatario",
//       "exchange_buy": {
//           "id": 1,
//           "amount": "20.010",
//           "price": "5.980",
//           "registeredBy": username a,
//           "created": "2025-05-01T22:06:38.907641-04:00"
//       },
//       "exchange_sell": {
//           "id": 2,
//           "amount": "18.500",
//           "price": "109.700",
//           "registered_by": username b,
//           "created": "2025-05-01T22:09:37.162068-04:00"
//       },
//       "created": "2025-05-01T21:56:37.172379-04:00",
//       "edited": "2025-05-01T22:09:37.208491-04:00",
//       "requested_amount": "120.000",
//       "rate": "18.344",
//       "result": "-205.680",
//       "status": 3,
//       "message": "recibe: Juan Carlos CI 29450134 Mercantil 041454637865.Envia Pedro Castillo CI 14566791",
//       "created_by": 1,
//       "pair": 2
//   },

function statusColor (value) {
  const extraClass = ' font-semibold';
  return value > 0 ? 'text-green-800' + extraClass :  'text-red-600' + extraClass
}

function RequestItem({data}) {
    const {getFiatPair} = useTradeRequest()
    const pair = getFiatPair(data.pair)
    const bennefitMargin = parseFloat(data.rate - data.client_offered_rate).toFixed(3);
    return (
    <li>
        <Card>
        <CardHeader>
          <CardTitle>Cambio de {pair.currencyFrom} a {pair.currencyTo}</CardTitle>
          <CardDescription>Enviados {pair.currencyFromSymbol} {data.requested_amount}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-2">
            <p>Tasa pagada al cliente {data.client_offered_rate} {pair.currencyToSymbol}/{pair.currencyFromSymbol}</p>
            <p>Tasa cobrada en binance {data.rate} {pair.currencyToSymbol}/{pair.currencyFromSymbol}</p>
            <p>
              Con un margen de 
              <span className={statusColor(bennefitMargin)}> {bennefitMargin} {pair.currencyToSymbol}/{pair.currencyFromSymbol} </span>
              tuvimos una ganancia estimada de 
              <span className={statusColor(data.result)}> {pair.currencyToSymbol} {data.result} </span>
            </p>
          </div>

            <p className="mb-1 text-sm text-black/60">{timeFormat(data.edited)}</p>
            <Badge>{data.status_text}</Badge>
        </CardContent>
        <CardFooter>
          <Accordion className="w-full" type="multiple" >
            <AccordionItem  value="general">
              <AccordionTrigger className="cursor-pointer" >Mensaje de la transacción</AccordionTrigger>
              <AccordionContent>
                {data.message}
              </AccordionContent>
            </AccordionItem>

            <AccordionItem  value="buyer">
              <AccordionTrigger className="cursor-pointer" >Información de {pair.currencyFrom} a USDT</AccordionTrigger>
              <AccordionContent>
                <p className="mb-2">
                <strong>{data.exchange_buy.registeredBy}</strong> registró la compra de {parseFloat(data.exchange_buy.amount)} USDT a {parseFloat(data.exchange_buy.price)} {pair.currencyFromSymbol} 
                </p>
                <p className="italic text-sm text-black/60">Registrado el {timeFormat(data.exchange_buy.created)}</p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem   value="seller">
              <AccordionTrigger  className="cursor-pointer">Información de USDT a {pair.currencyTo}</AccordionTrigger>
              <AccordionContent>
              <p className="mb-2">
                <strong>{data.exchange_sell.registeredBy}</strong> registró la venta de {parseFloat(data.exchange_sell.amount)} USDT a {parseFloat(data.exchange_sell.price)} {pair.currencyToSymbol}
                </p>
                <p className="italic text-sm text-black/60">Registrado el {timeFormat(data.exchange_sell.created)}</p>
              </AccordionContent>
            </AccordionItem>
          
          </Accordion>

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

