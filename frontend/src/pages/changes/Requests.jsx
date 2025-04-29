import { useChanges } from "@/contexts/ChangeContext"
import timeFormat from "@/lib/timeFormat"
import { Button } from "@/components/ui/button"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { Info } from "lucide-react"
import { Separator } from "@/components/ui/separator"
import axios from "@/lib/axios";
import { FormRegisterRequest } from "@/components/FormRegisterRequest"
import { toast } from "sonner"
import { useTradeRequest } from "@/contexts/TradeRequestContext"

export default function Requests() {
  const {fiatSuscriptions, insertNewTradeRequest} = useTradeRequest()

  const displaySuccess = () => {
      toast(
        "Peticion de cambio registrada", {
        action: {
            label: "cerrar",
            onClick: () => console.log("Undo"),
        },
    })
  }

  async function onSubmit(data) {
    const resp = await axios.post('/api/trade-requests', data)
    if (resp.status === 201) {
      displaySuccess();
      insertNewTradeRequest(resp.data)
      console.log(resp.data)
    }
  }

  // const fiat_pairs = [
  //       {
  //           "id": 2,
  //           "currencyFrom": "VES",
  //           "currencyTo": "BRL"
  //       }
  //   ]

  return (
    <section className="text-slate-900 text-center mt-4 space-y-4">
      <FormRegisterRequest onSubmit={onSubmit} pairs={fiatSuscriptions} />
    </section>
  )
}
