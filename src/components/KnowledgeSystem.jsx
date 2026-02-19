import React, { useEffect, useState } from 'react';
import Card from './Card';
import { Database, Network, GitPullRequest, ArrowUpRight, Save } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { fetchMemoryPatterns, fetchRootCauseAnalysis } from '../services/mockData';

const KnowledgeSystem = () => {
    const { phase } = useDemo();
    const [patterns, setPatterns] = useState([]);
    const [rootCause, setRootCause] = useState(null);

    useEffect(() => {
        if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
            setPatterns(fetchMemoryPatterns());
            setRootCause(fetchRootCauseAnalysis());
        } else {
            setPatterns([]);
            setRootCause(null);
        }
    }, [phase]);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">

            {/* Root Cause Analysis Panel */}
            <Card title="Root Cause Intelligence" className="flex flex-col">
                {rootCause ? (
                    <div className="flex-1 flex flex-col gap-4 animate-fade-in">
                        <div className="bg-[rgba(255,0,0,0.05)] border border-[rgba(255,0,0,0.2)] rounded-lg p-3">
                            <div className="text-[10px] uppercase text-[var(--neon-red)] font-bold mb-1">Primary Cause Identified</div>
                            <div className="text-sm font-semibold text-white leading-tight">{rootCause.primaryCause}</div>
                        </div>

                        <div className="flex-1 relative">
                            <div className="absolute left-2 top-0 bottom-0 w-[1px] bg-[rgba(255,255,255,0.1)]"></div>
                            {rootCause.contributingFactors.map((factor, i) => (
                                <div key={i} className="relative pl-6 mb-3 text-xs text-[var(--text-secondary)] flex items-start group">
                                    <div className="absolute left-[5px] top-[6px] w-1.5 h-1.5 rounded-full bg-[var(--text-dim)] group-hover:bg-[var(--neon-blue)] transition-colors"></div>
                                    <span className="group-hover:text-white transition-colors">{factor}</span>
                                </div>
                            ))}
                        </div>

                        <div className="bg-[rgba(0,255,157,0.05)] border border-[rgba(0,255,157,0.1)] rounded p-2 flex items-center gap-2">
                            <ArrowUpRight size={14} className="text-[var(--neon-green)]" />
                            <span className="text-xs font-mono text-[var(--neon-green)]">New heuristic rule generated.</span>
                        </div>
                    </div>
                ) : (
                    <div className="flex-1 flex flex-col items-center justify-center text-[var(--text-dim)]">
                        <Network size={32} className="mb-2 opacity-20" />
                        <span className="text-xs uppercase tracking-widest">Awaiting Analysis</span>
                    </div>
                )}
            </Card>

            {/* Memory Stream Panel */}
            <Card title="Long-Term Memory" className="flex flex-col">
                <div className="flex-1 overflow-y-auto custom-scrollbar">
                    {patterns.length > 0 ? (
                        <div className="space-y-3">
                            {patterns.map((item, i) => (
                                <div key={item.id} className="bg-[rgba(255,255,255,0.02)] hover:bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.05)] rounded-lg p-3 transition-colors animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                                    <div className="flex justify-between items-start mb-1">
                                        <div className="flex items-center gap-2">
                                            <Database size={12} className="text-[var(--neon-purple)]" />
                                            <span className="text-xs font-bold text-[var(--text-primary)]">{item.pattern}</span>
                                        </div>
                                        <span className="text-[10px] text-[var(--text-dim)]">{item.lastSeen}</span>
                                    </div>
                                    <div className="flex justify-between items-center text-[10px] text-[var(--text-secondary)] mt-2">
                                        <span>Freq: {item.frequency}</span>
                                        <span className="bg-[rgba(0,255,157,0.1)] text-[var(--neon-green)] px-1.5 py-0.5 rounded">
                                            {(item.confidence * 100).toFixed(0)}% Match
                                        </span>
                                    </div>
                                </div>
                            ))}
                            <div className="flex items-center justify-center gap-2 py-2 text-[var(--text-dim)] text-xs animate-pulse">
                                <Save size={12} />
                                <span>Encoding new incident data...</span>
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col items-center justify-center text-[var(--text-dim)]">
                            <Database size={32} className="mb-2 opacity-20" />
                            <span className="text-xs uppercase tracking-widest">Memory Idle</span>
                        </div>
                    )}
                </div>
            </Card>
        </div>
    );
};

export default KnowledgeSystem;
