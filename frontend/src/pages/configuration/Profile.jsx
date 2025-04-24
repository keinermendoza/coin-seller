import { Button } from "@/components/ui/button"
import { getCookie } from "@/lib/getCookie";

export default function Profile() {
  const cookie = getCookie('csrftoken');
  return (
    <section>
      <h1 className="text-3xl font-medium">Perfil</h1>
      <p className="text-xl">Sesion</p>
      <Button form="close-session" className="cursor-pointer" variant="destructive">Cerrar Sesion</Button>
      <form id="close-session" action="/accounts/logout/" >
        <input type="hidden" value={cookie} />
      </form>
    </section>
  )
}
