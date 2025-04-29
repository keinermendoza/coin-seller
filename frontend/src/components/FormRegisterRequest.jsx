import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
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
  const form = useForm({
    defaultValues: {
        pair: pairs[0].id,
        requested_amount: '',
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
                    <Select  onValueChange={field.onChange} value={field.value} >
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
                <FormLabel>Valor enviado</FormLabel>
                <FormControl>
                    <Input className="bg-white"  {...field} />
                </FormControl>
                <FormDescription className="text-start text-[0.75rem] italic">
                    Valor que el cliente transferirá a nuestras cuentas
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
