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
-   git rm --cached config.py# Intelligent Candidate Sourcing Engine

## Overview

This project is an advanced candidate search and ranking system designed to source qualified professionals from a large database. It leverages a hybrid approach combining semantic vector search with rule-based filtering and weighted scoring to identify the best candidates for various job roles. The system is highly configurable, allowing for nuanced and effective searches across diverse fields like technology, finance, and law.

The entire system was built and optimized through an iterative, data-driven process, evolving from a bug-ridden initial state to a robust and high-performing final product.

---

## Supported Job Categories

The system supports evaluation for the following 10 professional roles:

- **Legal**: Tax Lawyers, Junior Corporate Lawyers
- **Engineering**: Mechanical Engineers  
- **Medical**: Medical Doctors (MDs), Radiologists
- **Academic**: Biology PhD, Mathematics PhD, Anthropology PhD
- **Finance**: Quantitative Finance professionals, Healthcare Investment Bankers

Each category includes specialized criteria and scoring mechanisms tailored to industry-specific requirements.

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

## Technical Implementation

### Search Pipeline Architecture
1. **Query Expansion**: OpenAI GPT-4 expands base queries with relevant synonyms and industry terms
2. **Embedding Generation**: Voyage AI creates high-dimensional vector representations
3. **Vector Search**: TurboPuffer performs similarity search across candidate database
4. **Data Enrichment**: Custom text processing extracts structured information from profiles
5. **Hard Filtering**: Applies mandatory criteria (education, experience thresholds)
6. **Soft Scoring**: Weighted ranking based on preferred qualifications
7. **Results Validation**: Ensures exactly 10 candidates per job category

### Scoring Methodology
- **Hard Criteria**: Binary pass/fail filters (education requirements, minimum experience)
- **Soft Criteria**: Weighted scoring (0-10 scale) across multiple dimensions:
  - Domain expertise keywords
  - Technical proficiency indicators
  - Prestigious institution affiliations
  - Industry-specific experience markers

Final scores combine weighted averages with bonus multipliers for exceptional qualifications.

---

## Performance Metrics

The system is evaluated on:
- **Precision**: Quality of top-ranked candidates
- **Coverage**: Ability to find diverse qualified candidates
- **Consistency**: Reproducible results across multiple runs
- **Configuration Flexibility**: Easy adaptation to new job categories

Expected performance targets:
- Average evaluation scores: 7.5+ out of 10
- Hard filter pass rates: 15-25% of initial candidates
- Processing time: <30 seconds per job category

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

-   ### `utils.py`
    -   **Purpose**: A utility module for data parsing and evaluation.
    -   **Functionality**: Contains the `EnhancedTextProcessor` class responsible for cleaning raw text from candidate profiles and extracting structured data like years of experience and educational qualifications using robust regular expressions.

-   ### `evaluator.py`
    -   **Purpose**: Handles scoring and ranking logic.
    -   **Functionality**: Implements the weighted scoring algorithms and candidate evaluation methods.

-   ### Additional Support Files
    -   `logging_config.py`: Comprehensive logging setup for debugging and analysis
    -   `filter_logger.py`: Specialized logging for filter operations
    -   `run_filter_analysis.py`: Analysis tools for filter performance optimization

---

## Configuration Structure

Each job category follows a standardized configuration format:

```python
"job_category.yml": {
    "name": "Job Title",
    "query": "base search query with boolean operators",
    "hard_criteria": {
        "required_education": {"has_degree": True},
        "min_years_experience": 3
    },
    "soft_criteria": {
        "preferred_experience": 5,
        "weight_factors": {
            "domain_expertise": 3.5,
            "technical_skills": 2.5,
            "prestigious_background": 2.0
        },
        "keyword_categories": {
            "domain_expertise_keywords": ["keyword1", "keyword2"],
            "technical_skills_keywords": ["skill1", "skill2"]
        }
    }
}
```

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
    Create a `config.py` file in the root directory (this file is not included in the repository for security):
    ```python
    # config.py (create this file)
    OPENAI_API_KEY = "sk-..."
    VOYAGE_API_KEY = "vov-..."
    TURBOPUFFER_API_KEY = "tpuf-..."
    TPUF_NAMESPACE_NAME = "your_namespace_here"
    YOUR_FULL_NAME = "Your Name"
    YOUR_EMAIL = "your.email@example.com"
    ```

---

## How to Run

### Main Execution
To execute the final submission process, which runs all 10 job searches and sends the results to the grading service:

```bash
python3 final_submission.py
```

### Additional Analysis Tools
Run filter analysis for performance optimization:
```bash
python3 run_filter_analysis.py
```

### Testing Individual Configurations
To test specific job categories or debug configurations, modify the script to run individual searches.

---

## Output and Results

### Generated Files
- `final_grading_result.json`: Complete evaluation results with scores
- `test_results.json`: Individual test execution results
- `detailed_filter_logs.json`: Comprehensive filtering analysis
- `search_app.log`: Runtime application logs

### Result Structure
Each evaluation includes:
- Candidate LinkedIn profiles and identification
- Individual criteria scores with explanations
- Weighted composite scores
- Statistical summaries by job category
- Performance metrics and timing data

---

## Key Implementation Decisions

1. **Hybrid Search Approach**: Combines semantic similarity with rule-based filtering for optimal precision
2. **Weighted Scoring Model**: Flexible configuration allows fine-tuning for different job requirements
3. **Robust Text Processing**: Handles inconsistent profile data with comprehensive regex patterns
4. **Modular Architecture**: Separation of concerns enables easy maintenance and extension
5. **Comprehensive Logging**: Detailed logs support debugging and performance analysis

---

## Error Handling and Validation

- API timeout and retry mechanisms
- Input validation for all configuration parameters
- Graceful degradation when external services are unavailable
- Comprehensive error logging with contextual information
- Result validation ensuring exactly 10 candidates per job category

---

## Dependencies

Key external services and libraries:
- **OpenAI API**: Query expansion and natural language processing
- **Voyage AI**: High-quality embedding generation
- **TurboPuffer**: Scalable vector similarity search
- **Python Libraries**: pandas, numpy, requests, logging

See `requirements.txt` for complete dependency list. **Intelligent Text Processing**: A custom text processor parses raw candidate data to extract structured information like years of experience, educational degrees (JD, MD, PhD, etc.), and mentions of prestigious universities.

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