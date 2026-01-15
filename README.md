# TradeSentinel

TradeSentinel is a market intelligence backend that ingests, normalises, and serves financial news data via a RESTful API.  
It combines web scraping, an ETL pipeline, persistent storage, and a read-only API designed with production-minded engineering principles.

---

## Overview

Financial and market-related news is fragmented across multiple platforms and formats.  
TradeSentinel consolidates this data into a single, normalised schema, ensuring reliable storage, deduplication, and easy downstream consumption.

The system is built to be **safe to re-run**, **observable**, and **extensible**, reflecting real-world backend and data engineering practices.

---

## Features

- Web scraping from multiple live sources (Hacker News, Yahoo Finance)
- Automated ETL pipeline for ingestion and normalisation
- Idempotent database writes to prevent duplicate records
- Cloud-hosted PostgreSQL persistence
- REST API with pagination for querying stored news
- Health check endpoint for service monitoring
- Structured logging for debugging and observability

---

## Tech Stack

- **Language:** Python  
- **Backend API:** FastAPI  
- **Database:** PostgreSQL (Neon.tech)  
- **ORM:** SQLAlchemy  
- **Scraping:** Requests, BeautifulSoup  
- **Cloud & DevOps:** Microsoft Azure (AZ-900), GitHub Actions  
- **Engineering Practices:** Logging, data idempotency, transactions, unit-ready design

---

## System Architecture

1. **Scraping Layer**
   - Fetches live data from Hacker News and Yahoo Finance
   - Cleans and normalises raw HTML into structured dictionaries

2. **ETL & Persistence Layer**
   - Converts raw scraped data into ORM-mapped objects
   - Enforces data integrity using:
     - Database-level UNIQUE constraints
     - Application-level duplicate checks
   - Uses transactional commits for atomic batch inserts

3. **API Layer**
   - Exposes stored news articles via a RESTful FastAPI service
   - Supports pagination for scalable querying
   - Provides health and status endpoints for monitoring

---

## Running Locally

### Prerequisites
- Python 3.10+
- PostgreSQL database (local or cloud)
- `pip` or virtual environment manager


