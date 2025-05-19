# PDF Summarizer (فارسی)

این پروژه یک ابزار پایتون است که یک فایل PDF فارسی را به تصاویر تبدیل کرده، با استفاده از Tesseract متن آن را استخراج می‌کند و سپس با کمک ChatGPT خلاصه‌ای از آن تولید می‌کند.

## ویژگی‌ها
- تبدیل PDF به تصویر
- استخراج متن با OCR (زبان فارسی)
- خلاصه‌سازی متن با GPT-3.5

## پیش‌نیازها

- Python 3.10
- Tesseract OCR
- Poppler for Windows
- OpenAI API Key

## نصب وابستگی‌ها

```bash
pip install -r requirements.txt

///////////////////////

اجرا: 

```python main.py```

توجه: قبل از اجرا، مسیر فایل PDF و API Key را در فایل main.py تنظیم کنید..