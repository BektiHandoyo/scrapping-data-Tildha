from pdf2image import convert_from_path
from pytesseract import pytesseract
from PIL import Image
import os
from main import model

def convert_pdf_to_image(pdf_path="downloaded.pdf", save_dir="tmp-pdf", res=400) :
    pages = convert_from_path(pdf_path, res)
    for index, page in enumerate(pages):
        page.save(f"{save_dir}/{index}.png", 'PNG')
    print('successfully convert pdf to image')

def get_pdf_content(pdf_dir="tmp-pdf", lang="eng") :
    list_image = os.listdir(pdf_dir)
    content = ''
    for index, img_path in enumerate(sorted(list_image, key=lambda x: int(x.split(".")[0]))):
        image = Image.open(f"{pdf_dir}/{img_path}")
        extracted_text:str = pytesseract.image_to_string(image, lang)
        print(f'successfully read images number {str(index)}')
        content += extracted_text.replace('\n', '') + "\n"

    return content

def summarize_pdf_content(text) :
    prompt = "Summarize the following part of the text ( Attention ! please answer it without any formatting)"
    try :
        response = model.generate_content(prompt + text)
        print("successfully summarize text ")
        return response.text
    except ValueError as ve:
        print('Something Went wrong, error : ' + str(ve) )
        print(response)
        return "error"
    

