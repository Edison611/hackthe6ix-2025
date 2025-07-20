"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Plus, Trash2, Users } from "lucide-react"
import { useUser } from "@auth0/nextjs-auth0"

interface Role {
    id: string
    name: string
}

interface Question {
  id: string
  text: string
}

interface CreateInterviewDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const availableRoles = [
  "Frontend Developer",
  "Backend Developer",
  "Full Stack Developer",
  "DevOps Engineer",
  "Data Scientist",
  "Product Manager",
  "UX/UI Designer",
  "QA Engineer",
  "Mobile Developer",
  "System Architect",
]

export function CreateInterviewDialog({ open, onOpenChange }: CreateInterviewDialogProps) {
    const { user, isLoading } = useUser()
    console.log(user);
  const [interviewTitle, setInterviewTitle] = useState("")
  const [questions, setQuestions] = useState<Question[]>([{ id: "1", text: "" }])
  const [selectedRoles, setSelectedRoles] = useState<Role[]>([])
  const [description, setDescription] = useState("")
  const [roles, setRoles] = useState<Role[]>([])

  console.log(roles)    
//   console.log(roles ? roles[0].name : null)

  useEffect(() => {
    const fetchRoles = async () => {
      const res = await fetch("http://localhost:8000/roles")
      const data = await res.json()
      setRoles(data)
    }

    fetchRoles()
  }, [])

  const addQuestion = () => {
    const newQuestion: Question = {
      id: Date.now().toString(),
      text: "",
    }
    setQuestions([...questions, newQuestion])
  }

  const removeQuestion = (id: string) => {
    if (questions.length > 1) {
      setQuestions(questions.filter((q) => q.id !== id))
    }
  }

  const updateQuestion = (id: string, text: string) => {
    setQuestions(questions.map((q) => (q.id === id ? { ...q, text } : q)))
  }

  const toggleRole = (role: Role) => {
    setSelectedRoles((prev) => (prev.includes(role) ? prev.filter((r) => r !== role) : [...prev, role]))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const interviewData = {
      title: interviewTitle,
      questions: questions.map((q) => q.text),
      creator_email: user?.email || "<unknown>",
      roles: selectedRoles.map((role) => role.id),
    }

    console.log("Interview Data:", interviewData)

    console.log("Creating interview:", interviewData)

    // Reset form
    setInterviewTitle("")
    setQuestions([{ id: "1", text: "" }])
    setSelectedRoles([])
    setDescription("")

    // Close dialog
    onOpenChange(false)

    try {
      const res = await fetch("http://localhost:8000/interviews", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(interviewData),
      })

      const data = await res.json()
      console.log(data)
    } catch (err) {
      console.error("Error posting data:", err)
    }

    alert("Interview created successfully!")
  }

  const isFormValid =
    interviewTitle.trim() !== "" && questions.some((q) => q.text.trim() !== "") && selectedRoles.length > 0

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">
            Create New Interview
          </DialogTitle>
          <DialogDescription>Design your interview questions and assign target roles for candidates.</DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Interview Title */}
          <div className="space-y-2">
            <Label htmlFor="title" className="text-sm font-medium text-slate-700">
              Interview Title *
            </Label>
            <Input
              id="title"
              placeholder="e.g., Senior Frontend Developer Assessment"
              value={interviewTitle}
              onChange={(e) => setInterviewTitle(e.target.value)}
              className="border-slate-200 focus:border-slate-400"
            />
          </div>

          {/* Target Roles */}
          <div className="space-y-3">
            <Label className="text-sm font-medium text-slate-700 flex items-center gap-2">
              <Users className="w-4 h-4" />
              Target Roles * (Select all applicable roles)
            </Label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {roles.map((role) => (
                <div
                  key={role.id}
                  onClick={() => toggleRole(role)}
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                    selectedRoles.includes(role)
                      ? "border-slate-900 bg-slate-900 text-white"
                      : "border-slate-200 hover:border-slate-300 bg-white"
                  }`}
                >
                  <span className="text-sm font-medium">{role.name}</span>
                </div>
              ))}
            </div>
            {selectedRoles.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {selectedRoles.map((role) => (
                  <Badge key={role.id} variant="secondary" className="bg-slate-100 text-slate-700 hover:bg-slate-200">
                    {role.name}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Questions */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium text-slate-700">Interview Questions * (Minimum 1 required)</Label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addQuestion}
                className="gap-2 hover:bg-slate-50 bg-transparent"
              >
                <Plus className="w-4 h-4" />
                Add Question
              </Button>
            </div>

            <div className="space-y-3">
              {questions.map((question, index) => (
                <div key={question.id} className="flex gap-3 items-start">
                  <div className="flex-1 space-y-2">
                    <Label className="text-xs text-slate-500">Question {index + 1}</Label>
                    <Textarea
                      placeholder="Enter your interview question here..."
                      value={question.text}
                      onChange={(e) => updateQuestion(question.id, e.target.value)}
                      className="border-slate-200 focus:border-slate-400 min-h-[100px]"
                    />
                  </div>
                  {questions.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => removeQuestion(question.id)}
                      className="mt-6 text-red-500 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} className="hover:bg-slate-50">
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!isFormValid}
            className="bg-gradient-to-r from-slate-900 to-slate-700 hover:from-slate-800 hover:to-slate-600 text-white"
          >
            Create Interview
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
