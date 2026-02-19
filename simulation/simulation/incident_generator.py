"""
Sentinel-X Prime - Incident Generator
Generates realistic cybersecurity incidents for simulation
"""
import random
import json
import os
from datetime import datetime
from service_simulator import SystemSimulator, ServiceStatus
from config import Config, IncidentType

class IncidentGenerator:
    """Generates realistic incidents for the system"""
    
    def __init__(self, simulator):
        self.simulator = simulator
        self.incident_probability = Config.INCIDENT_PROBABILITY
        
    def generate_incident(self):
        """Randomly generate an incident based on probability"""
        if random.random() > self.incident_probability:
            return None
            
        incident_type = random.choice(list(IncidentType))
        service = random.choice(self.simulator.services)
        
        incidents = {
            IncidentType.HIGH_TRAFFIC: {
                "type": "high_traffic",
                "service": service.name,
                "severity": random.choice(["medium", "high"]),
                "description": f"Unusual high traffic detected on {service.name}",
                "metrics": {
                    "connections": random.randint(100, 1000),
                    "cpu_usage": random.randint(80, 100),
                    "response_time": random.randint(500, 2000),
                    "throughput": f"{random.randint(10, 100)} GB/hour"
                }
            },
            IncidentType.SERVICE_CRASH: {
                "type": "service_crash",
                "service": service.name,
                "severity": "critical",
                "description": f"{service.name} has crashed and is not responding",
                "metrics": {
                    "status": "down",
                    "error_code": random.choice(["500", "503", "404"]),
                    "uptime_before_crash": f"{random.randint(1, 72)} hours",
                    "last_signal": random.choice(["SIGSEGV", "SIGKILL", "SIGTERM"])
                }
            },
            IncidentType.UNAUTHORIZED_ACCESS: {
                "type": "unauthorized_access",
                "service": service.name,
                "severity": random.choice(["high", "critical"]),
                "description": f"Multiple failed login attempts detected on {service.name}",
                "metrics": {
                    "failed_attempts": random.randint(10, 100),
                    "source_ip": f"192.168.1.{random.randint(1, 255)}",
                    "user_account": random.choice(["admin", "root", "service_user"]),
                    "geolocation": random.choice(["Unknown", "RU", "CN", "US"])
                }
            },
            IncidentType.SLOW_RESPONSE: {
                "type": "slow_response",
                "service": service.name,
                "severity": "low",
                "description": f"{service.name} responding slowly to requests",
                "metrics": {
                    "avg_response_time": random.randint(1000, 5000),
                    "timeout_percentage": random.randint(10, 40),
                    "p95_latency": random.randint(2000, 8000)
                }
            },
            IncidentType.DATABASE_CONNECTION_FAILURE: {
                "type": "database_connection_failure",
                "service": service.name,
                "severity": "high",
                "description": f"{service.name} unable to connect to database",
                "metrics": {
                    "connection_pool": 0,
                    "queue_size": random.randint(50, 200),
                    "error": random.choice(["Connection timeout", "Authentication failed", "Network unreachable"]),
                    "retry_count": random.randint(3, 10)
                }
            },
            IncidentType.MEMORY_LEAK: {
                "type": "memory_leak",
                "service": service.name,
                "severity": "medium",
                "description": f"Memory usage steadily increasing on {service.name}",
                "metrics": {
                    "memory_usage": random.randint(85, 99),
                    "leak_rate": f"{random.randint(1, 10)}MB/minute",
                    "heap_usage": random.randint(70, 95)
                }
            }
        }
        
        incident = incidents[incident_type]
        return self.simulator.log_incident(incident)
    
    def simulate_day(self, cycles=50):
        """Simulate multiple cycles of operation with potential incidents"""
        incidents = []
        print(f"\n📊 Simulating {cycles} cycles of system operation...")
        print(f"   Incident probability: {self.incident_probability*100}% per cycle")
        print("-" * 50)
        
        for cycle in range(cycles):
            # Normal operation
            self.simulator.run_normal_cycle()
            
            # Generate incident
            incident = self.generate_incident()
            if incident:
                incidents.append(incident)
            
            # Progress indicator
            if cycle % 10 == 0:
                healthy = sum(1 for s in self.simulator.services if s.status == ServiceStatus.HEALTHY)
                print(f"  Cycle {cycle:3d}/{cycles} | Healthy services: {healthy}/5")
        
        print("-" * 50)
        print(f"\n📈 SIMULATION COMPLETE")
        print(f"   Total cycles: {cycles}")
        print(f"   Incidents generated: {len(incidents)}")
        
        # Ensure memory directory exists
        os.makedirs("../memory", exist_ok=True)
        
        # Save incidents to file
        with open("../memory/incidents.json", "w") as f:
            json.dump(incidents, f, indent=2, default=str)
        
        # Save final system state
        with open("../memory/system_state.json", "w") as f:
            json.dump(self.simulator.get_system_state(), f, indent=2, default=str)
        
        print(f"   Incident log saved to: ../memory/incidents.json")
        print(f"   System state saved to: ../memory/system_state.json")
        
        return incidents

def main():
    """Main execution function"""
    print("=" * 60)
    print("SENTINEL-X PRIME - SYSTEM SIMULATION")
    print("=" * 60)
    
    # Initialize simulator and generator
    simulator = SystemSimulator()
    generator = IncidentGenerator(simulator)
    
    # Run simulation
    incidents = generator.simulate_day(cycles=Config.SIMULATION_CYCLES)
    
    # Print summary
    if incidents:
        print("\n📋 RECENT INCIDENTS:")
        for i, incident in enumerate(incidents[-3:]):  # Show last 3
            severity_color = Config.SEVERITY_LEVELS[incident['severity']]['color']
            print(f"{severity_color} {incident['type'].replace('_', ' ').title():25} on {incident['service']:20} ({incident['severity']})")
        
        # Statistics
        print(f"\n📊 STATISTICS:")
        incident_types = {}
        for incident in incidents:
            incident_types[incident['type']] = incident_types.get(incident['type'], 0) + 1
        
        for inc_type, count in incident_types.items():
            percentage = (count / len(incidents)) * 100
            print(f"   {inc_type.replace('_', ' ').title():25}: {count:3d} ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ DAY 1 COMPLETE: System simulation is ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()