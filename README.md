# CommonRoom

_“Not every meeting needs to be a meeting.”_

## 🧠 Project Overview

**CommonRoom** is a Ribbon-powered platform designed to help teams reduce redundant stand-up meetings by replacing them with asynchronous, structured check-ins. 

Project managers and coordinators can use CommonRoom to send Ribbon-style interviews to employees — short, direct, and async. Team members answer questions on their own time, and their responses are analyzed with generative AI to surface key insights. 

Whether a manager wants detailed responses or just a quick summary of the overall team mood, CommonRoom delivers it — no calendar invites required.

---

## 🚩 Problem

Too many meetings waste time and drain productivity, especially when the purpose could have been met with a simple check-in.

> The modern workplace needs something **between “this could’ve been a message” and “we need to talk.”**

---

## ✅ Solution

CommonRoom makes daily syncs async:
- Managers send out structured interview flows to employees.
- Employees answer when it’s convenient.
- AI-powered summaries surface key themes and feedback.
- Managers can read full responses or just the highlights.

Save time, capture insight, and bring focus back to deep work.

---

## 🔗 Ribbon Endpoints Used

This project uses the following Ribbon API endpoints:
- POST request to /interview-flows, for creating "Meetings/Questionnaires"
- POST request to /interviews, several of these are made to create a special interview link for each person in a role
- GET request to /interviews, for retrieving transcripts of the "Meetings/Questionnaires" and display it for others to see

---

## 🧪 How It Works

1. **Create a Question Flow**
   - Define a set of questions for a specific project or role.
   - Assign a flow ID and role-based targeting.

2. **Invite Respondents**
   - Add recipients (employees) and assign them to roles.
   - Automatically distributes interview links to the interview flow.

3. **Respond**
   - Employees respond asynchronously.
   - Transcripts are stored and analyzed.

4. **Summarize**
   - Use Google Gemini API to summarize individual responses.
   - Optionally, generate an overall summary per question to gauge team sentiment.

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/Edison611/hackthe6ix-2025.git
cd hackthe6ix-2025

## ⚙️ How to Run Locally

Use the following .env file with your own API keys

AUTH0_SECRET=
APP_BASE_URL=http://localhost:3000
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_AUDIENCE='leave blank'
AUTH0_SCOPE=openid profile email read:shows
GEMINI_API=
MONGODB_URI=
RIBBON_API_KEY=
