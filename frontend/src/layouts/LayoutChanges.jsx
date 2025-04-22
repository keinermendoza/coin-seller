import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sell, Buy } from "@/pages/changes"
export default function LayoutChanges() {
  return (
    <>
      <h1 className="text-3xl font-medium mb-4">Cambios</h1>

      <Tabs defaultValue="sell" >
      <TabsList>
          <TabsTrigger value="sell">Vender</TabsTrigger>
          <TabsTrigger value="buy">Comprar</TabsTrigger>
      </TabsList>
      <TabsContent value="sell">
          <Sell />
      </TabsContent>
      <TabsContent value="buy">
          <Buy />
      </TabsContent>
      </Tabs>
    </>
        
  )
}
