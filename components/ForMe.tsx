"use client";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { useUser } from "@auth0/nextjs-auth0";

export interface AssignedResponse {
  _id: string; // MongoDB ObjectId as string
  user_email: string;
  question_id: string;
  interview_url: string;
  transcript: string | null;
  summary: string;
  question: Object;
}

// const assignedResponses: AssignedResponse[] = [
//   {
//     id: "r1",
//     question: "What are your thoughts on AI in hiring?",
//     assignedBy: "Evan Ma",
//     status: "Pending",
//   },
//   {
//     id: "r2",
//     question: "What is your greatest strength?",
//     assignedBy: "Jane Lee",
//     status: "Completed",
//   },
// ];

  

export function ForMe() {
  const { user } = useUser();
  const [data, setData] = useState<AssignedResponse[]>([]);

  const markAsComplete = async (id: string) => {
    try {
      const res = await fetch(`http://localhost:8000/summary/response/${id}`, {
        method: "GET",
      });

      if (!res.ok) throw new Error("Failed to mark as complete");

      const updated = await res.json();

      // Update the local state
      // setData((prev) =>
      //   prev.map((item) => (item._id === id ? { ...item, transcript: updated.transcript } : item))
      // );
    } catch (error) {
      console.error("Error:", error);
    }
  };


  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`http://localhost:8000/responses/${user?.email}`);
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
          <CardContent className="p-4 mx-8">
            <h3 className="text-lg font-semibold text-slate-900">{res.interview_url}</h3>
            <p className="text-sm text-slate-600">Assigned by {res.question.creator_email}</p>
            <p className="my-5 text-sm text-slate-600">Summary: {res.summary}</p>
            <Badge
              className={
                res.transcript
                  ? "bg-green-100 text-green-700 border-green-200"
                  : "bg-yellow-100 text-yellow-700 border-yellow-200"
              }
              variant="secondary"
            >
              {res.transcript ? "Completed" : "Pending"}
            </Badge>

            {!res.transcript && (
              <button
                className="
                  mt-2
                  ml-10
                  px-4
                  py-1.5
                  rounded-md
                  bg-blue-600
                  text-white
                  text-sm
                  font-medium
                  hover:bg-blue-700
                  focus:outline-none
                  focus:ring-2
                  focus:ring-blue-500
                  focus:ring-offset-1
                  transition
                  disabled:opacity-50
                  disabled:cursor-not-allowed
                "
                onClick={() => markAsComplete(res._id)}
                disabled={res.transcript !== null} // disable if already completed
              >
                Mark as Complete
              </button>

            )}
          </CardContent>

        </Card>
      ))}
    </div>
  );
}
