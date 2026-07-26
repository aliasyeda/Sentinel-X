import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import CyberTable from '../components/CyberTable';
import StatusBadge from '../components/StatusBadge';
import { fetchGovernanceData } from '../services/mockData';
import { Scale, Lock, FileText, UserCheck, Shield, Users } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';

const Governance = () => {
    const { phase } = useDemo();
    const [data, setData] = useState(null);

    useEffect(() => {
        setData(fetchGovernanceData());
    }, []);

    if (!data) return <div className="p-8 text-[var(--text-dim)]">Loading Compliance Data...</div>;

    const logHeaders = ['ID', 'Action', 'User/Agent', 'Timestamp', 'Detail'];
    const renderLogRow = (log) => (
        <>
            <td className="py-4 px-6 text-xs font-mono text-[var(--text-dim)]">{log.id}</td>
            <td className="py-4 px-6 text-sm font-bold text-[var(--text-primary)]">{log.action}</td>
            <td className="py-4 px-6 text-sm text-[var(--neon-blue)] flex items-center gap-2">
                <UserCheck size={14} /> {log.user}
            </td>
            <td className="py-4 px-6 text-xs text-[var(--text-secondary)] font-mono">{log.timestamp}</td>
            <td className="py-4 px-6 text-sm text-[var(--text-secondary)]">{log.detail}</td>
        </>
    );

    const isDefending = phase === PHASES.DEFENDING;

    return (
        <div className="space-y-8 animate-fade-in text-[var(--text-primary)]">

            {/* Trust Meter / Safety Locks */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card title="Autonomy Trust Level">
                    <div className="flex flex-col items-center justify-center p-4">
                        <div className="relative w-full h-4 bg-[rgba(255,255,255,0.1)] rounded-full overflow-hidden mb-4">
                            <div className="absolute top-0 left-0 h-full bg-gradient-to-r from-[var(--neon-blue)] to-[var(--neon-purple)]" style={{ width: '85%' }}></div>
                        </div>
                        <div className="flex justify-between w-full text-xs text-[var(--text-secondary)] uppercase tracking-wider">
                            <span>Human-in-Loop</span>
                            <span className="font-bold text-white">Semi-Autonomous (L4)</span>
                            <span>Fully Autonomous</span>
                        </div>
                    </div>
                </Card>

                <Card title="Safety Interlocks">
                    <div className="space-y-3">
                        <div className="flex justify-between items-center p-2 rounded bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.05)]">
                            <div className="flex items-center gap-2 text-sm">
                                <Lock size={14} className="text-[var(--neon-green)]" />
                                <span>Kill Switch</span>
                            </div>
                            <span className="text-xs text-[var(--neon-green)] px-2 py-0.5 border border-[var(--neon-green)] rounded">ARMED</span>
                        </div>
                        <div className={`flex justify-between items-center p-2 rounded border border-[rgba(255,255,255,0.05)] transition-colors ${isDefending ? 'bg-[rgba(255,60,60,0.1)] border-[var(--neon-red)]' : 'bg-[rgba(255,255,255,0.03)]'}`}>
                            <div className="flex items-center gap-2 text-sm">
                                <Users size={14} className={isDefending ? "text-[var(--neon-red)]" : "text-[var(--text-secondary)]"} />
                                <span>Human Override</span>
                            </div>
                            <span className={`text-xs px-2 py-0.5 border rounded ${isDefending ? 'text-[var(--neon-red)] border-[var(--neon-red)] animate-pulse' : 'text-[var(--text-dim)] border-[var(--text-dim)]'}`}>
                                {isDefending ? 'REQUIRED' : 'STANDBY'}
                            </span>
                        </div>
                    </div>
                </Card>

                <Card title="Compliance Score">
                    <div className="flex items-center justify-center h-full pb-6">
                        <div className="text-center">
                            <div className="text-4xl font-bold text-[var(--neon-green)]">99.9%</div>
                            <div className="text-xs text-[var(--text-secondary)] mt-1">SOC2 Type II Compliant</div>
                        </div>
                    </div>
                </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Active Policies */}
                <Card title="Active Security Policies">
                    <div className="space-y-4">
                        {data.policies.map((policy, i) => (
                            <div key={i} className="p-4 rounded-xl bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.05)] flex items-start justify-between group hover:border-[var(--border-active)] transition-colors">
                                <div>
                                    <div className="flex items-center gap-2 mb-2">
                                        <Lock size={16} className={policy.level === 'Critical' ? 'text-[var(--neon-red)]' : 'text-[var(--neon-orange)]'} />
                                        <h4 className="font-bold text-sm tracking-wide">{policy.title}</h4>
                                    </div>
                                    <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{policy.desc}</p>
                                </div>
                                <StatusBadge status={policy.status} />
                            </div>
                        ))}
                    </div>
                </Card>

                {/* Model Training Status */}
                <Card title="Adaptive Learning Engine">
                    <div className="flex items-center justify-center p-8">
                        <div className="relative w-40 h-40">
                            {/* Spinner Animation */}
                            <div className="absolute inset-0 rounded-full border-4 border-[rgba(255,255,255,0.05)]"></div>
                            <div className="absolute inset-0 rounded-full border-4 border-[var(--neon-purple)] border-t-transparent animate-spin duration-[3s]"></div>

                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <span className="text-3xl font-bold font-mono text-white">4.3</span>
                                <span className="text-[10px] uppercase tracking-widest text-[var(--text-dim)]">Version</span>
                            </div>
                        </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4 mt-4">
                        <div className="text-center p-2">
                            <div className="text-xs text-[var(--text-secondary)] mb-1">Patterns Learned</div>
                            <div className="text-xl font-bold text-[var(--neon-purple)]">{data.patternsLearned}</div>
                        </div>
                        <div className="text-center p-2">
                            <div className="text-xs text-[var(--text-secondary)] mb-1">Last Cycle</div>
                            <div className="text-sm font-bold text-white">{data.lastTraining}</div>
                        </div>
                    </div>
                </Card>
            </div>

            {/* Audit Logs */}
            <Card title="Immutable Audit Trail">
                <CyberTable
                    headers={logHeaders}
                    data={data.logs}
                    renderRow={renderLogRow}
                />
            </Card>
        </div>
    );
};

export default Governance;
