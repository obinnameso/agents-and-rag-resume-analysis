### Introduction 

This project aims to test the use of a multi-agent architecture combined with a RAG framework to create an agentic workflow

```
📦 Resume-Analysis-LLM
 ├── 📂 backend                  # Backend API and processing logic
 │    ├── 📂 models              # LLM model, embedding, and retrieval logic
 │    │    ├── llm_model.py      # Handles interactions with LLMs
 │    │    ├── resume_parser.py  # Extracts text from resumes (PDF, DOCX, TXT)
 │    │    ├── feedback_generator.py # Generates feedback on resumes
 │    │    ├── query_handler.py  # Handles user queries about resumes
 │    │    ├── embeddings.py     # Embedding storage & retrieval (FAISS/ChromaDB)
 │    │    └── __init__.py
 │    │
 │    ├── 📂 database            # Resume storage and retrieval
 │    │    ├── db.py             # Database connection logic (PostgreSQL, MongoDB)
 │    │    ├── resume_store.py   # Handles saving & retrieving resume data
 │    │    └── __init__.py
 │    │
 │    ├── 📂 api                 # API endpoints for integration
 │    │    ├── routes.py         # FastAPI/Flask API routes
 │    │    ├── query_api.py      # API for querying resume details
 │    │    ├── feedback_api.py   # API for returning resume feedback
 │    │    └── __init__.py
 │    │
 │    ├── 📂 utils               # Helper functions
 │    │    ├── file_handler.py   # File upload & conversion logic
 │    │    ├── text_processing.py # NLP preprocessing
 │    │    ├── config.py         # Configuration settings
 │    │    ├── logger.py         # Logging setup
 │    │    └── __init__.py
 │    │
 │    ├── main.py                # Backend entry point
 │    ├── requirements.txt       # Dependencies
 │
 ├── 📂 frontend                 # Frontend UI (Streamlit, React, Flask)
 │    ├── 📂 components          # UI components
 │    ├── 📂 pages               # Resume upload, feedback, chat
 │    ├── app.py                 # Web UI entry point
 │    ├── package.json           # Dependencies (if using React)
 │
 ├── 📂 tests                    # Unit & integration tests
 │    ├── test_resume_parser.py  # Test resume parsing logic
 │    ├── test_feedback.py       # Test feedback generation
 │    ├── test_api.py            # Test API endpoints
 │    ├── test_embeddings.py     # Test embedding retrieval
 │    └── __init__.py
 │
 ├── 📂 docs                     # Documentation
 │    ├── setup.md               # Installation guide
 │    ├── api_docs.md            # API documentation
 │    ├── usage_guide.md         # How to use the system
 │    ├── contributing.md        # Contribution guidelines
 │    ├── architecture.md        # System architecture overview
 │
 ├── .gitignore                   # Ignore logs, env files, etc.
 ├── README.md                     # Project overview
 ├── LICENSE                       # Open-source license
 ├── Dockerfile                    # Docker setup
 ├── docker-compose.yml            # Multi-container setup
 ├── config.yaml                   # Configuration file
 ├── setup.py                       # Package setup
 └── requirements.txt               # Dependencies
```