import React, { createContext, useContext, useState, useEffect } from 'react';

const DemoContext = createContext();

export const PHASES = {
    NORMAL: 'NORMAL',
    ATTACK: 'ATTACK_DETECTED',
    ANALYZING: 'AI_ANALYZING',
    DEFENDING: 'AUTO_DEFENSE',
    RESTORED: 'SYSTEM_RESTORED'
};

export const DemoProvider = ({ children }) => {
    const [phase, setPhase] = useState(PHASES.NORMAL);
    const [logs, setLogs] = useState([]);

    // Simulation Timer
    useEffect(() => {
        let timber;
        if (phase === PHASES.ATTACK) {
            setTimeout(() => setPhase(PHASES.ANALYZING), 5000);
        } else if (phase === PHASES.ANALYZING) {
            setTimeout(() => setPhase(PHASES.DEFENDING), 6000);
        } else if (phase === PHASES.DEFENDING) {
            setTimeout(() => setPhase(PHASES.RESTORED), 5000);
        } else if (phase === PHASES.RESTORED) {
            setTimeout(() => setPhase(PHASES.NORMAL), 4000);
        }
    }, [phase]);

    const startSimulation = () => {
        setPhase(PHASES.ATTACK);
        addLog('SIMULATION STARTED: Injecting specialized threat vector...');
    };

    const resetSimulation = () => {
        setPhase(PHASES.NORMAL);
        setLogs([]);
    };

    const addLog = (msg) => {
        setLogs(prev => [{ id: Date.now(), msg, time: new Date().toLocaleTimeString() }, ...prev]);
    };

    return (
        <DemoContext.Provider value={{ phase, startSimulation, resetSimulation, logs, addLog }}>
            {children}
        </DemoContext.Provider>
    );
};

export const useDemo = () => useContext(DemoContext);
