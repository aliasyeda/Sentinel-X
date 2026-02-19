import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import StatusBadge from '../components/StatusBadge';
import CyberTable from '../components/CyberTable';
import { fetchIncidents } from '../services/dataService';
import { Search, Filter, AlertOctagon, MoreHorizontal } from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';

const Incidents = () => {
    const { phase } = useDemo();
    const [incidents, setIncidents] = useState([]);

    useEffect(() => {
        const loadIncidents = async () => {
            const data = await fetchIncidents();
            // Map backend data to frontend model
            const mappedIncidents = data.map(inc => ({
                id: inc.incident_id || 'UNKNOWN',
                type: inc.analysis?.type || 'Unknown Incident',
                severity: (inc.analysis?.severity || 'Low').charAt(0).toUpperCase() + (inc.analysis?.severity || 'Low').slice(1),
                score: Math.round((inc.analysis?.impact_score || 0) * 10), // Scale 0-10 to 0-100
                status: 'Analyzed', // Default status from backend
                timestamp: new Date(inc.analysis?.timestamp).toLocaleTimeString() || 'Unknown',
                raw: inc
            }));

            setIncidents(mappedIncidents);
        };

        loadIncidents();

        // Poll for updates during active phases
        const interval = setInterval(() => {
            if (phase === PHASES.ATTACK || phase === PHASES.ANALYZING || phase === PHASES.DEFENDING) {
                loadIncidents();
            }
        }, 2000);

        return () => clearInterval(interval);
    }, [phase]);

    const headers = ['Incident ID', 'Type', 'Severity', 'Anomaly Score', 'Status', 'Time', 'Actions'];

    const renderIncidentRow = (incident) => (
        <>
            <td className="py-4 px-6 text-sm font-mono text-[var(--text-primary)]">
                <div className="flex items-center gap-3">
                    <div className={`p-1.5 rounded bg-[rgba(255,255,255,0.05)] ${incident.severity === 'Critical' ? 'text-[var(--neon-red)] animate-pulse' :
                        incident.severity === 'High' ? 'text-[var(--neon-orange)]' : 'text-[var(--text-dim)]'
                        }`}>
                        <AlertOctagon size={16} />
                    </div>
                    {incident.id}
                </div>
            </td>
            <td className="py-4 px-6 text-sm text-[var(--text-primary)] font-medium">{incident.type}</td>
            <td className="py-4 px-6">
                <span className={`text-xs font-bold tracking-wider px-2 py-1 rounded bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.05)] ${incident.severity === 'Critical' ? 'text-[var(--neon-red)] border-[rgba(255,42,42,0.3)]' :
                    incident.severity === 'High' ? 'text-[var(--neon-orange)] border-[rgba(255,159,0,0.3)]' :
                        'text-[var(--neon-blue)]'
                    }`}>
                    {incident.severity.toUpperCase()}
                </span>
            </td>
            <td className="py-4 px-6">
                <div className="flex items-center gap-3">
                    <div className="w-24 h-1.5 bg-[rgba(255,255,255,0.1)] rounded-full overflow-hidden">
                        <div
                            className={`h-full rounded-full shadow-[0_0_10px_currentColor] ${incident.score > 90 ? 'bg-[var(--neon-red)] text-[var(--neon-red)]' : incident.score > 70 ? 'bg-[var(--neon-orange)] text-[var(--neon-orange)]' : 'bg-[var(--neon-blue)] text-[var(--neon-blue)]'}`}
                            style={{ width: `${incident.score}%` }}
                        ></div>
                    </div>
                    <span className="text-xs font-mono text-[var(--text-secondary)]">{incident.score}</span>
                </div>
            </td>
            <td className="py-4 px-6">
                <StatusBadge status={incident.status} />
            </td>
            <td className="py-4 px-6 text-xs text-[var(--text-secondary)]">{incident.timestamp}</td>
            <td className="py-4 px-6 text-right">
                <button
                    onClick={() => alert(`Opening details for Incident ${incident.id}`)}
                    className="p-1 hover:bg-[rgba(255,255,255,0.1)] rounded transition-colors text-[var(--text-secondary)] hover:text-white"
                >
                    <MoreHorizontal size={18} />
                </button>
            </td>
        </>
    );

    return (
        <div className="space-y-6 animate-fade-in">
            <Card>
                <div className="flex flex-col md:flex-row gap-4 items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-[var(--text-primary)]">Incident Log</h2>

                    <div className="flex gap-3">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Search by ID or Type..."
                                className="bg-[rgba(0,0,0,0.2)] border border-[var(--border-color)] text-[var(--text-primary)] px-4 py-2 pl-10 rounded-lg text-sm w-64 focus:outline-none focus:border-[var(--neon-blue)] focus:ring-1 focus:ring-[var(--neon-blue)] transition-all"
                            />
                            <Search className="absolute left-3 top-2.5 text-[var(--text-dim)]" size={16} />
                        </div>
                        <button
                            onClick={() => alert("Advanced filters are disabled in Demo Mode.")}
                            className="flex items-center gap-2 px-4 py-2 bg-[rgba(255,255,255,0.03)] border border-[var(--border-color)] rounded-lg text-sm text-[var(--text-secondary)] hover:bg-[rgba(255,255,255,0.05)] hover:text-white transition-colors"
                        >
                            <Filter size={16} />
                            Filter
                        </button>
                    </div>
                </div>

                <CyberTable
                    headers={headers}
                    data={incidents}
                    renderRow={renderIncidentRow}
                />
            </Card>
        </div>
    );
};

export default Incidents;
