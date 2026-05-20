FROM python:3.11

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    nodejs \
    npm

# Copy everything
COPY . .

# Install backend dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Build frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Back to root
WORKDIR /app

ENV PORT=7860

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]