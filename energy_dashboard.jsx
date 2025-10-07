import React, { useState, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Battery, Sun, Wind, Zap, Cloud, Database } from 'lucide-react';
import { motion } from 'framer-motion';

export default function EnergyDashboard() {
  const [data, setData] = useState([]);
  const [solar, setSolar] = useState(0);
  const [wind, setWind] = useState(0);
  const [grid, setGrid] = useState(0);
  const [battery, setBattery] = useState(60);

  useEffect(() => {
    // Simulate real-time energy data updates
    const interval = setInterval(() => {
      const newData = {
        time: new Date().toLocaleTimeString(),
        solar: Math.random() * 80 + 20,
        wind: Math.random() * 60 + 10,
        demand: Math.random() * 100 + 30,
      };
      setData(prev => [...prev.slice(-9), newData]);
      setSolar(newData.solar);
      setWind(newData.wind);
      setGrid(Math.max(0, newData.demand - (newData.solar + newData.wind)));
      setBattery(Math.min(100, Math.max(0, battery + (newData.solar - newData.demand) / 10)));
    }, 3000);

    return () => clearInterval(interval);
  }, [battery]);

  return (
    <div className="p-6 bg-gradient-to-br from-sky-50 to-indigo-100 min-h-screen">
      <motion.h1 className="text-4xl font-bold mb-6 text-center" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>Campus Smart Energy Dashboard</motion.h1>
      
      <div className="grid md:grid-cols-4 gap-4 mb-6">
        <Card className="shadow-xl">
          <CardContent className="flex items-center justify-between p-4">
            <Sun className="text-yellow-500" size={40} />
            <div>
              <p className="text-sm text-gray-500">Solar Power</p>
              <p className="text-2xl font-semibold">{solar.toFixed(1)} kW</p>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-xl">
          <CardContent className="flex items-center justify-between p-4">
            <Wind className="text-blue-500" size={40} />
            <div>
              <p className="text-sm text-gray-500">Wind Power</p>
              <p className="text-2xl font-semibold">{wind.toFixed(1)} kW</p>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-xl">
          <CardContent className="flex items-center justify-between p-4">
            <Battery className="text-green-600" size={40} />
            <div>
              <p className="text-sm text-gray-500">Battery SOC</p>
              <p className="text-2xl font-semibold">{battery.toFixed(0)}%</p>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-xl">
          <CardContent className="flex items-center justify-between p-4">
            <Zap className="text-red-500" size={40} />
            <div>
              <p className="text-sm text-gray-500">Grid Import</p>
              <p className="text-2xl font-semibold">{grid.toFixed(1)} kW</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="shadow-lg">
        <CardContent className="p-4">
          <h2 className="text-xl font-semibold mb-2 flex items-center"><Database className="mr-2 text-indigo-500" /> Real-Time Energy Flow</h2>
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="solar" stroke="#facc15" name="Solar (kW)" />
              <Line type="monotone" dataKey="wind" stroke="#38bdf8" name="Wind (kW)" />
              <Line type="monotone" dataKey="demand" stroke="#ef4444" name="Demand (kW)" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="flex justify-center mt-6">
        <Button className="px-6 py-2 text-lg bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl shadow-md">Export Carbon Report (PDF)</Button>
      </div>
    </div>
  );
}
