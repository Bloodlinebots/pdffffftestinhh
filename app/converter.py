from fpdf import FPDF
from PIL import Image
import io

def images_to_pdf(images):
    pdf = FPDF(unit="pt", format="A4")
    for file in images:
        image = Image.open(file).convert("RGB")
        width, height = image.size
        a4_width, a4_height = 595, 842
        ratio = min(a4_width / width, a4_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size)

        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        pdf.add_page()
        pdf.image(img_bytes, x=(a4_width - new_size[0]) // 2, y=30, w=new_size[0], h=new_size[1])

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
