export default function TitleSection({title, subtitle}) {
  return (
    <div className="space-y-2 text-center mb-4">
        <p className="text-xl font-medium">{title}</p>
        <p className="italic">{subtitle}</p>
    </div>

  )
}
