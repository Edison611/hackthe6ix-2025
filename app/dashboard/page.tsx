"use client"
import { useState, useEffect } from "react";
import axios from "axios";

export default function Dashboard() {
  const [question, setQuestion] = useState("");
  const [responses, setResponses] = useState([]);
  const [summary, setSummary] = useState("");

  const createInterview = async () => {
    const res = await axios.post("http://localhost:8000/questions", { question });
    alert("Interview created successfully");
    setQuestion("");
  };

  useEffect(() => {
    const fetchResponses = async () => {
      const res = await axios.get("http://localhost:8000/responses");
      setResponses(res.data.responses);
      setSummary(res.data.summary);
    };
    fetchResponses();
  }, []);

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <div className="mb-6">
        <h2 className="text-xl mb-2">Create New Interview Question</h2>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="border p-2 w-full mb-2"
          placeholder="Enter your question"
        />
        <button
          onClick={createInterview}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Submit Question
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Responses</h2>
        <ul className="space-y-2">
          {responses.map((r: any, i: number) => (
            <li key={i} className="border p-2 bg-gray-50 rounded">
              <strong>{r.name}</strong>: {r.answer} <br />
              <em>Score: {r.score}</em>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-6 p-4 border bg-gray-100 rounded">
        <h2 className="text-xl font-semibold mb-2">Summary</h2>
        <p>{summary}</p>
      </div>
    </div>
  );
}