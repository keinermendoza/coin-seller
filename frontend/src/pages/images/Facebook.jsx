import SocialCanvas from "@/components/SocialCanvas";

export default function Facebook() {
  const data = {
    points: [
      {
        slug: "brl_ves",
        text: "15.45",
        initial: {x: 802, y: 528},
      },
      {
        slug: "ves_brl",
        text: "0.054",
        initial: {x: 800, y: 736},
      },
      {
        slug: "fecha",
        text: "12/04/25",
        initial:  {x: 768, y: 268},
        fontSize: 50,

      }
    ],
    fontSize:100,
    layout: {
      type: "facebook-feed",
      width: 1200, 
      height: 1200,
      image_base: "/facebook-feed.jpg"
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
