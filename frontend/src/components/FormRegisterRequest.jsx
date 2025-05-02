import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import {useState} from "react"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

import { Textarea } from "@/components/ui/textarea"


import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"


// const FormSchema = z.object({
//     pair: z
//       .string()
//       .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
//         message: "Seleccione un par valido",
//       })
//       .transform((val) => Number(val)),
//     requested_amount: z
//       .string()
//       .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
//         message: "Debe ser un número válido mayor a 0",
//       })
//       .transform((val) => Number(val)),
//   });

export function FormRegisterRequest({pairs, onSubmit}) {
    const [selectedPair, setSelectedPair] = useState(pairs[0]);
  
    const form = useForm({
    defaultValues: {
        pair: pairs[0].id,
        requested_amount: '',
        messsage: '',
      },
  })

  

  return (
    <div className="w-full max-w-5xl mx-auto bg-gray-300 rounded-xl p-4 ">

        <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
            control={form.control}
            name="pair"
            render={({ field }) => (
                <FormItem>
                <FormLabel>Selecciona el cambio a usar</FormLabel>
                <FormControl>
                    <Select  
                    onValueChange={(value) => {
                        field.onChange(value);
                        const selected = pairs.find((p) => p.id == value);
                        setSelectedPair(selected);
                      }}
                    value={field.value} 
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Seleccionar cambio" />
                        </SelectTrigger>
                        <SelectContent>
                            {pairs.map((pair) => (
                            <SelectItem key={pair.id} value={pair.id}> {pair.currencyFrom} a {pair.currencyTo}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </FormControl>
                <FormDescription className="text-start text-[0.75rem] italic">
                    Cambio que el cliente pidió realizar
                </FormDescription>
                <FormMessage />
                </FormItem>
            )}
            />
             <FormField
            control={form.control}
            name="requested_amount"
            render={({ field }) => (
                <FormItem>
                <FormLabel htmlFor="amount">Valor enviado</FormLabel>
                <FormControl>
                    <label className="flex items-center">
                        <span className="px-3 py-2 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md text-sm">
                            {selectedPair && selectedPair.currencyFromSymbol}
                        </span>
                        <Input id="amount" className="bg-white rounded-l-none "  {...field} />
                    </label>
                </FormControl>
                <FormDescription className="text-start text-[0.75rem] italic">
                    Valor que el cliente transferirá a nuestras cuentas
                </FormDescription>
                <FormMessage />
                </FormItem>
            )}
            />
             <FormField
            control={form.control}
            name="message"
            render={({ field }) => (
                <FormItem>
                <FormLabel htmlFor="message">Datos del destinatario</FormLabel>
                <FormControl>
                    <Textarea id="message" className="bg-white"  {...field} placeholder="Ejemplo: Recibe Pepe Babilonia, CI 998877665 Numero de cuenta: 123456789 Banco Banesco ... Envia juan mesopotamia CI 112233456"/>
                </FormControl>
                <FormDescription className="text-start text-[0.75rem] italic">
                    Datos de la persona que recibira la transferencia, puedes incluir tambien informacion de la persona que envia esta operacion
                </FormDescription>
                <FormMessage />
                </FormItem>
            )}
            />
            <div className="flex justify-end">
                <Button className="cursor-pointer" type="submit">Registrar</Button>
            </div>
        </form>
        </Form>
    </div>

  )
}
