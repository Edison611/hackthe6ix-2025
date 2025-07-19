import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Calendar, Edit, MoreHorizontal, Send, Users } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface CreatedInterview {
  id: string
  title: string
  position: string
  createdDate: string
  sentTo: number
  completed: number
  status: "Draft" | "Sent" | "Active"
  description: string
}

const mockCreatedInterviews: CreatedInterview[] = [
  {
    id: "1",
    title: "Frontend Developer Assessment",
    position: "Senior Frontend Developer",
    createdDate: "2024-01-10",
    sentTo: 5,
    completed: 3,
    status: "Active",
    description: "Technical assessment focusing on React, TypeScript, and system design",
  },
  {
    id: "2",
    title: "Backend Engineering Interview",
    position: "Backend Engineer",
    createdDate: "2024-01-12",
    sentTo: 3,
    completed: 1,
    status: "Active",
    description: "Deep dive into Node.js, databases, and API design principles",
  },
  {
    id: "3",
    title: "UX Design Portfolio Review",
    position: "UX Designer",
    createdDate: "2024-01-08",
    sentTo: 4,
    completed: 4,
    status: "Sent",
    description: "Portfolio presentation and design thinking process evaluation",
  },
  {
    id: "4",
    title: "Product Manager Strategy Session",
    position: "Product Manager",
    createdDate: "2024-01-14",
    sentTo: 0,
    completed: 0,
    status: "Draft",
    description: "Strategic thinking and product roadmap planning discussion",
  },
]

export function CreatedInterviews() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-900">Created Interviews</h2>
        <div className="flex gap-2">
          <Badge variant="secondary" className="bg-blue-100 text-blue-700">
            {mockCreatedInterviews.filter((i) => i.status === "Active").length} Active
          </Badge>
          <Badge variant="secondary" className="bg-amber-100 text-amber-700">
            {mockCreatedInterviews.filter((i) => i.status === "Draft").length} Drafts
          </Badge>
        </div>
      </div>

      <div className="grid gap-4">
        {mockCreatedInterviews.map((interview) => (
          <Card key={interview.id} className="hover:shadow-lg transition-all duration-200 border-slate-200 bg-white">
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="space-y-3 flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="font-semibold text-lg text-slate-900">{interview.title}</h3>
                    <Badge
                      variant="secondary"
                      className={
                        interview.status === "Active"
                          ? "bg-green-100 text-green-800 border-green-200"
                          : interview.status === "Sent"
                            ? "bg-blue-100 text-blue-800 border-blue-200"
                            : "bg-amber-100 text-amber-800 border-amber-200"
                      }
                    >
                      {interview.status}
                    </Badge>
                  </div>

                  <p className="text-slate-600 font-medium">{interview.position}</p>
                  <p className="text-slate-500 text-sm leading-relaxed">{interview.description}</p>

                  <div className="flex items-center gap-6 text-sm text-slate-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      Created {interview.createdDate}
                    </div>
                    <div className="flex items-center gap-1">
                      <Send className="w-4 h-4" />
                      Sent to {interview.sentTo} candidates
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="w-4 h-4" />
                      {interview.completed} completed
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 ml-4">
                  <Button variant="outline" size="sm" className="gap-2 hover:bg-slate-50 bg-transparent">
                    <Edit className="w-4 h-4" />
                    Edit
                  </Button>

                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm">
                        <MoreHorizontal className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>View Details</DropdownMenuItem>
                      <DropdownMenuItem>Duplicate</DropdownMenuItem>
                      <DropdownMenuItem>Send to More</DropdownMenuItem>
                      <DropdownMenuItem className="text-red-600">Delete</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>

              {interview.sentTo > 0 && (
                <div className="mt-4 pt-4 border-t border-slate-100">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">Completion Rate</span>
                    <span className="font-medium text-slate-900">
                      {Math.round((interview.completed / interview.sentTo) * 100)}%
                    </span>
                  </div>
                  <div className="mt-2 w-full bg-slate-100 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${(interview.completed / interview.sentTo) * 100}%` }}
                    />
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
