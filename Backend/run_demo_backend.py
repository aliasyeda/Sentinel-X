import sys
import os
import json
import random
from datetime import datetime

# ==========================================
# 1. SETUP ENVIRONMENT & IMPORTS
# ==========================================

current_dir = os.getcwd()
simulation_dir = os.path.join(current_dir, 'simulation', 'simulation')
sys.path.append(simulation_dir)

OUTPUT_DIR = os.path.join(current_dir, 'memory', 'memory')
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    os.chdir(simulation_dir)
    from incident_generator import IncidentGenerator
    from service_simulator import SystemSimulator
    os.chdir(current_dir)
except ImportError as e:
    print(f"❌ Error importing simulation modules: {e}")
    sys.exit(1)

# ==========================================
# 2. AGENT SIMULATION LOGIC
# ==========================================

def simulate_perception_agent(incidents):
    analyzed = []

    for inc in incidents:
        severity_map = {'low': 0.2, 'medium': 0.5, 'high': 0.8, 'critical': 0.99}
        impact_score = severity_map.get(inc.get('severity', 'low'), 0.2)

        analyzed_inc = {
            "incident_id": f"INC-{random.randint(1000,9999)}",
            "analysis": {
                "type": inc.get('type', 'unknown'),
                "severity": inc.get('severity', 'low'),
                "impact_score": impact_score,
                "timestamp": datetime.now().isoformat()
            }
        }

        analyzed.append(analyzed_inc)

    return analyzed


def simulate_reasoning_agent(analyzed_incidents):
    decisions = []
    critical_count = 0

    for inc in analyzed_incidents:
        severity = inc['analysis']['severity']

        action = "MONITOR"
        if severity == "critical":
            action = "ISOLATE_HOST"
            critical_count += 1
        elif severity == "high":
            action = "BLOCK_TRAFFIC"
        elif severity == "medium":
            action = "THROTTLE_REQUESTS"

        decisions.append({
            "incident_id": inc['incident_id'],
            "decision": action
        })

    return decisions, critical_count


# ==========================================
# 3. SINGLE RUN (NO LOOP)
# ==========================================

def run_demo_once():
    print("🚀 Running Stable Demo Mode...")

    simulator = SystemSimulator()
    generator = IncidentGenerator(simulator)

    os.chdir(simulation_dir)
    raw_incidents = generator.simulate_day(cycles=1)
    os.chdir(current_dir)

    analyzed = simulate_perception_agent(raw_incidents)
    decisions, critical_count = simulate_reasoning_agent(analyzed)

    total = len(analyzed)
    warning = sum(1 for i in analyzed if i["analysis"]["severity"] == "medium")
    safe = sum(1 for i in analyzed if i["analysis"]["severity"] == "low")
    mitigated = total - critical_count

    status = "stable"
    if critical_count > 2:
        status = "critical"
    elif critical_count > 0:
        status = "warning"

    dashboard_data = {
        "total_incidents": total,
        "critical": critical_count,
        "warning": warning,
        "safe": safe,
        "mitigated": mitigated,
        "status": status
    }

    with open(os.path.join(OUTPUT_DIR, 'dashboard_data.json'), 'w') as f:
        json.dump(dashboard_data, f, indent=2)

    print("✅ Dashboard data generated successfully.")
    print("📊 Status:", status)


if __name__ == "__main__":
    run_demo_once()


