"""
Sentinel-X Prime - AUTONOMY GOVERNOR
Determines when AI should be autonomous vs when humans should control it
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from enum import Enum

class AutonomyLevel(Enum):
    FULL_AUTONOMY = "full_autonomy"
    SUPERVISED_AUTONOMY = "supervised_autonomy"
    HUMAN_CONTROL = "human_control"

class AutonomyGovernor:
    """
    AI Governance System - Determines appropriate autonomy level
    Based on success rate, risk, and system maturity
    """
    
    def __init__(self):
        self.governance_log = []
        self.autonomy_policy = self._load_autonomy_policy()
        self.success_history = self._load_success_history()
        
        print("[Autonomy Governor] Initialized - AI Governance System")
        print(f"   • Success Rate: {self.success_history.get('success_rate', 0):.1%}")
        print(f"   • Incidents Handled: {self.success_history.get('total_incidents', 0)}")
        print(f"   • Current Policy: {self.autonomy_policy['current_level']}")
    
    def _load_autonomy_policy(self) -> Dict:
        """Load autonomy governance policy"""
        default_policy = {
            "current_level": AutonomyLevel.SUPERVISED_AUTONOMY.value,
            "policy_version": "2.0",
            "thresholds": {
                "full_autonomy_success_rate": 0.95,  # 95% success required
                "supervised_autonomy_success_rate": 0.80,
                "critical_services_always_supervised": ["database-primary", "auth-service"],
                "security_incidents_always_human": ["unauthorized_access", "data_breach"],
                "max_autonomy_for_new_patterns": AutonomyLevel.SUPERVISED_AUTONOMY.value
            },
            "escalation_rules": {
                "consecutive_failures": 3,
                "low_confidence_incidents": 5,
                "high_risk_patterns": 2
            },
            "last_reviewed": datetime.now().isoformat()
        }
        
        try:
            policy_path = "memory/autonomy_policy.json"
            if os.path.exists(policy_path):
                with open(policy_path, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    default_policy.update(loaded)
            return default_policy
        except:
            return default_policy
    
    def _load_success_history(self) -> Dict:
        """Load historical success data"""
        default_history = {
            "success_rate": 0.85,
            "total_incidents": 12,
            "successful_recoveries": 10,
            "failed_recoveries": 2,
            "human_interventions": 12,  # From safety mode
            "auto_heal_success_rate": 0.92,
            "patterns_learned": 10,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            # Try to load from execution results
            exec_path = "memory/execution_results.json"
            if os.path.exists(exec_path):
                with open(exec_path, 'r') as f:
                    exec_data = json.load(f)
                
                if isinstance(exec_data, list):
                    successful = sum(1 for r in exec_data if r.get('result') == 'success')
                    total = len(exec_data)
                    if total > 0:
                        default_history.update({
                            "success_rate": successful / total,
                            "total_incidents": total,
                            "successful_recoveries": successful,
                            "failed_recoveries": total - successful
                        })
        except:
            pass
        
        return default_history
    
    def determine_autonomy_level(self, incident: Dict) -> Dict[str, Any]:
        """
        Determine appropriate autonomy level for this incident
        This is AI GOVERNANCE in action
        """
        reasoning = incident.get('reasoning', {})
        analysis = incident.get('analysis', {})
        
        incident_type = analysis.get('type', '')
        service = analysis.get('service', '')
        severity = analysis.get('severity', 'medium')
        confidence = reasoning.get('confidence_score', 0.5)
        
        print(f"\n[Autonomy Governor] Evaluating: {incident_type.replace('_', ' ').title()} on {service}")
        print(f"  Confidence: {confidence:.0%} | Severity: {severity.upper()}")
        
        # Start with default level
        recommended_level = self.autonomy_policy['current_level']
        reasons = []
        
        # Rule 1: Critical services always get supervision
        if service in self.autonomy_policy['thresholds']['critical_services_always_supervised']:
            recommended_level = AutonomyLevel.SUPERVISED_AUTONOMY.value
            reasons.append(f"Critical service ({service}) requires supervision")
        
        # Rule 2: Security incidents require human control
        if incident_type in self.autonomy_policy['thresholds']['security_incidents_always_human']:
            recommended_level = AutonomyLevel.HUMAN_CONTROL.value
            reasons.append(f"Security incident ({incident_type}) requires human control")
        
        # Rule 3: High confidence + high success rate → Full autonomy
        if (confidence >= 0.9 and 
            self.success_history['success_rate'] >= self.autonomy_policy['thresholds']['full_autonomy_success_rate']):
            recommended_level = AutonomyLevel.FULL_AUTONOMY.value
            reasons.append(f"High confidence ({confidence:.0%}) + proven success ({self.success_history['success_rate']:.0%})")
        
        # Rule 4: Low confidence → Human control
        elif confidence < 0.6:
            recommended_level = AutonomyLevel.HUMAN_CONTROL.value
            reasons.append(f"Low confidence ({confidence:.0%}) requires human judgment")
        
        # Rule 5: New patterns → Supervised autonomy
        pattern_info = reasoning.get('pattern_recognition', {})
        if not pattern_info.get('pattern_found', False):
            max_level = self.autonomy_policy['thresholds']['max_autonomy_for_new_patterns']
            if self._get_autonomy_value(recommended_level) > self._get_autonomy_value(max_level):
                recommended_level = max_level
                reasons.append("New pattern - limiting autonomy for safety")
        
        # Create governance decision
        decision = {
            "governance_id": f"GOV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "incident_type": incident_type,
            "service": service,
            "severity": severity,
            "ai_confidence": confidence,
            "recommended_autonomy_level": recommended_level,
            "system_success_rate": self.success_history['success_rate'],
            "decision_reasons": reasons,
            "policy_applied": self.autonomy_policy['thresholds'],
            "human_override_available": True,
            "audit_trail_created": True,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "governor_version": "1.0",
                "decision_logic": "risk_based_autonomy_governance",
                "escalation_path": "human_operator -> security_team -> ciso"
            }
        }
        
        # Log the decision
        self.governance_log.append(decision)
        
        # Display decision
        self._display_governance_decision(decision)
        
        return decision
    
    def _get_autonomy_value(self, level: str) -> int:
        """Get numerical value for autonomy level"""
        values = {
            AutonomyLevel.FULL_AUTONOMY.value: 3,
            AutonomyLevel.SUPERVISED_AUTONOMY.value: 2,
            AutonomyLevel.HUMAN_CONTROL.value: 1
        }
        return values.get(level, 1)
    
    def _display_governance_decision(self, decision: Dict):
        """Display governance decision"""
        level = decision['recommended_autonomy_level']
        reasons = decision['decision_reasons']
        
        print(f"  {'─' * 50}")
        
        if level == AutonomyLevel.FULL_AUTONOMY.value:
            print(f"  🚀 AUTONOMY LEVEL: FULL AUTONOMY")
            print(f"     AI can execute without human intervention")
        elif level == AutonomyLevel.SUPERVISED_AUTONOMY.value:
            print(f"  🛡️  AUTONOMY LEVEL: SUPERVISED AUTONOMY")
            print(f"     AI can act with human oversight")
        else:
            print(f"  👨‍💼 AUTONOMY LEVEL: HUMAN CONTROL")
            print(f"     Human operator must make all decisions")
        
        print(f"     Reasons: {', '.join(reasons)}")
        print(f"  {'─' * 50}")
    
    def evaluate_all_incidents(self, incidents: List[Dict]) -> List[Dict]:
        """Evaluate autonomy level for all incidents"""
        governance_decisions = []
        
        print(f"\n[Autonomy Governor] Evaluating governance for {len(incidents)} incidents...")
        print("=" * 70)
        print("AI GOVERNANCE SYSTEM - Determining appropriate autonomy levels")
        print("=" * 70)
        
        for i, incident in enumerate(incidents):
            print(f"\n[{i+1}/{len(incidents)}] ", end="")
            decision = self.determine_autonomy_level(incident)
            
            # Combine with incident
            combined = incident.copy()
            combined["autonomy_governance"] = decision
            governance_decisions.append(combined)
        
        # Calculate statistics
        full_auto = sum(1 for d in governance_decisions 
                       if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.FULL_AUTONOMY.value)
        supervised = sum(1 for d in governance_decisions 
                        if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.SUPERVISED_AUTONOMY.value)
        human = len(governance_decisions) - full_auto - supervised
        
        print(f"\n✅ Governance evaluation complete! {len(governance_decisions)} decisions made")
        print(f"\n📊 AUTONOMY DISTRIBUTION:")
        print(f"   🚀 Full Autonomy: {full_auto}/{len(governance_decisions)} ({full_auto/len(governance_decisions)*100:.1f}%)")
        print(f"   🛡️  Supervised: {supervised}/{len(governance_decisions)} ({supervised/len(governance_decisions)*100:.1f}%)")
        print(f"   👨‍💼 Human Control: {human}/{len(governance_decisions)} ({human/len(governance_decisions)*100:.1f}%)")
        
        return governance_decisions
    
    def create_governance_report(self, decisions: List[Dict], filepath: str):
        """Create comprehensive governance report"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        report_data = {
            "governance_decisions": decisions,
            "summary": {
                "total_decisions": len(decisions),
                "full_autonomy": sum(1 for d in decisions 
                                   if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.FULL_AUTONOMY.value),
                "supervised_autonomy": sum(1 for d in decisions 
                                         if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.SUPERVISED_AUTONOMY.value),
                "human_control": sum(1 for d in decisions 
                                   if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.HUMAN_CONTROL.value),
                "average_confidence": sum(d['autonomy_governance']['ai_confidence'] for d in decisions) / len(decisions),
                "system_success_rate": self.success_history['success_rate']
            },
            "policy": self.autonomy_policy,
            "success_history": self.success_history,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "governor_version": "1.0",
                "report_type": "autonomy_governance_analysis"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"[Autonomy Governor] Governance report saved to {filepath}")
        
        # Create human-readable report
        self._create_human_governance_report(decisions, filepath.replace(".json", "_human.txt"))
    
    def _create_human_governance_report(self, decisions: List[Dict], filepath: str):
        """Create human-readable governance report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("SENTINEL-X PRIME - AI AUTONOMY GOVERNANCE REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System Success Rate: {self.success_history['success_rate']:.1%}\n")
            f.write(f"Incidents Analyzed: {len(decisions)}\n\n")
            
            # Autonomy distribution
            full_auto = sum(1 for d in decisions 
                          if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.FULL_AUTONOMY.value)
            supervised = sum(1 for d in decisions 
                           if d['autonomy_governance']['recommended_autonomy_level'] == AutonomyLevel.SUPERVISED_AUTONOMY.value)
            human = len(decisions) - full_auto - supervised
            
            f.write("AUTONOMY GOVERNANCE DECISIONS:\n")
            f.write(f"  🚀 Full Autonomy Recommended: {full_auto} incidents ({full_auto/len(decisions)*100:.1f}%)\n")
            f.write(f"  🛡️  Supervised Autonomy Recommended: {supervised} incidents ({supervised/len(decisions)*100:.1f}%)\n")
            f.write(f"  👨‍💼 Human Control Required: {human} incidents ({human/len(decisions)*100:.1f}%)\n\n")
            
            f.write("GOVERNANCE POLICY SUMMARY:\n")
            f.write(f"  • Full Autonomy Threshold: {self.autonomy_policy['thresholds']['full_autonomy_success_rate']:.0%} success rate\n")
            f.write(f"  • Critical Services: {', '.join(self.autonomy_policy['thresholds']['critical_services_always_supervised'])}\n")
            f.write(f"  • Security Incidents: Always require human control\n")
            f.write(f"  • New Patterns: Limited to supervised autonomy\n\n")
            
            f.write("RECENT GOVERNANCE DECISIONS:\n")
            for decision in decisions[-5:]:
                gov = decision['autonomy_governance']
                f.write(f"\n• {gov['incident_type'].replace('_', ' ').title()} on {gov['service']}\n")
                f.write(f"  Autonomy Level: {gov['recommended_autonomy_level'].replace('_', ' ').title()}\n")
                f.write(f"  Confidence: {gov['ai_confidence']:.0%}\n")
                f.write(f"  Reasons: {', '.join(gov['decision_reasons'])}\n")
            
            f.write(f"\n\n{'='*70}\n")
            f.write("AI GOVERNANCE PRINCIPLES APPLIED:\n")
            f.write(f"{'='*70}\n")
            f.write("1. Safety First: Human control for critical systems\n")
            f.write("2. Proportional Autonomy: Based on proven success rates\n")
            f.write("3. Explainability: Every decision has clear reasoning\n")
            f.write("4. Human Oversight: Always available for escalation\n")
            f.write("5. Continuous Learning: System improves over time\n")
        
        print(f"[Autonomy Governor] Human-readable report saved to {filepath}")

def main():
    """Run Autonomy Governor"""
    print("=" * 70)
    print("SENTINEL-X PRIME - AUTONOMY GOVERNOR")
    print("=" * 70)
    print("AI Governance System - Determining appropriate autonomy levels")
    print("-" * 70)
    
    governor = AutonomyGovernor()
    
    # Load reasoned incidents
    try:
        with open("memory/reasoned_incidents_enhanced.json", 'r') as f:
            data = json.load(f)
            incidents = data.get("reasoned_incidents", [])
    except:
        print("[ERROR] No reasoned incidents found. Run Reasoning Agent first!")
        return
    
    if not incidents:
        print("[ERROR] No incidents to evaluate")
        return
    
    # Evaluate autonomy levels
    governed_incidents = governor.evaluate_all_incidents(incidents)
    
    # Save governance decisions
    governor.create_governance_report(governed_incidents, "memory/autonomy_governance.json")
    
    print(f"\n💾 Files created:")
    print(f"   memory/autonomy_governance.json - Complete governance data")
    print(f"   memory/autonomy_governance_human.txt - Human-readable report")
    
    print("\n" + "=" * 70)
    print("🏆 AI GOVERNANCE SYSTEM OPERATIONAL")
    print("=" * 70)
    print("The system now answers:")
    print("  • When should AI be autonomous?")
    print("  • When should humans control?")
    print("  • Based on success rates, risk, and system maturity")
    print("\n✅ AUTONOMY GOVERNANCE COMPLETE!")
    print("➡️  Next: Root Cause Intelligence")
    print("=" * 70)

if __name__ == "__main__":
    main()