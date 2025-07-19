import Link from "next/link";

export default function Home() {
  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-4xl font-bold mb-4">InsightLoop</h1>
      <p className="mb-4">Turn async standups into product and team insights using Ribbon AI.</p>
      <div className="flex flex-col gap-4">
        <Link href="/dashboard" className="text-blue-500 underline">Go to Dashboard</Link>
        <Link href="/trends" className="text-blue-500 underline">View Trends</Link>
      </div>
    </div>
  );
}