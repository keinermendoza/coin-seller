import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sell, Buy, Update } from "@/pages/changes"
import { ChangesProvider } from "@/contexts/ChangeContext"
export default function LayoutChanges() {
  return (
    <ChangesProvider>
      <h1 className="text-3xl font-medium mb-4">Cambios</h1>

      <Tabs defaultValue="sell" >
      <TabsList>
          <TabsTrigger value="sell">Vender</TabsTrigger>
          <TabsTrigger value="buy">Comprar</TabsTrigger>
          <TabsTrigger value="update">Actualizar</TabsTrigger>

      </TabsList>
      <TabsContent value="sell">
          <Sell />
      </TabsContent>
      <TabsContent value="buy">
          <Buy />
      </TabsContent>
      <TabsContent value="update">
          <Update />
      </TabsContent>
      </Tabs>
    </ChangesProvider>
        
  )
}
