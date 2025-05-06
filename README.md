# Paper-Viz Platform

An end-to-end pipeline to summarize scientific papers and generate 3Blue1Brown-style mathematical animations using ManimGL.

## Features

- PDF ingestion and text extraction
- ML-based summarization and key-item (equations, theorems) extraction
- ManimGL-based animation of extracted LaTeX
- Interactive Next.js front-end
- Asynchronous orchestration with Redis and FastAPI microservices
- Containerized with Docker and docker-compose

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+

### Local Setup

1. Clone the repo:
   git clone https://github.com/your-username/paper-viz-platform.git
2. Build and run:
   docker-compose up --build
3. Navigate to http://localhost:3000

