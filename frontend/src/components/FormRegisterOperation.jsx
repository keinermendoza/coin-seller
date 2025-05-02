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



const FormSchema = z.object({
    price: z
      .string()
      .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
        message: "Debe ser un número válido mayor a 0",
      })
      .transform((val) => Number(val)),
  
    amount: z
      .string()
      .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
        message: "Debe ser un número válido mayor a 0",
      })
      .transform((val) => Number(val)),
  });

export function FormRegisterOperation({price, amount, onSubmit, extraParamsSubmit=null}) {
  const form = useForm({
    resolver: zodResolver(FormSchema),
    defaultValues: {
        price: price?.value || '',
        amount: amount?.value || '',
      },
  })

  

  return (
    <div className="w-full max-w-5xl mx-auto bg-gray-300 rounded-xl p-4 ">

        <Form {...form}>
        <form onSubmit={form.handleSubmit((data) => onSubmit(data, extraParamsSubmit?.trade_request_id, extraParamsSubmit?.side_operation))} className="space-y-6">
            <FormField
            control={form.control}
            name="price"
            render={({ field }) => (
                <FormItem>
                <FormLabel>{price.label}</FormLabel>
                <FormControl>
                    <Input  type="number" className="bg-white" placeholder={price.placeholder} {...field} />
                </FormControl>
                <FormDescription className="text-[0.75rem] italic">
                    {price.helpText}
                </FormDescription>
                <FormMessage />
                </FormItem>
            )}
            />
             <FormField
            control={form.control}
            name="amount"
            render={({ field }) => (
                <FormItem>
                <FormLabel>{amount.label}</FormLabel>
                <FormControl>
                    <Input  type="number" className="bg-white" placeholder={amount.placeholder} {...field} />
                </FormControl>
                <FormDescription className="text-[0.75rem] italic">
                    {amount.helpText}
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
