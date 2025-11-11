# aegisgpt — secure llm gateway (prototype)

a lightweight fastapi-based middleware that hardens llm access by enforcing prompt sanitization, pii redaction, authentication, and audit logging.  
built to demonstrate secure architecture principles for ai-driven systems.

---

## features

- prompt sanitization to mitigate prompt injection attacks  
- pii redaction for emails, phone numbers, and credit card data  
- jwt-based role authentication and access control  
- async audit logging to sqlite for traceability  
- dockerized deployment with network isolation  
- mock llm integration (easily replaceable with openai or vertex ai)

---

## tech stack

**python**, **fastapi**, **langchain**, **jwt**, **docker**, **sqlite**, **gcp (optional)**

---

## quick start (local)

**clone the repo:**
```bash
git clone https://github.com/<yourusername>/aegisgpt.git
cd aegisgpt

## security notes

- this is a demo prototype for campus and interview purposes

- replace mock llm call with openai or vertex ai for production demos

- use secure secret management (dotenv / vault)

- enforce stricter prompt blocking and logging policies for real deployments