# 1Z0-931-25 Oracle ADB Exam Trainer

Interactive Streamlit exam trainer for the **Oracle Autonomous Database Cloud 2025 Professional (1Z0-931-25)** certification.

## Features

- 🔴 **141 Questions** — full question bank including multi-select and single-answer
- ⚡ **Practice Mode** — instant feedback with explanations after each answer
- 📋 **Mock Exam Mode** — simulate real exam, submit all at once
- 📖 **Review All Mode** — browse all questions with correct answers highlighted
- 🔍 **Filter** by question type (Single / Multi-Select) and keyword search
- 🔀 **Shuffle** for randomized practice sessions
- 📊 **Score tracking** with pass/fail verdict

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set **Main file path** to `app.py`
4. Deploy!

## Local Run

```bash
pip install streamlit
streamlit run app.py
```

## Files

```
├── app.py              # Main Streamlit application
├── questions.json      # 141 exam questions with answers & explanations
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Light theme configuration
└── README.md
```
