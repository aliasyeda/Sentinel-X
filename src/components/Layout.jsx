import React from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
    Shield,
    Activity,
    BrainCircuit,
    Zap,
    Scale,
    Search,
    Bell,
    User,
    PlayCircle,
    RotateCcw,
    LogOut
} from 'lucide-react';
import { useDemo, PHASES } from '../context/DemoContext';
import { useAuth } from '../context/AuthContext';
import { PulsingDot } from './AnimatedComponents';

const SidebarItem = ({ to, icon: Icon, label }) => (
    <NavLink
        to={to}
        className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 my-1 mx-2 rounded-lg transition-all duration-200 group ${isActive
                ? 'bg-[rgba(0,234,255,0.1)] text-[var(--neon-blue)] border border-[rgba(0,234,255,0.2)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.03)]'
            }`
        }
    >
        <Icon size={18} className="group-hover:scale-110 transition-transform" />
        <span className="text-sm font-medium">{label}</span>
    </NavLink>
);

const Layout = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { phase, startSimulation, resetSimulation } = useDemo();
    const { user, logout } = useAuth();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const handleSimAttack = () => {
        // startSimulation(); // This only toggles frontend state if used. 
        // Better to guide user to use the real backend script.
        alert("🚀 To start the simulation, run the backend script:\n\npython run_demo_backend.py\n\nThe dashboard will automatically react!");
    };

    const getPageTitle = () => {
        const path = location.pathname.split('/')[1];
        if (!path) return 'Command Center';
        return path.charAt(0).toUpperCase() + path.slice(1);
    };

    const isEmergency = phase === PHASES.ATTACK || phase === PHASES.ANALYZING;

    return (
        <div className={`flex h-screen overflow-hidden font-sans transition-colors duration-1000 ${isEmergency ? 'bg-[#1a0505]' : 'bg-[var(--bg-dark)]'}`}>

            {/* Emergency Overlay Pulse */}
            {isEmergency && <div className="absolute inset-0 pointer-events-none z-50 border-4 border-[var(--neon-red)] animate-pulse opacity-50"></div>}

            {/* Sidebar */}
            <aside className="w-72 glass-panel border-r-0 border-r-[var(--border-color)] flex flex-col z-30 relative">
                <div className="p-8 pb-4 flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center shadow-[0_0_20px_rgba(0,243,255,0.3)] transition-colors duration-500 ${isEmergency ? 'bg-[var(--neon-red)]' : 'bg-gradient-to-tr from-[#00f3ff] to-[#0066ff]'}`}>
                        <Shield className="text-white" size={24} />
                    </div>
                    <div>
                        <h1 className="font-bold text-xl tracking-tight text-white">SENTINEL-X</h1>
                        <p className="text-[10px] text-[var(--text-dim)] font-medium uppercase tracking-widest">Enterprise Security</p>
                    </div>
                </div>

                <div className="px-8 py-4">
                    <div className="text-[11px] uppercase text-[var(--text-dim)] font-bold tracking-wider mb-2">Main Menu</div>
                    <nav className="flex flex-col space-y-1">
                        <SidebarItem to="/overview" icon={Activity} label="Review & Monitor" />
                        <SidebarItem to="/incidents" icon={Shield} label="Incident Response" />
                        <SidebarItem to="/decisions" icon={BrainCircuit} label="AI Reasoning" />
                        <SidebarItem to="/actions" icon={Zap} label="Auto-Remediation" />
                        <SidebarItem to="/governance" icon={Scale} label="Policy & Compliance" />
                    </nav>
                </div>

                {/* Dynamic System Alert */}
                <div className={`mt-auto p-4 mx-4 mb-4 rounded-xl border transition-all duration-500 ${isEmergency ? 'bg-[rgba(255,0,0,0.1)] border-[var(--neon-red)]' : 'bg-[rgba(0,255,157,0.05)] border-[var(--neon-green)]'}`}>
                    <div className="flex items-center gap-3 mb-2">
                        <PulsingDot color={isEmergency ? 'var(--neon-red)' : 'var(--neon-green)'} />
                        <span className={`text-xs font-bold uppercase tracking-wider ${isEmergency ? 'text-[var(--neon-red)]' : 'text-[var(--neon-green)]'}`}>
                            {isEmergency ? 'THREAT DETECTED' : 'SYSTEM SECURE'}
                        </span>
                    </div>
                    <p className="text-[11px] text-[var(--text-secondary)] leading-relaxed">
                        {isEmergency ? 'Unauthorized access attempt in Subnet-4. AI countermeasures engaged.' : 'All systems operating within normal parameters. Real-time monitoring active.'}
                    </p>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative overflow-hidden">
                {/* Top Header */}
                <header className="h-20 flex items-center justify-between px-8 z-20 border-b border-[rgba(255,255,255,0.03)] glass-panel bg-opacity-30">
                    <h2 className="text-xl font-semibold text-white tracking-tight">{getPageTitle()}</h2>

                    <div className="flex items-center gap-6">

                        {/* Simulation Controls */}
                        <div className="flex items-center gap-2 mr-4">
                            <button
                                onClick={handleSimAttack}
                                disabled={phase !== PHASES.NORMAL}
                                className={`flex items-center gap-2 px-3 py-1.5 rounded border text-xs font-bold uppercase tracking-wider transition-all
                        ${phase === PHASES.NORMAL
                                        ? 'border-[var(--neon-red)] text-[var(--neon-red)] hover:bg-[rgba(255,60,60,0.1)]'
                                        : 'border-[var(--text-dim)] text-[var(--text-dim)] opacity-50 cursor-not-allowed'}`}
                            >
                                <PlayCircle size={14} /> Sim Attack
                            </button>
                            <button
                                onClick={resetSimulation}
                                className="p-1.5 text-[var(--text-secondary)] hover:text-white transition-colors"
                                title="Reset Simulation"
                            >
                                <RotateCcw size={16} />
                            </button>
                        </div>

                        <div className="h-8 w-[1px] bg-[var(--border-color)]"></div>

                        <div className="relative group">
                            <input
                                type="text"
                                placeholder="Search systems..."
                                className="bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.1)] rounded-full px-4 py-2 pl-10 text-sm w-64 focus:outline-none focus:border-[var(--neon-blue)] focus:w-80 transition-all duration-300 text-[var(--text-primary)] placeholder-gray-500"
                            />
                            <Search className="absolute left-3 top-2.5 text-[var(--text-dim)]" size={16} />
                        </div>

                        <div className="flex items-center gap-4">
                            <button className="relative p-2 text-[var(--text-secondary)] hover:text-white transition-colors">
                                <Bell size={20} />
                                {isEmergency && <span className="absolute top-2 right-2 w-2 h-2 bg-[var(--neon-red)] rounded-full animate-ping"></span>}
                            </button>

                            <div className="flex items-center gap-4">
                                <div className="text-right hidden md:block">
                                    <div className="text-sm font-medium text-white">{user?.username || 'Unknown'}</div>
                                    <div className="text-[10px] text-[var(--text-dim)] uppercase font-bold">{user?.designation || 'Visitor'}</div>
                                </div>
                                <div className="relative group">
                                    <div className="w-10 h-10 rounded-full bg-[rgba(255,255,255,0.1)] border border-[rgba(255,255,255,0.1)] flex items-center justify-center cursor-pointer hover:border-[var(--neon-blue)] transition-colors">
                                        <User size={20} className="text-[var(--text-secondary)] group-hover:text-white" />
                                    </div>

                                    {/* Dropdown Menu */}
                                    <div className="absolute right-0 top-12 w-48 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 overflow-hidden backdrop-blur-xl">
                                        <div className="p-3 border-b border-[rgba(255,255,255,0.05)]">
                                            <div className="text-xs text-[var(--text-dim)] uppercase tracking-wider font-bold mb-1">Role</div>
                                            <div className="text-sm text-[var(--neon-blue)]">{user?.role}</div>
                                        </div>
                                        <button
                                            onClick={handleLogout}
                                            className="w-full text-left px-4 py-3 text-sm text-[var(--text-secondary)] hover:bg-[rgba(255,60,60,0.1)] hover:text-[var(--neon-red)] transition-colors flex items-center gap-2"
                                        >
                                            <LogOut size={14} /> Sign Out
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <div className="flex-1 overflow-auto p-8 relative z-10 scroll-smooth">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
