import { ChangeRate, Profile, SwitchAlarms } from "@/pages/configuration";
import { History} from "@/pages/changes";

import { Tabs, TabsList, TabsTrigger, TabsContent  } from "@/components/ui/tabs";


export default function LayoutConfiguration() {
  return (
    <>
    <h1 className="text-3xl font-medium mb-4">Configuraciones</h1>
    <Tabs defaultValue="history" className="">
        <TabsList>
            <TabsTrigger value="history">Historial</TabsTrigger>
            <TabsTrigger value="profile">Perfil</TabsTrigger>
            <TabsTrigger value="actions">Acciones</TabsTrigger>

        </TabsList>
        <TabsContent value="history">
          <History />
        </TabsContent>

        <TabsContent value="profile">
          <Profile />
        </TabsContent>
        
        <TabsContent value="actions">
          <SwitchAlarms/>
        </TabsContent>
        

    </Tabs>

    </>

  )
}
