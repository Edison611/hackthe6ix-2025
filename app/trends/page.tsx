import { useEffect, useState } from "react";
import axios from "axios";

export default function Trends() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    const fetchTrends = async () => {
      const res = await axios.get("http://localhost:8000/trends");
      setTrends(res.data.trends);
    };
    fetchTrends();
  }, []);

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Trends</h1>
      <ul className="space-y-4">
        {trends.map((trend: any, index: number) => (
          <li key={index} className="p-4 border rounded bg-white">
            <h3 className="text-lg font-semibold">{trend.theme}</h3>
            <p>{trend.description}</p>
            <p className="text-sm text-gray-500">Mentions: {trend.count}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
