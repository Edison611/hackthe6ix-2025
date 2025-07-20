import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/Sidebar"
import { ForMe } from "@/components/ForMe"
import { Interviews } from "@/components/Interviews"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function Dashboard() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-gradient-to-br from-slate-50 to-slate-100">
        <AppSidebar />
        <main className="flex-1 p-6">
          <div className="mb-6">
            <SidebarTrigger className="mb-4" />
            <div className="space-y-2">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">
                Interview Dashboard
              </h1>
              <p className="text-slate-600 text-lg">Manage and track your interviews</p>
            </div>
          </div>

          <Tabs defaultValue="all-interviews" className="space-y-6">
            <TabsList className="grid w-full max-w-md grid-cols-2 bg-white shadow-sm">
              <TabsTrigger
                value="all-interviews"
                className="data-[state=active]:bg-slate-900 data-[state=active]:text-white"
              >
                Created by Me
              </TabsTrigger>
              <TabsTrigger value="created" className="data-[state=active]:bg-slate-900 data-[state=active]:text-white">
                For Me
              </TabsTrigger>
            </TabsList>

            <TabsContent value="all-interviews" className="space-y-6">
              <Interviews />
            </TabsContent>

            <TabsContent value="created" className="space-y-6">
              <ForMe />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </SidebarProvider>
  )
}
