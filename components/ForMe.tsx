"use client";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { useUser } from "@auth0/nextjs-auth0";

interface AssignedResponse {
  _id: string;
  question: string;
  assignedBy: string;
  status: "Pending" | "Completed";
}

const assignedResponses: AssignedResponse[] = [
  {
    id: "r1",
    question: "What are your thoughts on AI in hiring?",
    assignedBy: "Evan Ma",
    status: "Pending",
  },
  {
    id: "r2",
    question: "What is your greatest strength?",
    assignedBy: "Jane Lee",
    status: "Completed",
  },
];

  

export function ForMe() {
  const { user } = useUser();
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`http://localhost:8000/questions/creator/${user?.email}`);
      const data = await res.json()
      console.log("data", data);
      setData(data)
    }

    fetchData()
  }, [])

  console.log(user);

  console.log(data)
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-slate-900 mb-2">My Responses</h2>
      {data.map((res) => (
        <Card key={res._id} className="border border-slate-200 bg-white shadow-sm">
          <CardContent className="p-4">
            <h3 className="text-lg font-semibold text-slate-900">{res.question}</h3>
            <p className="text-sm text-slate-600">Assigned by {res.assignedBy}</p>
            <Badge
              className={
                res.status === "Completed"
                  ? "bg-green-100 text-green-700 border-green-200"
                  : "bg-yellow-100 text-yellow-700 border-yellow-200"
              }
              variant="secondary"
            >
              {res.status}
            </Badge>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
