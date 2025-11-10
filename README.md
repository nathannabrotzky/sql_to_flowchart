# SQL Flowchart Generator

This project parses SQL queries and generates flowcharts representing their logical structure using Graphviz.

## 📁 Project Structure

queries/         # Folder containing .sql files to be parsed
output/          # Folder where generated flowcharts will be saved
cli/main.py      # Entry point for running the parser and generator

## 🚀 Getting Started

### 1. Install Dependencies

Make sure you have Python 3.8+ installed. Then install required packages:

```bash
pip install -r requirements.txt

### 2. Add SQL Files

Place your .sql files in the queries/ folder. Each file should contain a valid SQL query.

### 3. Run the CLI Script

To parse all SQL files and generate flowcharts:

python cli/main.py

Flowcharts will be saved in the output/ folder as .png or .pdf files depending on your configuration.

## 🧠 Features

Parses SQL queries into logical nodes (SELECT, FROM, JOIN, etc.)
Handles nested subqueries recursively
Visualizes query structure using Graphviz
Supports UNION, ORDER BY, LIMIT, and JOIN clauses

## 📦 Requirements

See requirements.txt for dependencies. Key libraries include:

graphviz – for rendering flowcharts
sqlparse – for SQL parsing
uuid – for unique node identifiers

## 🛠️ Future Improvements

Interactive web interface
Support for additional SQL dialects
Export to other formats (SVG, JSON)
