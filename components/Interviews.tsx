"use client";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ChevronDown, ChevronUp } from "lucide-react";

interface Response {
  respondent: string;
  summary: string;
}

interface Question {
  id: string;
  title: string;
  askedTo: number;
  responses: Response[];
}

const mockQuestions: Question[] = [
  {
    id: "q1",
    title: "What are your thoughts on AI in hiring?",
    askedTo: 5,
    responses: [
      { respondent: "Jane Doe", summary: "Supports fair screening using AI." },
      { respondent: "John Smith", summary: "Worried about algorithmic bias." },
    ],
  },
  {
    id: "q2",
    title: "What is your greatest strength?",
    askedTo: 3,
    responses: [
      { respondent: "Alice", summary: "Problem-solving under pressure." },
    ],
  },
];

export function Interviews() {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-slate-900 mb-2">My Questions</h2>
      {mockQuestions.map((q) => (
        <Card key={q.id} className="bg-white border border-slate-200 shadow-sm">
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-semibold text-slate-900">{q.title}</h3>
                <p className="text-slate-600 mt-1 text-sm">
                  Asked to {q.askedTo} people — {q.responses.length} responses
                </p>
              </div>
              <Button variant="outline" size="sm" onClick={() => setExpanded(expanded === q.id ? null : q.id)}>
                {expanded === q.id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                {expanded === q.id ? "Hide" : "View"} Responses
              </Button>
            </div>

            {expanded === q.id && (
              <div className="mt-4 space-y-3">
                {q.responses.map((res, idx) => (
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
