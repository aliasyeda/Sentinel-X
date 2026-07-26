import React, { useState, useEffect } from 'react';

export const PulsingDot = ({ color = 'var(--neon-green)', size = '8px' }) => (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <div className="absolute w-full h-full rounded-full opacity-75 animate-ping" style={{ backgroundColor: color }}></div>
        <div className="relative w-full h-full rounded-full" style={{ backgroundColor: color }}></div>
    </div>
);

export const ScanLine = ({ active = true }) => {
    if (!active) return null;
    return (
        <div className="absolute inset-0 pointer-events-none z-0 opacity-20 animate-scan"></div>
    );
};

export const TypewriterText = ({ text, speed = 30, className = '' }) => {
    const [displayedText, setDisplayedText] = useState('');

    useEffect(() => {
        let i = 0;
        setDisplayedText('');
        const timer = setInterval(() => {
            if (i < text.length) {
                setDisplayedText(prev => prev + text.charAt(i));
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
        return () => clearInterval(timer);
    }, [text, speed]);

    return <span className={`font-mono ${className}`}>{displayedText}</span>;
};

export const StatusLight = ({ status }) => {
    let color = 'var(--text-dim)';
    let animate = false;

    if (status === 'SECURE') color = 'var(--neon-green)';
    if (status === 'WARNING') color = 'var(--neon-orange)';
    if (status === 'CRITICAL' || status === 'ATTACK') {
        color = 'var(--neon-red)';
        animate = true;
    }

    return (
        <div className={`w-3 h-3 rounded-full ${animate ? 'animate-pulse' : ''}`} style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }}></div>
    );
};
