"""
Sentinel-X Prime - Perception Agent (Windows Compatible)
Fixed version for Windows Unicode issues
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any

class PerceptionAgent:
    """
    The first AI agent in the Sentinel-X Prime system.
    Its job: Read raw incidents and understand what's happening.
    """
    
    def __init__(self):
        self.incident_patterns = {
            "high_traffic": {
                "keywords": ["high traffic", "connections", "throughput", "cpu usage"],
                "priority": 2,
                "category": "performance"
            },
            "service_crash": {
                "keywords": ["crashed", "not responding", "down", "error", "signal"],
                "priority": 1,
                "category": "availability"
            },
            "unauthorized_access": {
                "keywords": ["failed login", "unauthorized", "access", "attempts", "ip"],
                "priority": 0,  # Highest priority
                "category": "security"
            },
            "slow_response": {
                "keywords": ["slow", "response time", "timeout", "latency"],
                "priority": 3,
                "category": "performance"
            },
            "database_connection_failure": {
                "keywords": ["database", "connection", "timeout", "authentication"],
                "priority": 1,
                "category": "infrastructure"
            },
            "memory_leak": {
                "keywords": ["memory", "leak", "increasing", "usage", "heap"],
                "priority": 2,
                "category": "resource"
            }
        }
        
        self.service_importance = {
            "database-primary": 10,  # Most important
            "auth-service": 9,
            "load-balancer": 8,
            "web-server-1": 7,
            "cache-redis": 6
        }
    
    def load_incidents(self, filepath: str) -> List[Dict]:
        """Load incidents from JSON file"""
        try:
            with open(filepath, 'r') as f:
                incidents = json.load(f)
            print(f"Loaded {len(incidents)} incidents from {filepath}")
            return incidents
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            print("Run Day 1 simulation first!")
            return []
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {filepath}: {e}")
            return []
    
    def analyze_incident(self, incident: Dict) -> Dict[str, Any]:
        """
        Analyze a single incident and create a structured understanding
        """
        raw_type = incident.get("type", "unknown")
        incident_type = raw_type.lower().replace(" ", "_")
        
        service = incident.get("service", "unknown")
        severity = incident.get("severity", "unknown")
        description = incident.get("description", "")
        metrics = incident.get("metrics", {})
        
        pattern = self.incident_patterns.get(incident_type, {})
        
        impact_score = self._calculate_impact_score(
            incident_type, 
            severity, 
            service,
            metrics
        )
        
        summary = self._generate_summary(
            incident_type, 
            service, 
            severity, 
            description,
            metrics
        )
        
        key_metrics = self._extract_key_metrics(incident_type, metrics)
        recommended_actions = self._suggest_actions(incident_type, severity, service)
        
        return {
            "incident_id": incident.get("timestamp", "").replace(":", "-").replace(".", "-"),
            "raw_incident": incident,
            "analysis": {
                "type": incident_type,
                "raw_type": raw_type,
                "category": pattern.get("category", "unknown"),
                "priority": pattern.get("priority", 3),
                "service": service,
                "service_importance": self.service_importance.get(service, 5),
                "severity": severity,
                "impact_score": impact_score,
                "human_summary": summary,
                "key_metrics": key_metrics,
                "timestamp": incident.get("timestamp", ""),
                "cycle": incident.get("cycle", 0)
            },
            "recommendations": {
                "immediate_actions": recommended_actions,
                "investigation_areas": self._get_investigation_areas(incident_type),
                "estimated_time_to_resolve": self._estimate_resolution_time(incident_type, severity)
            },
            "perception_metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "confidence": 0.85,
                "requires_human_review": severity in ["critical", "high"]
            }
        }
    
    def _calculate_impact_score(self, incident_type: str, severity: str, 
                               service: str, metrics: Dict) -> float:
        score = 0.0
        
        severity_scores = {"critical": 10, "high": 7, "medium": 4, "low": 1}
        score += severity_scores.get(severity, 3)
        
        importance = self.service_importance.get(service, 5) / 10.0
        score *= importance
        
        type_multipliers = {
            "unauthorized_access": 1.5,
            "service_crash": 1.3,
            "database_connection_failure": 1.4,
            "high_traffic": 1.1,
            "memory_leak": 1.2,
            "slow_response": 1.0
        }
        score *= type_multipliers.get(incident_type, 1.0)
        
        if incident_type == "high_traffic" and metrics.get("cpu_usage", 0) > 90:
            score += 2
        if incident_type == "memory_leak" and metrics.get("memory_usage", 0) > 95:
            score += 3
        
        return round(score, 2)
    
    def _generate_summary(self, incident_type: str, service: str, 
                         severity: str, description: str, metrics: Dict) -> str:
        # Remove emojis for Windows compatibility
        templates = {
            "high_traffic": [
                f"[PERF] Performance Alert: {service} experiencing unusually high traffic.",
                f"[TRAFFIC] Traffic Spike: {service} showing {metrics.get('connections', 'high')} connections with {metrics.get('cpu_usage', 'elevated')}% CPU usage.",
                f"[CAPACITY] Capacity Warning: {service} may require scaling due to traffic surge."
            ],
            "service_crash": [
                f"[CRITICAL] CRITICAL: {service} has crashed and is unavailable.",
                f"[FAILURE] Service Failure: {service} stopped responding with error {metrics.get('error_code', 'unknown')}.",
                f"[EMERGENCY] Emergency: {service} is DOWN requiring immediate intervention."
            ],
            "unauthorized_access": [
                f"[SECURITY] SECURITY ALERT: Suspicious login attempts on {service}.",
                f"[ACCESS] Access Violation: {metrics.get('failed_attempts', 'multiple')} failed attempts from IP {metrics.get('source_ip', 'unknown')}.",
                f"[BREACH] Breach Attempt: Potential security breach in progress on {service}."
            ],
            "slow_response": [
                f"[PERF] Performance Degradation: {service} responding slowly.",
                f"[LATENCY] Latency Issue: Average response time {metrics.get('avg_response_time', 'high')}ms on {service}.",
                f"[DEGRADED] Service Degraded: {service} experiencing performance issues."
            ],
            "database_connection_failure": [
                f"[DB] Database Issue: {service} cannot connect to database.",
                f"[CONNECTION] Connection Failure: Database connectivity lost for {service}.",
                f"[STORAGE] Storage Problem: {service} experiencing database access issues."
            ],
            "memory_leak": [
                f"[RESOURCE] Resource Alert: {service} showing memory usage of {metrics.get('memory_usage', 'high')}%.",
                f"[MEMORY] Memory Growth: {service} memory increasing at {metrics.get('leak_rate', 'unknown')}.",
                f"[EXHAUSTION] Resource Exhaustion: {service} may crash due to memory leak."
            ]
        }
        
        template_list = templates.get(incident_type, [description])
        severity_index = {"critical": 2, "high": 1, "medium": 1, "low": 0}
        idx = min(severity_index.get(severity, 0), len(template_list) - 1)
        
        return template_list[idx]
    
    def _extract_key_metrics(self, incident_type: str, metrics: Dict) -> Dict:
        key_metrics = {}
        
        if incident_type == "high_traffic":
            key_metrics = {
                "connections": metrics.get("connections", 0),
                "cpu_usage": f"{metrics.get('cpu_usage', 0)}%",
                "response_time": f"{metrics.get('response_time', 0)}ms",
                "status": "Overloaded" if metrics.get("cpu_usage", 0) > 80 else "Warning"
            }
        elif incident_type == "service_crash":
            key_metrics = {
                "status": "DOWN",
                "error_code": metrics.get("error_code", "Unknown"),
                "uptime_before_crash": metrics.get("uptime_before_crash", "Unknown"),
                "recovery_action": "Restart required"
            }
        elif incident_type == "unauthorized_access":
            key_metrics = {
                "attempts": metrics.get("failed_attempts", 0),
                "source_ip": metrics.get("source_ip", "Unknown"),
                "user_targeted": metrics.get("user_account", "Unknown"),
                "risk_level": "HIGH" if metrics.get("failed_attempts", 0) > 20 else "MEDIUM"
            }
        else:
            key_metrics = metrics.copy()
        
        return key_metrics
    
    def _suggest_actions(self, incident_type: str, severity: str, service: str) -> List[str]:
        actions = []
        
        if incident_type == "high_traffic":
            actions = [
                f"Monitor {service} CPU and memory closely",
                f"Consider scaling {service} horizontally",
                f"Check if this is a legitimate traffic surge or DDoS"
            ]
            if severity in ["high", "critical"]:
                actions.append(f"[IMMEDIATE] Implement rate limiting on {service}")
        
        elif incident_type == "service_crash":
            actions = [
                f"[IMMEDIATE] Restart {service}",
                f"Check logs for error: {service}",
                f"Verify dependencies of {service} are running",
                f"Monitor restart process of {service}"
            ]
        
        elif incident_type == "unauthorized_access":
            actions = [
                f"[IMMEDIATE] Block IP in firewall",
                f"Review authentication logs for {service}",
                f"Check for compromised accounts on {service}",
                f"Enable MFA if not already enabled"
            ]
            if severity == "critical":
                actions.append(f"[CONSIDER] Temporarily isolate {service}")
        
        elif incident_type == "slow_response":
            actions = [
                f"Check database queries on {service}",
                f"Monitor external API dependencies",
                f"Review recent deployments to {service}",
                f"Check for resource contention"
            ]
        
        elif incident_type == "database_connection_failure":
            actions = [
                f"Check database server status",
                f"Verify network connectivity to database",
                f"Review database connection pool settings",
                f"Check for database locks or deadlocks"
            ]
        
        elif incident_type == "memory_leak":
            actions = [
                f"Monitor memory usage trend on {service}",
                f"Check for recent code changes to {service}",
                f"Consider restarting {service} during low traffic",
                f"Profile memory allocation in {service}"
            ]
        
        if severity == "critical":
            actions.insert(0, "[URGENT] Requires immediate human intervention")
        elif severity == "high":
            actions.insert(0, "[HIGH PRIORITY] Address within 15 minutes")
        
        return actions
    
    def _get_investigation_areas(self, incident_type: str) -> List[str]:
        investigation_map = {
            "high_traffic": ["Network traffic", "User behavior", "DDoS protection", "Auto-scaling config"],
            "service_crash": ["Application logs", "System resources", "Dependencies", "Recent changes"],
            "unauthorized_access": ["Access logs", "Firewall rules", "User accounts", "Network ingress"],
            "slow_response": ["Database performance", "External APIs", "Code efficiency", "Infrastructure"],
            "database_connection_failure": ["Database server", "Network", "Credentials", "Connection pooling"],
            "memory_leak": ["Code profiling", "Library versions", "Resource management", "Monitoring gaps"]
        }
        return investigation_map.get(incident_type, ["General system investigation"])
    
    def _estimate_resolution_time(self, incident_type: str, severity: str) -> str:
        base_times = {
            "high_traffic": "10-30 minutes",
            "service_crash": "5-15 minutes",
            "unauthorized_access": "15-60 minutes",
            "slow_response": "30-120 minutes",
            "database_connection_failure": "15-45 minutes",
            "memory_leak": "60-240 minutes"
        }
        
        base = base_times.get(incident_type, "Unknown")
        
        if severity == "critical":
            return f"{base.split('-')[0]} minutes (URGENT)"
        elif severity == "high":
            return f"{base}"
        else:
            return base
    
    def process_all_incidents(self, incidents: List[Dict]) -> List[Dict]:
        analyzed_incidents = []
        
        print(f"\nPerception Agent analyzing {len(incidents)} incidents...")
        print("-" * 60)
        
        for i, incident in enumerate(incidents):
            analysis = self.analyze_incident(incident)
            analyzed_incidents.append(analysis)
            
            if i < 3:
                print(f"\nIncident {i+1} Analysis:")
                print(f"   Type: {analysis['analysis']['type'].replace('_', ' ').title()}")
                print(f"   Service: {analysis['analysis']['service']}")
                print(f"   Severity: {analysis['analysis']['severity'].upper()}")
                print(f"   Impact Score: {analysis['analysis']['impact_score']}/10")
                print(f"   Summary: {analysis['analysis']['human_summary']}")
        
        print(f"\nAnalysis complete! {len(analyzed_incidents)} incidents structured.")
        return analyzed_incidents
    
    def save_analysis(self, analyzed_incidents: List[Dict], filepath: str):
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(analyzed_incidents, f, indent=2)
        
        print(f"Analysis saved to: {filepath}")
        
        summary_path = filepath.replace(".json", "_summary.txt")
        self._create_summary_report(analyzed_incidents, summary_path)
    
    def _create_summary_report(self, analyzed_incidents: List[Dict], filepath: str):
        if not analyzed_incidents:
            return
        
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SENTINEL-X PRIME - PERCEPTION AGENT REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Incidents Analyzed: {len(analyzed_incidents)}\n\n")
            
            type_counts = {}
            for incident in analyzed_incidents:
                inc_type = incident['analysis']['type']
                type_counts[inc_type] = type_counts.get(inc_type, 0) + 1
            
            f.write("INCIDENT BREAKDOWN:\n")
            for inc_type, count in type_counts.items():
                f.write(f"   • {inc_type.replace('_', ' ').title():25}: {count:3d}\n")
            
            f.write("\nHIGH PRIORITY INCIDENTS:\n")
            high_priority = [i for i in analyzed_incidents 
                           if i['analysis']['severity'] in ['critical', 'high']]
            
            for incident in high_priority[:5]:
                f.write(f"   [PRIORITY] {incident['analysis']['service']}: ")
                f.write(f"{incident['analysis']['human_summary']}\n")
            
            avg_impact = sum(i['analysis']['impact_score'] for i in analyzed_incidents) / len(analyzed_incidents)
            f.write(f"\nSYSTEM HEALTH SCORE: {10 - avg_impact:.1f}/10\n")
            
            if avg_impact > 7:
                f.write("   [BAD] Status: POOR - Multiple critical incidents\n")
            elif avg_impact > 4:
                f.write("   [WARN] Status: DEGRADED - Requires attention\n")
            else:
                f.write("   [GOOD] Status: GOOD - System stable\n")
        
        print(f"Summary report saved to: {filepath}")


def main():
    print("=" * 60)
    print("SENTINEL-X PRIME - DAY 2: PERCEPTION AGENT")
    print("=" * 60)
    
    agent = PerceptionAgent()
    incidents = agent.load_incidents("memory/incidents.json")
    
    if not incidents:
        print("No incidents found. Run Day 1 simulation first!")
        return
    
    analyzed_incidents = agent.process_all_incidents(incidents)
    agent.save_analysis(analyzed_incidents, "memory/analyzed_incidents.json")
    
    print("\n" + "=" * 60)
    print("DAY 2 SUMMARY")
    print("=" * 60)
    
    critical_count = sum(1 for i in analyzed_incidents 
                        if i['analysis']['severity'] == 'critical')
    high_count = sum(1 for i in analyzed_incidents 
                    if i['analysis']['severity'] == 'high')
    
    print(f"Incidents analyzed: {len(analyzed_incidents)}")
    print(f"Critical incidents: {critical_count}")
    print(f"High severity: {high_count}")
    
    if analyzed_incidents:
        avg_impact = sum(i['analysis']['impact_score'] for i in analyzed_incidents) / len(analyzed_incidents)
        print(f"Average impact score: {avg_impact:.2f}/10")
    
    print("\nFiles created:")
    print("   memory/analyzed_incidents.json - Full analysis")
    print("   memory/analyzed_incidents_summary.txt - Human-readable report")
    
    print("\n" + "=" * 60)
    print("DAY 2 COMPLETE! Perception Agent is operational.")
    print("Next: Day 3 - Reasoning Agent (AI-powered analysis)")
    print("=" * 60)


if __name__ == "__main__":
    main()