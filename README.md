# Automated Resume Information Extraction, Scoring, and Ranking System

## Overview

This project is an automated recruitment intelligence system designed to process unstructured resumes and convert them into structured, machine-readable candidate profiles. The system then evaluates candidates using a deterministic scoring engine and produces an objective ranking.

The solution focuses on:
- High extraction accuracy across variable resume formats
- Deterministic and explainable scoring logic
- Reproducible ranking results
- Scalable batch processing for large candidate pools

---

## Problem and Solution

Organizations receive resumes in large volumes across multiple formats (PDF, DOC, DOCX). Manual screening is inefficient, inconsistent, and biased.

This system:
- Extracts structured information from resumes
- Applies a consistent scoring model (0–100 scale)
- Ranks candidates objectively
- Handles missing or ambiguous resume data

---

## Architecture Overview
Client (React + TypeScript)

↓

Auth Server (Authentication + Session Control)

↓

AI Server (Extraction + Scoring + Ranking)

↓

PostgreSQL + Redis




---

## Tech Stack

### Frontend
- React
- TypeScript
- Redux Toolkit
- HTML / CSS

### Backend
- Node.js
- Express / NestJS (Service Layer)
- PostgreSQL
- Prisma ORM
- Redis

### AI / Processing
- Python
- FastAPI
- LangChain
- Google ADK

---

## Core Features

- Resume Upload & Processing
- Structured Data Extraction
- Weighted Resume Scoring
- Candidate Ranking Engine
- Batch Resume Processing (25+ resumes)

---

## Repository Structure
client/ → Frontend React Application
auth-server/ → Authentication + User Management
ai-server/ → Resume Extraction + Scoring + Ranking Engine


---




