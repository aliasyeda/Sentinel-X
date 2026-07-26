import React, { useEffect, useState } from 'react';
import Card from './Card';
import { Shield, Lock, Unlock, Gavel, CheckCircle2, History, ArrowRight } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { fetchGovernance } from '../services/dataService';
import { useNavigate } from 'react-router-dom';

const GovernancePanel = () => {
    const { phase } = useDemo();
    const [data, setData] = useState(null);

    useEffect(() => {
        const loadGovernance = async () => {
            const govData = await fetchGovernance();
            if (govData.length > 0) {
                const latest = govData[0]; // Assuming latest is first or relevant
                // Transform backend data to UI format
                const policies = Object.entries(latest.policy_applied || {}).map(([key, value]) => ({
                    title: key.replace(/_/g, ' '),
                    status: 'Active',
                    value: value
                })).filter(p => !Array.isArray(p.value)); // Simple filter for display

                const logs = govData.map(g => ({
                    id: g.governance_id,
                    action: g.recommended_autonomy_level.replace('_', ' ').toUpperCase(),
                    timestamp: new Date(g.timestamp).toLocaleTimeString(),
                    detail: `Risk Score: ${(g.ai_confidence * 100).toFixed(1)}% | Service: ${g.service}`,
                    user: 'SENTINEL-GOV-AI'
                }));

                setData({ policies, logs });
            }
        };
        loadGovernance();

        const interval = setInterval(() => {
            if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
                loadGovernance();
            }
        }, 2000);
        return () => clearInterval(interval);
    }, [phase]);

    const isEmergency = phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING;
    const isHumanInLoop = isEmergency; // Simulating Human-in-the-loop during emergency

    if (!data) return <Card title="Autonomy Governor"><div className="p-4 text-[var(--text-dim)]">Loading Policies...</div></Card>;

    return (
        <Card title="Autonomy & Governance" className="h-[350px] flex flex-col">

            {/* 1. Autonomy State Header */}
            <div className={`p-4 rounded-lg border mb-3 flex items-center justify-between transition-all duration-500
                ${isHumanInLoop
                    ? 'bg-[rgba(255,165,0,0.05)] border-[var(--neon-orange)]'
                    : 'bg-[rgba(0,255,157,0.05)] border-[var(--neon-green)]'}
            `}>
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-full border ${isHumanInLoop ? 'border-[var(--neon-orange)] bg-[rgba(255,165,0,0.1)]' : 'border-[var(--neon-green)] bg-[rgba(0,255,157,0.1)]'}`}>
                        {isHumanInLoop ? <Lock size={20} className="text-[var(--neon-orange)]" /> : <Unlock size={20} className="text-[var(--neon-green)]" />}
                    </div>
                    <div>
                        <div className="text-[10px] uppercase font-bold tracking-widest text-[var(--text-dim)]">Current Mode</div>
                        <div className={`text-lg font-bold ${isHumanInLoop ? 'text-[var(--neon-orange)]' : 'text-[var(--neon-green)]'}`}>
                            {isHumanInLoop ? 'HUMAN-IN-THE-LOOP' : 'FULL AUTONOMY'}
                        </div>
                    </div>
                </div>
                {isHumanInLoop && (
                    <div className="text-right">
                        <div className="text-[10px] text-[var(--text-dim)]">Reason</div>
                        <div className="text-xs font-mono text-[var(--text-primary)]">Critical Risk Threshold Exceeded</div>
                    </div>
                )}
            </div>

            {/* 2. Active Policies */}
            <div className="mb-3">
                <div className="flex items-center gap-2 mb-2 px-1">
                    <Shield size={12} className="text-[var(--neon-blue)]" />
                    <span className="text-[10px] uppercase font-bold text-[var(--text-secondary)]">Active Guardrails</span>
                </div>
                <div className="grid grid-cols-1 gap-2">
                    {data.policies.slice(0, 2).map((policy, i) => (
                        <div key={i} className="flex items-center justify-between bg-[rgba(255,255,255,0.02)] p-2 rounded border border-[rgba(255,255,255,0.05)]">
                            <span className="text-xs text-[var(--text-primary)]">{policy.title}</span>
                            <span className={`text-[10px] px-1.5 py-0.5 rounded border ${policy.status === 'Active' ? 'border-[var(--neon-green)] text-[var(--neon-green)]' : 'border-[var(--neon-orange)] text-[var(--text-dim)]'}`}>
                                {policy.status}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* 3. Decision Log */}
            <div className="flex-1 flex flex-col min-h-0">
                <div className="flex items-center gap-2 mb-2 px-1">
                    <History size={12} className="text-[var(--text-dim)]" />
                    <span className="text-[10px] uppercase font-bold text-[var(--text-secondary)]">Governance Log</span>
                </div>
                <div className="flex-1 overflow-y-auto custom-scrollbar bg-[rgba(0,0,0,0.2)] rounded border border-[rgba(255,255,255,0.05)] p-2">
                    {data.logs.map((log, i) => (
                        <div key={log.id} className="flex gap-3 mb-3 last:mb-0 border-b border-[rgba(255,255,255,0.03)] pb-2 last:border-0 last:pb-0">
                            <div className="mt-1">
                                <Gavel size={12} className="text-[var(--text-dim)]" />
                            </div>
                            <div>
                                <div className="flex items-center gap-2">
                                    <span className="text-xs font-bold text-[var(--text-primary)]">{log.action}</span>
                                    <span className="text-[10px] text-[var(--text-dim)]">{log.timestamp.split(' ')[1]}</span>
                                </div>
                                <div className="text-[10px] text-[var(--text-secondary)]">{log.detail}</div>
                                <div className="text-[10px] text-[var(--neon-blue)] mt-0.5">By: {log.user}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>


            <button
                onClick={() => window.location.href = '/governance'}
                className="mt-2 w-full py-2 flex items-center justify-center gap-2 text-[10px] uppercase font-bold tracking-widest text-[var(--text-dim)] hover:text-[var(--neon-blue)] hover:bg-[rgba(0,234,255,0.05)] border border-transparent hover:border-[rgba(0,234,255,0.1)] rounded transition-all"
            >
                View Compliance Log <ArrowRight size={12} />
            </button>
        </Card >
    );
};

export default GovernancePanel;
