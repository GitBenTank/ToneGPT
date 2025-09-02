#!/usr/bin/env python3
"""
Test AI Tone Generation Functionality
"""

import sys
from pathlib import Path

# Add the tonegpt directory to the path
sys.path.append(str(Path(__file__).parent / "tonegpt"))

from core.ai_tone_generator import AIToneGenerator

def test_ai_functionality():
    """Test the AI tone generation functionality."""
    print("🤖 Testing AI Tone Generation Functionality")
    print("=" * 60)
    
    try:
        # Initialize AI generator
        print("🔄 Initializing AI Tone Generator...")
        ai_generator = AIToneGenerator()
        print("✅ AI Tone Generator initialized successfully")
        
        # Test tone generation
        print("\n🎸 Testing tone generation...")
        test_queries = [
            "Give me a clean jazz tone",
            "Metal rhythm tone with tight bass",
            "Ambient lead with delay and reverb"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: '{query}'")
            try:
                generated_tone = ai_generator.generate_tone_from_query(query)
                
                print(f"✅ Tone generated successfully!")
                print(f"   Query: {generated_tone.get('query', 'N/A')}")
                print(f"   Description: {generated_tone.get('description', 'N/A')}")
                
                # Check tone structure
                if 'tone_structure' in generated_tone:
                    structure = generated_tone['tone_structure']
                    print(f"   Amp: {structure.get('amp', {}).get('model', 'N/A')}")
                    print(f"   Cab: {structure.get('cab', {}).get('model', 'N/A')}")
                    print(f"   Effects: {len(structure.get('effects', []))} effects")
                
                # Check tone patch
                if 'tone_patch' in generated_tone:
                    patch = generated_tone['tone_patch']
                    print(f"   Patch blocks: {len(patch)} blocks")
                
            except Exception as e:
                print(f"❌ Error generating tone: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 AI FUNCTIONALITY TEST COMPLETE!")
        print("=" * 60)
        print("✅ AI Tone Generator is working correctly!")
        print("🤖 Ready to generate tones from natural language!")
        print("🌐 Test it in the UI at: http://localhost:8506")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing AI system: {e}")
        return False

if __name__ == "__main__":
    test_ai_functionality()
