# ---------- Build Stage ----------
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Upgrade pip and install generic utilities
RUN pip install --upgrade pip

# Copy only the requirements file to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies into user directory
RUN pip install --user --no-cache-dir -r requirements.txt


# ---------- Runtime Stage ----------
FROM python:3.11-slim AS runtime

# Set security contexts to not run as root
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy the dependencies from builder stage to the final image
COPY --from=builder /root/.local /home/appuser/.local

# Ensure installed binaries are in the path
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the application source code 
COPY ./app ./app

# Set correct ownership for the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI server via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
