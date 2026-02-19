import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import { fetchDecisions } from '../services/dataService';
import { BrainCircuit, GitBranch, ShieldCheck, AlertTriangle, Activity, CheckCircle2 } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { TypewriterText, ScanLine, PulsingDot } from '../components/AnimatedComponents';

const Decisions = () => {
    const { phase } = useDemo();
    const [decisions, setDecisions] = useState([]);

    useEffect(() => {
        const loadDecisions = async () => {
            const data = await fetchDecisions();

            // Map backend data to frontend model
            const mappedDecisions = data.map(d => ({
                id: d.decision?.decision_id || 'UNKNOWN',
                timestamp: new Date(d.decision?.timestamp).toLocaleTimeString() || 'Unknown',
                confidence: Math.round((d.decision?.input_analysis?.ai_confidence || 0) * 100),
                trigger: d.decision?.input_analysis?.human_summary || 'Unknown Trigger',
                aiAnalysis: d.reasoning?.llm_analysis?.slice(0, 100) + '...' || 'Analysis pending...',
                decision: (d.decision?.type || 'Standard').toUpperCase().replace('_', ' '),
                reasoning: d.decision?.explainability_trace?.decision_process?.map(step =>
                    `${step.step}: ${step.evaluation || step.decision_reason || step.action || ''}`
                ) || ['Processing...']
            }));

            setDecisions(mappedDecisions);
        };
        loadDecisions();

        // Poll for updates
        const interval = setInterval(() => {
            if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
                loadDecisions();
            }
        }, 2000);
        return () => clearInterval(interval);
    }, [phase]);

    const isAnalyzing = phase === PHASES.ANALYZING;

    return (
        <div className="space-y-6 animate-fade-in text-[var(--text-primary)]">

            {/* AI Highlight Panel */}
            {phase !== PHASES.NORMAL && (
                <div className="p-6 rounded-xl border border-[var(--neon-purple)] bg-[rgba(189,0,255,0.05)] relative overflow-hidden mb-8">
                    <ScanLine active={isAnalyzing} />
                    <div className="flex items-center gap-4 mb-4">
                        <BrainCircuit size={32} className={`text-[var(--neon-purple)] ${isAnalyzing ? 'animate-pulse' : ''}`} />
                        <div>
                            <h2 className="text-xl font-bold tracking-tight text-white">SENTINEL-CORE AI Reasoning</h2>
                            <p className="text-[var(--text-secondary)] font-mono text-xs">
                                {isAnalyzing ? 'ANALYZING THREAT VECTORS...' : phase === PHASES.DEFENDING ? 'EXECUTING COUNTERMEASURES' : 'MONITORING'}
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4 text-center">
                        <div className="p-4 bg-[rgba(0,0,0,0.3)] rounded-lg border border-[var(--border-color)]">
                            <div className="text-[10px] uppercase text-[var(--text-dim)] mb-2">Confidence Score</div>
                            <div className="text-3xl font-bold text-[var(--neon-green)]">
                                {isAnalyzing ? <span className="animate-pulse">calculating...</span> : '99.8%'}
                            </div>
                        </div>
                        <div className="p-4 bg-[rgba(0,0,0,0.3)] rounded-lg border border-[var(--border-color)]">
                            <div className="text-[10px] uppercase text-[var(--text-dim)] mb-2">Impact Analysis</div>
                            <div className="text-xl font-bold text-[var(--neon-orange)]">
                                {isAnalyzing ? 'ASSESSING' : 'CRITICAL'}
                            </div>
                        </div>
                        <div className="p-4 bg-[rgba(0,0,0,0.3)] rounded-lg border border-[var(--border-color)]">
                            <div className="text-[10px] uppercase text-[var(--text-dim)] mb-2">Action Type</div>
                            <div className="text-xl font-bold text-[var(--neon-blue)]">
                                {isAnalyzing ? 'PENDING' : 'ISOLATION'}
                            </div>
                        </div>
                    </div>

                    <div className="mt-6 p-4 bg-[rgba(0,0,0,0.5)] rounded border border-[var(--border-color)] font-mono text-sm text-[var(--neon-green)]">
                        &gt; <TypewriterText text={
                            isAnalyzing
                                ? "Scanning packet headers... Matching signature DB... Anomaly detected in port 443... Correlating with global threat intel..."
                                : phase === PHASES.DEFENDING
                                    ? "Threat confirmed. Origin: 192.168.x.x. Action decided: ISOLATE NODE & BLOCK SUBNET. Executing now."
                                    : "System optimal. Learning mode active."
                        } speed={20} />
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-6">
                    {decisions.map((decision) => (
                        <Card key={decision.id} className="relative overflow-hidden group hover:border-[var(--neon-blue)] transition-all">

                            {/* Header */}
                            <div className="flex items-center justify-between mb-6 pb-4 border-b border-[var(--border-color)]">
                                <div className="flex items-center gap-3">
                                    <span className="font-mono text-xs px-2 py-1 rounded bg-[rgba(255,255,255,0.05)] text-[var(--text-secondary)]">ID: {decision.id}</span>
                                    <span className="text-xs text-[var(--text-dim)]">{decision.timestamp}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="text-xs text-[var(--text-secondary)] uppercase font-bold">Confidence</span>
                                    <div className="px-3 py-1 rounded-full bg-[rgba(0,234,255,0.1)] text-[var(--neon-blue)] text-sm font-bold border border-[rgba(0,234,255,0.2)]">
                                        {decision.confidence}%
                                    </div>
                                </div>
                            </div>

                            {/* Flow Diagram */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative">
                                {/* Step 1: Trigger */}
                                <div className="p-4 rounded-lg bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.05)] relative z-10">
                                    <div className="flex items-center gap-2 mb-2 text-[var(--neon-orange)]">
                                        <AlertTriangle size={16} />
                                        <span className="text-xs font-bold uppercase tracking-wider">Trigger</span>
                                    </div>
                                    <p className="text-sm text-[var(--text-primary)] leading-snug">{decision.trigger}</p>
                                </div>

                                {/* Step 2: Analysis */}
                                <div className="p-4 rounded-lg bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.05)] relative z-10">
                                    <div className="flex items-center gap-2 mb-2 text-[var(--neon-blue)]">
                                        <Activity size={16} />
                                        <span className="text-xs font-bold uppercase tracking-wider">Analysis</span>
                                    </div>
                                    <p className="text-sm text-[var(--text-secondary)] leading-snug">{decision.aiAnalysis}</p>
                                </div>

                                {/* Step 3: Action */}
                                <div className="p-4 rounded-lg bg-[rgba(0,255,157,0.05)] border border-[rgba(0,255,157,0.2)] relative z-10">
                                    <div className="flex items-center gap-2 mb-2 text-[var(--neon-green)]">
                                        <ShieldCheck size={16} />
                                        <span className="text-xs font-bold uppercase tracking-wider">Decision</span>
                                    </div>
                                    <p className="text-sm font-bold text-[var(--text-primary)] leading-snug">{decision.decision}</p>
                                </div>

                                {/* Connecting Line (Desktop) */}
                                <div className="hidden md:block absolute top-1/2 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[var(--border-color)] to-transparent -z-0"></div>
                            </div>

                            {/* Detailed Reasoning */}
                            <div className="mt-6 pt-4 border-t border-[var(--border-color)]">
                                <h4 className="text-xs font-bold text-[var(--text-secondary)] uppercase tracking-wider mb-3">Logic Path</h4>
                                <ul className="space-y-2">
                                    {decision.reasoning.map((reason, i) => (
                                        <li key={i} className="flex items-start gap-3 text-sm text-[var(--text-dim)]">
                                            <GitBranch size={16} className="text-[var(--border-active)] mt-0.5" />
                                            <span>{reason}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </Card>
                    ))}
                </div>

                {/* Sidebar Widget */}
                <div className="space-y-6">
                    <Card title="Model Governance" className="h-full">
                        <div className="space-y-4">
                            <div className="p-4 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)]">
                                <div className="text-xs text-[var(--text-secondary)] mb-1 uppercase tracking-wider">Active Model</div>
                                <div className="text-lg font-bold text-[var(--text-primary)] font-mono">SENTINEL-CORE v4.3</div>
                                <div className="mt-2 text-xs text-[var(--text-dim)]">Last updated: 4h ago via Federated Learning</div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-3 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-center">
                                    <div className="text-xs text-[var(--text-secondary)] mb-1">Bias Check</div>
                                    <div className="text-sm font-bold text-[var(--neon-green)]">PASSED</div>
                                </div>
                                <div className="p-3 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-center">
                                    <div className="text-xs text-[var(--text-secondary)] mb-1">Drift</div>
                                    <div className="text-sm font-bold text-[var(--neon-blue)]">0.02%</div>
                                </div>
                            </div>

                            <button
                                onClick={() => window.location.href = '/governance'}
                                className="w-full py-2 mt-4 rounded-lg bg-[rgba(255,255,255,0.05)] border border-[var(--border-color)] text-sm text-[var(--text-secondary)] hover:bg-[rgba(255,255,255,0.1)] hover:text-white transition-colors"
                            >
                                View Full Model Audit
                            </button>
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default Decisions;
