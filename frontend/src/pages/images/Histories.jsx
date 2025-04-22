import SocialCanvas from "@/components/SocialCanvas";
export default function Histories() {

  const data = {
    data: [
      {
        slug: "brl_ves",
        text: "15.45",
        initial: {x: 714, y: 976},
      },
      {
        slug: "ves_brl",
        text: "0.054",
        initial: {x: 720, y: 1196},
      },
      {
        slug: "fecha",
        text: "12/04/25",
        initial: {x: 556, y: 728},
        fontSize: 54,
      }
    ],
    fontSize:80,
    layout: {
      type: "histories",
      width: 1080, 
      height: 1920,
      image_base: "/cambios-el-fuerte-instagram-facebook-history.jpg"
    }
  }

  const saveObjImageState = (data) => {
    // aqui axios
    console.log(data)
  }


  return (
    <div>
      <SocialCanvas canvasData={data} saveObjImageState={saveObjImageState} />
    </div>
  )
}
