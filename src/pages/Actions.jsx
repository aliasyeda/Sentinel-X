import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import StatCard from '../components/StatCard';
import CyberTable from '../components/CyberTable';
import StatusBadge from '../components/StatusBadge';
import { fetchActions } from '../services/mockData';
import { Zap, Clock, CheckCircle2, RotateCcw } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';

const Actions = () => {
    const { phase } = useDemo();
    const [actions, setActions] = useState([]);

    useEffect(() => {
        const baseActions = fetchActions();
        if (phase === PHASES.DEFENDING || phase === PHASES.RESTORED) {
            const newAction = {
                id: 'ACT-9999',
                type: 'Automated Containment',
                target: 'Subnet-4 Gateway',
                status: 'Success',
                duration: '0.05s',
                timestamp: 'Just Now',
                details: 'Isolated compromised segment to prevent lateral movement.'
            };
            setActions([newAction, ...baseActions]);
        } else {
            setActions(baseActions);
        }
    }, [phase]);

    const headers = ['Action Type', 'Target', 'Status', 'Duration', 'Timestamp', 'Details'];

    const renderActionRow = (action) => (
        <>
            <td className="py-4 px-6 text-sm font-bold text-[var(--text-primary)] flex items-center gap-2">
                <Zap size={14} className={action.id === 'ACT-9999' ? "text-[var(--neon-green)] animate-pulse" : "text-[var(--neon-orange)]"} />
                {action.type}
            </td>
            <td className="py-4 px-6 text-sm text-[var(--text-secondary)] font-mono">{action.target}</td>
            <td className="py-4 px-6 text-sm">
                <StatusBadge status={action.status} />
            </td>
            <td className="py-4 px-6 text-sm text-[var(--text-dim)] font-mono">{action.duration}</td>
            <td className="py-4 px-6 text-sm text-[var(--text-dim)] font-mono">{action.timestamp}</td>
            <td className="py-4 px-6 text-sm text-[var(--text-secondary)] max-w-xs truncate" title={action.details}>
                {action.details}
            </td>
        </>
    );

    return (
        <div className="space-y-8 animate-fade-in text-[var(--text-primary)]">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <StatCard
                    title="Mean Time to Recover"
                    value="1.2s"
                    icon={Clock}
                    status="success"
                    trend={-15}
                />
                <StatCard
                    title="Total Automations"
                    value={phase === PHASES.DEFENDING ? '148' : '147'}
                    subtext="Last 24 hours"
                    icon={Zap}
                    status="info"
                />
                <StatCard
                    title="Success Rate"
                    value="99.4%"
                    icon={CheckCircle2}
                    status="success"
                />
                <StatCard
                    title="Rollbacks"
                    value="2"
                    icon={RotateCcw}
                    status="warning"
                />
            </div>

            <Card title="Autonomous Action Log">
                <CyberTable
                    headers={headers}
                    data={actions}
                    renderRow={renderActionRow}
                />
            </Card>
        </div>
    );
};

export default Actions;
