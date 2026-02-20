# Fuel My Future 🚀

> *"Igniting Careers, Engineering Success."*

An AI-powered platform that provides personalized feedback on resumes and mock interview performance, helping job applicants iterate faster and land the roles they want.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Prerequisites](#prerequisites)
5. [Setup](#setup)
6. [Environment Configuration](#environment-configuration)
7. [Running the App](#running-the-app)
8. [Configuration Reference](#configuration-reference)
9. [Security Notes](#security-notes)
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview

Many job applicants lack access to actionable, personalized feedback. Existing solutions are often time-intensive, generalized, or socially uncomfortable, leading to inefficient iteration and weaker applications.

**Fuel My Future** is an integrated Streamlit platform that simulates interview environments and analyses resumes using AI-driven feedback systems. It enables iterative improvement by storing user history and benchmarking performance over time.

---

## Key Features

| Feature | Description |
|---|---|
| 🎙️ **Mock Interview System** | Simulates real interview conditions and generates targeted feedback on weak areas. |
| 📄 **Resume Feedback Engine** | Provides structured critique on resume content and phrasing using AI analysis. |
| 📊 **Progress Tracking (My Results)** | Tracks user improvement across multiple attempts to enable data-driven iteration. |
| 📁 **Document Hub** | Stores artifacts and allows longitudinal comparison of application materials. |
| 🤖 **FutureBot AI Chat** | On-demand career assistant powered by Google Gemini. |

---

## Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **AI Backend**: [Google Generative AI (Gemini)](https://ai.google.dev/)
- **PDF Processing**: PyPDF2, ReportLab
- **Config**: PyYAML
- **Package Management**: [uv](https://github.com/astral-sh/uv)
- **Python**: ≥ 3.13

---

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip
- A Google Generative AI API key — obtain one at <https://aistudio.google.com/app/apikey>

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/Vivaan-crypto/Fuel-My-Future.git
cd Fuel-My-Future

# 2. Install dependencies (using uv)
uv sync
# Or using pip:
# pip install -e .

# 3. Configure your API key (see next section)
cp .env.example .env
# Edit .env and set API_KEY=<your key>
```

---

## Environment Configuration

The application reads the Google Generative AI key from the **`API_KEY` environment variable**.

### Option A — `.env` file (recommended for local development)

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```dotenv
API_KEY=your_google_api_key_here
```

> **Never commit `.env` to version control.** It is already listed in `.gitignore`.

### Option B — Export the variable directly

```bash
export API_KEY=your_google_api_key_here
```

### Option C — CI / deployment environments

Set `API_KEY` as a secret or environment variable in your hosting platform (e.g., Streamlit Community Cloud → *App settings → Secrets*).

---

## Running the App

```bash
# With uv
uv run streamlit run app.py

# Or with an activated virtual environment
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Configuration Reference

| Variable | Required | Description |
|---|---|---|
| `API_KEY` | ✅ Yes | Google Generative AI API key used to power the AI features. |

`config.yaml` is present for reference only. **Do not store real secrets in it.**  
The application always prefers the `API_KEY` environment variable over any value in `config.yaml`.

---

## Security Notes

> ⚠️ **A Google API key was previously committed to this repository.**  
> That key has been removed and **must be considered compromised**.  
> If you have access to the Google Cloud / AI Studio console, **rotate or revoke the exposed key immediately** and restrict the replacement key to only the APIs and IPs it needs.

- **Never commit secrets** (API keys, passwords, tokens) to version control — even in private repos.
- Use `.env` files locally and rotate any key that has ever been exposed.
- `.env` and `.env.*` are ignored by `.gitignore` in this repository.
- See [`.env.example`](.env.example) for the list of required environment variables.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes, ensuring no secrets are committed.
3. Open a Pull Request with a clear description.
4. A maintainer will review and merge.

---

## License

This project is provided as-is for educational purposes. See the repository for license details.

