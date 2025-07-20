"use client";
import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useUser } from "@auth0/nextjs-auth0"

interface Response {
  respondent: string;
  summary: string;
}

interface Question {
  _id: string;
  title: string;
  askedTo: number;
  responses: Response[];
}

export function Interviews() {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const { user, isLoading } = useUser();

  useEffect(() => {
    if (isLoading || !user?.email) return;

    const fetchQuestions = async () => {
      try {
        const res = await fetch(`http://localhost:8000/questions/creator/${user.email}`);
        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();
        setQuestions(data);
      } catch (err) {
        console.error("Failed to load questions", err);
      }
    };

    fetchQuestions();
  }, [user, isLoading]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-2">My Questions</h2>
      {questions.map((q) => (
        <Card key={q._id} className="bg-white border border-slate-200 shadow-sm">
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-semibold text-slate-900">{q.title}</h3>
                <p className="text-slate-600 mt-1 text-sm">
                  Asked to {q.askedTo} people — {q.responses?.length || 0} responses
                </p>
              </div>
              <Button variant="outline" size="sm" onClick={() => setExpanded(expanded === q._id ? null : q._id)}>
                {expanded === q._id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                {expanded === q._id ? "Hide" : "View"} Responses
              </Button>
            </div>

            {expanded === q._id && (
              <div className="mt-4 space-y-3">
                {(q.responses || []).map((res, idx) => (
                  <div key={idx} className="p-3 bg-slate-50 rounded border text-sm">
                    <strong>{res.respondent}:</strong> {res.summary}
                  </div>
                ))}
                <Button className="mt-3 bg-slate-900 text-white hover:bg-slate-800">Summarize All</Button>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
