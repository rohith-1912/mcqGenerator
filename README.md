# 📘 **MCQ Generator – Technical Documentation**

### Version: 1.0

### Repository: [https://github.com/rohith-1912/mcqGenerator](https://github.com/rohith-1912/mcqGenerator)

### Author: Panathala Rohith

---

# 1. 📌 **Overview**

The **MCQ Generator** is an LLM-based application that automatically creates Multiple Choice Questions (MCQs) from uploaded text or PDF documents. It uses:

* **Streamlit** for UI
* **LangChain** for prompt orchestration
* **OpenAI models** for content generation
* **PyPDF2** for PDF parsing

The system generates:

* A structured MCQ quiz
* A review/analysis of the generated questions
* Difficulty-based question sets
* A clean table view of the MCQs

This tool is useful for:

* Teachers
* Students
* EdTech developers
* Exam question creators
* Learning and development teams

---

# 2. 🗂 **System Architecture**

```
                    ┌────────────────────────┐
                    │      Streamlit UI       │
                    └─────────────┬──────────┘
                                  │
                        User uploads PDF/TXT
                                  │
                    ┌─────────────▼──────────┐
                    │       utils.py          │
                    │ - read_file()           │
                    │ - get_table_data()      │
                    └─────────────┬──────────┘
                                  │
                        Extracted text
                                  │
                    ┌─────────────▼──────────┐
                    │   MCQGenerator.py       │
                    │ - Prompt Templates      │
                    │ - Quiz chain            │
                    │ - Review chain          │
                    │ - run_quiz_and_review() │
                    └─────────────┬──────────┘
                                  │
                   Generated MCQ JSON + Review
                                  │
                    ┌─────────────▼──────────┐
                    │      Streamlit UI       │
                    │  Table + Review output  │
                    └─────────────────────────┘
```

---

# 3. 🧩 **Modules Description**

## 3.1 `StreamlitApp.py`

Handles the entire UI:

* File upload
* Input collection
* Button actions
* Token usage display
* Table rendering
* Review rendering

Key functions:

* `st.file_uploader()`
* `st.selectbox()`
* `st.table()`
* `st.text_area()`

---

## 3.2 `MCQGenerator.py`

Handles LLM workflow:

### Components:

* **PromptTemplate** for quiz generation
* **PromptTemplate** for quiz evaluation
* **RunnableLambda** as a sequential chain replacement
* Calls to the OpenAI Chat Model through LangChain

### Core Function:

```python
def run_quiz_and_review(inputs):
    quiz = quiz_chain["quiz"].invoke(inputs)
    review = review_chain["review"].invoke({ ... })
    return {"quiz": quiz_text, "review": review_text}
```

---

## 3.3 `utils.py`

Provides helper functions:

### 🔹 `read_file(file)`

Reads:

* `.pdf` → using PyPDF2
* `.txt` → using UTF-8 decoding

### 🔹 `get_table_data(quiz)`

Converts JSON string into Pandas-friendly table data.

---

## 3.4 `logger.py`

Configures logging:

* Writes logs to a timestamped file
* Useful for debugging file reading & LLM errors

---

# 4. 🧠 **LLM Workflow**

### Step 1: Quiz Generation

Prompt instructs LLM to:

* Read input text
* Generate `N` MCQs
* Follow `RESPONSE_JSON` structure
* Maintain chosen complexity level

### Step 2: Review Generation

Prompt instructs LLM to:

* Evaluate difficulty
* Provide a short 50-word analysis
* Suggest improvements

---

# 5. 🖥 **User Interface (Streamlit)**

### Inputs:

* Upload file (PDF/TXT)
* Number of MCQs
* Subject
* Complexity Level (dropdown)
* Submit button

### Output:

* MCQ Table (if JSON is valid)
* Raw quiz text (fallback)
* Review text
* Token usage summary

---

# 6. ⚙️ **Installation Guide**

### 1️⃣ Clone the repo

```bash
git clone https://github.com/rohith-1912/mcqGenerator.git
cd mcqGenerator
```

### 2️⃣ Create a virtual environment

```bash
python -m venv mcq
source mcq/Scripts/activate
```

### 3️⃣ Install requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Add `.env` file

```
OPENAI_API_KEY=your_api_key
```

### 5️⃣ Launch the app

```bash
streamlit run StreamlitApp.py
```

---

# 7. 🧪 **Sample Input & Output**

### Input:

Upload `biology.pdf`, choose:

* MCQs: 5
* Subject: Biology
* Tone: Complex

### Output:

* 5 generated MCQs
* Table of MCQs with options
* Review section

---

# 8. 🐞 **Common Issues & Fixes**

### ❌ *JSONDecodeError*

**Cause:** LLM output not pure JSON
**Fix:** Use simpler tones or extract JSON using regex

### ❌ *DataFrame constructor error*

**Cause:** `get_table_data()` returns `[]` or invalid data
**Fix:** Validate JSON data before DataFrame

### ❌ *PDF reading error*

**Cause:** Scanned PDFs or PyPDF2 version issues
**Fix:** Ensure OCR PDF, or use `PyPDF2.PdfReader`

---

# 9. 🔐 **Environment Variables**

| Variable         | Description            |
| ---------------- | ---------------------- |
| `OPENAI_API_KEY` | Required for LLM calls |

---

# 10. 📄 **License**

MIT License. Free to use and modify.

---

# 11. 🤝 **Contributing**

Pull requests and issues are welcome.

---

Just tell me!
