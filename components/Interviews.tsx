"use client";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { useUser } from "@auth0/nextjs-auth0";

interface Response {
  user_email: string;
  summary: string;
  interview_url?: string;
}

interface Question {
  _id: string;
  title: string;
  askedTo: number;
  summary?: string;
  responses: Response[];
}

export function Interviews() {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loadingSummary, setLoadingSummary] = useState<string | null>(null);
  const { user, isLoading } = useUser();

  const fetchData = async () => {
    if (!user?.email) return;

    try {
      const res = await fetch(`http://localhost:8000/questions/creator/${user.email}`);
      if (!res.ok) throw new Error("Failed to fetch questions");

      const questionData = await res.json();
      if (!Array.isArray(questionData)) {
        console.error("Unexpected question response:", questionData);
        setQuestions([]);
        return;
      }

      const enriched = await Promise.all(
        questionData.map(async (q) => {
          try {
            const [resRes, statusRes] = await Promise.all([
              fetch(`http://localhost:8000/questions/${q._id}/responses`),
              fetch(`http://localhost:8000/questions/${q._id}/response-status`),
            ]);

            let responses: Response[] = [];
            let askedTo = 0;

            if (resRes.ok) {
              const raw = await resRes.json();
              if (Array.isArray(raw)) {
                responses = raw.filter((r) => r.summary && r.summary.trim() !== "");
              }
            }

            if (statusRes.ok) {
              const stat = await statusRes.json();
              askedTo = (stat.responded?.length || 0) + (stat.not_responded?.length || 0);
            }

            return {
              ...q,
              responses,
              askedTo,
              summary: q.summary ?? "", // in case it's undefined
            };
          } catch (err) {
            console.error(`Error enriching question ${q._id}`, err);
            return { ...q, responses: [], askedTo: 0, summary: "" };
          }
        })
      );

      setQuestions(enriched);
    } catch (err) {
      console.error("Failed to load data:", err);
      setQuestions([]);
    }
  };

  useEffect(() => {
    if (!isLoading && user?.email) {
      fetchData();
    }
  }, [user, isLoading]);

  const handleSummarize = async (questionId: string) => {
    setLoadingSummary(questionId);
    try {
      const res = await fetch(
        `http://localhost:8000/questions/summarize?question_id=${questionId}`,
        { method: "POST" }
      );

      const result = await res.json();
      if (!result.success) {
        console.error("Summarization failed:", result.message);
      }

      await fetchData(); // Refresh to show updated summary
    } catch (err) {
      console.error("Error during summarization:", err);
    } finally {
      setLoadingSummary(null);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-2">My Questions</h2>
      {questions.map((q) => (
        <Card key={q._id} className="bg-white border border-slate-200 shadow-sm">
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-slate-900">{q.title}</h3>
                <p className="text-slate-600 mt-1 text-sm">
                  Asked to {q.askedTo} people — {q.responses.length} responses
                </p>
                {q.summary && (
                  <div className="mt-2 text-sm text-slate-700">
                    <p className="font-medium text-slate-800">Group Summary:</p>
                    <p className="mt-1">{q.summary}</p>
                  </div>
                )}
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setExpanded(expanded === q._id ? null : q._id)}
              >
                {expanded === q._id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                {expanded === q._id ? "Hide" : "View"} Responses
              </Button>
            </div>

            {expanded === q._id && (
              <div className="mt-4 space-y-3">
                {q.responses.length === 0 ? (
                  <p className="text-sm text-slate-500 italic">No responses yet.</p>
                ) : (
                  q.responses.map((res, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded border text-sm">
                      <strong>{res.user_email}:</strong> {res.summary}
                      {res.interview_url && (
                        <a
                          href={res.interview_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-2 text-blue-600 underline"
                        >
                          View Interview
                        </a>
                      )}
                    </div>
                  ))
                )}
                <Button
                  onClick={() => handleSummarize(q._id)}
                  disabled={loadingSummary === q._id}
                  className="mt-3 bg-slate-900 text-white hover:bg-slate-800"
                >
                  {loadingSummary === q._id ? (
                    <>
                      <Loader2 className="animate-spin w-4 h-4 mr-2" /> Summarizing...
                    </>
                  ) : (
                    "Summarize All"
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
