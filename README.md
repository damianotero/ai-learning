# AI Learning

Python scripts, exercises, and reference implementations for Damian Otero's AI Engineer training roadmap.

This repository serves as a hands-on learning laboratory for experimenting with AI architectures, data manipulation, LLM integrations, and core engineering concepts.

## Structure

```
ai-learning/
├── AGENTS.md             ← Project context and guidelines
├── README.md             ← Project overview and execution instructions
├── requirements.txt      ← Python dependencies (reportlab, etc.)
├── day_01.py             ← Daily exercise scripts (day_NN.py)
├── day_02.py
├── guia-modelos-ia.py    ← AI models reference generator
└── docs/
    ├── tasks.md          ← Pending and completed exercises
    ├── session-log.md    ← Learning session log
    └── assets/           ← Generated reference materials (PDFs, diagrams)
```

## Stack

- **Python 3.11+**
- Local virtual environment (`venv`)
- Core libraries: `reportlab` (PDF generation), standard library (`pathlib`, `json`, `math`)

## Running Scripts

Activate a virtual environment and execute the desired exercise script:

```bash
# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run an exercise script
python3 day_01.py

# Generate reference guides
python3 guia-modelos-ia.py
```