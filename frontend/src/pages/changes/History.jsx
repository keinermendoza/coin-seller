import TitleSection from "@/components/TitleSection"
import RequestCompletedList from "@/components/RequestCompletedList"
import { useTradeRequest } from "@/contexts/TradeRequestContext"

export default function History() {
  const {historyRequests} = useTradeRequest()
  
  return (
    <section>

    <TitleSection
      title="Historial de Cambios"
      subtitle="Aqui puedes ver todas las operaciones que hemos completado o cancelado"
      />

    <RequestCompletedList data={historyRequests}/>
    </section>
   
  )
}
