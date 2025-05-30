
import { useState, useEffect } from "react";
import axios from "axios";

export default function CrewSchedulerApp() {
  const [crewList, setCrewList] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [monitoring, setMonitoring] = useState([]);

  useEffect(() => {
    fetchCrew();
    fetchSchedule();
    fetchMonitoring();
  }, []);

  const fetchCrew = async () => {
    const res = await axios.get("http://localhost:8000/api/crew");
    setCrewList(res.data);
  };

  const fetchSchedule = async () => {
    const res = await axios.get("http://localhost:8000/api/schedule");
    setSchedule(res.data);
  };

  const fetchMonitoring = async () => {
    const res = await axios.get("http://localhost:8000/api/monitoring");
    setMonitoring(res.data);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="text-3xl font-bold mb-6">Crew Scheduler & Monitoring</header>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="col-span-2">
          <div className="bg-white rounded-2xl shadow-md p-4 mb-4">
            <h2 className="text-xl font-semibold mb-2">Schedule Editor</h2>
            <p className="text-gray-500">Auto and manual schedule inputs, editable breaks, shift assignment, etc.</p>
            <pre className="text-xs text-gray-400">{JSON.stringify(schedule, null, 2)}</pre>
          </div>
          <div className="bg-white rounded-2xl shadow-md p-4">
            <h2 className="text-xl font-semibold mb-2">Monthly Monitoring</h2>
            <p className="text-gray-500">Tracks crew shifts, AWOLs, dailies %, and PDF export option</p>
            <pre className="text-xs text-gray-400">{JSON.stringify(monitoring, null, 2)}</pre>
          </div>
        </div>
        <div>
          <div className="bg-white rounded-2xl shadow-md p-4">
            <h3 className="text-lg font-semibold mb-2">Settings</h3>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Add/Edit Crew</li>
              <li>• Adjust Store Hours</li>
              <li>• Toggle Peak Days</li>
              <li>• Dailies Target: 7.5%</li>
              <li>• Shift Rules (max 6 consecutive days)</li>
            </ul>
          </div>
          <div className="mt-4">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-xl w-full hover:bg-blue-700">Export as PDF</button>
          </div>
        </div>
      </div>
    </div>
  );
}
