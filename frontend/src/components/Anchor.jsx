import { Card } from "@/components/ui/card"
import { Link as LinkIcon } from "lucide-react"

export default function Anchor({children, to}) {
      return (
        <Card className="p-0 overflow-hidden" >
          <a target="_blank" 
            className="transition-colors duration-200 hover:bg-amber-200 flex items-center  justify-between gap-4 py-4 px-6 w-full" 
            href={to}>
            <span>{children}</span>
            <LinkIcon />
          </a>
        </Card>
      )
}
