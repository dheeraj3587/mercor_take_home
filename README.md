# Intelligent Candidate Sourcing Engine

## Overview

This project is an advanced candidate search and ranking system designed to source qualified professionals from a large database. It leverages a hybrid approach combining semantic vector search with rule-based filtering and weighted scoring to identify the best candidates for various job roles. The system is highly configurable, allowing for nuanced and effective searches across diverse fields like technology, finance, and law.

The entire system was built and optimized through an iterative, data-driven process, evolving from a bug-ridden initial state to a robust and high-performing final product.

---

## Key Features

-    **AI-Powered Query Expansion**: Utilizes OpenAI's GPT models to expand simple user queries into comprehensive, boolean-ready search strings with relevant synonyms and industry keywords.
-    **Vector-Based Semantic Search**: Employs Voyage AI for generating high-quality embeddings and TurboPuffer for efficient, large-scale vector similarity searches to find semantically relevant candidates.
-    **Dynamic, Config-Driven Logic**: All search parameters—from the initial query to hard filters and soft scoring weights—are centralized in a single Python configuration file, allowing for easy tuning and addition of new job roles without changing the core engine logic.
-    **Two-Tier Filtering System**:
    1.  **Hard Filters**: Applies non-negotiable criteria (e.g., minimum experience, required degrees) to create a baseline of qualified candidates.
    2.  **Soft Scoring**: Ranks the remaining candidates using a flexible, weighted model based on preferred skills, experience, and other "nice-to-have" attributes.
-    **Intelligent Text Processing**: A custom text processor parses raw candidate data to extract structured information like years of experience, educational degrees (JD, MD, PhD, etc.), and mentions of prestigious universities.

---

## Codebase Architecture

The project is organized into several key modules, each with a distinct responsibility:

-   ### `final_submission.py`
    -   **Purpose**: The main entry point for the application.
    -   **Functionality**: This script initializes the `CandidateSearchEngine`, iterates through all job configurations defined in `query_configs.py`, runs the search for each, validates the results, and submits the final list of candidates for grading.

-   ### `search_engine.py`
    -   **Purpose**: The core of the search and ranking logic.
    -   **Functionality**: Contains the `CandidateSearchEngine` class, which orchestrates the entire pipeline: query expansion, vector generation, vector search, candidate data enrichment, and the application of both hard and soft filters.

-   ### `query_configs.py`
    -   **Purpose**: The central configuration hub or the "brain" of the system.
    -   **Functionality**: Contains the `QueryConfigurations` class, which holds a dictionary defining every job search. Each configuration specifies the initial query, the `hard_criteria` for filtering, and the `soft_criteria` for weighted scoring. **This is the primary file to modify for tuning search performance.**

-   ### `utils.py` (or `text_processor.py`)
    -   **Purpose**: A utility module for data parsing.
    -   **Functionality**: Contains the `EnhancedTextProcessor` class responsible for cleaning raw text from candidate profiles and extracting structured data like years of experience and educational qualifications using robust regular expressions.

-   ### `config.py`
    -   **Purpose**: Stores all API keys and sensitive constants.
    -   **Functionality**: Holds API keys for OpenAI, Voyage AI, and TurboPuffer, as well as namespace information and personal details for submission. This file is not committed to version control.

-   ### `requirements.txt`
    -   **Purpose**: Lists all necessary Python packages for the project.
    -   **Functionality**: Allows for easy setup of the project environment using `pip`.

---

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Create a `config.py` file in the root directory and add your API keys and personal information:
    ```python
    # config.py
    OPENAI_API_KEY = "sk-..."
    VOYAGE_API_KEY = "vov-..."
    TURBOPUFFER_API_KEY = "tpuf-..."
    TPUF_NAMESPACE_NAME = "your_namespace_here"
    YOUR_FULL_NAME = "Your Name"
    YOUR_EMAIL = "your.email@example.com"
    ```

---

## How to Run

To execute the final submission process, which runs all 10 job searches and sends the results to the grading service, run the following command from your terminal:

```bash
python3 final_submission.py