from pdf2image import convert_from_path
import pytesseract
from openai import OpenAI
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np

# مسیر نصب Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# کلید API ChatGPT
api_key = "کلید open ai خودتونو اینجا وارد کنید"
client = OpenAI(api_key=api_key)

# مسیر فایل PDF
pdf_file_path = r"مسیری که فایل pdf اونحاست رو وارد کنید"

# مسیر poppler
poppler_path = r"مسیر bin poppler رو اینجا وارد کنید"


# پیش‌پردازش تصویر برای بهبود OCR
def preprocess_image(image):
    image = image.convert("L")
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    open_cv_image = np.array(image)
    _, thresh = cv2.threshold(open_cv_image, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return Image.fromarray(processed_image)


# استخراج متن از PDF
def extract_text_from_pdf(pdf_path, poppler_path):
    print("تبدیل صفحات PDF به تصاویر...")
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    full_text = ""
    for page_number, image in enumerate(images, start=1):
        print(f"پردازش صفحه {page_number}...")
        image = preprocess_image(image)
        text = pytesseract.image_to_string(image, lang="fas")
        full_text += text + "\n\n"
    return full_text


# خلاصه‌سازی متن با استفاده از ChatGPT
def summarize_text(text):
    print("خلاصه‌سازی متن...")
    chunks = [text[i:i + 2000] for i in range(0, len(text), 2000)]
    summarized_text = ""
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "متن زیر را به زبان فارسی خلاصه کن."},
                {"role": "user", "content": chunk}
            ]
        )
        summarized_text += response.choices[0].message.content + "\n\n"
    return summarized_text


# ذخیره متن در فایل
def save_to_file(text, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"فایل در مسیر {file_path} ذخیره شد.")


# اجرای مراحل
if __name__ == "__main__":
    try:
        extracted_text = extract_text_from_pdf(pdf_file_path, poppler_path)
        extracted_text_file = r"C:\Users\nerdz\Desktop\extracted_text.txt"
        save_to_file(extracted_text, extracted_text_file)

        summarized_text = summarize_text(extracted_text)
        summarized_text_file = r"C:\Users\nerdz\Desktop\summarized_text.txt"
        save_to_file(summarized_text, summarized_text_file)

    except Exception as e:
        print(f"خطایی رخ داد: {e}")
