import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-gradient-to-br from-slate-50 to-slate-100">
        <AppSidebar />
        <main className="flex-1 p-6">
          <SidebarTrigger className="mb-4" />

          <div className="space-y-4">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">
              Welcome to Interview Central
            </h1>
            <p className="text-slate-600 text-lg max-w-2xl">
              Your centralized platform for creating, managing, and analyzing interviews. Start organizing your process efficiently with a few clicks.
            </p>

            <div className="flex space-x-4 mt-6">
              <Button className="bg-slate-900 text-white hover:bg-slate-700">
                View All Interviews
              </Button>
              <Button variant="outline" className="border-slate-900 text-slate-900 hover:bg-slate-100">
                Create New Interview
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">
              <FeatureCard
                title="Smart Organization"
                description="Easily group, filter, and prioritize interviews using custom tags and smart sorting."
              />
              <FeatureCard
                title="Real-Time Collaboration"
                description="Invite teammates, share notes, and work together in real-time."
              />
              <FeatureCard
                title="Analytics Dashboard"
                description="Track candidate performance and process efficiency with detailed metrics."
              />
              <FeatureCard
                title="Secure Data Storage"
                description="Your data is encrypted and stored securely with best-in-class infrastructure."
              />
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  )
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="text-xl font-semibold text-slate-900">{title}</h3>
      <p className="text-slate-600 mt-2">{description}</p>
    </div>
  )
}
