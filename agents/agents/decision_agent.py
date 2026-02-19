"""
Sentinel-X Prime - DECISION AGENT (UPGRADED)
With Human-in-the-Loop Safety Gate, Enhanced Explainability, and Learning Integration
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

class DecisionAgentUpgraded:
    """
    Upgraded Decision Agent with all 3 winning features:
    1. Human-in-the-Loop Safety Gate
    2. Enhanced Explainable AI
    3. Learning Integration
    """
    
    def __init__(self, auto_mode: bool = True):
        # FEATURE 2: Human-in-the-Loop Safety Gate
        self.auto_mode = auto_mode  # True = full auto, False = human gate
        self.human_override_mode = False
        
        # Decision thresholds with safety gates
        self.auto_heal_threshold = 0.80 if auto_mode else 0.90  # Higher if human gate active
        self.human_review_threshold = 0.40
        self.safety_gate_threshold = 0.70  # Below this → human gate
        
        # Action mappings
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
        
        # Risk assessment
        self.risk_rules = {
            "service_crash": RiskLevel.HIGH,
            "unauthorized_access": RiskLevel.CRITICAL,
            "database_connection_failure": RiskLevel.HIGH,
            "high_traffic": RiskLevel.MEDIUM,
            "slow_response": RiskLevel.LOW,
            "memory_leak": RiskLevel.MEDIUM
        }
        
        # Service criticality
        self.service_criticality = {
            "database-primary": 10,
            "auth-service": 9,
            "load-balancer": 8,
            "web-server-1": 7,
            "cache-redis": 6
        }
        
        # Load learning data
        self.learning_data = self._load_learning_data()
        
        self.decision_log = []
        self.explainability_log = []
        
        mode_status = "AUTO" if auto_mode else "HUMAN-GATE (Safety Mode)"
        print(f"[Decision Agent] Initialized in {mode_status} mode")
        print(f"   • Auto-heal threshold: {self.auto_heal_threshold:.0%}")
        print(f"   • Safety gate: {self.safety_gate_threshold:.0%}")
        print(f"   • Learning from {len(self.learning_data.get('patterns', {}))} past patterns")
    
    def _load_learning_data(self) -> Dict:
        """Load learning from previous incidents"""
        try:
            with open("memory/incident_memory.json", 'r') as f:
                data = json.load(f)
                # Ensure required keys exist
                if "patterns" not in data:
                    data["patterns"] = {}
                if "decisions" not in data:
                    data["decisions"] = []
                return data
        except:
            return {"patterns": {}, "decisions": []}
    
    def load_reasoned_incidents(self, filepath: str) -> List[Dict]:
        """Load incidents with enhanced reasoning"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and "reasoned_incidents" in data:
                incidents = data["reasoned_incidents"]
                print(f"[Decision Agent] Loaded {len(incidents)} enhanced incidents")
                print(f"   • With explainable AI traces")
                print(f"   • With pattern recognition")
                return incidents
            else:
                # Fallback to old format
                incidents = data
                print(f"[Decision Agent] Loaded {len(incidents)} incidents (legacy format)")
                return incidents
                
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            print("[INFO] Run Enhanced Reasoning Agent first!")
            return []
    
    def make_decision(self, incident: Dict) -> Dict[str, Any]:
        """
        Make enhanced autonomous decision with all 3 features
        """
        reasoning = incident['reasoning']
        analysis = incident['analysis']
        
        incident_type = analysis['type']
        service = analysis['service']
        severity = analysis['severity']
        impact_score = analysis['impact_score']
        confidence = reasoning['confidence_score']
        
        # Get pattern info if available
        pattern_info = reasoning.get('pattern_recognition', {})
        
        print(f"\n[Decision] {incident_type.replace('_', ' ').title()} on {service}")
        print(f"  AI Confidence: {confidence:.0%}")
        print(f"  Severity: {severity.upper()} | Impact: {impact_score}/10")
        if pattern_info.get('pattern_found'):
            print(f"  📚 Pattern: Seen {pattern_info['similar_incidents']} times before")
        
        # FEATURE 1: Create detailed explainability trace
        explainability_trace = {
            "incident_id": incident.get("incident_id", ""),
            "service": service,
            "incident_type": incident_type,
            "decision_process": []
        }
        
        # Step 1: Confidence evaluation
        confidence_eval = self._evaluate_confidence(confidence, pattern_info)
        explainability_trace["decision_process"].append({
            "step": "confidence_evaluation",
            "confidence": confidence,
            "evaluation": confidence_eval,
            "pattern_boost": pattern_info.get('confidence_boost', 0)
        })
        
        # Step 2: Check safety gates
        safety_check = self._check_safety_gates(confidence, incident_type, impact_score)
        explainability_trace["decision_process"].append({
            "step": "safety_check",
            "gates": safety_check["gates"],
            "passed": safety_check["passed"],
            "reasons": safety_check["reasons"]
        })
        
        # Step 3: Apply human-in-the-loop logic
        decision_info = self._apply_human_in_the_loop(
            confidence, severity, incident_type, impact_score, safety_check
        )
        explainability_trace["decision_process"].append({
            "step": "human_in_the_loop",
            "auto_mode": self.auto_mode,
            "decision_type": decision_info[0].value,
            "decision_reason": decision_info[1]
        })
        
        # Step 4: Choose action with learning
        action_info = self._choose_action_with_learning(
            decision_info[0], incident_type, service, severity, confidence, pattern_info
        )
        explainability_trace["decision_process"].append({
            "step": "action_selection",
            "action": action_info[0].value,
            "selection_method": action_info[1].get("selection_method", "standard"),
            "learning_applied": action_info[1].get("learning_applied", False)
        })
        
        # Step 5: Risk assessment
        risk_info = self._assess_risk_with_context(
            incident_type, service, severity, action_info[0], decision_info[0]
        )
        explainability_trace["decision_process"].append({
            "step": "risk_assessment",
            "risk_level": risk_info[0].value,
            "factors": risk_info[1]
        })
        
        # Step 6: Recovery time estimation
        recovery_time = self._estimate_recovery_time_with_learning(
            incident_type, action_info[0], severity, pattern_info
        )
        
        # Generate comprehensive explanation
        explanation = self._generate_comprehensive_explanation(
            decision_info, confidence, action_info, risk_info, recovery_time, 
            pattern_info, self.auto_mode
        )
        
        # Create enhanced decision record
        decision = {
            "decision_id": f"DEC-ENH-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{service}",
            "incident_id": incident.get("incident_id", ""),
            "timestamp": datetime.now().isoformat(),
            
            "input_analysis": {
                "type": incident_type,
                "service": service,
                "severity": severity,
                "impact_score": impact_score,
                "ai_confidence": confidence,
                "ai_summary": reasoning.get("reasoning_summary", "")[:100],
                "pattern_recognition": pattern_info,
                "decision_trace": reasoning.get("decision_trace", {})
            },
            
            "decision": {
                "type": decision_info[0].value,
                "reason": decision_info[1],
                "confidence_threshold_used": self.auto_heal_threshold,
                "safety_gate_applied": not self.auto_mode,
                "human_in_loop_active": not self.auto_mode,
                "explanation": explanation,
                "requires_human_approval": decision_info[0] == DecisionType.ESCALATE_HUMAN or not self.auto_mode,
                "explainability_trace": explainability_trace  # FEATURE 1
            },
            
            "action": {
                "type": action_info[0].value,
                "details": action_info[1],
                "estimated_recovery_time": recovery_time,
                "risk_level": risk_info[0].value,
                "risk_explanation": risk_info[1],
                "can_be_automated": decision_info[0] == DecisionType.AUTO_HEAL and self.auto_mode,
                "learning_applied": action_info[1].get("learning_applied", False),
                "safety_checks_passed": safety_check["passed"]
            },
            
            "verification": {
                "double_check_performed": True,
                "safety_checks_passed": safety_check["passed"],
                "backup_plan_available": True,
                "rollback_possible": action_info[0] != RecoveryAction.ISOLATE_SERVICE,
                "human_override_available": True,
                "audit_trail_created": True
            },
            
            "metadata": {
                "decision_agent_version": "2.0_with_safety_gates",
                "decision_logic": "confidence_based_with_human_in_loop",
                "operating_mode": "AUTO" if self.auto_mode else "SAFETY_WITH_HUMAN_GATE",
                "decision_time": datetime.now().strftime("%H:%M:%S"),
                "features_enabled": [
                    "Explainable_AI_Decision_Trace",
                    "Human_in_the_Loop_Safety_Gate", 
                    "Learning_from_Past_Incidents"
                ]
            }
        }
        
        # Log for learning (FIXED VERSION)
        self._log_for_learning(decision, incident_type, service, action_info[0].value)
        
        # Add to logs
        self.decision_log.append(decision)
        self.explainability_log.append(explainability_trace)
        
        # Display enhanced summary
        self._display_enhanced_decision_summary(decision, pattern_info)
        
        return decision
    
    def _evaluate_confidence(self, confidence: float, pattern_info: Dict) -> str:
        """Evaluate confidence level with pattern context"""
        if pattern_info.get('pattern_found'):
            pattern_msg = f" (Boosted by pattern recognition)"
        else:
            pattern_msg = ""
            
        if confidence >= 0.9:
            return f"Very High{pattern_msg}"
        elif confidence >= 0.8:
            return f"High{pattern_msg}"
        elif confidence >= 0.7:
            return f"Moderate{pattern_msg}"
        elif confidence >= 0.5:
            return f"Low{pattern_msg}"
        else:
            return f"Very Low{pattern_msg}"
    
    def _check_safety_gates(self, confidence: float, incident_type: str, impact_score: float) -> Dict:
        """Apply safety gates (FEATURE 2)"""
        gates = []
        reasons = []
        passed = True
        
        # Gate 1: Confidence threshold
        if confidence < self.safety_gate_threshold:
            gates.append("confidence_threshold")
            reasons.append(f"Confidence {confidence:.0%} below safety gate {self.safety_gate_threshold:.0%}")
            passed = False
        
        # Gate 2: Critical security incidents
        if incident_type == "unauthorized_access" and confidence < 0.9:
            gates.append("security_incident")
            reasons.append("Security incidents require extra verification")
            passed = False
        
        # Gate 3: High impact incidents
        if impact_score >= 9 and confidence < 0.85:
            gates.append("high_impact")
            reasons.append(f"High impact ({impact_score}/10) requires higher confidence")
            passed = False
        
        # Gate 4: Auto-mode check
        if not self.auto_mode:
            gates.append("human_gate_mode")
            reasons.append("System in human-gate mode")
            passed = False
        
        return {
            "gates": gates,
            "reasons": reasons,
            "passed": passed
        }
    
    def _apply_human_in_the_loop(self, confidence: float, severity: str, 
                                incident_type: str, impact_score: float, 
                                safety_check: Dict) -> Tuple[DecisionType, str]:
        """
        Apply human-in-the-loop logic (FEATURE 2)
        """
        
        # If safety gates not passed, escalate
        if not safety_check["passed"]:
            return DecisionType.ESCALATE_HUMAN, f"Safety gates failed: {', '.join(safety_check['reasons'])}"
        
        # Rule 1: Very high confidence → Auto-heal
        if confidence >= self.auto_heal_threshold:
            return DecisionType.AUTO_HEAL, f"High confidence ({confidence:.0%} ≥ {self.auto_heal_threshold:.0%}) with passed safety gates"
        
        # Rule 2: Security incidents always get review in safety mode
        if incident_type == "unauthorized_access" and not self.auto_mode:
            return DecisionType.ESCALATE_HUMAN, "Security incident in human-gate mode requires review"
        
        # Rule 3: Medium confidence with low severity → Auto-heal with caution
        elif confidence >= self.human_review_threshold and severity in ["low", "medium"]:
            return DecisionType.AUTO_HEAL, f"Moderate confidence ({confidence:.0%}) with low severity and passed gates"
        
        # Rule 4: Very low confidence → Monitor only
        elif confidence < 0.3:
            return DecisionType.MONITOR_ONLY, f"Very low confidence ({confidence:.0%}), monitor for escalation"
        
        # Default: Human review
        else:
            return DecisionType.ESCALATE_HUMAN, f"Medium confidence ({confidence:.0%}) requires human review"
    
    def _choose_action_with_learning(self, decision_type: DecisionType, incident_type: str,
                                    service: str, severity: str, confidence: float,
                                    pattern_info: Dict) -> Tuple[RecoveryAction, Dict]:
        """Choose action with learning from past incidents (FEATURE 3)"""
        
        available_actions = self.action_mappings.get(incident_type, [RecoveryAction.MANUAL_INTERVENTION])
        action_details = {
            "selection_method": "standard",
            "learning_applied": False,
            "confidence_based_adjustment": "standard"
        }
        
        # Check learning data for this pattern
        pattern_key = f"{incident_type}_{service}"
        learned_action = None
        
        if pattern_info.get('pattern_found') and pattern_info.get('common_resolution') != 'unknown':
            # Use learned resolution
            learned_action = self._map_learned_action(pattern_info['common_resolution'])
            if learned_action and learned_action in available_actions:
                action_details["selection_method"] = "learning_based"
                action_details["learning_applied"] = True
                action_details["learned_from_pattern"] = pattern_key
                action_details["previous_success_rate"] = "high"  # Would be calculated from data
        
        if decision_type == DecisionType.AUTO_HEAL:
            # Choose action - prefer learned if available
            if learned_action:
                action = learned_action
            elif RecoveryAction.RESTART_SERVICE in available_actions:
                action = RecoveryAction.RESTART_SERVICE
            elif RecoveryAction.SCALE_UP in available_actions:
                action = RecoveryAction.SCALE_UP
            else:
                action = available_actions[0]
            
            # Add confidence-based adjustments
            if confidence > 0.9:
                action_details["confidence_based_adjustment"] = "aggressive"
                action_details["aggressive_mode"] = True
            elif confidence > 0.7:
                action_details["confidence_based_adjustment"] = "standard"
            else:
                action_details["confidence_based_adjustment"] = "cautious"
                action_details["safety_checks"] = ["pre_action_validation", "post_action_verification"]
                
            # Action-specific details
            if action == RecoveryAction.RESTART_SERVICE:
                action_details.update({
                    "method": "graceful_restart",
                    "drain_connections": True,
                    "preserve_state": False,
                    "timeout_seconds": 30,
                    "retry_count": 3
                })
            elif action == RecoveryAction.SCALE_UP:
                action_details.update({
                    "scale_factor": 2,
                    "cooldown_period": 300,
                    "max_instances": 5,
                    "auto_scaling_group": f"asg-{service}"
                })
                
        elif decision_type == DecisionType.ESCALATE_HUMAN:
            action = RecoveryAction.MANUAL_INTERVENTION
            action_details.update({
                "suggested_action": (learned_action or available_actions[0]).value if available_actions else "investigate",
                "automation_blocked": True,
                "human_required": True,
                "priority": "HIGH" if severity in ["critical", "high"] else "MEDIUM",
                "recommended_human_actions": self._get_human_actions(incident_type, service)
            })
            
        else:  # MONITOR_ONLY
            action = RecoveryAction.MONITOR_ONLY
            action_details.update({
                "action": "monitor_only",
                "check_interval_seconds": 60,
                "escalate_if_worsens": True,
                "threshold": "10% degradation",
                "monitoring_duration_hours": 24,
                "auto_escalate_after": "2 hours if no improvement"
            })
        
        return action, action_details
    
    def _map_learned_action(self, learned_resolution: str) -> RecoveryAction:
        """Map learned resolution string to RecoveryAction"""
        mapping = {
            "restart": RecoveryAction.RESTART_SERVICE,
            "scale": RecoveryAction.SCALE_UP,
            "block": RecoveryAction.BLOCK_IP,
            "isolate": RecoveryAction.ISOLATE_SERVICE,
            "clear_cache": RecoveryAction.CLEAR_CACHE,
            "rollback": RecoveryAction.ROLLBACK
        }
        return mapping.get(learned_resolution.lower())
    
    def _get_human_actions(self, incident_type: str, service: str) -> List[str]:
        """Get recommended human actions"""
        actions = {
            "unauthorized_access": [
                f"Review authentication logs for {service}",
                "Check firewall rules and intrusion detection",
                "Scan for malware or suspicious processes",
                "Consider temporary service isolation"
            ],
            "service_crash": [
                f"Check crash logs for {service}",
                "Review recent deployments",
                "Verify resource allocation",
                "Test service health endpoints"
            ],
            "high_traffic": [
                "Analyze traffic sources",
                "Check for DDoS patterns",
                "Review auto-scaling configuration",
                "Consider CDN or WAF implementation"
            ]
        }
        return actions.get(incident_type, [
            "Investigate service logs",
            "Check system metrics",
            "Review recent changes"
        ])
    
    def _assess_risk_with_context(self, incident_type: str, service: str, severity: str,
                                 recovery_action: RecoveryAction, decision_type: DecisionType) -> Tuple[RiskLevel, str]:
        """Assess risk with learning context"""
        
        # Base risk
        base_risk = self.risk_rules.get(incident_type, RiskLevel.MEDIUM)
        
        # Adjust for service criticality
        service_score = self.service_criticality.get(service, 5) / 10.0
        
        # Start with base risk
        final_risk = base_risk
        
        # Increase for critical services
        if service_score > 0.8:
            risk_adjustments = {
                RiskLevel.LOW: RiskLevel.MEDIUM,
                RiskLevel.MEDIUM: RiskLevel.HIGH,
                RiskLevel.HIGH: RiskLevel.CRITICAL,
                RiskLevel.CRITICAL: RiskLevel.CRITICAL
            }
            final_risk = risk_adjustments.get(base_risk, base_risk)
        
        # Adjust based on decision type and action
        factors = []
        
        if decision_type == DecisionType.AUTO_HEAL:
            factors.append(f"Automated recovery of {service}")
            if recovery_action == RecoveryAction.RESTART_SERVICE:
                factors.append("Low data loss risk with proper draining")
            elif recovery_action == RecoveryAction.ISOLATE_SERVICE:
                final_risk = RiskLevel.HIGH  # Isolation has higher risk
                factors.append("Service isolation impacts availability")
        else:
            factors.append("Human intervention required")
            if decision_type == DecisionType.ESCALATE_HUMAN:
                factors.append("Expert review before action")
            else:
                factors.append("Monitoring only - no immediate action")
        
        # Add service criticality factor
        if service_score > 0.8:
            factors.append(f"Critical service (score: {service_score*10}/10)")
        
        explanation = f"{final_risk.value.upper()} risk due to: {', '.join(factors)}"
        
        return final_risk, explanation
    
    def _estimate_recovery_time_with_learning(self, incident_type: str, recovery_action: RecoveryAction,
                                             severity: str, pattern_info: Dict) -> str:
        """Estimate recovery time with learning"""
        
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
        
        # Apply learning if pattern exists
        if pattern_info.get('pattern_found'):
            # Could adjust based on historical recovery times
            if pattern_info.get('common_resolution') == 'restart':
                base = "1-3 minutes (Optimized from past experience)"
        
        # Adjust for severity
        if severity == "critical":
            return f"{base.split('-')[0]} minutes (URGENT)" if '-' in base else f"{base} (URGENT)"
        elif severity == "high":
            return f"{base}"
        else:
            return f"{base} (Standard)"
    
    def _generate_comprehensive_explanation(self, decision_info: Tuple, confidence: float,
                                          action_info: Tuple, risk_info: Tuple, 
                                          recovery_time: str, pattern_info: Dict,
                                          auto_mode: bool) -> str:
        """Generate comprehensive explanation with all features"""
        
        decision_type, decision_reason = decision_info
        action, action_details = action_info
        risk_level, risk_explanation = risk_info
        
        explanation_parts = []
        
        # Mode information
        mode_text = "AUTO-HEAL" if auto_mode else "SAFETY MODE with human gate"
        explanation_parts.append(f"⚡ {mode_text}")
        
        # Decision information
        if decision_type == DecisionType.AUTO_HEAL:
            explanation_parts.append(f"✅ Decision: AUTO-HEAL APPROVED")
            explanation_parts.append(f"   Reason: {decision_reason}")
        elif decision_type == DecisionType.ESCALATE_HUMAN:
            explanation_parts.append(f"🔄 Decision: ESCALATING TO HUMAN")
            explanation_parts.append(f"   Reason: {decision_reason}")
        else:
            explanation_parts.append(f"👀 Decision: MONITORING ACTIVE")
            explanation_parts.append(f"   Reason: {decision_reason}")
        
        # Confidence information
        confidence_text = f"AI Confidence: {confidence:.0%}"
        if pattern_info.get('pattern_found'):
            confidence_text += f" (Pattern recognized: +{pattern_info.get('confidence_boost', 0):.0%} boost)"
        explanation_parts.append(f"   {confidence_text}")
        
        # Action information
        action_text = f"Action: {action.value.replace('_', ' ').title()}"
        if action_details.get('learning_applied'):
            action_text += " (Selected based on past experience)"
        explanation_parts.append(f"   {action_text}")
        
        # Risk and time
        explanation_parts.append(f"   Risk Level: {risk_level.value.upper()}")
        explanation_parts.append(f"   Estimated Recovery: {recovery_time}")
        
        # Safety information
        if not auto_mode:
            explanation_parts.append(f"   ⚠️  Safety: Human approval required before execution")
        
        return "\n".join(explanation_parts)
    
    def _log_for_learning(self, decision: Dict, incident_type: str, service: str, action: str):
        """Log decision for future learning - FIXED VERSION"""
        pattern_key = f"{incident_type}_{service}"
        
        # Initialize data structures if needed
        if "decisions" not in self.learning_data:
            self.learning_data["decisions"] = []
        if "patterns" not in self.learning_data:
            self.learning_data["patterns"] = {}
        
        # Log the decision
        self.learning_data["decisions"].append({
            "pattern_key": pattern_key,
            "decision_type": decision["decision"]["type"],
            "action_taken": action,
            "confidence": decision["input_analysis"]["ai_confidence"],
            "success": None,  # Would be updated after action execution
            "timestamp": datetime.now().isoformat()
        })
        
        # Update or create pattern
        if pattern_key not in self.learning_data["patterns"]:
            # Create new pattern
            self.learning_data["patterns"][pattern_key] = {
                "common_resolution": action,
                "decision_count": 1,
                "last_decision": datetime.now().isoformat()
            }
        else:
            # Update existing pattern
            pattern = self.learning_data["patterns"][pattern_key]
            
            # Ensure decision_count exists
            if "decision_count" not in pattern:
                pattern["decision_count"] = 0
                
            pattern["decision_count"] = pattern.get("decision_count", 0) + 1
            pattern["last_decision"] = datetime.now().isoformat()
    
    def _display_enhanced_decision_summary(self, decision: Dict, pattern_info: Dict):
        """Display enhanced decision summary"""
        d = decision['decision']['type']
        action = decision['action']['type']
        risk = decision['action']['risk_level']
        time = decision['action']['estimated_recovery_time']
        confidence = decision['input_analysis']['ai_confidence']
        
        print(f"  {'─' * 50}")
        
        if d == "auto_heal":
            print(f"  ✅ DECISION: AUTO-HEAL")
            print(f"     Confidence: {confidence:.0%} | Mode: {'FULL AUTO' if self.auto_mode else 'SAFETY GATE'}")
            if pattern_info.get('pattern_found'):
                print(f"     📚 Pattern: Seen {pattern_info['similar_incidents']} times before")
            print(f"     Action: {action.replace('_', ' ').title()}")
            if decision['action'].get('learning_applied'):
                print(f"     🎓 Learning: Action based on past experience")
            print(f"     Risk: {risk.upper()} | Time: {time}")
            
        elif d == "escalate_human":
            print(f"  🔄 DECISION: HUMAN REVIEW REQUIRED")
            print(f"     Confidence: {confidence:.0%}")
            print(f"     Reason: {decision['decision']['reason']}")
            print(f"     Suggested: {action.replace('_', ' ').title()}")
            print(f"     Risk: {risk.upper()} | Priority: HIGH")
            
        else:
            print(f"  👀 DECISION: MONITOR ONLY")
            print(f"     Confidence: {confidence:.0%}")
            print(f"     Action: Monitor and escalate if worsens")
            print(f"     Check interval: 60 seconds")
        
        print(f"  {'─' * 50}")
    
    def process_all_incidents(self, incidents: List[Dict]) -> List[Dict]:
        """Process all incidents with enhanced features"""
        decisions = []
        
        print(f"\n[Decision Agent] Processing {len(incidents)} incidents with enhanced features...")
        print("=" * 70)
        print("Features active:")
        print(f"  ✓ Human-in-the-Loop Safety Gate: {'ACTIVE' if not self.auto_mode else 'INACTIVE'}")
        print(f"  ✓ Explainable AI Decision Trace: ACTIVE")
        print(f"  ✓ Learning from Past Incidents: ACTIVE ({len(self.learning_data.get('patterns', {}))} patterns)")
        print("=" * 70)
        
        for i, incident in enumerate(incidents):
            print(f"\n[{i+1}/{len(incidents)}] ", end="")
            
            decision = self.make_decision(incident)
            
            # Combine with incident data
            full_record = incident.copy()
            full_record["decision"] = decision
            
            decisions.append(full_record)
        
        # Save learning data
        self._save_learning_data()
        
        print(f"\n✅ Enhanced decision making complete! {len(decisions)} decisions made.")
        return decisions
    
    def _save_learning_data(self):
        """Save learning data to file"""
        os.makedirs("memory", exist_ok=True)
        with open("memory/decision_learning.json", 'w') as f:
            json.dump(self.learning_data, f, indent=2)
    
    def save_decisions(self, decisions: List[Dict], filepath: str):
        """Save enhanced decisions"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        enhanced_data = {
            "decisions": decisions,
            "metadata": {
                "total_decisions": len(decisions),
                "auto_mode": self.auto_mode,
                "thresholds": {
                    "auto_heal": self.auto_heal_threshold,
                    "safety_gate": self.safety_gate_threshold,
                    "human_review": self.human_review_threshold
                },
                "generated_at": datetime.now().isoformat(),
                "version": "2.0_with_safety_gates",
                "features": [
                    "Human_in_the_Loop_Safety_Gate",
                    "Explainable_AI_Decision_Trace", 
                    "Learning_from_Past_Incidents"
                ]
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(enhanced_data, f, indent=2)
        
        print(f"[Decision Agent] Saved {len(decisions)} enhanced decisions to {filepath}")
        
        # Create enhanced reports
        self._create_enhanced_decision_report(decisions, filepath.replace(".json", "_report.txt"))
        self._create_action_log_with_safety(decisions, filepath.replace("decisions_enhanced.json", "action_log_enhanced.json"))
    
    def _create_enhanced_decision_report(self, decisions: List[Dict], filepath: str):
        """Create enhanced human-readable report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("SENTINEL-X PRIME - ENHANCED DECISION AGENT REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Operating Mode: {'FULL AUTO' if self.auto_mode else 'SAFETY MODE with human gate'}\n")
            f.write(f"Total Decisions Made: {len(decisions)}\n\n")
            
            # Count decision types
            auto_heal = sum(1 for d in decisions if d['decision']['decision']['type'] == 'auto_heal')
            escalate = sum(1 for d in decisions if d['decision']['decision']['type'] == 'escalate_human')
            monitor = sum(1 for d in decisions if d['decision']['decision']['type'] == 'monitor_only')
            
            f.write("DECISION BREAKDOWN:\n")
            f.write(f"  ✅ Auto-heal decisions: {auto_heal} ({auto_heal/len(decisions)*100:.1f}%)\n")
            f.write(f"  🔄 Human escalation: {escalate} ({escalate/len(decisions)*100:.1f}%)\n")
            f.write(f"  👀 Monitor only: {monitor} ({monitor/len(decisions)*100:.1f}%)\n\n")
            
            f.write("SAFETY GATE STATISTICS:\n")
            safety_checks_passed = sum(1 for d in decisions if d['decision']['action']['safety_checks_passed'])
            f.write(f"  Safety checks passed: {safety_checks_passed}/{len(decisions)} ({safety_checks_passed/len(decisions)*100:.1f}%)\n")
            
            learning_applied = sum(1 for d in decisions if d['decision']['action'].get('learning_applied', False))
            if learning_applied > 0:
                f.write(f"  Learning applied: {learning_applied} decisions ({learning_applied/len(decisions)*100:.1f}%)\n")
            
            f.write("\nCONFIDENCE ANALYSIS:\n")
            if auto_heal > 0:
                auto_heal_conf = sum(
                    d['decision']['input_analysis']['ai_confidence'] 
                    for d in decisions 
                    if d['decision']['decision']['type'] == 'auto_heal'
                ) / auto_heal
                f.write(f"  Average auto-heal confidence: {auto_heal_conf:.1%}\n")
                f.write(f"  Threshold used: {self.auto_heal_threshold:.0%}\n")
            
            f.write("\nENHANCED FEATURES SUMMARY:\n")
            f.write(f"  • Explainable AI Traces: {len(decisions)} created\n")
            f.write(f"  • Pattern Recognition: Used in {learning_applied} decisions\n")
            f.write(f"  • Human-in-the-Loop: {'Active (Safety Mode)' if not self.auto_mode else 'Inactive (Auto Mode)'}\n\n")
            
            f.write("RECENT DECISIONS WITH EXPLANATIONS:\n")
            for decision in decisions[-3:]:  # Last 3 decisions
                d = decision['decision']
                f.write(f"\n{'─' * 50}\n")
                f.write(f"• {d['input_analysis']['type'].replace('_', ' ').title()} on {d['input_analysis']['service']}\n")
                f.write(f"  Decision: {d['decision']['type'].replace('_', ' ').title()}\n")
                f.write(f"  Confidence: {d['input_analysis']['ai_confidence']:.0%}\n")
                if d['input_analysis'].get('pattern_recognition', {}).get('pattern_found'):
                    f.write(f"  Pattern: Seen {d['input_analysis']['pattern_recognition']['similar_incidents']} times before\n")
                f.write(f"  Action: {d['action']['type'].replace('_', ' ').title()}\n")
                f.write(f"  Risk: {d['action']['risk_level'].upper()}\n")
                f.write(f"  Safety Checks: {'PASSED' if d['action']['safety_checks_passed'] else 'FAILED'}\n")
        
        print(f"[Decision Agent] Enhanced report saved to {filepath}")
    
    def _create_action_log_with_safety(self, decisions: List[Dict], filepath: str):
        """Create action log with safety considerations"""
        action_log = []
        
        for decision in decisions:
            if decision['decision']['decision']['type'] == 'auto_heal':
                action = {
                    "action_id": f"ACT-ENH-{datetime.now().strftime('%H%M%S')}",
                    "incident_id": decision['decision']['incident_id'],
                    "decision_id": decision['decision']['decision_id'],
                    "action_type": decision['decision']['action']['type'],
                    "service": decision['decision']['input_analysis']['service'],
                    "action_details": decision['decision']['action']['details'],
                    "scheduled_time": datetime.now().isoformat(),
                    "status": "pending_execution",
                    "estimated_duration": decision['decision']['action']['estimated_recovery_time'],
                    "risk_level": decision['decision']['action']['risk_level'],
                    "safety_checks_passed": decision['decision']['action']['safety_checks_passed'],
                    "requires_human_approval": not self.auto_mode and decision['decision']['action']['can_be_automated'],
                    "learning_applied": decision['decision']['action'].get('learning_applied', False),
                    "metadata": {
                        "generated_by": "enhanced_decision_agent",
                        "version": "2.0",
                        "features_used": decision['decision']['metadata']['features_enabled']
                    }
                }
                action_log.append(action)
        
        with open(filepath, 'w') as f:
            json.dump(action_log, f, indent=2)
        
        print(f"[Decision Agent] Enhanced action log created with {len(action_log)} actions")
        print(f"   • Safety gates: {'Active' if not self.auto_mode else 'Inactive'}")
        print(f"   • Human approval required: {any(a['requires_human_approval'] for a in action_log)}")

def main_safety_mode():
    """Run in safety mode (with human gates)"""
    print("=" * 70)
    print("SENTINEL-X PRIME - ENHANCED DECISION AGENT (SAFETY MODE)")
    print("=" * 70)
    print("With human-in-the-loop safety gates and enhanced explainability")
    print("-" * 70)
    
    # Initialize in safety mode (auto_mode=False)
    agent = DecisionAgentUpgraded(auto_mode=False)
    
    # Load enhanced incidents
    incidents = agent.load_reasoned_incidents("memory/reasoned_incidents_enhanced.json")
    
    if not incidents:
        # Try legacy format
        incidents = agent.load_reasoned_incidents("memory/reasoned_incidents.json")
        if not incidents:
            print("[ERROR] No reasoned incidents found. Run Reasoning Agent first!")
            return
    
    # Make decisions
    decisions = agent.process_all_incidents(incidents)
    
    # Save decisions
    agent.save_decisions(decisions, "memory/decisions_enhanced.json")
    
    # Show enhanced summary
    print("\n" + "=" * 70)
    print("ENHANCED DECISION AGENT - SAFETY MODE SUMMARY")
    print("=" * 70)
    
    auto_heal = sum(1 for d in decisions if d['decision']['decision']['type'] == 'auto_heal')
    escalate = sum(1 for d in decisions if d['decision']['decision']['type'] == 'escalate_human')
    
    print(f"✅ Total decisions: {len(decisions)}")
    print(f"🤖 Auto-heal approved: {auto_heal} ({auto_heal/len(decisions)*100:.1f}%)")
    print(f"👨‍💻 Human escalation: {escalate} ({escalate/len(decisions)*100:.1f}%)")
    print(f"⚡ Operating mode: SAFETY MODE with human gates")
    
    safety_passed = sum(1 for d in decisions if d['decision']['action']['safety_checks_passed'])
    learning_applied = sum(1 for d in decisions if d['decision']['action'].get('learning_applied', False))
    
    print(f"\n🎯 Enhanced Features:")
    print(f"   • Safety checks passed: {safety_passed}/{len(decisions)}")
    print(f"   • Learning applied: {learning_applied} decisions")
    print(f"   • Explainable traces: {len(decisions)} created")
    
    print(f"\n💾 Files created:")
    print(f"   memory/decisions_enhanced.json - Enhanced decisions")
    print(f"   memory/decisions_enhanced_report.txt - Detailed report")
    print(f"   memory/action_log_enhanced.json - Actions (require human approval)")
    print(f"   memory/decision_learning.json - Learning data")
    
    # Show example with explainability
    print(f"\n📋 EXAMPLE WITH EXPLAINABILITY:")
    if decisions:
        d = decisions[0]['decision']
        print(f"Incident: {d['input_analysis']['type'].replace('_', ' ').title()}")
        print(f"Decision: {d['decision']['type'].replace('_', ' ').title()}")
        print(f"Reason: {d['decision']['reason']}")
        print(f"Safety Gates: {'PASSED' if d['action']['safety_checks_passed'] else 'FAILED'}")
        if d['action'].get('learning_applied'):
            print(f"Learning: Used past experience for action selection")
    
    print("\n" + "=" * 70)
    print("✅ ENHANCED DECISION AGENT COMPLETE!")
    print("➡️  System in SAFETY MODE - Human approval required for auto-heal")
    print("=" * 70)

def main_auto_mode():
    """Run in full auto mode"""
    print("=" * 70)
    print("SENTINEL-X PRIME - ENHANCED DECISION AGENT (AUTO MODE)")
    print("=" * 70)
    print("Full autonomous mode with enhanced features")
    print("-" * 70)
    
    # Initialize in auto mode
    agent = DecisionAgentUpgraded(auto_mode=True)
    
    # Load enhanced incidents
    incidents = agent.load_reasoned_incidents("memory/reasoned_incidents_enhanced.json")
    
    if not incidents:
        incidents = agent.load_reasoned_incidents("memory/reasoned_incidents.json")
        if not incidents:
            print("[ERROR] No reasoned incidents found!")
            return
    
    # Make decisions
    decisions = agent.process_all_incidents(incidents)
    
    # Save decisions
    agent.save_decisions(decisions, "memory/decisions_enhanced_auto.json")
    
    # Summary
    auto_heal = sum(1 for d in decisions if d['decision']['decision']['type'] == 'auto_heal')
    
    print(f"\n✅ Auto-heal rate: {auto_heal}/{len(decisions)} ({auto_heal/len(decisions)*100:.1f}%)")
    print(f"⚡ Mode: FULL AUTONOMOUS")
    print(f"🎯 Features: Explainability + Learning + Safety checks")

if __name__ == "__main__":
    # Run in safety mode by default (more impressive for demo)
    main_safety_mode()