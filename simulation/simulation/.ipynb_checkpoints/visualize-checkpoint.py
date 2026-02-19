"""
Sentinel-X Prime - Incident Visualization
Creates charts and summaries from simulation data
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from simulation.config import Config

def visualize_incidents():
    """Create visualizations from incident data"""
    try:
        with open(Config.INCIDENT_LOG_PATH, "r") as f:
            incidents = json.load(f)
        
        if not incidents:
            print("No incidents to visualize.")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(incidents)
        
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sentinel-X Prime: Incident Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Incident types (pie chart)
        type_counts = df["type"].value_counts()
        colors = plt.cm.Set3(range(len(type_counts)))
        axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
                      colors=colors, startangle=90)
        axes[0, 0].set_title("Incident Types Distribution", fontweight='bold')
        
        # Plot 2: Severity levels
        severity_order = ["critical", "high", "medium", "low"]
        severity_counts = df["severity"].value_counts().reindex(severity_order, fill_value=0)
        severity_colors = ["red", "orange", "gold", "green"]
        axes[0, 1].bar(severity_counts.index, severity_counts.values, color=severity_colors)
        axes[0, 1].set_title("Incidents by Severity", fontweight='bold')
        axes[0, 1].set_xlabel("Severity Level")
        axes[0, 1].set_ylabel("Count")
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # Plot 3: Timeline of incidents
        df['hour'] = df['timestamp'].dt.hour
        hourly_counts = df.groupby('hour').size()
        axes[1, 0].plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2)
        axes[1, 0].fill_between(hourly_counts.index, 0, hourly_counts.values, alpha=0.3)
        axes[1, 0].set_title("Incidents by Hour", fontweight='bold')
        axes[1, 0].set_xlabel("Hour of Day")
        axes[1, 0].set_ylabel("Incident Count")
        axes[1, 0].set_xticks(range(0, 24, 3))
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Services affected
        service_counts = df["service"].value_counts()
        axes[1, 1].barh(service_counts.index, service_counts.values, color='steelblue')
        axes[1, 1].set_title("Most Affected Services", fontweight='bold')
        axes[1, 1].set_xlabel("Incident Count")
        axes[1, 1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("memory/incident_analysis.png", dpi=150, bbox_inches='tight')
        print("📊 Visualization saved as 'memory/incident_analysis.png'")
        
        # Print summary statistics
        print(f"\n📈 SIMULATION SUMMARY:")
        print(f"   Total Incidents: {len(df)}")
        print(f"   Simulation Duration: {Config.SIMULATION_CYCLES} cycles")
        print(f"   Time Range: {df['timestamp'].min().strftime('%H:%M:%S')} to {df['timestamp'].max().strftime('%H:%M:%S')}")
        print(f"   Most Common Incident: {type_counts.index[0]} ({type_counts.iloc[0]} times)")
        print(f"   Most Affected Service: {service_counts.index[0]} ({service_counts.iloc[0]} incidents)")
        
        # Save summary to file
        summary = {
            "total_incidents": len(df),
            "simulation_cycles": Config.SIMULATION_CYCLES,
            "incident_types": type_counts.to_dict(),
            "severity_distribution": severity_counts.to_dict(),
            "most_affected_service": service_counts.index[0],
            "most_common_incident": type_counts.index[0]
        }
        
        with open("memory/simulation_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
            
    except FileNotFoundError:
        print("❌ No incident data found. Run the simulation first.")
    except Exception as e:
        print(f"❌ Error visualizing data: {e}")

if __name__ == "__main__":
    visualize_incidents()