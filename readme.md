📚 LLM-Based Claim Verification with Long-Context Retrieval

Track A – Kharagpur Data Science Hackathon 2026

An end-to-end LLM-assisted claim verification system that checks biographical claims against long literary sources using retrieval-augmented generation (RAG).
The system scales to book-length documents, retrieves relevant evidence, and produces verdicts with rationales.

🚀 Overview

Modern language models struggle with long context and evidence attribution.
This project addresses that by combining:

Document cleaning and chunking

Semantic retrieval using sentence embeddings

LLM-based reasoning over retrieved evidence

Structured outputs with rationale and evidence snippets

The system verifies whether a claim is:

consistent

contradict

unknown (LLM unavailable or insufficient evidence)

🧠 High-Level Architecture
Claim
  │
  ▼
Claim Extraction
  │
  ▼
Document Cleaning (Project Gutenberg)
  │
  ▼
Chunking (Sliding Window)
  │
  ▼
Embedding Index (Sentence Transformers)
  │
  ▼
Top-K Evidence Retrieval
  │
  ▼
LLM Reasoner (GPT-4o-mini)
  │
  ▼
Verdict + Rationale + Evidence
  │
  ▼
results/results.csv

📂 Project Structure
project/
│
├── app/                     # Pipeline orchestration
│   ├── main.py
│   ├── pipeline.py
│   └── prompts.py
│
├── src/                     # Core logic
│   ├── claims.py            # Claim extraction
│   ├── clean_text.py        # Text normalization
│   ├── chunking.py          # Long-context chunking
│   ├── retrieval.py         # Semantic search
│   ├── llm_reasoner.py      # LLM-based judgment
│   ├── generate_results.py
│   └── reasoning.py
│
├── books/                   # Source corpus
│   ├── in search of the castaways.txt
│   └── The Count of Monte Cristo.txt
│
├── data/
│   ├── train.csv
│   └── test.csv
│
├── results/
│   └── results.csv
│
├── report/
│   └── report.pdf
│
├── evaluate_train_accuracy.py
├── verify_llm.py
├── requirements.txt
└── README.md

🔍 Methodology
1️⃣ Long-Context Handling

Entire books are cleaned and chunked

Each chunk is embedded using all-MiniLM-L6-v2

Avoids passing full books to the LLM

2️⃣ Retrieval-Augmented Reasoning

Claims are matched to top-K relevant chunks

Only relevant evidence is sent to the LLM

Reduces hallucination and token usage

3️⃣ LLM-Based Verdict Generation

Uses gpt-4o-mini for claim verification

Outputs both:

verdict (consistent / contradict / unknown)

rationale (short explanation)

4️⃣ Robust Failure Handling

API rate-limit or network failures return:

verdict = "unknown"
rationale = "LLM unavailable"


Ensures pipeline never crashes

📊 Evaluation

Temporary evaluation is performed using training labels:

accuracy ≈ 0.64


This reflects:

Strong recall for consistent claims

Conservative behavior under uncertainty

Rate-limit effects on LLM availability

Accuracy improves significantly with uninterrupted LLM access.

⚠️ Known Limitations

LLM rate limits can cause unknown outputs

Semantic retrieval may miss subtle contradictions

No fine-tuning (zero-shot reasoning only)

Evidence quality depends on chunk boundaries

These limitations are explicitly handled and documented.

🔐 API Key Setup

Set your OpenAI API key as an environment variable:

Windows (PowerShell)
SETX OPENAI_API_KEY "your_api_key_here"


Restart the terminal after setting.

To verify:

python verify_llm.py

▶️ How to Run
1️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the pipeline
python -m app.main


Results will be generated in:

results/results.csv

🧪 Sample Output
id	prediction	rationale
80	contradict	Evidence conflicts with claim timeline
95	consistent	Claim aligns with retrieved text
78	unknown	LLM unavailable due to rate limit
🏁 Conclusion

This project demonstrates a practical, scalable approach to long-context claim verification using modern LLMs.
It prioritizes robustness, explainability, and evidence grounding, making it suitable for real-world deployment and evaluation.

👤 Authors:
Team Tech4change

Kharagpur Data Science Hackathon 2026
Track A Submission