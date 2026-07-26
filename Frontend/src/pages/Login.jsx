import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, Key, ChevronRight, AlertTriangle } from 'lucide-react';
import { PulsingDot, ScanLine } from '../components/AnimatedComponents';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);

        try {
            await login(username, password);
            navigate('/overview');
        } catch (err) {
            setError(err);
            setIsLoading(false);
        }
    };

    // Auto-fill helper for demo purposes
    const fillCredentials = (u) => {
        setUsername(u);
        setPassword('demo123');
    };

    return (
        <div className="min-h-screen bg-[var(--bg-dark)] flex items-center justify-center relative overflow-hidden font-sans">

            {/* Background Effects */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,234,255,0.05)_0%,transparent_70%)]"></div>
            <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-[var(--neon-blue)] to-transparent opacity-50"></div>
            <ScanLine active={true} />

            <div className="relative z-10 w-full max-w-md px-6">

                {/* Header Logo */}
                <div className="flex flex-col items-center mb-8 animate-fade-in">
                    <div className="w-16 h-16 rounded-xl bg-gradient-to-tr from-[rgba(0,243,255,0.2)] to-[rgba(0,102,255,0.2)] border border-[var(--neon-blue)] flex items-center justify-center shadow-[0_0_30px_rgba(0,234,255,0.2)] mb-4">
                        <Shield className="text-[var(--neon-blue)]" size={32} />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight text-white mb-1">SENTINEL-X</h1>
                    <p className="text-[var(--text-dim)] text-xs uppercase tracking-[0.2em]">Enterprise Security Platform</p>
                </div>

                {/* Login Card */}
                <div className="glass-panel p-8 rounded-2xl border border-[var(--border-color)] shadow-2xl backdrop-blur-xl relative overflow-hidden animate-fade-in" style={{ animationDelay: '0.1s' }}>

                    {/* Decorative Corner */}
                    <div className="absolute top-0 right-0 w-16 h-16 pointer-events-none overflow-hidden">
                        <div className="absolute top-0 right-0 w-2 h-2 bg-[var(--neon-blue)]"></div>
                        <div className="absolute top-0 right-2 w-8 h-[1px] bg-[var(--neon-blue)] opacity-50"></div>
                        <div className="absolute top-2 right-0 w-[1px] h-8 bg-[var(--neon-blue)] opacity-50"></div>
                    </div>

                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                        <Lock size={18} className="text-[var(--neon-green)]" />
                        Secure Login
                    </h2>

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="space-y-1">
                            <label className="text-xs font-medium text-[var(--text-secondary)] uppercase tracking-wider ml-1">Identity</label>
                            <div className="relative group">
                                <User className="absolute left-3 top-3 text-[var(--text-dim)] group-focus-within:text-[var(--neon-blue)] transition-colors" size={18} />
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full bg-[rgba(255,255,255,0.03)] border border-[var(--border-color)] rounded-lg py-2.5 pl-10 pr-4 text-white placeholder-[var(--text-dim)] focus:outline-none focus:border-[var(--neon-blue)] focus:bg-[rgba(0,234,255,0.05)] transition-all"
                                    placeholder="Enter Username"
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-1">
                            <label className="text-xs font-medium text-[var(--text-secondary)] uppercase tracking-wider ml-1">Access Key</label>
                            <div className="relative group">
                                <Key className="absolute left-3 top-3 text-[var(--text-dim)] group-focus-within:text-[var(--neon-blue)] transition-colors" size={18} />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-[rgba(255,255,255,0.03)] border border-[var(--border-color)] rounded-lg py-2.5 pl-10 pr-4 text-white placeholder-[var(--text-dim)] focus:outline-none focus:border-[var(--neon-blue)] focus:bg-[rgba(0,234,255,0.05)] transition-all"
                                    placeholder="Enter Password"
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="bg-[rgba(255,60,60,0.1)] border border-[rgba(255,60,60,0.3)] rounded p-2 flex items-center gap-2 text-[var(--neon-red)] text-sm animate-fade-in">
                                <AlertTriangle size={14} />
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={isLoading}
                            className={`w-full py-3 rounded-lg font-bold text-sm uppercase tracking-wider flex items-center justify-center gap-2 transition-all duration-300
                            ${isLoading
                                    ? 'bg-[rgba(255,255,255,0.1)] text-[var(--text-dim)] cursor-wait'
                                    : 'bg-gradient-to-r from-[var(--neon-blue)] to-[#0066ff] text-white hover:shadow-[0_0_20px_rgba(0,234,255,0.4)] hover:scale-[1.02]'
                                }`}
                        >
                            {isLoading ? 'Authenticating...' : (
                                <>
                                    Establish Session <ChevronRight size={16} />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Quick Login Helpers (For Demo) */}
                    <div className="mt-8 pt-6 border-t border-[rgba(255,255,255,0.05)]">
                        <div className="text-[10px] text-[var(--text-dim)] text-center mb-3">DEMO ACCESS PROFILES</div>
                        <div className="flex gap-2 justify-center">
                            {['Syed', 'Alia', 'Samiya'].map(user => (
                                <button
                                    key={user}
                                    onClick={() => fillCredentials(user)}
                                    className="px-3 py-1.5 rounded border border-[rgba(255,255,255,0.1)] bg-[rgba(255,255,255,0.02)] text-[var(--text-secondary)] text-xs hover:border-[var(--neon-blue)] hover:text-[var(--neon-blue)] transition-all"
                                >
                                    {user}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="mt-8 text-center text-[10px] text-[var(--text-dim)] font-mono">
                    SECURED BY SENTINEL-X CORE v4.3.0
                    <br />
                    UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED
                </div>
            </div>
        </div>
    );
};

export default Login;
