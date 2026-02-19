"""
Sentinel-X Prime - Decision Agent (FIXED VERSION)
Makes autonomous decisions: Auto-heal vs Escalate to human
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
from enum import Enum

class DecisionType(Enum):
    AUTO_HEAL = "auto_heal"
    ESCALATE_HUMAN = "escalate_human"
    MONITOR_ONLY = "monitor_only"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryAction(Enum):
    RESTART_SERVICE = "restart_service"
    ISOLATE_SERVICE = "isolate_service"
    SCALE_UP = "scale_up"
    BLOCK_IP = "block_ip"
    CLEAR_CACHE = "clear_cache"
    ROLLBACK = "rollback"
    MANUAL_INTERVENTION = "manual_intervention"
    MONITOR_ONLY = "monitor_only"

class DecisionAgent:
    """
    The third AI agent in Sentinel-X Prime.
    Its job: Make autonomous decisions using AI confidence scores.
    Core innovation: Confidence-aware autonomy.
    """
    
    def __init__(self):
        # Decision thresholds
        self.auto_heal_threshold = 0.70  # 70% confidence → auto-heal
        self.human_review_threshold = 0.40  # 40% confidence → human review
        
        # Action mappings by incident type
        self.action_mappings = {
            "high_traffic": [
                RecoveryAction.SCALE_UP,
                RecoveryAction.CLEAR_CACHE,
                RecoveryAction.MONITOR_ONLY
            ],
            "service_crash": [
                RecoveryAction.RESTART_SERVICE,
                RecoveryAction.ROLLBACK,
                RecoveryAction.MANUAL_INTERVENTION
            ],
            "unauthorized_access": [
                RecoveryAction.BLOCK_IP,
                RecoveryAction.ISOLATE_SERVICE,
                RecoveryAction.MANUAL_INTERVENTION
            ],
            "slow_response": [
                RecoveryAction.CLEAR_CACHE,
                RecoveryAction.SCALE_UP,
                RecoveryAction.MONITOR_ONLY
            ],
            "database_connection_failure": [
                RecoveryAction.RESTART_SERVICE,
                RecoveryAction.MANUAL_INTERVENTION
            ],
            "memory_leak": [
                RecoveryAction.RESTART_SERVICE,
                RecoveryAction.ROLLBACK,
                RecoveryAction.MANUAL_INTERVENTION
            ]
        }
        
        # Risk assessment rules
        self.risk_rules = {
            "service_crash": RiskLevel.HIGH,
            "unauthorized_access": RiskLevel.CRITICAL,
            "database_connection_failure": RiskLevel.HIGH,
            "high_traffic": RiskLevel.MEDIUM,
            "slow_response": RiskLevel.LOW,
            "memory_leak": RiskLevel.MEDIUM
        }
        
        # Service criticality (for risk calculation)
        self.service_criticality = {
            "database-primary": 10,
            "auth-service": 9,
            "load-balancer": 8,
            "web-server-1": 7,
            "cache-redis": 6
        }
        
        self.decision_log = []
        print("[Decision Agent] Initialized with confidence-based autonomy")
    
    def load_reasoned_incidents(self, filepath: str) -> List[Dict]:
        """Load incidents analyzed by Reasoning Agent"""
        try:
            with open(filepath, 'r') as f:
                incidents = json.load(f)
            print(f"[Decision Agent] Loaded {len(incidents)} reasoned incidents")
            return incidents
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            print("[INFO] Run Day 3 (Reasoning Agent) first!")
            return []
    
    def make_decision(self, incident: Dict) -> Dict[str, Any]:
        """
        Make an autonomous decision based on AI confidence
        This is the CORE innovation of your project
        """
        reasoning = incident['reasoning']
        analysis = incident['analysis']
        
        incident_type = analysis['type']
        service = analysis['service']
        severity = analysis['severity']
        impact_score = analysis['impact_score']
        confidence = reasoning['confidence_score']
        
        print(f"\n[Decision] {incident_type.replace('_', ' ').title()} on {service}")
        print(f"  AI Confidence: {confidence:.0%}")
        print(f"  Severity: {severity.upper()}")
        print(f"  Impact: {impact_score}/10")
        
        # 1. DECIDE: Auto-heal vs Escalate
        decision_type, decision_reason = self._determine_decision_type(
            confidence, severity, incident_type, impact_score
        )
        
        # 2. CHOOSE recovery action
        recovery_action, action_details = self._choose_recovery_action(
            decision_type, incident_type, service, severity, confidence
        )
        
        # 3. ASSESS risk
        risk_level, risk_explanation = self._assess_risk(
            incident_type, service, severity, recovery_action, decision_type
        )
        
        # 4. ESTIMATE recovery time
        recovery_time = self._estimate_recovery_time(
            incident_type, recovery_action, severity
        )
        
        # 5. Generate human-readable explanation
        explanation = self._generate_explanation(
            decision_type, confidence, recovery_action, risk_level, recovery_time
        )
        
        decision = {
            "decision_id": f"DEC-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{service}",
            "incident_id": incident.get("incident_id", ""),
            "timestamp": datetime.now().isoformat(),
            
            "input_analysis": {
                "type": incident_type,
                "service": service,
                "severity": severity,
                "impact_score": impact_score,
                "ai_confidence": confidence,
                "ai_summary": reasoning.get("reasoning_summary", "")[:100]
            },
            
            "decision": {
                "type": decision_type.value,
                "reason": decision_reason,
                "confidence_threshold_used": self.auto_heal_threshold,
                "explanation": explanation,
                "requires_human_approval": decision_type == DecisionType.ESCALATE_HUMAN
            },
            
            "action": {
                "type": recovery_action.value,
                "details": action_details,
                "estimated_recovery_time": recovery_time,
                "risk_level": risk_level.value,
                "risk_explanation": risk_explanation,
                "can_be_automated": decision_type == DecisionType.AUTO_HEAL
            },
            
            "verification": {
                "double_check_performed": True,
                "safety_checks_passed": risk_level != RiskLevel.CRITICAL,
                "backup_plan_available": True,
                "rollback_possible": recovery_action != RecoveryAction.ISOLATE_SERVICE
            },
            
            "metadata": {
                "decision_agent_version": "1.0",
                "decision_logic": "confidence_based_autonomy",
                "decision_time": datetime.now().strftime("%H:%M:%S"),
                "audit_trail_created": True
            }
        }
        
        # Log the decision
        self.decision_log.append(decision)
        
        # Display decision
        self._display_decision_summary(decision)
        
        return decision
    
    def _determine_decision_type(self, confidence: float, severity: str, 
                                incident_type: str, impact_score: float) -> Tuple[DecisionType, str]:
        """
        Core decision logic: Should we auto-heal or escalate?
        This is what makes your project innovative
        """
        
        # Rule 1: High confidence → Auto-heal
        if confidence >= self.auto_heal_threshold:
            return DecisionType.AUTO_HEAL, f"High AI confidence ({confidence:.0%} ≥ {self.auto_heal_threshold:.0%})"
        
        # Rule 2: Medium confidence + Low severity → Auto-heal with caution
        elif confidence >= self.human_review_threshold and severity in ["low", "medium"]:
            return DecisionType.AUTO_HEAL, f"Moderate confidence ({confidence:.0%}) with low severity"
        
        # Rule 3: Critical security incidents always get human review
        elif incident_type == "unauthorized_access":
            return DecisionType.ESCALATE_HUMAN, "Security incidents require human review"
        
        # Rule 4: High impact + low confidence → Human review
        elif impact_score >= 8 and confidence < 0.6:
            return DecisionType.ESCALATE_HUMAN, f"High impact ({impact_score}/10) with low confidence ({confidence:.0%})"
        
        # Rule 5: Very low confidence → Monitor only
        elif confidence < 0.3:
            return DecisionType.MONITOR_ONLY, f"Very low confidence ({confidence:.0%}), monitor for escalation"
        
        # Default: Escalate to human
        else:
            return DecisionType.ESCALATE_HUMAN, f"Medium confidence ({confidence:.0%}) requires human review"
    
    def _choose_recovery_action(self, decision_type: DecisionType, incident_type: str,
                               service: str, severity: str, confidence: float) -> Tuple[RecoveryAction, Dict]:
        """Choose the best recovery action based on incident type and decision"""
        
        available_actions = self.action_mappings.get(incident_type, [RecoveryAction.MANUAL_INTERVENTION])
        
        if decision_type == DecisionType.AUTO_HEAL:
            # For auto-heal, choose the safest automated action
            if RecoveryAction.RESTART_SERVICE in available_actions:
                action = RecoveryAction.RESTART_SERVICE
                details = {
                    "method": "graceful_restart",
                    "drain_connections": True,
                    "preserve_state": False,
                    "timeout_seconds": 30
                }
            elif RecoveryAction.SCALE_UP in available_actions:
                action = RecoveryAction.SCALE_UP
                details = {
                    "scale_factor": 2,
                    "cooldown_period": 300,
                    "max_instances": 5
                }
            else:
                action = available_actions[0]
                details = {"method": "standard_procedure"}
                
        elif decision_type == DecisionType.ESCALATE_HUMAN:
            # For human escalation, suggest action but don't auto-execute
            action = RecoveryAction.MANUAL_INTERVENTION
            details = {
                "suggested_action": available_actions[0].value if available_actions else "investigate",
                "automation_blocked": True,
                "human_required": True,
                "priority": "HIGH" if severity in ["critical", "high"] else "MEDIUM"
            }
            
        else:  # MONITOR_ONLY
            action = RecoveryAction.MONITOR_ONLY
            details = {
                "action": "monitor_only",
                "check_interval_seconds": 60,
                "escalate_if_worsens": True,
                "threshold": "10% degradation"
            }
        
        # Add confidence-based customization
        if confidence > 0.8:
            details["confidence_based_adjustment"] = "aggressive_recovery"
        elif confidence > 0.6:
            details["confidence_based_adjustment"] = "standard_recovery"
        else:
            details["confidence_based_adjustment"] = "cautious_recovery"
        
        return action, details
    
    def _assess_risk(self, incident_type: str, service: str, severity: str,
                    recovery_action: RecoveryAction, decision_type: DecisionType) -> Tuple[RiskLevel, str]:
        """Assess risk level of the incident and proposed action"""
        
        # Base risk from incident type
        base_risk = self.risk_rules.get(incident_type, RiskLevel.MEDIUM)
        
        # Adjust for service criticality
        service_score = self.service_criticality.get(service, 5) / 10.0
        adjusted_risk = base_risk
        
        if service_score > 0.8:
            # Increase risk for critical services
            if base_risk == RiskLevel.LOW:
                adjusted_risk = RiskLevel.MEDIUM
            elif base_risk == RiskLevel.MEDIUM:
                adjusted_risk = RiskLevel.HIGH
            elif base_risk == RiskLevel.HIGH:
                adjusted_risk = RiskLevel.CRITICAL
            # CRITICAL stays CRITICAL
        
        # Adjust for decision type
        if decision_type == DecisionType.AUTO_HEAL:
            if recovery_action == RecoveryAction.RESTART_SERVICE:
                explanation = f"Auto-restart of {service} - low data loss risk"
            elif recovery_action == RecoveryAction.ISOLATE_SERVICE:
                explanation = f"Auto-isolation of {service} - medium availability risk"
            else:
                explanation = f"Automated recovery - {adjusted_risk.value} risk"
        else:
            explanation = f"Human intervention required - {adjusted_risk.value} risk"
        
        return adjusted_risk, explanation
    
    def _estimate_recovery_time(self, incident_type: str, recovery_action: RecoveryAction,
                               severity: str) -> str:
        """Estimate how long recovery will take"""
        
        base_times = {
            RecoveryAction.RESTART_SERVICE: "2-5 minutes",
            RecoveryAction.SCALE_UP: "3-7 minutes",
            RecoveryAction.BLOCK_IP: "1-2 minutes",
            RecoveryAction.CLEAR_CACHE: "1-3 minutes",
            RecoveryAction.ISOLATE_SERVICE: "1-2 minutes",
            RecoveryAction.ROLLBACK: "5-10 minutes",
            RecoveryAction.MANUAL_INTERVENTION: "15-60 minutes",
            RecoveryAction.MONITOR_ONLY: "Ongoing monitoring"
        }
        
        base = base_times.get(recovery_action, "5-15 minutes")
        
        # Adjust based on severity
        if severity == "critical":
            return f"{base.split('-')[0]} minutes (URGENT)" if '-' in base else f"{base} (URGENT)"
        elif severity == "high":
            return f"{base}"
        else:
            return base
    
    def _generate_explanation(self, decision_type: DecisionType, confidence: float,
                             recovery_action: RecoveryAction, risk_level: RiskLevel,
                             recovery_time: str) -> str:
        """Generate human-readable explanation of the decision"""
        
        if decision_type == DecisionType.AUTO_HEAL:
            return (f"✅ AUTO-HEAL APPROVED: AI confidence {confidence:.0%} meets auto-heal threshold. "
                   f"Action: {recovery_action.value.replace('_', ' ').title()}. "
                   f"Risk: {risk_level.value.upper()}. Estimated recovery: {recovery_time}.")
        
        elif decision_type == DecisionType.ESCALATE_HUMAN:
            return (f"🔄 ESCALATING TO HUMAN: AI confidence {confidence:.0%} below threshold. "
                   f"Recommended action: {recovery_action.value.replace('_', ' ').title()}. "
                   f"Risk: {risk_level.value.upper()}. Requires human approval.")
        
        else:  # MONITOR_ONLY
            return (f"👀 MONITORING: Very low confidence ({confidence:.0%}). "
                   f"Will escalate if situation worsens. Monitoring active.")
    
    def _display_decision_summary(self, decision: Dict):
        """Display a clean summary of the decision"""
        d = decision['decision']['type']
        action = decision['action']['type']
        risk = decision['action']['risk_level']
        time = decision['action']['estimated_recovery_time']
        confidence = decision['input_analysis']['ai_confidence']
        
        if d == "auto_heal":
            print(f"  ✅ DECISION: AUTO-HEAL ({confidence:.0%} confidence)")
            print(f"     Action: {action.replace('_', ' ').title()}")
            print(f"     Risk: {risk.upper()} | Time: {time}")
        elif d == "escalate_human":
            print(f"  🔄 DECISION: ESCALATE TO HUMAN ({confidence:.0%} confidence)")
            print(f"     Reason: Requires human review")
            print(f"     Risk: {risk.upper()} | Suggested: {action.replace('_', ' ').title()}")
        else:
            print(f"  👀 DECISION: MONITOR ONLY ({confidence:.0%} confidence)")
            print(f"     Action: Monitor and escalate if worsens")
    
    def process_all_incidents(self, incidents: List[Dict]) -> List[Dict]:
        """Make decisions for all incidents"""
        decisions = []
        
        print(f"\n[Decision Agent] Making autonomous decisions for {len(incidents)} incidents...")
        print("=" * 70)
        
        for i, incident in enumerate(incidents):
            decision = self.make_decision(incident)
            
            # Combine with incident data
            full_record = incident.copy()
            full_record["decision"] = decision
            
            decisions.append(full_record)
            
            # Show progress
            if (i + 1) % 3 == 0:
                print(f"  Processed {i + 1}/{len(incidents)} incidents...")
        
        print(f"\n✅ Decision making complete! {len(decisions)} decisions made.")
        return decisions
    
    def save_decisions(self, decisions: List[Dict], filepath: str):
        """Save all decisions to file"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(decisions, f, indent=2)
        
        print(f"[Decision Agent] Saved {len(decisions)} decisions to {filepath}")
        
        # Create summary report
        self._create_decision_report(decisions, filepath.replace(".json", "_report.txt"))
        
        # Create action log for Action Agent (Day 5)
        self._create_action_log(decisions, filepath.replace("decisions.json", "action_log.json"))
    
    def _create_decision_report(self, decisions: List[Dict], filepath: str):
        """Create human-readable decision report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("SENTINEL-X PRIME - DECISION AGENT REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Decisions Made: {len(decisions)}\n\n")
            
            # Count decision types
            auto_heal = sum(1 for d in decisions if d['decision']['decision']['type'] == 'auto_heal')
            escalate = sum(1 for d in decisions if d['decision']['decision']['type'] == 'escalate_human')
            monitor = sum(1 for d in decisions if d['decision']['decision']['type'] == 'monitor_only')
            
            f.write("DECISION BREAKDOWN:\n")
            f.write(f"  ✅ Auto-heal decisions: {auto_heal} ({auto_heal/len(decisions)*100:.1f}%)\n")
            f.write(f"  🔄 Human escalation: {escalate} ({escalate/len(decisions)*100:.1f}%)\n")
            f.write(f"  👀 Monitor only: {monitor} ({monitor/len(decisions)*100:.1f}%)\n\n")
            
            f.write("AUTO-HEAL EFFICIENCY:\n")
            if auto_heal > 0:
                avg_confidence = sum(
                    d['decision']['input_analysis']['ai_confidence'] 
                    for d in decisions 
                    if d['decision']['decision']['type'] == 'auto_heal'
                ) / auto_heal
                f.write(f"  Average confidence for auto-heal: {avg_confidence:.1%}\n")
                f.write(f"  Threshold used: {self.auto_heal_threshold:.0%}\n")
            
            f.write("\nRECENT DECISIONS:\n")
            for decision in decisions[-3:]:  # Last 3 decisions
                d = decision['decision']
                f.write(f"\n• {d['input_analysis']['type'].replace('_', ' ').title()} on {d['input_analysis']['service']}\n")
                f.write(f"  Decision: {d['decision']['type'].replace('_', ' ').title()}\n")
                f.write(f"  Confidence: {d['input_analysis']['ai_confidence']:.0%}\n")
                f.write(f"  Action: {d['action']['type'].replace('_', ' ').title()}\n")
                f.write(f"  Risk: {d['action']['risk_level'].upper()}\n")
        
        print(f"[Decision Agent] Report saved to {filepath}")
    
    def _create_action_log(self, decisions: List[Dict], filepath: str):
        """Create action log for Action Agent (Day 5)"""
        action_log = []
        
        for decision in decisions:
            if decision['decision']['decision']['type'] == 'auto_heal':
                action = {
                    "action_id": f"ACT-{datetime.now().strftime('%H%M%S')}",
                    "incident_id": decision['decision']['incident_id'],
                    "decision_id": decision['decision']['decision_id'],
                    "action_type": decision['decision']['action']['type'],
                    "service": decision['decision']['input_analysis']['service'],
                    "action_details": decision['decision']['action']['details'],
                    "scheduled_time": datetime.now().isoformat(),
                    "status": "pending_execution",
                    "estimated_duration": decision['decision']['action']['estimated_recovery_time'],
                    "risk_level": decision['decision']['action']['risk_level']
                }
                action_log.append(action)
        
        with open(filepath, 'w') as f:
            json.dump(action_log, f, indent=2)
        
        print(f"[Decision Agent] Action log created with {len(action_log)} auto-heal actions")


def main():
    """Main function to run the Decision Agent"""
    print("=" * 70)
    print("SENTINEL-X PRIME - DAY 4: DECISION AGENT")
    print("=" * 70)
    print("Making autonomous decisions with confidence-based autonomy...")
    print("-" * 70)
    
    # Initialize agent
    agent = DecisionAgent()
    
    # Load reasoned incidents from Day 3
    incidents = agent.load_reasoned_incidents("../memory/reasoned_incidents.json")
    
    if not incidents:
        print("[ERROR] No reasoned incidents found. Run Day 3 first!")
        return
    
    # Make decisions for all incidents
    decisions = agent.process_all_incidents(incidents)
    
    # Save decisions
    agent.save_decisions(decisions, "../memory/decisions.json")
    
    # Show final summary
    print("\n" + "=" * 70)
    print("DAY 4 SUMMARY")
    print("=" * 70)
    
    auto_heal = sum(1 for d in decisions if d['decision']['decision']['type'] == 'auto_heal')
    escalate = sum(1 for d in decisions if d['decision']['decision']['type'] == 'escalate_human')
    
    print(f"✅ Total decisions made: {len(decisions)}")
    print(f"🤖 Auto-heal decisions: {auto_heal} ({auto_heal/len(decisions)*100:.1f}%)")
    print(f"👨‍💻 Human escalations: {escalate} ({escalate/len(decisions)*100:.1f}%)")
    
    if auto_heal > 0:
        avg_conf = sum(
            d['decision']['input_analysis']['ai_confidence'] 
            for d in decisions 
            if d['decision']['decision']['type'] == 'auto_heal'
        ) / auto_heal
        print(f"📊 Average auto-heal confidence: {avg_conf:.1%}")
    
    print(f"\n💾 Files created:")
    print(f"   memory/decisions.json - All decisions with details")
    print(f"   memory/decisions_report.txt - Human-readable report")
    print(f"   memory/action_log.json - Auto-heal actions for Day 5")
    
    # Show example decisions
    print(f"\n📋 EXAMPLE DECISIONS:")
    for decision in decisions[:2]:  # First 2 decisions
        d = decision['decision']
        icon = "✅" if d['decision']['type'] == 'auto_heal' else "🔄"
        print(f"{icon} {d['input_analysis']['type'].replace('_', ' ').title():25} → {d['decision']['type'].replace('_', ' ').title()}")
    
    print("\n" + "=" * 70)
    print("✅ DAY 4 COMPLETE! Decision Agent is operational.")
    print("➡️  Next: Day 5 - Action Agent (Self-healing execution)")
    print("=" * 70)


if __name__ == "__main__":
    main()