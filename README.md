# 🚀 Customer Support Resolution Agent (CSRA)

An AI-powered customer support system that automates customer query resolution using **LangGraph**, **RAG (Retrieval-Augmented Generation)**, **FastAPI**, and **React**. The system retrieves relevant company policies, analyzes customer requests, executes business tools, applies safety guardrails, and proposes resolutions with human approval for sensitive actions.

---

## ✨ Features

- 🤖 AI-powered customer support agent
- 🔍 Retrieval-Augmented Generation (RAG)
- 📚 Policy-aware responses
- 📦 Order lookup integration
- 💰 Refund eligibility checking
- 🎁 Goodwill credit recommendations
- 🔒 Prompt injection detection
- 🛡️ Guardrails for sensitive operations
- 👤 Human-in-the-loop approval
- 📊 Confidence scoring
- 📝 Audit logging
- ⚡ Modern React dashboard

---

# 🏗️ Architecture

```text
                    Customer Query
                           │
                           ▼
               Intent Detection (LLM)
                           │
                           ▼
                 Retrieve Policies (RAG)
                           │
                           ▼
                  Tool Selection Layer
        ┌────────────┬────────────┬────────────┐
        │            │            │            │
 Order Lookup   Refund Check  Goodwill   Escalation
        │            │            │            │
        └────────────┴────────────┴────────────┘
                           │
                           ▼
                Resolution Generation
                           │
                           ▼
                  Confidence Evaluation
                           │
              ┌────────────┴────────────┐
              │                         │
      Auto Resolution           Human Approval
```

---

# 📁 Project Structure

```text
customer-support-resolution-agent/
│
├── backend/
│   ├── app/
│   ├── agents/
│   ├── api/
│   ├── services/
│   ├── rag/
│   ├── database/
│   ├── tools/
│   ├── models/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── services/
│   └── App.tsx
│
├── README.md
├── .env.example
└── requirements.txt
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- LangGraph
- LangChain
- ChromaDB
- SQLite
- SQLAlchemy
- Pydantic

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios

## AI

- OpenAI GPT
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/customer-support-resolution-agent.git

cd customer-support-resolution-agent
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt

python main.py
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key

DATABASE_URL=sqlite:///support.db

CHROMA_DB=./chroma
```

---

# 🔄 AI Workflow

1. Customer submits a request.
2. AI detects customer intent.
3. Relevant policies are retrieved using RAG.
4. Required business tools are executed.
5. AI generates a grounded response.
6. Confidence score is calculated.
7. Guardrails validate safety.
8. Human approval is requested for sensitive actions.
9. Final response is returned.

---

# 🎯 Supported Use Cases

- Order Status
- Late Delivery
- Refund Request
- Damaged Item
- Missing Item
- Goodwill Credit
- Password Reset
- Account Support
- Out-of-Scope Queries
- Prompt Injection Detection

---

# 🛡️ Safety Features

- Prompt Injection Detection
- Policy Grounding
- Confidence Threshold
- Human Approval Workflow
- Refund Guardrails
- Audit Logs
- Secure Tool Execution

---

# 📷 Screenshots

Add screenshots inside a folder named `screenshots/`.

Example:

```
screenshots/
│
├── dashboard.png
├── late-order.png
├── refund.png
├── injection-test.png
└── approval.png
```

Then display them:

```markdown
## Dashboard

![Dashboard](screenshots/dashboard.png)

## Refund Workflow

![Refund](screenshots/refund.png)
```

---

# 🚀 Future Improvements

- Voice-based customer support
- Multi-language support
- Email integration
- CRM integration
- Analytics Dashboard
- Live Agent Chat
- Knowledge Base Expansion
- Multi-tenant deployment

---

# 👩‍💻 Author

**Jyothi Islavath**

GitHub: https://github.com/Jyothi-D3

---

# 📄 License

This project is developed for educational and portfolio purposes.
