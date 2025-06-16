import { Button } from "@/components/ui/button"
import TitleSection from "@/components/TitleSection";
import { useEffect, useRef, useState } from "react";
import useFetch from "@/hooks/useFetch";
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

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { toast } from "sonner"
import timeFormat from "@/lib/timeFormat";
import axios from "@/lib/axios"

export default function Profile() {
  const {data: pairs} = useFetch("/api/fiat-exchange-pairs")
  const [currentFiatPairMarketData, setCurrentFiatPairMarketData] = useState(null)
  const [selectedSlug, setSelectedSlug] = useState(null)
  const [currentRate, setCurrentRate] = useState(null)
  const [loadingNewMarketConditions, setLoadingNewMarketConditions] = useState(false)
  
  useEffect(() => {
    if(currentFiatPairMarketData) {
      setCurrentRate(currentFiatPairMarketData.current_rate)
    }
  },[currentFiatPairMarketData])

  const newPriceRef = useRef()
  
  const fetchFiatPairMarketData = async (slug) => {
    setSelectedSlug(slug)
    const resp = await fetch("/api/fiat-exchange-pairs/" + slug)
    const data = await resp.json()
    setCurrentFiatPairMarketData(data)
  }

  const copySugestedPrice = () => {
    newPriceRef.current.value = currentFiatPairMarketData.sugested_rate
  } 

  const storeNewRate = async (e) => {
    e.preventDefault()
    if (!selectedSlug) return;

    const newRateForm = e.target; 
    const formData = new FormData(newRateForm);
    const resp = await axios.post("/api/fiat-exchange-pairs/" + selectedSlug, formData)
    if (resp.status === 201) {
      setCurrentRate(formData.get('newrate'))
      toast(
          "Tasa actualizada con exito", {
          action: {
              label: "cerrar",
              onClick: () => console.log("Undo"),
          },
      })
      console.log(resp.data);
    }
  }

  const refetchMarketConditions = async () => {
    setLoadingNewMarketConditions(true)
    const resp = await axios.post("/api/refetch-currency-exchange-conditions");
    
    if (resp.status === 200) {
      toast(
        "Nuevo registro de condiciones de Mercado creado", {
        action: {
            label: "cerrar",
            onClick: () => console.log("Undo"),
        },
      })

      setLoadingNewMarketConditions(false)

      if (selectedSlug) {
        fetchFiatPairMarketData(selectedSlug)
      }
    }
  }
  
  return (
    <section className="flex flex-col items-center">
      <TitleSection title="Actualizar Cambios" subtitle="Usa estas opciones para actualizar el valor de los tipos de cambio" />

      <Dialog>
              <Button className="my-2" asChild>
                  <DialogTrigger>Consultar Tazas de Referencia</DialogTrigger>
              </Button>
              <DialogContent>
                  <DialogHeader>
                  <DialogTitle className="mb-2">
                    Consultar Binance
                  </DialogTitle>
                  <DialogDescription >
                    <p>
                    Realizar una nueva consulta del estado del mercado utiliza espacio en la base de datos. Para continuar precione el siguiente botón 

                    </p>
                  <Button 
                    className="my-2 cursor-pointer hover:scale-105" 
                    onClick={refetchMarketConditions}
                    disabled={loadingNewMarketConditions}
                    >
                      {loadingNewMarketConditions ? 'Por favor espere...' : 'Consultar Mercado Nuevamente'}
                    </Button>
                     
                  </DialogDescription>
                  </DialogHeader>
              </DialogContent>
          </Dialog>

      
      
     

      {pairs &&
      <div className="flex gap-3 justify-evenly mb-4">
        {pairs.map(pair => (
          <Button key={pair.id} 
          onClick={() => fetchFiatPairMarketData(pair.slug)}
          className={`cursor-pointer border-2 ${selectedSlug === pair.slug ? 'bg-purple-400 hover:bg-purple-300': 'bg-white'}`}
          variant="secondary">{pair.currency_from} / {pair.currency_to} </Button>
        ))}
      </div>
      }

      {currentFiatPairMarketData &&
          <Card className="w-full max-w-sm ">
            <CardHeader>
              <CardTitle>Cambio de {currentFiatPairMarketData.currency_from} a {currentFiatPairMarketData.currency_to}</CardTitle>
              <CardDescription>
                <p>Establece el precio para el tipo de cambio</p>
                <p>Sugerencia con base en margen deseado de {currentFiatPairMarketData.optimum_margin_expected}%</p>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-evenly flex-wrap gap-3">
                <Badge className="text-base" variant="secondary">Mercado {parseFloat(currentFiatPairMarketData.market_rate).toFixed(4)}</Badge>
                <Badge 
                  onClick={copySugestedPrice} 
                  className="border-solid border-2 border-black text-base cursor-pointer" 
                  variant="secondary">Sugerencia {currentFiatPairMarketData.sugested_rate}</Badge>

                <div className="text-center text-[0.70rem] space-y-1 italic text-black/60">
                  <p className="text-[0.765rem]">Sugerencia construida con consultas de fecha</p>
                  <p>Compra de {currentFiatPairMarketData.currency_from}: {timeFormat(currentFiatPairMarketData.market_time.buy_time)}</p>
                  <p>Venta de {currentFiatPairMarketData.currency_to}: {timeFormat(currentFiatPairMarketData.market_time.sell_time)}</p>
                </div>
              </div>

              <div>
                <Badge variant="outline" className="flex-col p-2 text-lg w-full">
                  <p className="text-sm text-black/60">Tasa Actual</p>
                  <p>{currentRate} {currentFiatPairMarketData.currency_to} por {currentFiatPairMarketData.currency_from}</p>
                </Badge> 

               
              </div>

              <form onSubmit={storeNewRate} id="update-fiat-exchange-pair">
                <div className="flex flex-col gap-6">
                  <div className="grid gap-2">
                    <Label htmlFor="newrate">Nueva taza</Label>
                    <Input
                      id="newrate"
                      name="newrate"
                      ref={newPriceRef}
                      type="number"
                      required
                      min="0.000000001"
                      step="0.000000001"

                    />
                  </div>

                </div>
              </form>
            </CardContent>
            <CardFooter className="flex-col gap-2">
              <Button form="update-fiat-exchange-pair" type="submit" className="w-full">
                Actualizar
              </Button>
            </CardFooter>
          </Card>
      }
      
{/* <form id="close-session" action="/accounts/logout/" >
      <Button form="close-session" className="cursor-pointer" variant="destructive">Cerrar Sesion</Button>
      </form> */}
    </section>
  )
}