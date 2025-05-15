
FROM ubuntu:22.04

# Install dev tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gdb \
    clang \
    pkg-config \
    git \
    libpoppler-cpp-dev \
    libglib2.0-dev \
    && apt-get clean
