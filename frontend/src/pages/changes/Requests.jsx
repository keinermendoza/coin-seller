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
    }
  }

  return (
    <section className="text-slate-900 text-center mt-4 space-y-4">
      {fiatSuscriptions?.length > 0 ? (
        <FormRegisterRequest onSubmit={onSubmit} pairs={fiatSuscriptions} />
      ) : (
        <p className="text-4xl">Cargando...</p>
      )}
    </section>
  )
}
