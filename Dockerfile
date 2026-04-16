FROM python:3.12-slim

LABEL maintainer="NovaOS Team <hello@novaos.ai>"
LABEL description="NovaOS — The desktop AI that sees, thinks and acts on your computer."

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    scrot \
    xdotool \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 7860

ENTRYPOINT ["novaos"]
CMD ["dashboard", "--port", "7860"]
