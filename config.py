import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = "mongodb+srv://candidate:aQ7hHSLV9QqvQutP@hardfiltering.awwim.mongodb.net/"
TURBOPUFFER_API_KEY = "tpuf_dQHBpZEvl612XAdP0MvrQY5dbS0omPMy"
TURBOPUFFER_REGION = "aws-us-west-2"
DB_NAME = "interview_data"
COLLECTION_NAME = "linkedin_data_subset"

FULL_NAME = "Dheeraj Joshi"
EMAIL = "anikatyonzon111@gmail.com"
TPUF_NAMESPACE_NAME = "dheeraj_joshi_tpuf_key"

VOYAGE_API_KEY = "pa-vNEmoJfc5evP_SSvpxIAj3uFzs9dfppEZkpx-3kOFZy"
OPENAI_API_KEY = "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"

BATCH_SIZE = 1000
MAX_RETRIES = 3
SEARCH_TOP_K = 100
FINAL_CANDIDATES = 10

EVALUATE_URL = "https://mercor-dev--search-eng-interview.modal.run/evaluate"
GRADE_URL = "https://mercor-dev--search-eng-interview.modal.run/grade"
