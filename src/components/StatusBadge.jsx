import React from 'react';

const StatusBadge = ({ status }) => {
    const getStyles = () => {
        switch (status.toLowerCase()) {
            case 'critical':
            case 'high':
            case 'failure':
            case 'attack':
                return 'bg-[rgba(255,42,42,0.1)] text-[var(--neon-red)] border-[var(--neon-red)]';
            case 'warning':
            case 'medium':
                return 'bg-[rgba(255,159,0,0.1)] text-[var(--neon-orange)] border-[var(--neon-orange)]';
            case 'safe':
            case 'success':
            case 'active':
            case 'protected':
                return 'bg-[rgba(0,255,65,0.1)] text-[var(--neon-green)] border-[var(--neon-green)]';
            case 'info':
            case 'analyzing':
            case 'recovering':
                return 'bg-[rgba(0,243,255,0.1)] text-[var(--neon-blue)] border-[var(--neon-blue)]';
            default:
                return 'bg-[rgba(255,255,255,0.1)] text-[var(--text-secondary)] border-[var(--text-secondary)]';
        }
    };

    return (
        <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${getStyles()}`}>
            {status}
        </span>
    );
};

export default StatusBadge;
