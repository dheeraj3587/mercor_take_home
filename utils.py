import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

def normalize_score(score: float, min_score: float, max_score: float) -> float:
    if max_score == min_score:
        return 0.5
    return (score - min_score) / (max_score - min_score)

class EnhancedTextProcessor:
    def __init__(self):
        self.university_tiers = {
            'top_us_universities': [
                'harvard', 'stanford', 'mit', 'yale', 'princeton', 'columbia', 
                'ucla', 'berkeley', 'uchicago', 'university of chicago', 'penn', 
                'upenn', 'university of pennsylvania', 'northwestern', 'johns hopkins', 
                'duke', 'cornell', 'nyu', 'new york university'
            ],
            'm7_mba': [
                'harvard business school', 'stanford graduate school of business', 
                'wharton', 'kellogg', 'booth', 'columbia business school', 'mit sloan'
            ],
        }

    def clean_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _calculate_experience_from_dates(self, text: str, current_year: int) -> int:
        date_ranges = []
        pattern = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\'?(\d{2,4})\b\s*(?:-|to)\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\'?(\d{2,4})|present|current|date|today)'

        for match in re.finditer(pattern, text):
            try:
                start_year_str = match.group(1)
                start_year = int(f"20{start_year_str}" if len(start_year_str) == 2 else start_year_str)

                end_str = match.group(2)
                end_year = current_year if end_str in ['present', 'current', 'date', 'today'] else int(f"20{end_str}" if len(end_str) == 2 else end_str)

                if 1980 <= start_year < end_year <= current_year:
                    date_ranges.append((start_year, end_year))
            except (ValueError, IndexError, TypeError):
                continue

        date_ranges.sort()

        if not date_ranges:
            return 0

        merged_ranges = []
        for start, end in date_ranges:
            if not merged_ranges or merged_ranges[-1][1] < start:
                merged_ranges.append([start, end])
            else:
                merged_ranges[-1][1] = max(merged_ranges[-1][1], end)

        return sum(end - start for start, end in merged_ranges)

    def extract_years_experience(self, text: str) -> int:
        if not text or not isinstance(text, str):
            return 0
        text_lower = text.lower()
        explicit_years = 0

        match = re.search(r'(\d{1,2})\+?\s*years? of (?:professional\s*)?experience', text_lower)
        if match:
            try:
                explicit_years = int(match.group(1))
            except (ValueError, IndexError):
                explicit_years = 0

        date_range_years = self._calculate_experience_from_dates(text_lower, datetime.now().year) or 0

        logger.debug(f"Explicit Years: {explicit_years}, Date Range Years: {date_range_years}")
        return min(int(max(explicit_years, date_range_years)), 50)

    def check_education_level(self, text: str) -> Dict[str, bool]:
        if not text:
            return {}
        text_lower = f" {text.lower()} "

        return {
            "has_bachelors": bool(re.search(r'\b(b\.?s\.?|b\.?a\.?|bachelor)\b', text_lower)),
            "has_masters": bool(re.search(r'\b(m\.?s\.?|m\.?a\.?|master|mba)\b', text_lower)),
            "has_phd": bool(re.search(r'\b(ph\.?d|phd|doctorate|doctoral)\b', text_lower)),
            "has_jd": bool(re.search(r'\b(j\.?d|jd|juris doctor)\b', text_lower)),
            "has_llm": bool(re.search(r'\b(llm|l\.?l\.?m)\b', text_lower)),
            "has_md": bool(re.search(r'\b(m\.?d|md|medical doctor)\b', text_lower)),
        }

    def check_university_tier(self, text: str) -> Dict[str, bool]:
        if not text:
            return {}
        text_lower = self.clean_text(text)
        return {
            tier_name: any(school in text_lower for school in schools)
            for tier_name, schools in self.university_tiers.items()
        }

    def parse_candidate_comprehensive(self, candidate_data: Dict) -> Dict:
        full_text = candidate_data.get('full_text', '') or candidate_data.get('rerank_summary', '')

        if not full_text:
            logger.warning(f"No text data found for candidate ID: {candidate_data.get('id', 'N/A')}")
            return {
                **candidate_data,
                'years_experience': 0,
                'has_bachelors': False,
                'has_masters': False,
                'has_phd': False,
                'has_jd': False,
                'has_llm': False,
                'has_md': False
            }

        education_info = self.check_education_level(full_text)
        years_experience = self.extract_years_experience(full_text)
        school_tiers = self.check_university_tier(full_text)

        return {
            **candidate_data,
            **education_info,
            **school_tiers,
            'years_experience': years_experience
        }

TextProcessor = EnhancedTextProcessor
