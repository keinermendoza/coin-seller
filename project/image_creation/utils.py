from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.conf import settings
from django.utils import timezone


class DrawImage:
   
    def __init__(self, ves_brl, brl_ves, date):
        self.ves_brl = ves_brl
        self.brl_ves = brl_ves
        self.date = date
        self.image = settings.BASE_DIR / "static/image_creation/img/banner-tazas.jpg"
        
        self.rate_font = ImageFont.truetype(settings.BASE_DIR /  "static/image_creation/fonts/Montserrat-Medium.ttf", size=64)
        self.date_font = ImageFont.truetype(settings.BASE_DIR / "static/image_creation/fonts/Montserrat-Medium.ttf", size=48)
        self.colors= {
            "brown": (68,19,6)
        }

        self.text_nodes = [
            {
                "id": "brl_ves",
                "coordinates": (730,970),
                "font": self.rate_font,
                "color": self.colors["brown"],
                "content": "a"
            },
            {
                "id": "ves_brl",
                "coordinates": (730,1186),
                "font": self.rate_font,
                "color": self.colors["brown"],
                "content": "a"

            },
            {
                "id": "date",
                "coordinates": (500,730),
                "font": self.date_font,
                "color": self.colors["brown"],
                "content": "a"

            }
        ]

        self.update_base()

    def update_base(self):
        for node in self.text_nodes:
            match node["id"]:
                case "brl_ves":
                    node["content"] = self.brl_ves
                case "ves_brl":
                    node["content"] = self.ves_brl
                case "date":
                    node["content"] = self.date


    def draw_texts(self):
        image = Image.open(self.image)
        drawble_image = ImageDraw.Draw(image)
        for node in self.text_nodes:
            drawble_image.text(node["coordinates"], node["content"], fill=node["color"], font=node["font"])

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def get_date():
        today = timezone.now()  
        return today.strftime("%d-%m-%Y")
    
    @classmethod
    def generate_name(cls):
        date = DrawImage.get_date()
        return f"tasas-del-dia_{date}.jpg"