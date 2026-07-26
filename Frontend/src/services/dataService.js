
// Service to fetch data from the backend JSON files
// These files are expected to be located in the /memory/memory/ directory at the project root

const BASE_PATH = '/memory/memory';

// Helper to fetch and parse JSON
const fetchData = async (filename) => {
    try {
        const timestamp = new Date().getTime(); // Prevent caching
        const response = await fetch(`${BASE_PATH}/${filename}?t=${timestamp}`);
        if (!response.ok) {
            console.warn(`Failed to fetch ${filename}: ${response.statusText}`);
            return []; // Return empty array/object on failure to prevent crash
        }
        return await response.json();
    } catch (error) {
        console.error(`Error loading ${filename}:`, error);
        return [];
    }
};

export const fetchIncidents = async () => {
    return await fetchData('analyzed_incidents.json');
};

export const fetchDecisions = async () => {
    const data = await fetchData('decisions_enhanced.json');
    // The file structure has a "decisions" array within the root object
    return data.decisions || [];
};

export const fetchRootCause = async () => {
    return await fetchData('root_cause_analysis.json');
};

export const fetchGovernance = async () => {
    const data = await fetchData('autonomy_governance.json');
    return data.governance_decisions || [];
};

export const fetchActionLog = async () => {
    return await fetchData('action_log.json');
};

export const fetchSystemStatus = async () => {
    // In a real scenario, this might come from a dedicated status endpoint
    // Here we derive it from incidents and decisions
    const incidents = await fetchIncidents();
    const actions = await fetchActionLog();

    const activeIncidents = incidents.filter(i => i.analysis && i.analysis.severity === 'critical').length;
    const activeThreats = incidents.length;

    return {
        status: activeIncidents > 0 ? 'CRITICAL' : 'SECURE',
        activeThreats: activeThreats,
        networkLoad: '45%', // Mock for now, could be derived
        autonomyLevel: 'LEVEL 4', // Fixed for now
        health: Math.max(0, 100 - (activeIncidents * 10))
    };
};
