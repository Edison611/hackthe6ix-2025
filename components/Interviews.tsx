import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Calendar, Clock, Play, User, Volume2 } from "lucide-react"

interface Interview {
  id: string
  candidateName: string
  position: string
  date: string
  time: string
  status: "Pending" | "Complete"
  audioUrl?: string
  avatar?: string
  duration?: string
  interviewer: string
}

const mockInterviews: Interview[] = [
  {
    id: "1",
    candidateName: "Sarah Johnson",
    position: "Frontend Developer",
    date: "2024-01-15",
    time: "10:00 AM",
    status: "Complete",
    audioUrl: "/audio/interview-1.mp3",
    avatar: "/placeholder.svg?height=40&width=40",
    duration: "45 min",
    interviewer: "John Smith",
  },
  {
    id: "2",
    candidateName: "Michael Chen",
    position: "Backend Engineer",
    date: "2024-01-16",
    time: "2:00 PM",
    status: "Pending",
    avatar: "/placeholder.svg?height=40&width=40",
    interviewer: "Emily Davis",
  },
  {
    id: "3",
    candidateName: "Jessica Williams",
    position: "UX Designer",
    date: "2024-01-14",
    time: "11:30 AM",
    status: "Complete",
    audioUrl: "/audio/interview-3.mp3",
    avatar: "/placeholder.svg?height=40&width=40",
    duration: "38 min",
    interviewer: "Alex Thompson",
  },
  {
    id: "4",
    candidateName: "David Rodriguez",
    position: "Product Manager",
    date: "2024-01-17",
    time: "3:30 PM",
    status: "Pending",
    avatar: "/placeholder.svg?height=40&width=40",
    interviewer: "Sarah Wilson",
  },
]

export function Interviews() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-slate-900">All Interviews</h2>
        <div className="flex gap-2">
          <Badge variant="secondary" className="bg-slate-100 text-slate-700">
            {mockInterviews.filter((i) => i.status === "Pending").length} Pending
          </Badge>
          <Badge variant="secondary" className="bg-green-100 text-green-700">
            {mockInterviews.filter((i) => i.status === "Complete").length} Complete
          </Badge>
        </div>
      </div>

      <div className="grid gap-4">
        {mockInterviews.map((interview) => (
          <Card key={interview.id} className="hover:shadow-lg transition-all duration-200 border-slate-200 bg-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Avatar className="w-12 h-12 ring-2 ring-slate-100">
                    <AvatarImage src={interview.avatar || "/placeholder.svg"} alt={interview.candidateName} />
                    <AvatarFallback className="bg-gradient-to-br from-slate-100 to-slate-200 text-slate-700">
                      {interview.candidateName
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>

                  <div className="space-y-1">
                    <h3 className="font-semibold text-lg text-slate-900">{interview.candidateName}</h3>
                    <p className="text-slate-600 font-medium">{interview.position}</p>
                    <div className="flex items-center gap-4 text-sm text-slate-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {interview.date}
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {interview.time}
                      </div>
                      <div className="flex items-center gap-1">
                        <User className="w-4 h-4" />
                        {interview.interviewer}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  {interview.status === "Complete" && interview.audioUrl && (
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm" className="gap-2 hover:bg-slate-50 bg-transparent">
                        <Play className="w-4 h-4" />
                        Play Recording
                      </Button>
                      {interview.duration && (
                        <div className="flex items-center gap-1 text-sm text-slate-500">
                          <Volume2 className="w-4 h-4" />
                          {interview.duration}
                        </div>
                      )}
                    </div>
                  )}

                  <Badge
                    variant={interview.status === "Complete" ? "default" : "secondary"}
                    className={
                      interview.status === "Complete"
                        ? "bg-green-100 text-green-800 hover:bg-green-200 border-green-200"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200 border-slate-200"
                    }
                  >
                    {interview.status}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
