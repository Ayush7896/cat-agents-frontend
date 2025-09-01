# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Expose port 8501 (Streamlit default)
EXPOSE 8501

# Run Streamlit application
# Since your main.py is directly in the folder (not in subfolder)
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]