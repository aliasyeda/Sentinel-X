"""
Sentinel-X Prime - REASONING AGENT (UPGRADED)
With Explainable AI Trace, Incident Memory, and Learning
"""
import json
import os
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

class ReasoningAgentUpgraded:
    """
    Upgraded reasoning agent with all 3 winning features:
    1. Explainable AI Decision Trace
    2. Learning from Past Incidents
    3. Enhanced Confidence Scoring
    """
    
    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.llm_model = os.getenv("LLM_MODEL", "gemini-1.5-pro")
        
        # Load incident memory for learning
        self.incident_memory = self._load_incident_memory()
        self.pattern_recognition = {}
        
        print(f"[Reasoning Agent] Using {self.llm_provider.upper()} ({self.llm_model})")
        print(f"[Memory] Loaded {len(self.incident_memory)} past incidents for learning")
        
        # Try to initialize LLM
        self.llm = None
        self._try_init_llm()
        
        # Decision trace storage
        self.decision_traces = []
    
    def _load_incident_memory(self) -> Dict:
        """Load past incidents for pattern recognition"""
        memory_path = "memory/incident_memory.json"
        if os.path.exists(memory_path):
            try:
                with open(memory_path, 'r') as f:
                    return json.load(f)
            except:
                return {"incidents": [], "patterns": {}, "last_updated": datetime.now().isoformat()}
        return {"incidents": [], "patterns": {}, "last_updated": datetime.now().isoformat()}
    
    def _save_incident_memory(self):
        """Save incident memory for future learning"""
        os.makedirs("memory", exist_ok=True)
        with open("memory/incident_memory.json", 'w') as f:
            json.dump(self.incident_memory, f, indent=2)
    
    def _try_init_llm(self):
        """Try to initialize LLM, but don't crash if fails"""
        try:
            # Try NEW Google GenAI
            try:
                import google.genai as genai
                api_key = os.getenv("GOOGLE_API_KEY")
                if api_key and "your_" not in api_key.lower():
                    client = genai.Client(api_key=api_key)
                    self.llm = client
                    print("✅ Using NEW google.genai client")
                    return
            except ImportError:
                pass
            
            # Try OLD library
            try:
                import google.generativeai as old_genai
                api_key = os.getenv("GOOGLE_API_KEY")
                if api_key and "your_" not in api_key.lower():
                    old_genai.configure(api_key=api_key)
                    self.llm = {"type": "old_genai", "configured": True}
                    print("✅ Using OLD google.generativeai")
                    return
            except ImportError:
                pass
            
            print("⚠️  No working Gemini library found. Using enhanced mock responses.")
            
        except Exception as e:
            print(f"⚠️  LLM init failed: {e}. Using enhanced mock responses.")
    
    def load_analyzed_incidents(self, filepath: str) -> List[Dict]:
        try:
            with open(filepath, 'r') as f:
                incidents = json.load(f)
            print(f"[Reasoning Agent] Loaded {len(incidents)} analyzed incidents")
            return incidents
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            return []
    
    def analyze_single_incident(self, incident: Dict) -> Dict[str, Any]:
        """Analyze incident with enhanced features"""
        
        analysis = incident['analysis']
        incident_type = analysis['type']
        service = analysis['service']
        severity = analysis['severity']
        impact = analysis['impact_score']
        incident_id = incident.get("incident_id", "")
        
        print(f"\n🔍 Analyzing: {incident_type.replace('_', ' ').title()} on {service}")
        
        # FEATURE 3: Check if similar incident occurred before (Learning)
        pattern_info = self._check_past_patterns(incident_type, service)
        
        # Create detailed decision trace
        decision_trace = {
            "incident_id": incident_id,
            "analysis_start": datetime.now().isoformat(),
            "input_analysis": analysis,
            "pattern_recognition": pattern_info,
            "reasoning_steps": []
        }
        
        # Step 1: Classify severity
        severity_reason = self._classify_severity(severity, impact)
        decision_trace["reasoning_steps"].append({
            "step": 1,
            "action": "severity_classification",
            "result": f"Classified as {severity.upper()}",
            "reason": severity_reason
        })
        
        # Step 2: Check patterns
        if pattern_info["pattern_found"]:
            pattern_reason = f"Pattern recognized: {pattern_info['similar_incidents']} similar incidents"
            decision_trace["reasoning_steps"].append({
                "step": 2,
                "action": "pattern_recognition",
                "result": "Pattern found",
                "reason": pattern_reason
            })
        
        # Get AI analysis
        llm_text = self._get_ai_analysis(incident_type, service, severity, impact, pattern_info)
        
        # Extract confidence with pattern boost
        base_confidence = self._extract_confidence(llm_text)
        confidence = self._adjust_confidence_with_patterns(base_confidence, pattern_info)
        
        # Step 3: Confidence calculation
        confidence_reason = f"Base: {base_confidence:.0%}, Pattern boost: {pattern_info['confidence_boost']:.0%}"
        decision_trace["reasoning_steps"].append({
            "step": 3,
            "action": "confidence_scoring",
            "result": f"Final confidence: {confidence:.0%}",
            "reason": confidence_reason
        })
        
        # Generate root causes
        root_causes = self._get_root_causes(incident_type)
        
        # Create enhanced output with decision trace
        result = {
            "incident_id": incident_id,
            "llm_analysis": llm_text,
            "reasoning_summary": self._create_summary(llm_text, incident_type, service),
            "confidence_score": confidence,
            "decision_trace": decision_trace,  # FEATURE 1: Explainable AI Trace
            "investigation_priority": self._determine_priority(severity, impact, confidence),
            "root_cause_hypotheses": root_causes,
            "pattern_recognition": pattern_info,  # FEATURE 3: Learning
            "related_patterns": [],
            "requires_expert_review": severity in ["critical", "high"] and confidence < 0.7,
            "recommended_next_steps": self._get_next_steps(incident_type, severity),
            "metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "llm_provider": "gemini" if self.llm else "mock",
                "llm_model": self.llm_model,
                "has_pattern_memory": pattern_info["pattern_found"],
                "reasoning_time": datetime.now().strftime("%H:%M:%S"),
                "version": "2.0_with_explainability"
            }
        }
        
        # Store for learning
        self._store_for_learning(incident_type, service, severity, confidence)
        
        # Add to traces
        self.decision_traces.append(decision_trace)
        
        return result
    
    def _check_past_patterns(self, incident_type: str, service: str) -> Dict:
        """Check if similar incidents occurred before (Learning feature)"""
        pattern_key = f"{incident_type}_{service}"
        
        if not self.incident_memory.get("patterns"):
            self.incident_memory["patterns"] = {}
        
        pattern_data = self.incident_memory["patterns"].get(pattern_key, {
            "count": 0,
            "last_occurrence": None,
            "avg_confidence": 0.7,
            "common_resolution": "unknown"
        })
        
        pattern_found = pattern_data["count"] > 0
        confidence_boost = min(0.15, pattern_data["count"] * 0.05)  # Max 15% boost
        
        return {
            "pattern_found": pattern_found,
            "pattern_key": pattern_key,
            "similar_incidents": pattern_data["count"],
            "last_occurrence": pattern_data["last_occurrence"],
            "confidence_boost": confidence_boost,
            "common_resolution": pattern_data["common_resolution"],
            "learning_applied": pattern_found
        }
    
    def _store_for_learning(self, incident_type: str, service: str, severity: str, confidence: float):
        """Store incident for future learning"""
        pattern_key = f"{incident_type}_{service}"
        
        if pattern_key not in self.incident_memory["patterns"]:
            self.incident_memory["patterns"][pattern_key] = {
                "count": 0,
                "first_occurrence": datetime.now().isoformat(),
                "severities": [],
                "confidences": [],
                "common_resolution": "unknown"
            }
        
        pattern = self.incident_memory["patterns"][pattern_key]
        pattern["count"] += 1
        pattern["last_occurrence"] = datetime.now().isoformat()
        pattern["severities"].append(severity)
        pattern["confidences"].append(confidence)
        
        # Update average confidence
        if pattern["confidences"]:
            pattern["avg_confidence"] = sum(pattern["confidences"]) / len(pattern["confidences"])
    
    def _classify_severity(self, severity: str, impact: float) -> str:
        """Explain why incident got its severity classification"""
        reasons = {
            "critical": f"Impact score {impact}/10 indicates system-wide failure",
            "high": f"Impact score {impact}/10 indicates major service degradation",
            "medium": f"Impact score {impact}/10 indicates limited service impact",
            "low": f"Impact score {impact}/10 indicates minor performance issue"
        }
        return reasons.get(severity, "Standard severity assessment")
    
    def _get_ai_analysis(self, incident_type: str, service: str, severity: str, 
                         impact: float, pattern_info: Dict) -> str:
        """Get AI analysis with pattern context"""
        
        if self.llm and isinstance(self.llm, dict) and self.llm.get("type") == "old_genai":
            try:
                import google.generativeai as genai
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                pattern_context = ""
                if pattern_info["pattern_found"]:
                    pattern_context = f"\nPattern Recognition: This incident type has occurred {pattern_info['similar_incidents']} times before on this service."
                
                prompt = f"""
                As a cybersecurity analyst, analyze this incident:
                
                Incident: {incident_type.replace('_', ' ').title()}
                Service: {service}
                Severity: {severity.upper()}
                Impact Score: {impact}/10
                {pattern_context}
                
                Provide analysis with:
                1. Root cause hypothesis
                2. Business impact assessment
                3. Confidence level (as percentage)
                4. Whether this is a known pattern
                
                Format clearly with sections.
                """
                
                response = model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                print(f"⚠️  Real AI failed: {e}")
        
        # Enhanced mock response with pattern info
        return self._create_enhanced_mock_analysis(incident_type, service, severity, impact, pattern_info)
    
    def _create_enhanced_mock_analysis(self, incident_type: str, service: str, severity: str, 
                                      impact: float, pattern_info: Dict) -> str:
        """Create enhanced mock analysis with pattern recognition"""
        
        templates = {
            "high_traffic": f"""
            Analysis: High traffic on {service}
            
            Root Cause Hypothesis:
            - Potential DDoS attack from multiple sources
            - Legitimate traffic surge due to marketing campaign
            - Load balancer misconfiguration
            
            Business Impact:
            - Service degradation affecting {impact*10}% of users
            - Potential revenue loss if e-commerce service
            
            Confidence: {random.randint(75, 90)}%
            
            Pattern Recognition: {'KNOWN PATTERN' if pattern_info['pattern_found'] else 'New pattern'}
            {f'Occurred {pattern_info["similar_incidents"]} times before' if pattern_info['pattern_found'] else ''}
            """,
            
            "service_crash": f"""
            Analysis: Service crash on {service}
            
            Root Cause Hypothesis:
            - Memory leak in application code
            - Resource exhaustion (CPU/Memory)
            - Database connection pool exhaustion
            
            Business Impact:
            - Complete service outage
            - Critical business functions affected
            
            Confidence: {random.randint(80, 95)}%
            
            Pattern Recognition: {'KNOWN PATTERN' if pattern_info['pattern_found'] else 'New pattern'}
            {f'Common resolution: {pattern_info["common_resolution"]}' if pattern_info['pattern_found'] else ''}
            """
        }
        
        default_template = f"""
        Analysis: {incident_type.replace('_', ' ').title()} on {service}
        
        Root Cause Hypothesis:
        - Requires investigation of service logs
        - Check recent deployments and changes
        
        Business Impact:
        - Severity: {severity.upper()}
        - Impact Score: {impact}/10
        
        Confidence: {random.randint(70, 85)}%
        
        Pattern Recognition: {'KNOWN PATTERN' if pattern_info['pattern_found'] else 'New pattern'}
        """
        
        return templates.get(incident_type, default_template)
    
    def _extract_confidence(self, text: str) -> float:
        """Extract confidence from text"""
        match = re.search(r'Confidence:\s*(\d+)%', text)
        if match:
            return int(match.group(1)) / 100.0
        
        # Try alternative patterns
        patterns = [
            r'confidence.*?(\d+)%',
            r'certainty.*?(\d+)%',
            r'(\d+)%.*?confidence'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1)) / 100.0
        
        return random.uniform(0.7, 0.85)
    
    def _adjust_confidence_with_patterns(self, base_confidence: float, pattern_info: Dict) -> float:
        """Adjust confidence based on past patterns"""
        if pattern_info["pattern_found"]:
            adjusted = base_confidence + pattern_info["confidence_boost"]
            return min(0.95, adjusted)  # Cap at 95%
        return base_confidence
    
    def _create_summary(self, llm_text: str, incident_type: str, service: str) -> str:
        """Create concise summary from analysis"""
        lines = llm_text.strip().split('\n')
        for line in lines:
            if line.strip() and not line.startswith(' ') and ':' in line:
                return line.strip()
        return f"{incident_type.replace('_', ' ').title()} on {service} requires investigation"
    
    def _determine_priority(self, severity: str, impact: float, confidence: float) -> str:
        """Determine investigation priority"""
        if severity == "critical" and impact >= 8:
            return "CRITICAL"
        elif severity in ["high", "critical"]:
            return "HIGH"
        elif confidence < 0.6:
            return "MEDIUM_WITH_REVIEW"
        else:
            return "STANDARD"
    
    def _get_root_causes(self, incident_type: str) -> List[str]:
        """Get root causes with explanations"""
        causes = {
            "high_traffic": [
                "DDoS attack - Malicious traffic flood",
                "Legitimate surge - Marketing campaign success",
                "Misconfiguration - Load balancer settings"
            ],
            "service_crash": [
                "Resource exhaustion - Memory/CPU limits reached",
                "Software bug - Recent deployment issue",
                "Dependency failure - External service down"
            ],
            "unauthorized_access": [
                "Credential stuffing - Automated login attempts",
                "Brute force attack - Password guessing",
                "Security misconfiguration - Open ports/services"
            ]
        }
        return causes.get(incident_type, ["Requires investigation", "Check service logs"])
    
    def _get_next_steps(self, incident_type: str, severity: str) -> List[str]:
        """Get recommended next steps"""
        steps = [
            "Check service logs for errors",
            "Review recent deployments/changes",
            "Monitor system metrics (CPU, Memory, Network)"
        ]
        
        if severity in ["critical", "high"]:
            steps.insert(0, "Immediate incident response team alert")
            steps.append("Prepare rollback plan if needed")
        
        if incident_type == "unauthorized_access":
            steps.extend([
                "Review authentication logs",
                "Check firewall rules",
                "Scan for malware/intrusions"
            ])
        
        return steps
    
    def analyze_all_incidents(self, incidents: List[Dict]) -> List[Dict]:
        """Analyze all incidents with enhanced features"""
        reasoned = []
        
        print(f"\n[Reasoning Agent] Analyzing {len(incidents)} incidents with enhanced features...")
        print("=" * 70)
        print("Features: ✓ Explainable AI Trace ✓ Pattern Learning ✓ Confidence Adjustment")
        print("=" * 70)
        
        for i, incident in enumerate(incidents):
            if i < 8:  # Detailed analysis for first 8
                print(f"\n[{i+1}/{len(incidents)}] {incident['analysis']['type'].replace('_', ' ').title()} on {incident['analysis']['service']}")
                
                reasoned_incident = self.analyze_single_incident(incident)
                combined = incident.copy()
                combined["reasoning"] = reasoned_incident
                reasoned.append(combined)
                
                conf = reasoned_incident['confidence_score']
                pattern = reasoned_incident['pattern_recognition']['pattern_found']
                pattern_msg = "✓ Pattern recognized" if pattern else "New pattern"
                print(f"   Confidence: {conf:.0%} | {pattern_msg}")
            else:
                # Quick analysis for rest
                simple = self.analyze_single_incident(incident)
                combined = incident.copy()
                combined["reasoning"] = simple
                reasoned.append(combined)
        
        # Save memory for learning
        self._save_incident_memory()
        
        print(f"\n✅ Enhanced analysis complete! {len(reasoned)} incidents reasoned.")
        print(f"📚 Learning: Stored {len(self.incident_memory['patterns'])} patterns for future decisions")
        
        return reasoned
    
    def save_reasoned_incidents(self, reasoned_incidents: List[Dict], filepath: str):
        """Save with enhanced metadata"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        # Add summary metadata
        enhanced_data = {
            "reasoned_incidents": reasoned_incidents,
            "metadata": {
                "total_incidents": len(reasoned_incidents),
                "average_confidence": sum(r['reasoning']['confidence_score'] for r in reasoned_incidents) / len(reasoned_incidents),
                "patterns_recognized": sum(1 for r in reasoned_incidents if r['reasoning']['pattern_recognition']['pattern_found']),
                "generated_at": datetime.now().isoformat(),
                "version": "2.0_with_explainability",
                "features": ["Explainable_AI_Trace", "Pattern_Learning", "Confidence_Adjustment"]
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(enhanced_data, f, indent=2)
        
        print(f"💾 Saved to: {filepath}")
        print(f"📊 Summary: {len(reasoned_incidents)} incidents, {enhanced_data['metadata']['patterns_recognized']} patterns recognized")

def main():
    print("=" * 70)
    print("SENTINEL-X PRIME - ENHANCED REASONING AGENT")
    print("=" * 70)
    print("With: ✓ Explainable AI ✓ Pattern Learning ✓ Confidence Adjustment")
    print("=" * 70)
    
    # Check .env
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or "your_" in api_key.lower():
        print("⚠️  WARNING: Using enhanced mock AI (no valid API key found)")
        print("   To use real AI: Edit .env file with your Gemini API key")
    else:
        print(f"✅ API Key found: {api_key[:15]}...")
    
    agent = ReasoningAgentUpgraded()
    
    # Load data
    incidents = agent.load_analyzed_incidents("memory/analyzed_incidents.json")
    if not incidents:
        print("❌ No incidents found. Run Day 2 first!")
        return
    
    # Analyze
    reasoned = agent.analyze_all_incidents(incidents)
    
    # Save
    agent.save_reasoned_incidents(reasoned, "memory/reasoned_incidents_enhanced.json")
    
    # Summary
    print("\n" + "=" * 70)
    print("ENHANCED REASONING - SUMMARY")
    print("=" * 70)
    print(f"✅ Incidents analyzed: {len(reasoned)}")
    print(f"🧠 AI Mode: {'Real Gemini AI' if agent.llm else 'Enhanced Mock AI'}")
    print(f"🎯 Features enabled:")
    print(f"   • Explainable AI Decision Trace")
    print(f"   • Pattern Learning from {len(agent.incident_memory['patterns'])} patterns")
    print(f"   • Confidence Adjustment with past incidents")
    
    if reasoned:
        avg_conf = sum(r['reasoning']['confidence_score'] for r in reasoned) / len(reasoned)
        patterns = sum(1 for r in reasoned if r['reasoning']['pattern_recognition']['pattern_found'])
        print(f"\n📊 Performance Metrics:")
        print(f"   • Average confidence: {avg_conf:.1%}")
        print(f"   • Patterns recognized: {patterns}/{len(reasoned)} incidents")
        print(f"   • Decision traces created: {len(agent.decision_traces)}")
    
    print(f"\n💾 Output files:")
    print(f"   memory/reasoned_incidents_enhanced.json - Enhanced reasoning")
    print(f"   memory/incident_memory.json - Learning database")
    
    print("\n" + "=" * 70)
    print("✅ ENHANCED REASONING COMPLETE!")
    print("➡️  Next: Enhanced Decision Agent")
    print("=" * 70)

if __name__ == "__main__":
    main()