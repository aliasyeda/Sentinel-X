
import json
import time
import os
import random
from datetime import datetime

# Paths
MEMORY_DIR = os.path.join(os.getcwd(), 'memory', 'memory')
os.makedirs(MEMORY_DIR, exist_ok=True)

def write_json(filename, data):
    path = os.path.join(MEMORY_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    # print(f"  -> Updated {filename}")

def print_step(step, msg):
    print(f"\n[T+{step}s] {msg}")

def run_cinematic_attack():
    print("🎬 STARTING CINEMATIC ATTACK SCENARIO")
    print("=====================================")
    print("Keep your dashboard open. The show is about to start.")
    
    # T=0: Normal State
    print_step(0, "System Normal. Monitoring...")
    # (Optional: Clear files to normal first? Yes)
    # actions -> empty
    write_json('action_log.json', [])
    write_json('analyzed_incidents.json', [])
    write_json('decisions_enhanced.json', {"decisions": []})
    write_json('root_cause_analysis.json', {"root_causes": []})
    
    time.sleep(3)

    # T=3: ATTACK INJECTION
    print_step(3, "🔥 INJECTING ATTACK: Critical SQL Injection in Auth Service")
    incident_id = f"INC-{int(time.time())}"
    incident = [{
        "incident_id": incident_id,
        "raw_incident": {
            "type": "unauthorized_access",
            "service": "auth-service", 
            "severity": "critical",
            "timestamp": datetime.now().isoformat()
        },
        "analysis": {
            "type": "SQL Injection",
            "severity": "critical",
            "impact_score": 0.98,
            "timestamp": datetime.now().isoformat(),
            "human_summary": "Malicious SQL patterns detected in login payload."
        }
    }]
    write_json('analyzed_incidents.json', incident)
    print("  -> Dashboard should turn RED now.")
    
    time.sleep(4)

    # T=7: REASONING & ROOT CAUSE
    print_step(7, "🧠 AI ANALYSIS: Identifying Root Cause & Determining Action")
    
    root_cause = {
        "root_causes": [{
            "likely_root_cause": "Unsanitized Input in Legacy Auth Module",
            "evidence": {"correlation_strength": 0.99},
            "impact_assessment": "Data Exfiltration Imminent",
            "affected_services": ["auth-service", "user-db"]
        }]
    }
    write_json('root_cause_analysis.json', root_cause)
    
    decisions = {
        "decisions": [{
            "decision_id": f"DEC-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "confidence": 99,
            "trigger": "SQL Injection Pattern",
            "decision": {
                "type": "ISOLATE_HOST",
                "explainability_trace": {
                    "decision_process": [
                        {"step": "Detection", "evaluation": "Confirmed SQLi signature."},
                        {"step": "Policy", "evaluation": "Auto-Defense Active."},
                        {"step": "Action", "action": "ISOLATE_HOST"}
                    ]
                }
            },
            "reasoning": {
                "llm_analysis": "Attack vector confirms known CVE-2024-xyz. Host isolation required immediately to prevent database dump."
            }
        }]
    }
    write_json('decisions_enhanced.json', decisions)
    print("  -> Dashboard should show AI Analysis & Root Cause.")

    time.sleep(4)

    # T=11: ACTION & REMEDIATION
    print_step(11, "⚡ ACTION: Executing Autonomous Defense")
    
    actions = [{
        "action_id": f"ACT-{int(time.time())}",
        "action_type": "ISOLATE_HOST",
        "service": "auth-service",
        "status": "success",
        "estimated_duration": "0.5s",
        "risk_level": "medium",
        "timestamp": datetime.now().isoformat(),
        "action_details": {"method": "Network ACL Update"}
    }]
    write_json('action_log.json', actions)
    print("  -> Dashboard should show specific Remediation Action.")

    time.sleep(5)
    
    # T=16: GOVERNANCE LOG
    print_step(16, "⚖️ GOVERNANCE: Logging Audit Trail")
    # Update governance to show it approved the action
    gov_log = {
        "governance_decisions": [{
            "governance_id": f"GOV-{int(time.time())}",
            "recommended_autonomy_level": "FULL_AUTONOMY",
            "timestamp": datetime.now().isoformat(),
            "ai_confidence": 0.99,
            "service": "auth-service",
            "policy_applied": {"Zero_Trust_Policy": ["Block Critical Threats"]}
        }]
    }
    write_json('autonomy_governance.json', gov_log)
    
    time.sleep(5)

    # T=21: RECOVERY / MITIGATION
    print_step(21, "✅ RECOVERY: Threat Neutralized. System Stabilizing.")
    # In a real loop, we'd clear incidents or mark resolved. 
    # For demo, let's leave the logs but maybe show status change? 
    # The frontend calculates status based on active incidents. 
    # To go back to green, we'd typically archive the incident.
    # Let's clear the incident list to simulate 'Resolution'.
    write_json('analyzed_incidents.json', [])
    print("  -> Dashboard should return to GREEN/SECURE.")

    print("\n🎉 SCENARIO COMPLETE")

if __name__ == "__main__":
    run_cinematic_attack()
