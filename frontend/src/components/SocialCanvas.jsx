import React, { useState, useEffect, useRef } from 'react';
import { Stage, Layer, Image as KonvaImage } from 'react-konva';
import DraggableText from './DragableText';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from '@/components/ui/label';
// obtengo los tipos de cambios
// obtengo las imagenes 
/*
# models 
class BannerItem(models.Model):
  Exchange = models.ForeingKey()
  pointX = models.IntegerField()
  pointY = models.IntegerField()

class Banner(models.Model):
  image = models.ImageField()
  items = models.ManyToMany(BannerItem)

  fechaPointX = models.IntegerField()
  fechaPointY = models.IntegerField()
*/

/*
# views
class ListCreateBanner(ListCreateAPIView):
  queryset = Banner.objects.all()
  
# urls 
/api/banner/list-create
[
  {
    id: 1,
    image: "/images/bolivar-real.jpg",
    items: [
      {
        exchange: BRL/VES,
        pointX: 40,
        pointY: 115
      },
      {
        exchange: VES/BRL,
        pointX: 80,
        pointY: 250
      }, 
    ]
  },
  {
    id: 2,
    image: "/images/bolivar-real-peso.jpg"
    items: [
      {
        exchange: BRL/VES,
        pointX: 40,
        pointY: 115
      },
      {
        exchange: VES/BRL,
        pointX: 80,
        pointY: 250
      }, 
      {
        exchange: VES/COL,
        pointX: 80,
        pointY: 250
      }, 
      {
        exchange: COL/VES,
        pointX: 80,
        pointY: 250
      }, 
    ]
  },
]
*/


/*
/api/banner/view-edit-delete/<int:pk>

*/

function getShortDate() {
  
  const fecha = new Date();
  const dia = fecha.getDate().toString().padStart(2, '0');
  const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
  const anio = fecha.getFullYear();
  
  return `${dia}/${mes}/${anio}`;
}

export default function SocialCanvas({canvasData, saveObjImageState}) {
  const [objImgaeData, setObjImageData] = useState(canvasData)
  const [imageObj, setImageObj] = useState(null);
  const [fecha, setFecha] = useState('');

  const stageRef = useRef();

  const { width, height } = objImgaeData.layout;
  const scaleFactor = 0.25; // solo visual

  // carga de imagen, agregar dependencia a datos de imagen
  useEffect(() => {
    const img = new window.Image();
    img.src = objImgaeData.layout.image_base;
    img.onload = () => setImageObj(img);
    handleUpdateDate(getShortDate())
  }, []);

  const handleDownload = () => {
    const stage = stageRef.current;
    const originalScale = stage.scale();

    // Reset scale for full-res image
    stage.scale({ x: 1, y: 1 });

    const uri = stage.toDataURL({ pixelRatio: 2 });

    // Restore scale
    stage.scale(originalScale);

    const link = document.createElement("a");
    link.download = `${objImgaeData.layout.type}.png`;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleChangeFontSize = (value) => {
    setObjImageData((prev) => ({
      ...prev, fontSize: value
      })
    )
  }

  const handleUpdateTextPosition = ( slug, x, y) => {
    console.log("recibiendo", slug, x, y)
    setObjImageData((prev) => {
      const updatedPoints = prev.points.map((item) =>
        item.slug === slug ? { ...item, position: { x, y } } : item
      );
  
      return {
        ...prev,
        points: updatedPoints,
      };
    });
  };


  const handleUpdateDate = (value) => {
    console.log("recibiendo", value)
    setFecha(value)
    
    setObjImageData((prev) => {
      const updatedPoints = prev.points.map((item) =>
        item.slug === "fecha" ? { ...item, text: value } : item
      );
  
      return {
        ...prev,
        points: updatedPoints,
      };
    });
  }

  

  return (
    <div className='w-fit '>

      <div className="flex items-center gap-2 mb-4">

        <Button className='mx-auto' onClick={handleDownload}>Descargar imagen</Button>      
      </div>





      <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center" }}>
        {/* Este div contiene el canvas visualmente escalado */}

       

        

        
        <div
          style={{
            transform: `scale(${scaleFactor})`,
            transformOrigin: "top left",
            marginBottom: "1rem",
            width: width * scaleFactor,
            height: height * scaleFactor,
          }}
        >
          <Stage
            width={width}
            height={height}
            ref={stageRef}
            style={{ border: "1px solid #ccc", background: "transparent" }}
          >
            <Layer>
              {imageObj && (
                <KonvaImage image={imageObj} width={width} height={height} />
              )}
              {objImgaeData?.points.map((t) => (
                <DraggableText
                  key={t.slug}
                  slug={t.slug}
                  text={t.text}
                  position={t.position}
                  fontSize={t.fontSize || objImgaeData.fontSize}
                  onChange={handleUpdateTextPosition}
                />
              ))}
            </Layer>

          </Stage>
        </div>

        <div className="w-full max-w-5xl mx-auto space-y-4  bg-gray-300 rounded-xl p-4 ">
        <Label htmlFor="date-text">
          Texto de la Fecha
        </Label>
        <Input
          id="date-text" 
          onInput={(e) => handleUpdateDate(e.target.value)} 
          className="bg-white" value={fecha} placeholder="ingresa la fecha"  />
        <Label htmlFor="font-size">
          Tamaño de los precios
        </Label>
        <Input
          id="font-size"
          className="bg-white" placeholder="tamaño de los precios"  
          onInput={(e) => handleChangeFontSize(e.target.value)} 
          value={objImgaeData.fontSize} type="number" />


          <Button onClick={() => saveObjImageState(objImgaeData)}>Guardar Cambios</Button>
        
        </div>
      </div>
    </div>
  );
}
