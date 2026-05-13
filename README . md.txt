# 🩺 Gemma-Pulse: Clinical Intelligence Terminal

**Gemma-Pulse** is a high-performance, privacy-first clinical assistant designed for healthcare environments. By leveraging local Large Language Models (LLMs) and a modern Glassmorphism UI, it provides clinicians with an offline tool for symptom triage, patient context management, and real-time inventory monitoring.

---

## 🌟 Key Features

### 🧠 Local-First AI Intelligence

* **Privacy by Design:** Uses **Ollama** to run models locally. No patient data is sent to the cloud, ensuring HIPAA-compliant workflows.
* **Clinical Triage:** Optimized to process complex medical symptoms and lab values using the `Gemma-4-26B` model.
* **Contextual Awareness:** Automatically injects patient age, sex, and medical history into AI prompts for personalized clinical reasoning.

### 📊 Modern Clinical Terminal

* **Glassmorphism UI:** A sleek, dark-themed interface built with **Streamlit** that reduces eye strain in clinical settings.
* **Interactive Inventory:** Live monitoring of medical supplies (e.g., Insulin, Antibiotics) with automated low-stock threshold alerts.
* **Multimodal Input:** Integrated **Voice-to-Text** capabilities allowing doctors to dictate notes hands-free during patient examinations.

### 📁 Clinical Data Management

* **JSON Foundation:** Uses a robust `clinical_data.json` structure for managing patient records and clinic state.
* **Portable Reports:** One-click export of clinical sessions into JSON format for integration into Electronic Health Records (EHR).

---

## 🛠️ Tech Stack

* **Framework:** [Streamlit](https://streamlit.io/)
* **AI Inference:** [Ollama](https://ollama.com/)
* **Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Model:** `Gemma-4-26B-A4B-it-heretic` (Q4_K_M Quantization)
* **Audio:** `streamlit-mic-recorder`

---

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have **Python 3.9+** and **Ollama** installed.

### 2. Prepare the AI Model

Download the specialized clinical model:

```bash
ollama pull pdurlej/gemma-4-26B-A4B-it-heretic:Q4_K_M

```

### 3. Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/your-username/gemma-pulse.git
cd gemma-pulse
pip install streamlit ollama plotly streamlit-mic-recorder pandas

```

### 4. Launch the Terminal

```bash
streamlit run gemma_pulse.py

```

---

## 💻 System Requirements

| Level | CPU | RAM | GPU (VRAM) |
| --- | --- | --- | --- |
| **Minimum** | 6-Core | 16 GB | 8 GB (e.g., RTX 3060) |
| **Recommended** | 12-Core | 32 GB+ | 24 GB (e.g., RTX 4090) |

---

## 📂 Project Structure

```text
├── gemma_pulse.py        # Main Streamlit Application
├── clinical_data.json    # Database for patients and inventory
├── README.md             # Project Documentation
└── requirements.txt      # Python dependencies

```

---

## 📝 Usage Guide

1. **Select Patient:** Use the sidebar to select a patient profile or enter a new Patient ID.
2. **Input Symptoms:** Type symptoms in the chat bar or click the **🎤 icon** to record audio notes.
3. **Monitor Stocks:** Keep an eye on the "Real-time Inventory" chart in the sidebar.
4. **Export:** At the end of a session, click **Export Clinical Report** to save the conversation for record-keeping.

---

## ⚖️ Disclaimer

**Gemma-Pulse is a Clinical Decision Support Tool (CDST) and is NOT a substitute for professional medical judgment.** This software is intended for educational and demonstrative purposes only. Always consult board-certified clinical protocols for actual patient care.

---

*Created by the Yug.V.Gupta.*