import { ChangeRate, Profile, SwitchAlarms } from "@/pages/configuration";
import { Tabs, TabsList, TabsTrigger, TabsContent  } from "@/components/ui/tabs";

export default function LayoutConfiguration() {
  return (
    <>
    <h1 className="text-3xl font-medium mb-4">Configuraciones</h1>
    <Tabs defaultValue="update-changes" className="w-[400px]">
        <TabsList>
            <TabsTrigger value="update-changes">Actualizar Cambios</TabsTrigger>
            <TabsTrigger value="profile">Perfil</TabsTrigger>
            <TabsTrigger value="actions">Acciones</TabsTrigger>

        </TabsList>
        <TabsContent value="update-changes">
          <ChangeRate/>
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
