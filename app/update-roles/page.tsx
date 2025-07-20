"use client";

import { useEffect, useState } from "react";
import { useUser } from "@auth0/nextjs-auth0";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { all } from "axios";

export default function UpdateRolesPage() {
  const { user, isLoading } = useUser();
  const [allRoles, setAllRoles] = useState<{ id: string; name: string }[]>([]);
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);
  const [message, setMessage] = useState("");
  const [loadingSave, setLoadingSave] = useState(false);

  console.log(allRoles);

  console.log(selectedRoles)

  useEffect(() => {
    if (isLoading) return;
    if (!user) {
      window.location.href = "/auth/login";
      return;
    }

    const fetchData = async () => {
      try {
        const rolesRes = await fetch("http://localhost:8000/roles");
        const roles = await rolesRes.json();
        setAllRoles(roles);

        const userRes = await fetch(`http://localhost:8000/users/${user.email}`);
        const userData = await userRes.json();
        setSelectedRoles(userData.role_ids || []);
      } catch (err) {
        console.error("Error loading roles or user data:", err);
      }
    };

    fetchData();
  }, [user, isLoading]);

  const toggleRole = (roleId: string, checked: boolean) => {
  if (!roleId) return; // safeguard

  setSelectedRoles((prev) =>
    checked ? [...prev, roleId] : prev.filter((r) => r !== roleId)
  );
};


  const saveRoles = async () => {
    setLoadingSave(true);
    try {
      const res = await fetch(`http://localhost:8000/users/${user?.email}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_ids: selectedRoles }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        const errorMsg = errData.message || "Unknown error";
        setMessage(`❌ Failed: ${errorMsg}`);
        return;
      }

      const data = await res.json();
      setMessage(`✅ ${data.message || "Roles updated successfully!"}`);
    } catch (error) {
      setMessage(`❌ ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
      setLoadingSave(false);
    }
  };

  if (isLoading || !user) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader2 className="animate-spin h-6 w-6 text-gray-500" />
        <span className="ml-2 text-gray-600">Loading...</span>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto mt-10 p-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Update Your Roles</CardTitle>
          <p className="text-sm text-muted-foreground">Logged in as: {user.email}</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {allRoles.length === 0 ? (
              <p>No roles available.</p>
            ) : (
              allRoles.map((role) => (
                <div key={role.id} className="flex items-center space-x-2 mb-2">
                  <Checkbox
                    key={role.id}
                    id={role.id}
                    checked={selectedRoles.includes(role.id)}
                    onCheckedChange={(checked) => toggleRole(role.id, Boolean(checked))}
                  />
                  <label htmlFor={role.id} className="text-sm">
                    {role.name}
                  </label>
                </div>
))
            )}

            <Button onClick={saveRoles} disabled={loadingSave} className="mt-4 w-full">
              {loadingSave ? (
                <>
                  <Loader2 className="animate-spin h-4 w-4 mr-2" />
                  Saving...
                </>
              ) : (
                "Save Roles"
              )}
            </Button>

            {message && (
              <p
                className={`text-sm mt-2 ${
                  message.startsWith("✅") ? "text-green-600" : "text-red-600"
                }`}
              >
                {message}
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
