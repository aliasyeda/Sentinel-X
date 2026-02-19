"""
Sentinel-X Prime - Action Agent
Executes self-healing actions and completes the autonomous lifecycle
"""
import json
import os
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

class ActionStatus(Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class RecoveryStage(Enum):
    PREPARATION = "preparation"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    COMPLETION = "completion"

class ActionAgent:
    """
    The fourth and final AI agent in Sentinel-X Prime.
    Its job: Execute self-healing actions and complete the autonomous recovery.
    This completes the full lifecycle: Detect → Understand → Reason → Decide → Heal
    """
    
    def __init__(self):
        self.action_history = []
        self.system_state = {}
        self.load_system_state()
        
        # Action execution configurations
        self.action_configs = {
            "restart_service": {
                "stages": 4,
                "stage_names": ["Draining connections", "Stopping service", "Starting service", "Health checks"],
                "avg_duration": 180,  # 3 minutes
                "success_rate": 0.95
            },
            "scale_up": {
                "stages": 3,
                "stage_names": ["Allocating resources", "Launching instances", "Updating load balancer"],
                "avg_duration": 300,  # 5 minutes
                "success_rate": 0.90
            },
            "block_ip": {
                "stages": 2,
                "stage_names": ["Updating firewall rules", "Propagating changes"],
                "avg_duration": 60,  # 1 minute
                "success_rate": 0.98
            },
            "clear_cache": {
                "stages": 2,
                "stage_names": ["Invalidating cache", "Warming cache"],
                "avg_duration": 120,  # 2 minutes
                "success_rate": 0.97
            },
            "isolate_service": {
                "stages": 3,
                "stage_names": ["Disconnecting network", "Suspending processes", "Logging isolation"],
                "avg_duration": 90,  # 1.5 minutes
                "success_rate": 0.99
            },
            "rollback": {
                "stages": 4,
                "stage_names": ["Creating backup", "Reverting changes", "Restarting service", "Verifying rollback"],
                "avg_duration": 600,  # 10 minutes
                "success_rate": 0.85
            }
        }
        
        print("[Action Agent] Initialized - Ready for self-healing execution")
        
        # FIX: Handle both dict and list formats safely
        if isinstance(self.system_state, dict):
            services_count = len(self.system_state.get('services', []))
        elif isinstance(self.system_state, list):
            services_count = len(self.system_state)
        else:
            services_count = 0
        
        print(f"[Action Agent] System state loaded: {services_count} services")
    
    def load_system_state(self):
        """Load current system state from file"""
        try:
            # FIX: Changed from "../memory/" to "memory/"
            with open("memory/system_state.json", "r") as f:
                data = json.load(f)
                
            # Handle both list and dictionary formats
            if isinstance(data, list):
                # It's a list of services (from Day 1)
                self.system_state = {
                    "services": data,
                    "last_updated": datetime.now().isoformat(),
                    "note": "Converted from list to dictionary format"
                }
            elif isinstance(data, dict):
                # It's already a dictionary
                self.system_state = data
            else:
                # Unknown format, create default
                raise ValueError("Unknown system state format")
                
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"[WARNING] Could not load system state: {e}. Creating default state...")
            self.system_state = {
                "services": [
                    {"name": "web-server-1", "status": "healthy", "last_health_check": None},
                    {"name": "database-primary", "status": "healthy", "last_health_check": None},
                    {"name": "auth-service", "status": "healthy", "last_health_check": None},
                    {"name": "cache-redis", "status": "healthy", "last_health_check": None},
                    {"name": "load-balancer", "status": "healthy", "last_health_check": None}
                ],
                "last_updated": datetime.now().isoformat(),
                "note": "Default system state created"
            }
    
    def load_action_log(self, filepath: str) -> List[Dict]:
        """Load actions to execute from Decision Agent"""
        try:
            with open(filepath, "r") as f:
                actions = json.load(f)
            print(f"[Action Agent] Loaded {len(actions)} actions to execute")
            return actions
        except FileNotFoundError:
            print(f"[ERROR] Action log not found: {filepath}")
            print("[INFO] Run Day 4 (Decision Agent) first!")
            return []
    
    def execute_action(self, action: Dict) -> Dict[str, Any]:
        """
        Execute a single self-healing action with realistic simulation
        """
        action_id = action.get("action_id", "UNKNOWN")
        action_type = action.get("action_type", "")
        service = action.get("service", "unknown")
        incident_id = action.get("incident_id", "")
        
        # Clean up action type for display
        display_type = action_type.replace("_service", "").replace("_", " ").title()
        
        print(f"\n⚡ EXECUTING ACTION: {display_type} on {service}")
        print(f"  Action ID: {action_id}")
        print(f"  Incident: {incident_id}")
        print(f"  Risk Level: {action.get('risk_level', 'medium').upper()}")
        
        # Get action configuration
        config = self.action_configs.get(action_type, {
            "stages": 3,
            "stage_names": ["Preparing", "Executing", "Verifying"],
            "avg_duration": 180,
            "success_rate": 0.90
        })
        
        # Initialize execution record
        execution_record = {
            "action_id": action_id,
            "incident_id": incident_id,
            "action_type": action_type,
            "service": service,
            "start_time": datetime.now().isoformat(),
            "stages": [],
            "status": ActionStatus.EXECUTING.value,
            "progress": 0,
            "estimated_completion": None,
            "actual_duration": None,
            "result": None,
            "logs": []
        }
        
        # Simulate execution with progress updates
        success = random.random() < config["success_rate"]
        duration_variation = random.uniform(0.7, 1.3)  # ±30% variation
        estimated_duration = config["avg_duration"] * duration_variation
        
        for stage_num in range(config["stages"]):
            stage_name = config["stage_names"][stage_num] if stage_num < len(config["stage_names"]) else f"Stage {stage_num + 1}"
            
            # Calculate stage progress
            stage_progress = int(((stage_num + 1) / config["stages"]) * 100)
            
            # Simulate stage execution
            stage_duration = estimated_duration / config["stages"]
            self._simulate_stage_execution(stage_name, stage_duration, stage_progress)
            
            # Record stage completion
            stage_record = {
                "stage": stage_num + 1,
                "name": stage_name,
                "completed_at": datetime.now().isoformat(),
                "status": "completed",
                "duration_seconds": round(stage_duration, 1)
            }
            
            execution_record["stages"].append(stage_record)
            execution_record["progress"] = stage_progress
            execution_record["logs"].append(f"Stage {stage_num + 1}: {stage_name} completed")
        
        # Determine result
        if success:
            execution_record["status"] = ActionStatus.SUCCESS.value
            execution_record["result"] = "Action completed successfully"
            print(f"  ✅ RESULT: SUCCESS - {display_type} completed")
            
            # Update system state
            self._update_service_state(service, "healthy", f"Recovered via {display_type}")
            
        else:
            execution_record["status"] = ActionStatus.FAILED.value
            execution_record["result"] = "Action failed - requires manual intervention"
            print(f"  ❌ RESULT: FAILED - {display_type} failed")
            
            # Attempt rollback
            rollback_success = random.random() < 0.8  # 80% rollback success rate
            if rollback_success:
                execution_record["rollback_attempted"] = True
                execution_record["rollback_status"] = "success"
                execution_record["status"] = ActionStatus.ROLLED_BACK.value
                print(f"  🔄 Rollback attempted and successful")
            else:
                execution_record["rollback_attempted"] = True
                execution_record["rollback_status"] = "failed"
                print(f"  ⚠️  Rollback failed - manual intervention required")
        
        # Complete execution record
        end_time = datetime.now()
        start_time = datetime.fromisoformat(execution_record["start_time"])
        actual_duration = (end_time - start_time).total_seconds()
        
        execution_record["end_time"] = end_time.isoformat()
        execution_record["actual_duration"] = round(actual_duration, 1)
        execution_record["estimated_vs_actual"] = f"Estimated: {estimated_duration:.1f}s, Actual: {actual_duration:.1f}s"
        
        # Add to history
        self.action_history.append(execution_record)
        
        return execution_record
    
    def _simulate_stage_execution(self, stage_name: str, duration: float, progress: int):
        """Simulate a stage execution with progress bar"""
        print(f"  [{progress:3d}%] {stage_name}", end="", flush=True)
        
        # Simulate work with progress dots (speed up for demo)
        steps = min(5, int(duration / 0.5))  # Max 5 dots, adjust based on duration
        if steps < 1:
            steps = 1
            
        step_duration = duration / steps
        
        for i in range(steps):
            time.sleep(step_duration / 20)  # Speed up for demo (20x faster)
            print(".", end="", flush=True)
        
        print(" ✓")
    
    def _update_service_state(self, service_name: str, status: str, reason: str):
        """Update the state of a service after recovery"""
        # FIX: Handle both dict and list formats
        if isinstance(self.system_state, dict):
            services_list = self.system_state.get("services", [])
        elif isinstance(self.system_state, list):
            services_list = self.system_state
        else:
            services_list = []
        
        for service in services_list:
            if service["name"] == service_name:
                service["status"] = status
                service["last_health_check"] = datetime.now().isoformat()
                service["recovery_reason"] = reason
                service["last_recovery"] = datetime.now().isoformat()
                break
        
        if isinstance(self.system_state, dict):
            self.system_state["last_updated"] = datetime.now().isoformat()
        
        print(f"  📊 System state updated: {service_name} → {status.upper()}")
    
    def execute_all_actions(self, actions: List[Dict]) -> List[Dict]:
        """Execute all pending actions"""
        if not actions:
            print("[Action Agent] No actions to execute")
            return []
        
        print(f"\n[Action Agent] Starting execution of {len(actions)} self-healing actions...")
        print("=" * 70)
        
        execution_results = []
        
        for i, action in enumerate(actions):
            print(f"\n[{i+1}/{len(actions)}] ", end="")
            
            result = self.execute_action(action)
            execution_results.append({
                "action": action,
                "execution": result
            })
            
            # Brief pause between actions
            if i < len(actions) - 1:
                time.sleep(0.3)  # Reduced pause for faster demo
        
        print(f"\n✅ All actions executed! {len(execution_results)} results recorded.")
        
        # Save updated system state
        self.save_system_state()
        
        return execution_results
    
    def save_system_state(self):
        """Save updated system state to file"""
        os.makedirs("memory", exist_ok=True)  # FIX: Changed from "../memory"
        
        with open("memory/system_state_updated.json", "w") as f:  # FIX: Changed from "../memory"
            json.dump(self.system_state, f, indent=2)
        
        print(f"[Action Agent] System state saved to memory/system_state_updated.json")
    
    def save_execution_results(self, results: List[Dict], filepath: str):
        """Save execution results to file"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"[Action Agent] Execution results saved to {filepath}")
        
        # Create recovery report
        self._create_recovery_report(results, filepath.replace(".json", "_report.txt"))
        
        # Create dashboard data
        self._create_dashboard_data(results, filepath.replace("execution_results.json", "dashboard_data.json"))
    
    def _create_recovery_report(self, results: List[Dict], filepath: str):
        """Create human-readable recovery report"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("SENTINEL-X PRIME - ACTION AGENT RECOVERY REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Actions Executed: {len(results)}\n\n")
            
            # Statistics
            successful = sum(1 for r in results if r["execution"]["status"] == "success")
            failed = sum(1 for r in results if r["execution"]["status"] == "failed")
            rolled_back = sum(1 for r in results if r["execution"]["status"] == "rolled_back")
            
            f.write("EXECUTION SUMMARY:\n")
            f.write(f"  ✅ Successful: {successful} ({successful/len(results)*100:.1f}%)\n")
            f.write(f"  ❌ Failed: {failed} ({failed/len(results)*100:.1f}%)\n")
            f.write(f"  🔄 Rolled Back: {rolled_back} ({rolled_back/len(results)*100:.1f}%)\n")
            
            total_duration = sum(r['execution']['actual_duration'] for r in results)
            f.write(f"  ⏱️  Total execution time: {total_duration:.1f} seconds\n\n")
            
            f.write("RECOVERY DETAILS:\n")
            for result in results:
                exec_data = result["execution"]
                action_data = result["action"]
                
                icon = "✅" if exec_data["status"] == "success" else "❌" if exec_data["status"] == "failed" else "🔄"
                action_type_display = action_data['action_type'].replace('_', ' ').title()
                
                f.write(f"\n{icon} {action_type_display} on {action_data['service']}\n")
                f.write(f"  Status: {exec_data['status'].upper()}\n")
                f.write(f"  Duration: {exec_data['actual_duration']} seconds\n")
                f.write(f"  Result: {exec_data.get('result', 'N/A')}\n")
                
                if exec_data["status"] == "success":
                    f.write(f"  System Impact: {action_data['service']} recovered to HEALTHY state\n")
        
        print(f"[Action Agent] Recovery report saved to {filepath}")
    
    def _create_dashboard_data(self, results: List[Dict], filepath: str):
        """Create data for Streamlit dashboard (Day 6-7)"""
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_actions": len(results),
                "successful": sum(1 for r in results if r["execution"]["status"] == "success"),
                "failed": sum(1 for r in results if r["execution"]["status"] == "failed"),
                "total_duration": sum(r["execution"]["actual_duration"] for r in results),
                "avg_duration": sum(r["execution"]["actual_duration"] for r in results) / len(results) if results else 0
            },
            "actions_by_type": {},
            "services_recovered": [],
            "timeline": [],
            "system_state": self.system_state
        }
        
        # Count actions by type
        for result in results:
            action_type = result["action"]["action_type"]
            dashboard_data["actions_by_type"][action_type] = dashboard_data["actions_by_type"].get(action_type, 0) + 1
        
        # List recovered services
        for result in results:
            if result["execution"]["status"] == "success":
                service = result["action"]["service"]
                if service not in dashboard_data["services_recovered"]:
                    dashboard_data["services_recovered"].append(service)
        
        # Create timeline
        for result in results:
            dashboard_data["timeline"].append({
                "time": result["execution"]["start_time"],
                "action": result["action"]["action_type"],
                "service": result["action"]["service"],
                "status": result["execution"]["status"],
                "duration": result["execution"]["actual_duration"]
            })
        
        with open(filepath, "w") as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"[Action Agent] Dashboard data saved to {filepath}")
    
    def print_execution_summary(self, results: List[Dict]):
        """Print a clean summary of execution results"""
        print("\n" + "=" * 70)
        print("ACTION EXECUTION SUMMARY")
        print("=" * 70)
        
        successful = sum(1 for r in results if r["execution"]["status"] == "success")
        failed = sum(1 for r in results if r["execution"]["status"] == "failed")
        
        print(f"✅ Successful: {successful}/{len(results)}")
        print(f"❌ Failed: {failed}/{len(results)}")
        
        if results:
            avg_duration = sum(r["execution"]["actual_duration"] for r in results) / len(results)
            print(f"⏱️  Average duration: {avg_duration:.1f} seconds")
            
            # Show services recovered
            recovered_services = []
            for result in results:
                if result["execution"]["status"] == "success":
                    service = result["action"]["service"]
                    if service not in recovered_services:
                        recovered_services.append(service)
            
            if recovered_services:
                print(f"🏥 Services recovered: {', '.join(recovered_services)}")
        
        print("\n📊 System State After Recovery:")
        # FIX: Handle both dict and list formats
        if isinstance(self.system_state, dict):
            services_list = self.system_state.get("services", [])
        elif isinstance(self.system_state, list):
            services_list = self.system_state
        else:
            services_list = []
            
        for service in services_list:
            status = service.get("status", "unknown").lower()
            status_icon = "🟢" if status == "healthy" else "🔴" if status in ["down", "failed"] else "🟡"
            print(f"  {status_icon} {service['name']:20} → {status.upper()}")


def main():
    """Main function to run the Action Agent"""
    print("=" * 70)
    print("SENTINEL-X PRIME - DAY 5: ACTION AGENT")
    print("=" * 70)
    print("Executing self-healing actions to complete autonomous recovery...")
    print("-" * 70)
    
    # Initialize agent
    agent = ActionAgent()
    
    # Load actions from Decision Agent - FIX: Changed from "../memory/"
    actions = agent.load_action_log("memory/action_log.json")
    
    if not actions:
        print("[ERROR] No actions found to execute. Run Day 4 first!")
        return
    
    # Execute all actions
    results = agent.execute_all_actions(actions)
    
    # Save results - FIX: Changed from "../memory/"
    agent.save_execution_results(results, "memory/execution_results.json")
    
    # Print summary
    agent.print_execution_summary(results)
    
    # Show final status
    print("\n" + "=" * 70)
    print("DAY 5 SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for r in results if r["execution"]["status"] == "success")
    
    print(f"⚡ Actions executed: {len(results)}")
    print(f"✅ Successful recoveries: {successful}")
    print(f"🏥 Services affected: {len(set(a['action']['service'] for a in results))}")
    
    print(f"\n💾 Files created:")
    print(f"   memory/execution_results.json - Complete execution logs")
    print(f"   memory/execution_results_report.txt - Recovery report")
    print(f"   memory/system_state_updated.json - Updated system state")
    print(f"   memory/dashboard_data.json - Data for Streamlit dashboard")
    
    print(f"\n📈 AUTONOMOUS CYCLE COMPLETE:")
    print(f"   Day 1: Simulation → {len(actions)} incidents")
    print(f"   Day 2: Perception → Understanding")
    print(f"   Day 3: Reasoning → {len(actions)} AI analyses")
    print(f"   Day 4: Decision → {len(actions)} auto-heal decisions")
    print(f"   Day 5: Action → {successful}/{len(actions)} successful recoveries")
    
    print("\n" + "=" * 70)
    print("🎉 PROJECT MILESTONE ACHIEVED!")
    print("✅ FULL AUTONOMOUS CYBERSECURITY CYCLE COMPLETE")
    print("➡️  Next: Days 6-7 - Dashboard & Polish")
    print("=" * 70)


if __name__ == "__main__":
    main()