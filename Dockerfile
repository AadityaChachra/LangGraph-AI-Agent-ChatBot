FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
# Expose the ports for FastAPI (8000) and Streamlit (8501) - Port Exposing 
EXPOSE 8000 8501
# Start both FastAPI and Streamlit servers
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run user_interface.py --server.port 8501 --server.address 0.0.0.0"]