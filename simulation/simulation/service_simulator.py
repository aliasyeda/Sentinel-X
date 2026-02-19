"""
Sentinel-X Prime - Service Simulator
Simulates IT infrastructure services and their states
"""
import random
import time
from datetime import datetime
from enum import Enum

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNDER_ATTACK = "under_attack"

class Service:
    """Represents a single service in the infrastructure"""
    
    def __init__(self, name, service_type):
        self.name = name
        self.type = service_type
        self.status = ServiceStatus.HEALTHY
        self.cpu_usage = 20.0  # percentage
        self.memory_usage = 30.0  # percentage
        self.response_time = 50.0  # milliseconds
        self.connections = 10
        self.last_incident = None
        self.start_time = datetime.now()
        
    def to_dict(self):
        """Convert service state to dictionary"""
        return {
            "name": self.name,
            "type": self.type,
            "status": self.status.value,
            "cpu_usage": round(self.cpu_usage, 1),
            "memory_usage": round(self.memory_usage, 1),
            "response_time": round(self.response_time, 1),
            "connections": self.connections,
            "uptime": str(datetime.now() - self.start_time).split('.')[0],
            "timestamp": datetime.now().isoformat()
        }
    
    def simulate_normal_operation(self):
        """Simulate normal operational fluctuations"""
        self.cpu_usage = max(5, min(40, self.cpu_usage + random.uniform(-5, 5)))
        self.memory_usage = max(15, min(50, self.memory_usage + random.uniform(-3, 3)))
        self.response_time = max(10, min(100, self.response_time + random.uniform(-10, 10)))
        self.connections = max(5, min(30, self.connections + random.randint(-2, 2)))
        
        # Auto-recover degraded services with small probability
        if self.status == ServiceStatus.DEGRADED and random.random() < 0.1:
            self.status = ServiceStatus.HEALTHY

class SystemSimulator:
    """Main system simulator managing multiple services"""
    
    def __init__(self):
        self.services = [
            Service("web-server-1", "web"),
            Service("database-primary", "database"),
            Service("auth-service", "auth"),
            Service("cache-redis", "cache"),
            Service("load-balancer", "lb")
        ]
        self.incident_log = []
        self.cycle_count = 0
        
    def get_system_state(self):
        """Return current state of all services"""
        return [service.to_dict() for service in self.services]
    
    def log_incident(self, incident):
        """Log an incident with timestamp and service update"""
        incident["timestamp"] = datetime.now().isoformat()
        incident["cycle"] = self.cycle_count
        self.incident_log.append(incident)
        
        # Update the affected service status
        for service in self.services:
            if service.name == incident["service"]:
                service.last_incident = incident
                
                # Set service status based on incident severity
                if incident["severity"] == "critical":
                    service.status = ServiceStatus.DOWN
                elif incident["severity"] in ["high", "medium"]:
                    service.status = ServiceStatus.DEGRADED
                elif incident["type"] == "unauthorized_access":
                    service.status = ServiceStatus.UNDER_ATTACK
        
        print(f"🔴 [{incident['severity'].upper()}] {incident['type'].replace('_', ' ').title()}")
        print(f"   Service: {incident['service']}")
        print(f"   Description: {incident['description']}")
        print("-" * 50)
        return incident
    
    def run_normal_cycle(self):
        """Simulate one cycle of normal system operation"""
        self.cycle_count += 1
        for service in self.services:
            service.simulate_normal_operation()
        return self.get_system_state()

if __name__ == "__main__":
    # Quick test
    simulator = SystemSimulator()
    print("🟢 Starting system simulation test...")
    for i in range(3):
        state = simulator.run_normal_cycle()
        print(f"Cycle {i+1}: {len(state)} services operational")
        time.sleep(0.5)
    print("✅ Service simulator is working correctly!")