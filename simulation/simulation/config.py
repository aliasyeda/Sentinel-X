"""
Sentinel-X Prime - Configuration
Centralized configuration for the simulation
"""
from enum import Enum

class ServiceType(Enum):
    WEB = "web"
    DATABASE = "database"
    AUTH = "auth"
    CACHE = "cache"
    LOAD_BALANCER = "lb"

class IncidentType(Enum):
    HIGH_TRAFFIC = "high_traffic"
    SERVICE_CRASH = "service_crash"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SLOW_RESPONSE = "slow_response"
    DATABASE_CONNECTION_FAILURE = "database_connection_failure"
    MEMORY_LEAK = "memory_leak"

class Config:
    """Main configuration class"""
    
    # Simulation settings
    SIMULATION_CYCLES = 50
    INCIDENT_PROBABILITY = 0.3
    
    # Service definitions
    SERVICES = [
        {"name": "web-server-1", "type": ServiceType.WEB},
        {"name": "database-primary", "type": ServiceType.DATABASE},
        {"name": "auth-service", "type": ServiceType.AUTH},
        {"name": "cache-redis", "type": ServiceType.CACHE},
        {"name": "load-balancer", "type": ServiceType.LOAD_BALANCER}
    ]
    
    # Incident severity mapping
    SEVERITY_LEVELS = {
        "low": {"color": "🟡", "priority": 3, "auto_heal_threshold": 0.8},
        "medium": {"color": "🟠", "priority": 2, "auto_heal_threshold": 0.6},
        "high": {"color": "🔴", "priority": 1, "auto_heal_threshold": 0.4},
        "critical": {"color": "💀", "priority": 0, "auto_heal_threshold": 0.2}
    }
    
    # Output paths
    INCIDENT_LOG_PATH = "memory/incidents.json"
    SYSTEM_STATE_PATH = "memory/system_state.json"