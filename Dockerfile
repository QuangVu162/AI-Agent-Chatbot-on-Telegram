# 1. Choose a lightweight Python environment
FROM python:3.11-slim

# 2. Set the working directory inside the virtual computer
WORKDIR /app

# 3. Copy only the requirements file first to optimize caching
COPY requirements.txt .

# 4. Install all the necessary Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your entire project code (the src folder, .env, etc.) into the container
COPY . .

# 6. Set the command to automatically start your Telegram bot
CMD ["python", "bot.py"]