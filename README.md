# 🌾 GovSchemeAI

### AI-Powered Government Scheme Discovery & Eligibility Assistant

GovSchemeAI is a farmer-friendly platform that helps users discover relevant government schemes, search available schemes, and understand eligibility and benefits using **AI + RAG (Retrieval-Augmented Generation)**.

## 🚀 Live Demo

### 👉 [Open GovSchemeAI Live Demo](https://govschemeai-3pnmuhsz9bs3wh5um5dxuw.streamlit.app/)

Try the application directly in your browser.

---

## ✨ Features

* 🤖 **AI Scheme Assistant** — Ask questions about government schemes in natural language.
* 🔎 **Find Schemes** — Search schemes using relevant filters.
* 🎯 **Eligibility Checker** — Find schemes matching a farmer's profile.
* 📚 **RAG-based Retrieval** — Retrieves relevant schemes from the government-scheme database before generating an answer.
* 🌾 **Farmer-Friendly Interface** — Presents scheme information in simple language.
* 📋 **Scheme Information** — Shows eligibility, benefits, documents and application information.

---

## 🧠 How It Works

```text
                 User
                   │
                   ▼
             Streamlit UI
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
       AI Chat   Search   Eligibility
          │        │        │
          └────────┼────────┘
                   ▼
             RAG Retriever
                   │
                   ▼
        Government Scheme Database
                   │
                   ▼
          Relevant Schemes
                   │
                   ▼
               AI Model
                   │
                   ▼
          Simple AI Response
```

---

## 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **Pandas**
* **Scikit-learn**
* **Sentence Transformers**
* **RAG (Retrieval-Augmented Generation)**
* **Ollama**
* **Gemma 3**
* **GitHub**

---

## 📂 Project Structure

```text
GovSchemeAI/
│
├── app.py
│
├── pages/
│   ├── 1_AI_Chat.py
│   ├── 2_Find_Schemes.py
│   └── 3_Eligibility.py
│
├── rag/
│   └── retriever.py
│
├── utils/
│   └── ai.py
│
├── data/
│   └── government_schemes.csv
│
├── assets/
│   └── style.css
│
├── requirements.txt
└── README.md
```

---

## 🎯 Example Query

```text
What irrigation schemes are available for farmers in Maharashtra?
```

GovSchemeAI retrieves the most relevant schemes and presents their:

* Scheme name
* Eligibility
* Benefits
* Subsidy
* Required documents
* Application information

---

## ⚠️ Disclaimer

GovSchemeAI is a prototype designed for educational, demonstration and research purposes.

Scheme information should always be verified with the relevant official government department or official scheme portal before applying.

---

## 🚀 Run Locally

Clone the repository:

```bash
git clone https://github.com/Chaitaligawade/GovSchemeAI.git
cd GovSchemeAI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 👨‍💻 Project

**GovSchemeAI**
AI + RAG based Government Scheme Discovery Platform
