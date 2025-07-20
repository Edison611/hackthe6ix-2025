"use client"

import { Calendar, FileText, Home, Plus, Settings, Users, Mic, BarChart3 } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { useState } from "react"
import { CreateInterviewDialog } from "@/components/Create_Interview_Dialog"
import { useUser } from "@auth0/nextjs-auth0"

const menuItems = [
  {
    title: "Dashboard",
    url: "/dashboard",
    icon: Home,
  },
  {
    title: "Update Roles",      // <-- New tab added here
    url: "/update-roles",
    icon: Users,
  },
]

export function AppSidebar() {
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const { user } = useUser()

  return (
    <Sidebar className="border-r border-slate-200">
      <SidebarHeader className="p-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-slate-900 to-slate-700 rounded-xl flex items-center justify-center">
            <Mic className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">CommonRoom</h2>
            <p className="text-sm text-slate-500">Simplify Your Meetings</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-2">
              <SidebarMenuItem>
                <SidebarMenuButton
                  onClick={() => setCreateDialogOpen(true)}
                  className="bg-gradient-to-r from-slate-900 to-slate-700 text-white hover:from-slate-800 hover:to-slate-600 shadow-lg transition-all duration-200"
                >
                  <div className="flex items-center gap-3 px-4 py-3 rounded-lg w-full">
                    <Plus className="w-5 h-5 text-white" />
                    <span className="font-medium text-white">Create</span>
                  </div>
                </SidebarMenuButton>
              </SidebarMenuItem>

              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild className="hover:bg-slate-100 transition-all duration-200">
                    <a href={item.url} className="flex items-center gap-3 px-4 py-3 rounded-lg">
                      <item.icon className="w-5 h-5 text-slate-600" />
                      <span className="font-medium text-slate-700">{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}

              {user ? (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild className="hover:bg-slate-100 transition-all duration-200">
                    <a href="/auth/logout" className="flex items-center gap-3 px-4 py-3 rounded-lg">
                      <Settings className="w-5 h-5 text-slate-600" />
                      <span className="font-medium text-slate-700">Logout ({user.email})</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ) : (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild className="hover:bg-slate-100 transition-all duration-200">
                    <a href="/auth/login" className="flex items-center gap-3 px-4 py-3 rounded-lg">
                      <Settings className="w-5 h-5 text-slate-600" />
                      <span className="font-medium text-slate-700">Login</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <CreateInterviewDialog open={createDialogOpen} onOpenChange={setCreateDialogOpen} />
    </Sidebar>
  )
}
