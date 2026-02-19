
import os
import json

# Define paths
MEMORY_DIR = os.path.join(os.getcwd(), 'memory', 'memory')
FILES_TO_RESET = [
    'analyzed_incidents.json',
    'incidents.json', 
    'decisions_enhanced.json',
    'root_cause_analysis.json',
    'action_log.json',
    'autonomy_governance.json'
]

def reset_files():
    print(f"Cleaning up backend memory in: {MEMORY_DIR}")
    
    if not os.path.exists(MEMORY_DIR):
        print(f"Directory not found: {MEMORY_DIR}")
        return

    for filename in FILES_TO_RESET:
        file_path = os.path.join(MEMORY_DIR, filename)
        
        # Default empty state
        empty_data = []
        
        # Specific structures for certain files
        if filename == 'decisions_enhanced.json':
            empty_data = {"decisions": []}
        elif filename == 'root_cause_analysis.json':
            empty_data = {"root_causes": []}
        elif filename == 'autonomy_governance.json':
            # Create a "Normal" state entry so the panel isn't empty/broken
            empty_data = {
                "governance_decisions": [{
                    "governance_id": "GOV-INIT",
                    "recommended_autonomy_level": "FULL_AUTONOMY",
                    "timestamp": "Just Now",
                    "ai_confidence": 1.0,
                    "service": "System-Wide",
                    "policy_applied": {
                        "Standard_Operating_Procedure": ["Monitor Only"]
                    }
                }]
            }
            
        with open(file_path, 'w') as f:
            json.dump(empty_data, f, indent=2)
            print(f"Reset: {filename}")

    print("\nSystem State Reset to NORMAL.")
    print("Refresh your dashboard to see the 'Secure' state.")

if __name__ == "__main__":
    reset_files()
