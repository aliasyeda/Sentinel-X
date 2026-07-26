import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import StrategicAnalysis from '../components/StrategicAnalysis';
import IncidentTimeline from '../components/IncidentTimeline';
import ReasoningEngine from '../components/ReasoningEngine';
import KnowledgeSystem from '../components/KnowledgeSystem';
import GovernancePanel from '../components/GovernancePanel';
import ActionPanel from '../components/ActionPanel';
import { fetchActivityData, fetchSystemNodes } from '../services/mockData';
import { fetchSystemStatus } from '../services/dataService';
import { ShieldCheck, Activity, AlertTriangle, Cpu, Globe, Server } from 'lucide-react';
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';
import { useDemo, PHASES } from '../context/DemoContext';
import { ScanLine } from '../components/AnimatedComponents';

const Overview = () => {
    const { phase, logs } = useDemo(); // logs used in IncidentTimeline now, but we keep it here if needed or clear unused
    const [stats, setStats] = useState(null);
    const [activity, setActivity] = useState([]);
    const [nodes, setNodes] = useState([]);

    // Load initial data
    useEffect(() => {
        const loadData = async () => {
            const statusData = await fetchSystemStatus();
            setStats(statusData);
            setActivity(fetchActivityData());
            setNodes(fetchSystemNodes());
        };
        loadData();

        const interval = setInterval(() => {
            // Refresh status frequently
            loadData();
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    // Update data based on simulation phase
    useEffect(() => {
        if (!stats) return;

        if (phase === PHASES.ATTACK) {
            setStats(prev => ({ ...prev, status: 'CRITICAL', activeThreats: 142, health: 45.2 }));
            setActivity(prev => {
                const newData = [...prev];
                newData[newData.length - 1] = { time: 'Now', traffic: 9800, threats: 850 };
                return newData;
            });
        } else if (phase === PHASES.DEFENDING) {
            setStats(prev => ({ ...prev, status: 'MITIGATING', autonomyLevel: 'ENGAGED' }));
        } else if (phase === PHASES.RESTORED) {
            setStats(prev => ({ ...prev, status: 'SECURE', activeThreats: 0, health: 99.1 }));
            setActivity(fetchActivityData()); // Reset chart
        }
    }, [phase]);

    if (!stats) return <div className="p-8 text-[var(--text-dim)]">Loading Telementry...</div>;

    const isCritical = phase === PHASES.ATTACK;

    return (
        <div className="space-y-6 animate-fade-in relative pb-10">
            {/* Background Scanline for Grid */}
            <ScanLine active={phase === PHASES.ANALYZING} />

            {/* Top Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="System Status"
                    value={stats.status}
                    icon={ShieldCheck}
                    status={isCritical ? 'critical' : 'success'}
                    subtext={isCritical ? 'MULTIPLE INCURSIONS DETECTED' : 'All systems operational'}
                />
                <StatCard
                    title="Active Threat Vectors"
                    value={stats.activeThreats}
                    icon={AlertTriangle}
                    status={stats.activeThreats > 0 ? 'critical' : 'neutral'}
                    trend={stats.activeThreats > 0 ? 999 : 0}
                />
                <StatCard
                    title="Network Load"
                    value={isCritical ? '99% (SATURATED)' : stats.networkLoad}
                    icon={Activity}
                    status={isCritical ? 'warning' : 'info'}
                    trend={isCritical ? 400 : 12}
                />
                <StatCard
                    title="AI Autonomy"
                    value={phase === PHASES.DEFENDING ? 'ACTIVE DEFENSE' : stats.autonomyLevel}
                    icon={Cpu}
                    status="warning"
                    subtext="Countermeasures Enabled"
                />
            </div>

            {/* Strategic Analysis Pipeline (Agents 1-5) */}
            <StrategicAnalysis />

            {/* MIDDLE ROW: PERCEPTION & REASONING & CONTROL */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[350px]">

                {/* 1. PERCEPTION (Traffic) - Width 3 */}
                <div className="lg:col-span-3 flex flex-col">
                    <Card
                        title="Perception: Telemetry"
                        className={`flex-1 transition-all duration-500 ${isCritical ? 'border-[var(--neon-red)]' : ''}`}
                    >
                        <div className="h-full w-full pt-4">
                            <ResponsiveContainer width="100%" height="90%">
                                <AreaChart data={activity}>
                                    <defs>
                                        <linearGradient id="colorTraffic" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor={isCritical ? 'var(--neon-red)' : 'var(--neon-blue)'} stopOpacity={0.3} />
                                            <stop offset="95%" stopColor={isCritical ? 'var(--neon-red)' : 'var(--neon-blue)'} stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis dataKey="time" hide />
                                    <YAxis hide />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-color)', borderRadius: '8px', fontSize: '10px' }}
                                        itemStyle={{ color: 'var(--text-primary)' }}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="traffic"
                                        stroke={isCritical ? 'var(--neon-red)' : 'var(--neon-blue)'}
                                        strokeWidth={2}
                                        fillOpacity={1}
                                        fill="url(#colorTraffic)"
                                        animationDuration={1000}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </Card>
                </div>

                {/* 2. REASONING (The Brain) - Width 5 */}
                <div className="lg:col-span-6">
                    <ReasoningEngine />
                </div>

                {/* 3. GOVERNANCE (The Control) - Width 3 */}
                <div className="lg:col-span-3">
                    <GovernancePanel />
                </div>
            </div>

            {/* BOTTOM ROW: KNOWLEDGE & ACTION & EVENTS */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[300px]">

                {/* 1. KNOWLEDGE (Memory) - Width 4 */}
                <div className="lg:col-span-4">
                    <KnowledgeSystem />
                </div>

                {/* 2. ACTION (Execution) - Width 4 */}
                <div className="lg:col-span-4">
                    <ActionPanel />
                </div>

                {/* 3. TIMELINE (Events) - Width 4 */}
                <div className="lg:col-span-4">
                    <IncidentTimeline />
                </div>
            </div>
        </div>
    );
};

export default Overview;
