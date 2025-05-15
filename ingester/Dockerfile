# ingester/Dockerfile

# Stage 1: build the C++ code
FROM ubuntu:22.04 AS cppbuilder

RUN apt update && apt install -y \
  build-essential \
  cmake \
  curl \
  poppler-utils \
  pkg-config \
  libpoppler-cpp-dev \
  && rm -rf /var/lib/apt/lists/*

# Download nlohmann/json single-header version
RUN mkdir -p /usr/include/nlohmann && \
    curl -sSL https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp -o /usr/include/nlohmann/json.hpp
WORKDIR /app
COPY src/ ./src/
COPY CMakeLists.txt ./
RUN cmake -S . -B build && cmake --build build

# Stage 2: Python + FastAPI app
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt update && apt install -y \
  poppler-utils \
  libpoppler-cpp-dev \
  && rm -rf /var/lib/apt/lists/*


# Copy Python API
COPY main.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy C++ binary from previous stage
COPY --from=cppbuilder /app/build/pdf_ingest ./build/pdf_ingest

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
