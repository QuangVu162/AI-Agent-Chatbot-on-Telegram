# AI Business Performance Agent for Small and Medium enterprises

Author: Ho Quang Vu Le (Student ID: 270777903)

Supervisor: Dr. Sherry Feng

## Project Overview

This project develops a low-friction, high-impact Generative AI Business Assistant designed specifically for Small and Medium Enterprises (SMEs) in New Zealand. By leveraging Retrieval-Augmented Generation (RAG) and Google's Gemini LLM, the agent enables SME owners to query structured relational databases using natural language via Telegram, receiving immediate visual charts and actionable business insights without requiring specialized technical skills.

## Core Features

* Multi-Agent Orchestration: Uses specialized agents to handle distinct tasks: intent routing, SQL generation, and business insight synthesis.

* Text-to-SQL RAG: Securely bridges natural language queries with a MySQL database using SQL-RAG architecture.

* Automated Visualization: Dynamically generates charts using Matplotlib based on queried datasets.

* Actionable Insights: Translates raw financial data into concise, strategic business recommendations.

## Technology Stack

* Backend: Python 3.11+
* AI Framework: LangChain & LangGraph
* LLM Engine: Google Gemini 2.5 Flash (via langchain-google-genai)
* Database: MySQL (Relational Schema)
* Messaging: Telegram Bot API
* Deployment: Docker containerization

## 📂 System Architecture & Codebase Structure


This repository is structured to deploy a scalable, secure, and highly efficient multi-agent AI system. The architecture is deliberately designed to address the core operational constraints of New Zealand SMEs, focusing on data sovereignty, cost efficiency, and decision-making usability.

```text
├── database/
│   ├── init.sql                # Database DDL (customers, locations, products, orders, order_details)
├── service/
│   ├── ai_base.py              # Foundational LLM configuration for Google Gemini
│   ├── ai_agent.py             # Multi-agent orchestrator (Intent, SQL Generator, and Insight agents)
│   ├── db_manager.py           # Database connection manager with strict Read-Only enforcement
│   ├── template_queries.py     # Pre-validated SQL templates for common business inquiries
│   ├── chart_package.py        # Logic engine for selecting optimal visualization types
│   └── visualizer.py           # Matplotlib integration for dynamic chart rendering
├── TCT testing/                # Human-Computer Interaction (HCI) Experimental Data
│   └── Project Capstone - TCT experiment analysis.ipynb  # Statistical evaluation scripts to evaluate the result of TCT experiment
├── output_images/              # Directory for dynamically generated data visualizations
├── sql_security_audit.log      # Compliance tracking for all LLM-generated database queries
├── bot.py                      # Telegram Bot interface and API webhook listener
├── docker-compose.yml          # Container orchestration for rapid SME deployment
├── Dockerfile                  # Isolated environment setup for the Python application
├── requirements.txt            # Project dependencies (LangChain, Pandas, Matplotlib, etc.)
└── .env                        # Secure environment variables (Do not commit to version control)