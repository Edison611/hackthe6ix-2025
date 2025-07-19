// components/Navbar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const linkClass = (path: string) =>
    `px-3 py-2 rounded-md font-medium cursor-pointer ${
      pathname === path
        ? "bg-white text-blue-600 shadow-md"
        : "text-white hover:bg-blue-500 hover:bg-opacity-80"
    }`;

  return (
    <nav className="bg-blue-600 text-white p-4 flex space-x-4 shadow-md">
      <Link href="/" className={linkClass("/")}>
        Home
      </Link>
      <Link href="/dashboard" className={linkClass("/dashboard")}>
        Dashboard
      </Link>
      <Link href="/trends" className={linkClass("/trends")}>
        Trends
      </Link>
      <a href="/auth/login">Login</a>
      <a href="/auth/logout">Logout</a>
    </nav>
  );
}
