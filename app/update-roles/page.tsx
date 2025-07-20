"use client";

import { useEffect, useState } from "react";
import { useUser } from "@auth0/nextjs-auth0";

export default function UpdateRolesPage() {
  const { user, isLoading } = useUser();
  const [allRoles, setAllRoles] = useState<{ _id: string; name: string }[]>([]);
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (isLoading) return;
    if (!user) {
      window.location.href = "/auth/login";
      return;
    }

    // Fetch all available roles
    fetch("http://localhost:8000/roles/roles")
      .then((res) => res.json())
      .then((data) => setAllRoles(data))
      .catch((err) => console.error("Failed to fetch roles:", err));

    // Fetch current user roles
    fetch(`http://localhost:8000/users/${user.email}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.role_ids) {
          setSelectedRoles(data.role_ids);
        }
      })
      .catch((err) => console.error("Failed to fetch user roles:", err));
  }, [user, isLoading]);

  if (isLoading) return <p>Loading...</p>;
  if (!user) return <p>Redirecting to login...</p>;

  const toggleRole = (roleId: string) => {
    setSelectedRoles((prev) =>
      prev.includes(roleId) ? prev.filter((r) => r !== roleId) : [...prev, roleId]
    );
  };

  // Here is the saveRoles function you need
  const saveRoles = async () => {
    try {
      const res = await fetch(`http://localhost:8000/users/${user.email}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_ids: selectedRoles }),
      });

      if (!res.ok) {
        let errorMsg = "Unknown error";
        try {
            const errData = await res.json();
            errorMsg = JSON.stringify(errData);
        } catch {
            // fallback, no JSON body
        }
        setMessage(`Failed: ${errorMsg}`);
        return;
        }

      const data = await res.json();
      setMessage(data.message || "Roles updated successfully!");
    } catch (error) {
      setMessage(`Error updating roles: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", padding: "1rem", border: "1px solid #ccc" }}>
      <h1>Update Your Roles</h1>
      <p>Logged in as: {user.email}</p>

      {allRoles.length === 0 ? (
        <p>No roles available.</p>
      ) : (
        allRoles.map((role) => (
          <label key={role._id} style={{ display: "block", marginBottom: 4 }}>
            <input
              type="checkbox"
              checked={selectedRoles.includes(role._id)}
              onChange={() => toggleRole(role._id)}
            />{" "}
            {role.name}
          </label>
        ))
      )}

      <button onClick={saveRoles} style={{ marginTop: 16, padding: "8px 16px" }}>
        Save Roles
      </button>

      {message && <p style={{ marginTop: 12 }}>{message}</p>}
    </div>
  );
}
