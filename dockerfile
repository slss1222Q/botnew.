# Python'ning so'nggi versiyasini olamiz
FROM python:3.11-slim

# Ishchi papkani belgilaymiz
WORKDIR /app

# Kutubxonalarni nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Barcha kodni nusxalaymiz
COPY . .

# Botni ishga tushiramiz
CMD ["python", "main.py"]
