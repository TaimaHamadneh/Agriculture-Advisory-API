FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency file
COPY pyproject.toml .

# Install dependencies using uv (faster than pip)
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system -r requirements.txt
    
# Copy application code
COPY ./app ./app
COPY ./crop_optimal_conditions.csv .

# Expose port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]