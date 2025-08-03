# query_configs.py

from typing import Dict, Any

class QueryConfigurations:

    @staticmethod
    def get_all_configs() -> Dict[str, Dict[str, Any]]:
        """Get all refined query configurations."""
        
        configs = {
            "tax_lawyer.yml": {
                "name": "Tax Lawyer",
                "query": 'tax attorney lawyer irs audit "big four" "am law 100" corporate tax',
                "hard_criteria": {
                    "required_education": {"any_of": ["has_jd", "has_llm"]},
                    "min_years_experience": 3,
                },
                "soft_criteria": {
                    "preferred_experience": 5,
                    "weight_factors": {
                        "irs_experience": 3.0,
                        "corporate_tax_experience": 2.5,
                        "big_four_experience": 2.0
                    },
                    "irs_experience_keywords": ["irs audit", "tax controversy", "tax dispute"],
                    "corporate_tax_experience_keywords": ["m&a tax", "transactional tax", "corporate tax", "tax structuring"],
                    "big_four_experience_keywords": ["deloitte", "ey", "ernst & young", "pwc", "kpmg"]
                }
            },

            "mechanical_engineers.yml": {
                "name": "Mechanical Engineer",
                "query": "mechanical engineer product design manufacturing simulation solidworks ansys",
                "hard_criteria": {
                    "required_education": {"has_bachelors": True},
                    "min_years_experience": 3,
                },
                "soft_criteria": {
                    "preferred_experience": 5,
                    "weight_factors": {
                        "cad_simulation_tools": 3.0,
                        "domain_specialization": 2.5,
                        "product_lifecycle_involvement": 2.0
                    },
                    "cad_simulation_tools_keywords": ["solidworks", "ansys", "fea", "cad", "comsol", "autocad"],
                    "domain_specialization_keywords": ["thermal analysis", "structural analysis", "cfd", "fluid dynamics", "mechatronics"],
                    "product_lifecycle_involvement_keywords": ["prototyping", "manufacturing", "product development", "testing"]
                }
            },

            "junior_corporate_lawyer.yml": {
                "name": "Junior Corporate Lawyer",
                "query": "('junior corporate associate' OR 'corporate law clerk' OR 'legal intern' OR 'entry-level attorney') AND ('M&A' OR 'due diligence' OR 'contract drafting')",
                "hard_criteria": {
                    "required_education": {"has_jd": True},
                    "min_years_experience": 0 
                },
                "soft_criteria": {
                    "preferred_experience": 3,
                    "weight_factors": {
                        "ma_experience": 3.0,
                        "prestigious_employer": 2.5
                    },
                    "ma_experience_keywords": ["m&a", "mergers acquisitions", "due diligence"],
                    "prestigious_employer_keywords": ["am law 100", "vault 100", "magic circle", "fortune 500"]
                }
            },

            "doctors_md.yml": {
                "name": "Medical Doctor",
                "query": 'physician MD "US medical school" OR "American medical graduate" OR "ECFMG certified" healthcare "board certified"',
                "hard_criteria": {
                    "required_education": {"has_md": True},
                    "min_years_experience": 2
                },
                "soft_criteria": {
                    "preferred_experience": 4,
                    "weight_factors": {
                        "outpatient_experience": 3.0,
                        "telemedicine_experience": 2.5,
                        "bonus_for_board_certification": 2.0,
                        "bonus_for_top_us_school": 1.5 
                    },
                    "outpatient_experience_keywords": ["outpatient", "family medicine", "ambulatory", "primary care"],
                    "telemedicine_experience_keywords": ["telemedicine", "telehealth", "virtual care"],
                    "bonus_for_board_certification_keywords": ["board certified", "abr certified", "diplomate american board"],
                   # Doctors MD - bonus_for_top_us_school_keywords
"bonus_for_top_us_school_keywords": [
    'harvard', 'johns hopkins', 'stanford', 'ucsf', 'ucla', 
    'washington university', 'columbia', 'duke', 'yale', 
    'university of washington', 'university of michigan', 'northwestern'
]
                }
            },

            "biology_expert.yml": {
                "name": "Biology Expert",
                "query": "PhD (biologist OR molecular biology OR cell biology OR genetics OR biochemistry) research scientist (CRISPR OR sequencing OR genomics)",
                "hard_criteria": {
                    "required_education": {"has_phd": True}
                },
                "soft_criteria": {
                    "preferred_experience": 4,
                    "weight_factors": {
                        "research_publications": 3.5,
                        "lab_techniques": 2.5,
                        "bonus_for_top_university": 2.0
                    },
                    "research_publications_keywords": ["peer reviewed", "publication", "published", "author", "nature", "cell", "science journal"],
                    "lab_techniques_keywords": ["crispr", "pcr", "sequencing", "ngs", "assay", "genomics"],
                   # For Maths & Biology - bonus_for_top_university_keywords
                "bonus_for_top_university_keywords": [
                 "harvard", "stanford", "mit", "yale", "princeton", "columbia",
                 "berkeley", "uchicago", "penn", "johns hopkins", "caltech",
                "oxford", "cambridge", "eth zurich", "epfl", "university of toronto",
                 "waterloo", "max planck", "karolinska"
                ]
                }
            },

            "mathematics_phd.yml": {
                "name": "Mathematics PhD",
                "query": "phd mathematics OR phd statistics OR phd applied math research statistical modeling",
                "hard_criteria": {
                    "required_education": {"has_phd": True}
                },
                "soft_criteria": {
                    "preferred_experience": 3,
                    "weight_factors": {
                        "research_expertise": 3.5,
                        "modeling_proficiency": 2.5,
                        "bonus_for_top_university": 2.0
                    },
                    "research_expertise_keywords": ["publication", "peer reviewed", "preprint", "research", "journal of mathematics"],
                    "modeling_proficiency_keywords": ["statistical modeling", "quantitative analysis", "stochastic", "algorithms", "pde", "numerical analysis"],
                    # For Maths & Biology - bonus_for_top_university_keywords
                "bonus_for_top_university_keywords": [
                "harvard", "stanford", "mit", "yale", "princeton", "columbia",
                "berkeley", "uchicago", "penn", "johns hopkins", "caltech",
                "oxford", "cambridge", "eth zurich", "epfl", "university of toronto",
                 "waterloo", "max planck", "karolinska"
                ]
                }
            },

            "anthropology.yml": {
                "name": "Anthropology PhD",
                "query": "phd anthropology OR phd sociology OR anthropologist OR sociologist research fieldwork",
                "hard_criteria": {
                    "required_education": {"has_phd": True},
                },
                "soft_criteria": {
                    "preferred_experience": 2,
                    "weight_factors": {
                        "ethnographic_methods": 3.5,
                        "academic_output": 2.5,
                        "bonus_for_prestigious_university": 2.0
                    },
                    "ethnographic_methods_keywords": ["ethnography", "fieldwork", "participant observation", "interviews"],
                    "academic_output_keywords": ["publication", "conference", "working paper", "author"],
                    "bonus_for_prestigious_university_keywords": ["harvard", "chicago", "oxford", "lse", "berkeley", "stanford"]
                }
            },

          "quantitative_finance.yml": {
                "name": "Quantitative Finance",
                "query": "('quantitative analyst' OR 'financial engineer' OR 'PhD physics' OR 'PhD mathematics') AND ('Goldman Sachs' OR 'Jane Street' OR 'Citadel' OR 'Two Sigma' OR 'hedge fund' OR 'investment bank') AND (python OR c++)",
                "hard_criteria": {
                    "min_years_experience": 2
                },
                "soft_criteria": {
                    "preferred_experience": 5,
                    "weight_factors": {
                        "quantitative_modeling": 3.0,
                        "technical_proficiency": 2.5,
                        "high_stakes_environment": 2.0,
                        "bonus_for_m7_mba": 1.5
                    },
                    "quantitative_modeling_keywords": [
                        "risk modeling", "algorithmic trading", "derivatives pricing", "stochastic calculus", 
                        "monte carlo", "black-scholes", "asset pricing", "portfolio optimization"
                    ],
                    "technical_proficiency_keywords": [
                        "python", "pandas", "numpy", "c++", "quantlib", "scikit-learn", "tensorflow"
                    ],
                    "high_stakes_environment_keywords": [
                        "investment firm", "hedge fund", "trading", "investment bank", "asset management"
                    ],
                    "bonus_for_m7_mba_keywords": [
                        "harvard business school", "stanford gsb", "wharton", "kellogg", 
                        "booth", "columbia business school", "mit sloan"
                    ]
                }
            },
            
            "radiology.yml": {
                "name": "Radiologist",
                "query": 'radiologist OR "radiology physician" OR "diagnostic radiologist" OR "medical imaging md"',
                "hard_criteria": {
                    "required_education": {"has_md": True},
                    "min_years_experience": 3,
                },
                "soft_criteria": {
                    "preferred_experience": 4,
                    "weight_factors": {
                        "bonus_for_board_certification": 3.5,
                        "ai_imaging_experience": 2.5,
                    },
                    "bonus_for_board_certification_keywords": ["board certified", "abr", "frcr", "fellowship", "diplomate"],
                    "ai_imaging_experience_keywords": ["ai", "artificial intelligence", "image analysis", "machine learning", "computer vision"]
                }
            },

            "bankers.yml": {
                "name": "Healthcare Investment Banker",
                "query": '("investment banking" OR "M&A advisory") AND (healthcare OR biotech OR pharma) AND "MBA"',
                "hard_criteria": {
                    "required_education": {"has_masters": True}, 
                    "min_years_experience": 2,
                },
                "soft_criteria": {
                    "preferred_experience": 4,
                    "weight_factors": {
                        "healthcare_specialization": 4.0,
                        "ma_transaction_experience": 3.0,
                        "prestigious_employer": 2.0
                    },
                    "healthcare_specialization_keywords": ["healthcare", "biotech", "pharma", "medical devices", "life sciences"],
                    "ma_transaction_experience_keywords": ["m&a", "mergers", "recapitalization", "growth equity", "due diligence"],
                    "prestigious_employer_keywords": ["jp morgan", "goldman sachs", "morgan stanley", "kkr", "blackstone", "lazard", "evercore"]
                }
            }
        }
        
        return configs