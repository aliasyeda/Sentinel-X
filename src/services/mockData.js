// SENTINEL-X Mock Data Service
// Simulates API responses for the frontend dashboard.

export const fetchSystemStatus = () => {
    return {
        status: 'SECURE',
        health: 98.2,
        activeThreats: 0,
        networkLoad: '64 TB',
        nodesOnline: 142,
        autonomyLevel: 'LEVEL 4'
    };
};

export const fetchActivityData = () => {
    return [
        { time: '00:00', traffic: 4000, threats: 24 },
        { time: '04:00', traffic: 3000, threats: 13 },
        { time: '08:00', traffic: 2000, threats: 98 },
        { time: '12:00', traffic: 2780, threats: 39 },
        { time: '16:00', traffic: 1890, threats: 48 },
        { time: '20:00', traffic: 2390, threats: 38 },
        { time: '24:00', traffic: 3490, threats: 43 },
    ];
};

export const fetchSystemNodes = () => {
    return [
        { id: 'NODE-A1', location: 'Virginia', type: 'Compute', status: 'Protected', load: '45%' },
        { id: 'NODE-B2', location: 'Frankfurt', type: 'Analysis', status: 'Analyzing', load: '78%' },
        { id: 'DB-MAIN', location: 'Singapore', type: 'Storage', status: 'Protected', load: '32%' },
        { id: 'GTWY-01', location: 'Tokyo', type: 'Gateway', status: 'Warning', load: '92%' },
        { id: 'EDGE-99', location: 'London', type: 'Edge', status: 'Protected', load: '12%' },
    ];
};

export const fetchIncidents = () => {
    return [
        { id: 'INC-2024-001', type: 'SQL Injection', severity: 'High', status: 'Blocked', timestamp: '2024-03-10 14:23:01', source: '192.168.1.45', score: 98 },
        { id: 'INC-2024-002', type: 'Port Scanning', severity: 'Medium', status: 'Analyzing', timestamp: '2024-03-10 14:15:22', source: '10.0.0.12', score: 65 },
        { id: 'INC-2024-003', type: 'Unusual Login', severity: 'Low', status: 'Cleared', timestamp: '2024-03-10 13:45:10', source: 'Internal', score: 32 },
        { id: 'INC-2024-004', type: 'DDoS Attempt', severity: 'Critical', status: 'Mitigated', timestamp: '2024-03-10 12:30:00', source: 'Global Botnet', score: 99 },
        { id: 'INC-2024-005', type: 'Malware Download', severity: 'High', status: 'Isolated', timestamp: '2024-03-10 11:20:15', source: 'User Endpoint', score: 88 },
    ];
};

export const fetchDecisions = () => {
    return [
        {
            id: 'DEC-8921',
            trigger: 'Anomalous traffic from unknown IP range detected affecting DB-MAIN.',
            aiAnalysis: 'Pattern matches known Botnet signature "Red-Alpha". High probability of DDoS initiation.',
            confidence: 98.4,
            decision: 'Isolate Node & Block IP Range',
            reasoning: [
                'Request rate exceeded 5000/sec (Threshold: 1000/sec)',
                'Source IP geolocation mismatch with user profile',
                'Payload contains SQL injection patterns'
            ],
            timestamp: '16:55:22',
            impact: 'Low - Preemptive Action'
        },
        {
            id: 'DEC-8920',
            trigger: 'User login attempt failed 15 times in 1 minute.',
            aiAnalysis: 'Brute force attack signature. Source localized to internal network (compromised endpoint?).',
            confidence: 89.2,
            decision: 'Lock Account & Alert Admin',
            reasoning: [
                'Velocity check failed',
                'Password dictionary match detected'
            ],
            timestamp: '15:30:10',
            impact: 'Medium - User Lockout'
        }
    ];
};

export const fetchActions = () => {
    return [
        { id: 'ACT-9002', type: 'IP Block', target: '192.168.1.45', status: 'Success', duration: '0.2s', timestamp: '14:23:05', details: 'Added to firewall deny list permanently.' },
        { id: 'ACT-9001', type: 'Service Restart', target: 'Auth-Service-01', status: 'Success', duration: '4.5s', timestamp: '14:23:02', details: 'Restarted instance to flush thread pool.' },
        { id: 'ACT-8999', type: 'Isolate Node', target: 'NODE-B2', status: 'Pending', duration: '-', timestamp: '14:10:00', details: 'Waiting for drain connection.' },
        { id: 'ACT-8840', type: 'Patch Deployment', target: 'Entire Cluster', status: 'Failed', duration: '12s', timestamp: '12:00:00', details: 'Rollback initiated due to checksum error.' },
    ];
};

export const fetchGovernanceData = () => {
    return {
        model: 'SENTINEL-CORE-v4.3',
        lastTraining: '4 hours ago',
        patternsLearned: 142,
        policies: [
            { title: 'Auto-Isolation', status: 'Active', desc: 'System can isolate compromised nodes without human approval.', level: 'High' },
            { title: 'Data Encryption', status: 'Active', desc: 'All data at rest must be encrypted with AES-256.', level: 'Critical' },
            { title: 'External Access', status: 'Restricted', desc: 'Only VPN traffic allowed for admin interfaces.', level: 'Med' },
        ],
        logs: [
            { id: 'LOG-5501', action: 'Policy Update', user: 'Admin_Sys', timestamp: '2024-03-10 09:12:00', detail: 'Updated firewall rule set #44' },
            { id: 'LOG-5502', action: 'Manual Override', user: 'Sec_Ops_Lead', timestamp: '2024-03-10 10:45:11', detail: 'Prevented auto-shutdown of DB-Shard-04' },
            { id: 'LOG-5503', action: 'Model Retraining', user: 'System (Auto)', timestamp: '2024-03-09 23:00:00', detail: 'Ingested new threat signatures from global feed' },
        ]
    };
};

export const fetchReasoningTraces = () => {
    return [
        {
            id: 'TRACE-001',
            step: 'Context Retrieval',
            detail: 'Retrieved 4 relevant policy documents and 12 historical incident logs.',
            status: 'success',
            agent: 'Reasoning Engine'
        },
        {
            id: 'TRACE-002',
            step: 'Pattern Matching',
            detail: 'Identified SQL Injection signature with 98.4% confidence. Correlated with "Red-Alpha" botnet Activity.',
            status: 'success',
            agent: 'Reasoning Engine'
        },
        {
            id: 'TRACE-003',
            step: 'Impact Prediction',
            detail: 'Predicted 85% chance of Database Exfiltration if not blocked within 30s.',
            status: 'warning',
            agent: 'Decision Agent'
        },
        {
            id: 'TRACE-004',
            step: 'Action Formulation',
            detail: 'Selected optimal response: "Isolate Node & IP Block". Minimal service disruption expected.',
            status: 'success',
            agent: 'Decision Agent'
        }
    ];
};

export const fetchMemoryPatterns = () => {
    return [
        {
            id: 'MEM-2101',
            pattern: 'SQL Injection via Auth Headers',
            frequency: 'High (Detected 14 times)',
            confidence: 0.99,
            lastSeen: '2 mins ago',
            learnedAt: '2023-11-15'
        },
        {
            id: 'MEM-2104',
            pattern: 'Slow-loris DDoS Attack',
            frequency: 'Medium',
            confidence: 0.88,
            lastSeen: '4 days ago',
            learnedAt: '2024-01-20'
        }
    ];
};

export const fetchRootCauseAnalysis = () => {
    return {
        incidentId: 'INC-2024-001',
        primaryCause: 'Unsanitized Input Field in Legacy Auth Module',
        contributingFactors: [
            'Outdated WAF ruleset (v2.1)',
            'Missing input validation on /api/v1/login',
            'Service account has excessive read permissions'
        ],
        recommendation: 'Patch Auth Service to v4.5 and restrict DB user permissions.'
    };
};
