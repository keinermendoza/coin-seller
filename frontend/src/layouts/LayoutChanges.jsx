import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sell, Buy, Requests, History } from "@/pages/changes"
import { ChangesProvider } from "@/contexts/ChangeContext"
export default function LayoutChanges() {
  return (
    <ChangesProvider>
      <h1 className="text-3xl font-medium mb-4">Cambios</h1>

      <Tabs defaultValue="sell" >
        <TabsList>
            <TabsTrigger value="sell">Vender</TabsTrigger>
            <TabsTrigger value="buy">Comprar</TabsTrigger>
            <TabsTrigger value="requests">Nuevos</TabsTrigger>
            <TabsTrigger value="history">Historial</TabsTrigger>


        </TabsList>
        <TabsContent value="sell">
            <Sell />
        </TabsContent>
        <TabsContent value="buy">
            <Buy />
        </TabsContent>
        <TabsContent value="requests">
            <Requests />
        </TabsContent>
        <TabsContent value="history">
            <History />
        </TabsContent>
      </Tabs>
    </ChangesProvider>
        
  )
}
