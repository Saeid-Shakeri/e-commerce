# انتخاب تصویر پایه
FROM python:3.10-slim

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های requirements
COPY requirements.txt .

# نصب وابستگی‌ها
# in the last uncommit this
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -r requirements.txt

# کپی کردن کد منبع
COPY . .

# تعیین فرمانی برای اجرای سرور
CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]
