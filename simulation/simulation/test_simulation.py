#!/usr/bin/env python3
"""
Test script for  completion
"""
import os
import json

def test_day1():
    """Run all Day 1 tests"""
    print("🧪 TESTING DAY 1 COMPLETION...")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Can we import modules?
    try:
        from simulation.service_simulator import SystemSimulator, ServiceStatus
        from simulation.incident_generator import IncidentGenerator
        from simulation.config import Config
        print("✅ Test 1/5: Imports working")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Test 1/5: Import failed - {e}")
        return False
    
    # Test 2: Run simulation
    try:
        simulator = SystemSimulator()
        generator = IncidentGenerator(simulator)
        incidents = generator.simulate_day(cycles=10)  # Quick test
        print("✅ Test 2/5: Simulation runs without errors")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2/5: Simulation failed - {e}")
        return False
    
    # Test 3: Check incident file exists
    if os.path.exists(Config.INCIDENT_LOG_PATH):
        print("✅ Test 3/5: Incident log created")
        tests_passed += 1
    else:
        print(f"❌ Test 3/5: Incident log not found at {Config.INCIDENT_LOG_PATH}")
    
    # Test 4: Check incident data structure
    try:
        with open(Config.INCIDENT_LOG_PATH, 'r') as f:
            incidents = json.load(f)
        if isinstance(incidents, list) and len(incidents) > 0:
            print("✅ Test 4/5: Incident data is valid")
            tests_passed += 1
        else:
            print("❌ Test 4/5: Incident data is empty or invalid")
    except Exception as e:
        print(f"❌ Test 4/5: Failed to read incident data - {e}")
    
    # Test 5: Check services changed state
    if os.path.exists(Config.SYSTEM_STATE_PATH):
        with open(Config.SYSTEM_STATE_PATH, 'r') as f:
            state = json.load(f)
        if len(state) == 5:  # We have 5 services
            print("✅ Test 5/5: Services have state data")
            tests_passed += 1
        else:
            print(f"❌ Test 5/5: Expected 5 services, got {len(state)}")
    else:
        print(f"❌ Test 5/5: System state file not found")
    
    # Final result
    print("=" * 50)
    print(f"📊 RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("\n🎉 DAY 1 IS OFFICIALLY COMPLETE!")
        print("✅ All systems operational")
        print("✅ Ready for Day 2: Perception Agent")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    test_day1()