import React, { useEffect, useState } from 'react';
import Card from './Card';
import { Zap, CheckCircle2, XCircle, Clock, Server, Play, ArrowRight } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { fetchActionLog } from '../services/dataService';

const ActionPanel = () => {
    const { phase } = useDemo();
    const [actions, setActions] = useState([]);

    useEffect(() => {
        const loadActions = async () => {
            const data = await fetchActionLog();
            const mappedActions = data.map(a => ({
                id: a.action_id,
                type: a.action_type.replace('_', ' ').toUpperCase(),
                target: a.service,
                status: a.status === 'pending_execution' ? 'Pending' : 'Success', // Mock status mapping
                duration: a.estimated_duration,
                details: `${a.action_details?.method || 'Standard'} (${a.risk_level} risk)`
            }));
            setActions(mappedActions);
        };
        loadActions();

        const interval = setInterval(() => {
            if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
                loadActions();
            }
        }, 2000);
        return () => clearInterval(interval);
    }, [phase]);

    return (
        <Card title="Action Execution & Self-Healing" className="h-[300px] flex flex-col">
            <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
                {actions.length > 0 ? (
                    <div className="space-y-3">
                        {actions.map((action, i) => (
                            <div key={action.id} className="bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.05)] rounded-lg p-3 hover:bg-[rgba(255,255,255,0.04)] transition-colors animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                                <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center gap-2">
                                        <div className={`p-1.5 rounded bg-[rgba(255,255,255,0.05)] text-[var(--neon-blue)]`}>
                                            <Zap size={14} />
                                        </div>
                                        <div>
                                            <div className="text-xs font-bold text-[var(--text-primary)]">{action.type}</div>
                                            <div className="text-[10px] text-[var(--text-dim)] flex items-center gap-1">
                                                <Server size={10} /> Target: {action.target}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Status Badge */}
                                    <div className={`flex items-center gap-1 px-2 py-1 rounded text-[10px] font-bold border
                                        ${action.status === 'Success' ? 'bg-[rgba(0,255,157,0.1)] border-[var(--neon-green)] text-[var(--neon-green)]' :
                                            action.status === 'Failed' ? 'bg-[rgba(255,0,0,0.1)] border-[var(--neon-red)] text-[var(--neon-red)]' :
                                                'bg-[rgba(255,165,0,0.1)] border-[var(--neon-orange)] text-[var(--neon-orange)]'}
                                    `}>
                                        {action.status === 'Success' && <CheckCircle2 size={10} />}
                                        {action.status === 'Failed' && <XCircle size={10} />}
                                        {action.status === 'Pending' && <Clock size={10} />}
                                        {action.status.toUpperCase()}
                                    </div>
                                </div>

                                <div className="flex justify-between items-center text-[10px] text-[var(--text-secondary)] pl-8">
                                    <div className="flex items-center gap-1">
                                        <Play size={10} /> {action.details}
                                    </div>
                                    <div className="font-mono opacity-70">
                                        {action.duration !== '-' && `Time: ${action.duration}`}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-[var(--text-dim)] opacity-50">
                        <Zap size={32} className="mb-2" />
                        <span className="text-xs uppercase tracking-widest">No Active Remediation</span>
                    </div>
                )}
            </div>
            <button
                onClick={() => window.location.href = '/actions'}
                className="mt-2 w-full py-2 flex items-center justify-center gap-2 text-[10px] uppercase font-bold tracking-widest text-[var(--text-dim)] hover:text-[var(--neon-purple)] hover:bg-[rgba(189,0,255,0.05)] border border-transparent hover:border-[rgba(189,0,255,0.1)] rounded transition-all"
            >
                View Full Audit Trail <ArrowRight size={12} />
            </button>
        </Card>
    );
};

export default ActionPanel;
