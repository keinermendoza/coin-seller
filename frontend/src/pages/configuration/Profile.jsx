import { Button } from "@/components/ui/button"
import { getCookie } from "@/lib/getCookie";
import TitleSection from "@/components/TitleSection";
export default function Profile() {
  const cookie = getCookie('csrftoken');
  return (
    <section>
      <TitleSection title="Perfil" subtitle="Aqui puedes administrar las configuraciones relacionadas a tu cuenta" />
      <p className="text-sm my-2"> actualmente la unica opción habilitada es <em>Cerrar Sesion</em> para salir.</p>
      <Button form="close-session" className="cursor-pointer" variant="destructive">Cerrar Sesion</Button>
      <form id="close-session" action="/accounts/logout/" >
        <input type="hidden" value={cookie} />
      </form>
    </section>
  )
}
