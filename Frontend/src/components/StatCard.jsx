import React from 'react';

const StatCard = ({ title, value, subtext, icon: Icon, trend, status = 'neutral' }) => {
    const getStatusColor = () => {
        switch (status) {
            case 'critical': return 'var(--neon-red)';
            case 'warning': return 'var(--neon-orange)';
            case 'success': return 'var(--neon-green)';
            case 'info': return 'var(--neon-blue)';
            default: return 'var(--text-secondary)';
        }
    };

    const color = getStatusColor();

    return (
        <div className="glass-card rounded-xl p-6 relative overflow-hidden group">
            {/* Background Glow */}
            <div className="absolute -right-6 -top-6 w-24 h-24 bg-gradient-to-br from-white to-transparent opacity-5 rounded-full blur-xl group-hover:opacity-10 transition-opacity"></div>

            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-sm font-medium text-[var(--text-secondary)] uppercase tracking-wider">{title}</h3>
                </div>
                <div className={`p-2 rounded-lg bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.05)] text-[${color}]`}>
                    {Icon && <Icon size={20} style={{ color }} />}
                </div>
            </div>

            <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-[var(--text-primary)] tracking-tight">{value}</span>
                {subtext && <span className="text-xs text-[var(--text-dim)] font-mono">{subtext}</span>}
            </div>

            {trend && (
                <div className={`mt-2 text-xs font-medium flex items-center gap-1 ${trend > 0 ? 'text-[var(--neon-green)]' : 'text-[var(--neon-red)]'}`}>
                    <span>{trend > 0 ? '▲' : '▼'} {Math.abs(trend)}%</span>
                    <span className="text-[var(--text-dim)]">vs last hour</span>
                </div>
            )}

            {/* Bottom accent line */}
            <div className="absolute bottom-0 left-0 h-1 w-full bg-gradient-to-r from-transparent via-[rgba(255,255,255,0.1)] to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        </div>
    );
};

export default StatCard;
