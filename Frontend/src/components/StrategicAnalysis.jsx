import React, { useState, useEffect } from 'react';
import { fetchRootCause } from '../services/dataService';
import {
    BrainCircuit,
    Zap,
    ShieldCheck,
    Eye,
    Lock,
    Unlock,
    AlertTriangle,
    CheckCircle2,
    GitBranch
} from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import Card from './Card';
import { PulsingDot, TypewriterText } from './AnimatedComponents';

const PipelineStep = ({ icon: Icon, label, isActive, isCompleted, isPending, index }) => (
    <div className={`flex flex-col items-center relative z-10 transition-all duration-500 ${isActive ? 'scale-110' : 'scale-100 opacity-70'}`}>
        <div
            className={`w-12 h-12 rounded-full flex items-center justify-center border-2 mb-2 transition-all duration-500
            ${isActive
                    ? 'bg-[rgba(0,234,255,0.1)] border-[var(--neon-blue)] shadow-[0_0_15px_var(--neon-blue)]'
                    : isCompleted
                        ? 'bg-[rgba(0,255,157,0.05)] border-[var(--neon-green)] text-[var(--neon-green)]'
                        : 'bg-[rgba(255,255,255,0.02)] border-[rgba(255,255,255,0.1)] text-[var(--text-dim)]'
                }
            ${isPending ? 'animate-pulse border-[var(--neon-orange)] text-[var(--neon-orange)]' : ''}
            `}
        >
            <Icon size={20} className={isActive ? 'animate-pulse' : ''} />
        </div>
        <span className={`text-[10px] uppercase font-bold tracking-wider ${isActive ? 'text-[var(--neon-blue)]' : 'text-[var(--text-dim)]'}`}>
            {label}
        </span>
        {isActive && (
            <div className="absolute top-14 mt-4 w-32 text-center bg-[var(--bg-card)] border border-[var(--border-color)] p-2 rounded text-[10px] text-[var(--text-secondary)] shadow-lg z-50 animate-fade-in">
                Processing...
            </div>
        )}
    </div>
);

const Connector = ({ active, completed }) => (
    <div className="flex-1 h-[2px] mx-2 relative top-[-14px]">
        {/* Base line */}
        <div className="absolute inset-0 bg-[rgba(255,255,255,0.1)] rounded-full"></div>

        {/* Active Beam */}
        <div
            className={`absolute inset-0 transition-all duration-1000 rounded-full ${active
                    ? 'bg-gradient-to-r from-transparent via-[var(--neon-blue)] to-transparent w-full animate-shimmer opacity-100'
                    : completed
                        ? 'bg-[var(--neon-green)] w-full shadow-[0_0_10px_var(--neon-green)] opacity-80'
                        : 'w-0 opacity-0'
                }`}
        ></div>

        {/* Moving Particle if active */}
        {active && (
            <div className="absolute top-1/2 -translate-y-1/2 h-1.5 w-1.5 bg-white rounded-full shadow-[0_0_10px_white] animate-travel-right"></div>
        )}
    </div>
);

const StrategicAnalysis = () => {
    const { phase } = useDemo();
    const [pipelineState, setPipelineState] = useState(0); // 0: Idle, 1-5: Agents
    const [rootCause, setRootCause] = useState(null);

    useEffect(() => {
        const loadRootCause = async () => {
            const data = await fetchRootCause();
            if (data && data.root_causes && data.root_causes.length > 0) {
                setRootCause(data.root_causes[0]); // Take the first major root cause
            }
        };
        loadRootCause();

        const interval = setInterval(() => {
            if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
                loadRootCause();
            }
        }, 2000);
        return () => clearInterval(interval);
    }, [phase]);

    // Simulate pipeline progression during attack
    useEffect(() => {
        if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING) {
            // Rapid progression through 5 steps
            const interval = setInterval(() => {
                setPipelineState(prev => (prev < 5 ? prev + 1 : 1));
            }, 1000); // Faster pulse
            return () => clearInterval(interval);
        } else if (phase === PHASES.DEFENDING) {
            setPipelineState(5); // Actively defending
        } else {
            setPipelineState(0); // Idle
        }
    }, [phase]);

    const isEmergency = phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

            {/* 1. Pipeline Visualization */}
            <div className="lg:col-span-2">
                <Card title="Autonomous Agent Pipeline" className="flex flex-col justify-center relative overflow-hidden">
                    {/* Background flow effect */}
                    <div className="absolute inset-x-0 top-1/2 h-[1px] bg-[rgba(255,255,255,0.05)] z-0"></div>

                    <div className="grid grid-cols-5 gap-2 px-4 py-8 relative z-10 text-center">

                        <PipelineStep
                            icon={Eye}
                            label="Perception Agent"
                            isActive={pipelineState === 1}
                            isCompleted={pipelineState > 1}
                            index={1}
                        />

                        <PipelineStep
                            icon={BrainCircuit}
                            label="Reasoning Agent"
                            isActive={pipelineState === 2}
                            isCompleted={pipelineState > 2}
                            index={2}
                        />

                        <PipelineStep
                            icon={GitBranch}
                            label="Decision Agent"
                            isActive={pipelineState === 3}
                            isCompleted={pipelineState > 3}
                            index={3}
                        />

                        <PipelineStep
                            icon={Lock}
                            label="Autonomy Governor"
                            isActive={pipelineState === 4}
                            isCompleted={pipelineState > 4}
                            index={4}
                        />

                        <PipelineStep
                            icon={Zap}
                            label="Action Agent"
                            isActive={pipelineState === 5}
                            isCompleted={pipelineState > 5}
                            index={5}
                        />
                    </div>
                </Card>
            </div>

            {/* 2. Intelligence Unit (Root Cause + AI Explanation) */}
            <Card title="Intelligence Unit" className="flex flex-col gap-4">

                {/* Autonomy Level */}
                <div className="flex items-center justify-between bg-[rgba(255,255,255,0.03)] p-3 rounded-lg border border-[rgba(255,255,255,0.05)]">
                    <div className="flex items-center gap-3">
                        <div className={`p-2 rounded bg-[rgba(0,234,255,0.1)] text-[var(--neon-blue)]`}>
                            {pipelineState > 2 && isEmergency ? <Unlock size={16} /> : <Lock size={16} />}
                        </div>
                        <div>
                            <div className="text-[10px] uppercase text-[var(--text-dim)] font-bold">Autonomy Level</div>
                            <div className="text-sm font-medium text-[var(--text-primary)]">
                                {isEmergency ? 'Level 4: Human-in-the-Loop' : 'Level 5: Full Autonomy'}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Root Cause / AI Explanation */}
                <div className="flex-1 flex flex-col gap-2">
                    <div className="text-[10px] uppercase text-[var(--text-dim)] font-bold flex items-center gap-2">
                        <BrainCircuit size={12} /> AI Reasoning Logic
                    </div>

                    <div className={`flex-1 rounded-lg border p-3 text-xs leading-relaxed transition-colors duration-500
                        ${isEmergency
                            ? 'bg-[rgba(255,0,0,0.05)] border-[rgba(255,0,0,0.2)] text-[var(--text-primary)]'
                            : 'bg-[rgba(0,255,157,0.02)] border-[rgba(0,255,157,0.1)] text-[var(--text-dim)]'
                        }
                    `}>
                        {/* Backend Integrated Data */}
                        {rootCause ? (
                            <>
                                <div className="mb-2 font-bold text-[var(--neon-red)] flex items-center gap-2 animate-pulse">
                                    <AlertTriangle size={12} /> ROOT CAUSE DETECTED
                                </div>
                                <p className="mb-2 text-xs">
                                    <span className="text-[var(--text-secondary)]">Cause:</span> {rootCause.likely_root_cause}
                                </p>
                                <p className="mb-2 text-xs">
                                    <span className="text-[var(--text-secondary)]">Evidence:</span> {rootCause.evidence?.correlation_strength * 100}% Correlation
                                </p>
                                <p className="text-xs">
                                    <span className="text-[var(--text-secondary)]">Impact:</span> <span className="text-[var(--neon-orange)]">{rootCause.impact_assessment}</span>
                                </p>
                            </>
                        ) : isEmergency ? (
                            // Fallback if no backend data but in emergency
                            <>
                                <div className="mb-2 font-bold text-[var(--neon-red)] flex items-center gap-2">
                                    <AlertTriangle size={12} /> THREAT IDENTIFIED
                                </div>
                                <p className="mb-2">
                                    <span className="text-[var(--text-secondary)]">Root Cause:</span> SQL Injection pattern detected in Auth-Service-04 via Gateway-Tokyo.
                                </p>
                                <p>
                                    <span className="text-[var(--text-secondary)]">Decision:</span> <span className="text-[var(--neon-blue)]">ISOLATE NODE</span> (Confidence: 98.4%).
                                    Action taken to prevent lateral movement.
                                </p>
                            </>
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-center opacity-60">
                                <CheckCircle2 size={24} className="mb-2 text-[var(--neon-green)]" />
                                <p>System operating within normal parameters.</p>
                                <p>Continuous heuristic analysis active.</p>
                            </div>
                        )}
                    </div>
                </div>
            </Card>
        </div>
    );
};

export default StrategicAnalysis;
