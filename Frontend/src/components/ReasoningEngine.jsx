import React, { useEffect, useState } from 'react';
import Card from './Card';
import { BrainCircuit, CheckCircle2, AlertTriangle, ArrowRight, Activity, Terminal } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { fetchReasoningTraces } from '../services/mockData';

const TraceStep = ({ step, index, active }) => (
    <div className={`relative pl-6 pb-6 border-l transition-all duration-300 ${active ? 'border-[var(--neon-blue)]' : 'border-[rgba(255,255,255,0.05)]'}`}>
        <div className={`absolute left-[-5px] top-0 w-2.5 h-2.5 rounded-full border transition-all duration-300
            ${active
                ? 'bg-[var(--neon-blue)] border-[var(--neon-blue)] shadow-[0_0_10px_var(--neon-blue)]'
                : 'bg-[var(--bg-dark)] border-[rgba(255,255,255,0.2)]'
            }`}
        />

        <div className={`transition-all duration-500 ${active ? 'opacity-100 translate-x-0' : 'opacity-40 translate-x-2'}`}>
            <div className="flex items-center gap-2 mb-1">
                <span className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded
                    ${step.agent === 'Decision Agent' ? 'bg-[rgba(189,0,255,0.1)] text-[var(--neon-purple)]' : 'bg-[rgba(0,234,255,0.1)] text-[var(--neon-blue)]'}
                `}>
                    {step.agent}
                </span>
                <span className="text-xs font-mono text-[var(--text-dim)]">STEP 0{index + 1}</span>
            </div>
            <h4 className="text-sm font-semibold text-[var(--text-primary)] mb-1">{step.step}</h4>
            <p className="text-xs text-[var(--text-secondary)] leading-relaxed font-mono">
                {active ? <Typewriter text={step.detail} delay={10} /> : step.detail}
            </p>
        </div>
    </div>
);

const Typewriter = ({ text, delay = 20 }) => {
    const [displayedText, setDisplayedText] = useState('');

    useEffect(() => {
        let i = 0;
        setDisplayedText(''); // Reset
        const interval = setInterval(() => {
            setDisplayedText(prev => prev + text.charAt(i));
            i++;
            if (i >= text.length) clearInterval(interval);
        }, delay);
        return () => clearInterval(interval);
    }, [text, delay]);

    return <span>{displayedText}</span>;
};

const ReasoningEngine = () => {
    const { phase } = useDemo();
    const [traces, setTraces] = useState([]);
    const [activeStep, setActiveStep] = useState(-1);

    useEffect(() => {
        if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING) {
            setTraces(fetchReasoningTraces());

            // Animate through steps
            let step = 0;
            const interval = setInterval(() => {
                setActiveStep(step);
                step++;
                if (step >= 4) clearInterval(interval);
            }, 1500);

            return () => clearInterval(interval);
        } else {
            setTraces([]);
            setActiveStep(-1);
        }
    }, [phase]);

    if (phase === PHASES.NORMAL) {
        return (
            <Card title="Reasoning Engine" className="h-[350px] flex items-center justify-center">
                <div className="text-center opacity-30">
                    <BrainCircuit size={48} className="mx-auto mb-4 animate-pulse" />
                    <p className="text-sm font-mono uppercase tracking-widest">Wating for input...</p>
                </div>
            </Card>
        );
    }

    return (
        <Card title="AI Reasoning Trace (XAI)" className="h-[350px] overflow-hidden flex flex-col">
            <div className="flex-1 overflow-y-auto custom-scrollbar p-2">
                {traces.map((trace, index) => (
                    <TraceStep
                        key={trace.id}
                        step={trace}
                        index={index}
                        active={activeStep >= index}
                    />
                ))}
            </div>

            {/* Real-time Metrics Footer */}
            <div className="border-t border-[rgba(255,255,255,0.05)] p-3 bg-[rgba(0,0,0,0.2)] flex justify-between items-center text-xs">
                <div className="flex items-center gap-2">
                    <Activity size={14} className="text-[var(--neon-blue)]" />
                    <span className="text-[var(--text-secondary)]">Confidence Score:</span>
                    <span className="font-bold text-[var(--neon-green)]">98.4%</span>
                </div>
                <div className="flex items-center gap-2">
                    <AlertTriangle size={14} className="text-[var(--neon-orange)]" />
                    <span className="text-[var(--text-secondary)]">Risk Assessment:</span>
                    <span className="font-bold text-[var(--neon-red)]">CRITICAL</span>
                </div>
            </div>
        </Card>
    );
};

export default ReasoningEngine;
