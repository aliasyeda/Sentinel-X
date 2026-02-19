import React, { useEffect, useState } from 'react';
import { useDemo, PHASES } from '../context/DemoContext';
import Card from './Card';
import { AlertCircle, Shield, CheckCircle, Search, Terminal } from 'lucide-react';

const TimelineItem = ({ event, isNew }) => (
    <div className={`flex gap-4 animate-fade-in ${isNew ? 'bg-[rgba(0,234,255,0.03)]' : ''}`}>
        <div className="flex flex-col items-center">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center border 
                ${event.type === 'THREAT' ? 'bg-[rgba(255,0,0,0.1)] border-[var(--neon-red)] text-[var(--neon-red)]' :
                    event.type === 'ACTION' ? 'bg-[rgba(0,234,255,0.1)] border-[var(--neon-blue)] text-[var(--neon-blue)]' :
                        event.type === 'SUCCESS' ? 'bg-[rgba(0,255,157,0.1)] border-[var(--neon-green)] text-[var(--neon-green)]' :
                            'bg-[rgba(255,255,255,0.05)] border-[var(--border-color)] text-[var(--text-dim)]'
                }`}>
                {event.type === 'THREAT' && <AlertCircle size={14} />}
                {event.type === 'ACTION' && <Terminal size={14} />}
                {event.type === 'SUCCESS' && <CheckCircle size={14} />}
                {event.type === 'INFO' && <Search size={14} />}
            </div>
            <div className="w-[1px] h-full bg-[rgba(255,255,255,0.05)] my-2"></div>
        </div>
        <div className="pb-6 pt-1">
            <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-mono text-[var(--text-dim)]">{event.time}</span>
                <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded
                     ${event.type === 'THREAT' ? 'bg-[rgba(255,0,0,0.2)] text-[var(--neon-red)]' :
                        event.type === 'ACTION' ? 'bg-[rgba(0,234,255,0.1)] text-[var(--neon-blue)]' :
                            event.type === 'SUCCESS' ? 'bg-[rgba(0,255,157,0.1)] text-[var(--neon-green)]' :
                                'bg-[rgba(255,255,255,0.1)] text-[var(--text-secondary)]'
                    }
                `}>{event.label}</span>
            </div>
            <p className="text-sm text-[var(--text-primary)]">{event.message}</p>
            {event.detail && (
                <p className="text-xs text-[var(--text-secondary)] mt-1 bg-[rgba(0,0,0,0.2)] p-1 rounded font-mono">
                    &gt; {event.detail}
                </p>
            )}
        </div>
    </div>
);

const IncidentTimeline = () => {
    const { phase, logs } = useDemo();
    const [events, setEvents] = useState([]);

    // Transform simple logs into structured timeline events
    useEffect(() => {
        if (phase === PHASES.NORMAL) {
            setEvents([{
                id: 'init',
                time: 'Now',
                type: 'INFO',
                label: 'MONITORING',
                message: 'System monitoring active. No anomalies detected.',
                detail: 'Scanning 142 nodes...'
            }]);
        } else {
            // Convert logs to timeline events
            const newEvents = logs.map((log, index) => {
                let type = 'INFO';
                let label = 'SYSTEM';

                if (log.msg.includes('DETECTED') || log.msg.includes('Attack') || log.msg.includes('High')) {
                    type = 'THREAT';
                    label = 'DETECTION';
                } else if (log.msg.includes('Redirecting') || log.msg.includes('Isolating') || log.msg.includes('Deploying')) {
                    type = 'ACTION';
                    label = 'RESPONSE';
                } else if (log.msg.includes('Restored') || log.msg.includes('mitigated')) {
                    type = 'SUCCESS';
                    label = 'RECOVERY';
                }

                return {
                    id: index,
                    time: log.time,
                    type,
                    label,
                    message: log.msg,
                    detail: null // Add detail generation if needed
                };
            });
            setEvents(newEvents.reverse());
        }
    }, [logs, phase]);

    return (
        <Card title="Live Incident Timeline" className="h-[400px] flex flex-col">
            <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
                {events.map((event, index) => (
                    <TimelineItem key={event.id || index} event={event} isNew={index === 0} />
                ))}
            </div>
        </Card>
    );
};

export default IncidentTimeline;
