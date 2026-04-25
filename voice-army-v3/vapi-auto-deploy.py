#!/usr/bin/env python3
"""
GHOST ARMY v3.0 — AUTOMATED VAPI DEPLOYMENT
MJ's AI Voice Agent Auto-Deploy System
Created: 2026-04-26

WHAT THIS DOES:
1. Creates all 16 Vapi.ai assistants with v3.0 human-grade configs
2. Launches test calls to MJ's phone automatically
3. Retrieves transcripts and analyzes for AI-tells
4. Generates a report showing which agents pass/fail
5. Ready for MJ to approve → deploy to 562 leads

USAGE:
    export VAPI_API_KEY='your-key-here'
    python3 vapi-auto-deploy.py
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# ===================================================================
# CONFIGURATION
# ===================================================================

VAPI_API_KEY = os.environ.get('VAPI_API_KEY', '')
TEST_PHONE = '+13066308369'
WEBHOOK_URL = 'https://ag-automation.app.n8n.cloud/webhook/vapi-call-ended'
BASE_URL = 'https://api.vapi.ai'

# 16 Agent Definitions — v3.0 Anti-Bullshit Upgrade
AGENTS = [
    {
        "name": "Sarah",
        "squad": "Sarah Squad",
        "specialty": "HVAC",
        "voice_id": "Bella",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 25,
        "opening": "Hey [name], Sarah here — quick question, you lose calls when you're on a furnace job?"
    },
    {
        "name": "Riley",
        "squad": "Sarah Squad",
        "specialty": "HVAC",
        "voice_id": "Jessica",
        "speed": 1.10,
        "style": 0.55,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 25,
        "opening": "Hi [name], Riley from AG — when your phone rings and you can't answer, where do those calls go?"
    },
    {
        "name": "Jordan",
        "squad": "Sarah Squad",
        "specialty": "HVAC",
        "voice_id": "Josh",
        "speed": 1.20,
        "style": 0.65,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 25,
        "opening": "Jordan, AG Automation — data question: how many emergency calls do you miss per week?"
    },
    {
        "name": "Morgan",
        "squad": "Sarah Squad",
        "specialty": "HVAC",
        "voice_id": "Laura",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 25,
        "opening": "Hey [name]! Morgan from AG — real talk, does your website actually book jobs or just sit there?"
    },
    {
        "name": "Mike",
        "squad": "Mike Squad",
        "specialty": "Plumbing",
        "voice_id": "Josh",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 24,
        "opening": "Mike, AG Automation — when you're under a sink and the phone rings, who answers?"
    },
    {
        "name": "Danny",
        "squad": "Mike Squad",
        "specialty": "Plumbing",
        "voice_id": "Josh",
        "speed": 1.20,
        "style": 0.65,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 24,
        "opening": "Danny here — quick one: how many calls go to voicemail while you're on a job?"
    },
    {
        "name": "Frank",
        "squad": "Mike Squad",
        "specialty": "Plumbing",
        "voice_id": "Josh",
        "speed": 1.10,
        "style": 0.55,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 24,
        "opening": "Frank, AG Automation Calgary. You miss calls during the day, right?"
    },
    {
        "name": "Terry",
        "squad": "Mike Squad",
        "specialty": "Plumbing",
        "voice_id": "Josh",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 25,
        "opening": "Terry — hey, do you ever wonder how many jobs you lost to voicemail this month?"
    },
    {
        "name": "Emma",
        "squad": "Emma Squad",
        "specialty": "Electrical",
        "voice_id": "Bella",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 22,
        "opening": "Emma, AG Automation — when you're on a panel and the phone rings, what happens?"
    },
    {
        "name": "Chloe",
        "squad": "Emma Squad",
        "specialty": "Electrical",
        "voice_id": "Bella",
        "speed": 1.10,
        "style": 0.55,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 22,
        "opening": "Chloe here — when a customer calls after hours, do they get you or voicemail?"
    },
    {
        "name": "Alex",
        "squad": "Emma Squad",
        "specialty": "Electrical",
        "voice_id": "Josh",
        "speed": 1.20,
        "style": 0.65,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 22,
        "opening": "Alex, AG — straight question: how many leads do you lose to missed calls?"
    },
    {
        "name": "Sam",
        "squad": "Emma Squad",
        "specialty": "Electrical",
        "voice_id": "Bella",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 22,
        "opening": "Sam from AG — do you have a system that books jobs while you're working?"
    },
    {
        "name": "David",
        "squad": "David Squad",
        "specialty": "General",
        "voice_id": "Josh",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 45,
        "opening": "David, AG Automation — how do you handle calls when your whole crew is on a job?"
    },
    {
        "name": "Chris",
        "squad": "David Squad",
        "specialty": "General",
        "voice_id": "Josh",
        "speed": 1.20,
        "style": 0.65,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 45,
        "opening": "Chris here — do you ever think about how much business you lose to voicemail?"
    },
    {
        "name": "Pat",
        "squad": "David Squad",
        "specialty": "General",
        "voice_id": "Bella",
        "speed": 1.15,
        "style": 0.60,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 45,
        "opening": "Pat, AG — when customers call after 5 PM, do they book with you or someone else?"
    },
    {
        "name": "Taylor",
        "squad": "David Squad",
        "specialty": "General",
        "voice_id": "Josh",
        "speed": 1.10,
        "style": 0.55,
        "stability": 0.30,
        "similarity": 0.80,
        "leads": 44,
        "opening": "Taylor, AG Automation — what's your system for after-hours calls?"
    }
]

# Anti-AI system prompt template
SYSTEM_PROMPT_TEMPLATE = """You are {name}, a {specialty} industry specialist from AG Automation in Calgary. You talk fast, direct, no-bullshit.

CRITICAL RULES — NEVER BREAK:
1. NEVER say "I understand", "I'm here to help", "As an AI", "Let me assist you", "I appreciate your time"
2. Use contractions: "I'm", "don't", "can't", "gonna", "wanna", "ya"
3. Keep EVERY response under 15 seconds. 1-2 sentences MAX.
4. Natural filler: "um", "hmm", "yeah", "so", "listen", "real talk"
5. If they say "not interested" → "Fair enough. Have a good one." HANG UP.
6. Sound like you're between jobs — walking to your truck.
7. Get to the POINT in the first 5 words.
8. INTERRUPT yourself: "Actually — no wait, let me say it simpler"
9. DON'T be too polite. You're busy too.
10. If they're rude → match their energy. Short. Direct. Move on.

OPENING LINE:
"{opening}"

NO "How are you today?" NO "Hope I'm not bothering you." Just HEY → QUESTION → DONE.

VALUE PITCH (if they engage):
"We set up a system that answers your missed calls, books appointments, texts you the details. You never lose another emergency call. Takes 15 minutes to see it."

CLOSE:
"Wanna see it? MJ's free Thursday at 4 or Friday at 10. Which works?"

OBJECTIONS:
- "Too expensive" → "One emergency call you miss costs you $350. System pays for itself in one job."
- "I have a website" → "Does it book jobs at 2 AM when someone's {specialty_lower} dies?"
- "Too busy" → "That's why you need this. It handles the calls you can't get to."
- "Send info" → "What's your email? I'll shoot you a 2-minute video."
- "Call back later" → "What time works? I'll call then."
"""

# AI-tell patterns to detect
AI_TELLS = [
    "I understand",
    "I'm here to help",
    "As an AI",
    "Let me assist you",
    "I appreciate your time",
    "How may I assist you",
    "Thank you for your time",
    "I hope this helps",
    "Is there anything else",
    "I'm an AI assistant",
    "virtual assistant",
    "artificial intelligence"
]

# ===================================================================
# FUNCTIONS
# ===================================================================

def print_banner():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  GHOST ARMY v3.0 — AUTOMATED VAPI DEPLOYMENT               ║")
    print("║  Creating 16 agents • Testing • Analyzing • Deploying      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

def check_api_key():
    if not VAPI_API_KEY:
        print("❌ ERROR: VAPI_API_KEY not set!")
        print("   export VAPI_API_KEY='your-key-here'")
        print()
        print("   Get your key from: https://dashboard.vapi.ai → Profile → API Keys")
        sys.exit(1)
    print(f"✅ API Key found: {VAPI_API_KEY[:10]}...")
    print()

def create_assistant(agent):
    """Create a single Vapi assistant"""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build system prompt with agent-specific details
    specialty_lower = agent['specialty'].lower()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        name=agent['name'],
        specialty=agent['specialty'],
        specialty_lower=specialty_lower,
        opening=agent['opening']
    )
    
    payload = {
        "name": f"{agent['name']} v3.0 — {agent['specialty']} Specialist",
        "voice": {
            "provider": "11labs",
            "voiceId": agent['voice_id'],
            "model": "eleven_turbo_v2_5",
            "settings": {
                "stability": agent['stability'],
                "similarityBoost": agent['similarity'],
                "style": agent['style'],
                "speed": agent['speed'],
                "speakerBoost": True
            }
        },
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "maxTokens": 75,
            "temperature": 0.8
        },
        "firstMessage": agent['opening'].replace("[name]", "there"),
        "systemPrompt": system_prompt,
        "endCallPhrases": ["bye", "thanks", "talk later", "not interested", "take me off your list", "stop calling"],
        "recordingEnabled": True,
        "silenceTimeoutSeconds": 10,
        "responseDelaySeconds": 0.5,
        "maxDurationSeconds": 180,
        "backgroundSound": "office-ambience",
        "webhook": WEBHOOK_URL
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/assistant",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            assistant_id = data.get('id', 'unknown')
            print(f"    ✅ Created — ID: {assistant_id[:20]}...")
            return {"success": True, "id": assistant_id, "name": agent['name']}
        else:
            print(f"    ❌ FAILED — HTTP {response.status_code}")
            print(f"       Error: {response.text[:100]}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:100]}")
        return {"success": False, "error": str(e)}

def launch_test_call(assistant_id, agent_name):
    """Launch a test call to MJ's phone"""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "assistantId": assistant_id,
        "phoneNumber": {
            "number": TEST_PHONE
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/call",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            call_id = data.get('id', 'unknown')
            print(f"    ✅ Call launched — ID: {call_id[:20]}...")
            return {"success": True, "id": call_id, "name": agent_name}
        else:
            print(f"    ❌ Call failed — HTTP {response.status_code}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:100]}")
        return {"success": False, "error": str(e)}

def get_call_transcript(call_id):
    """Retrieve call transcript from Vapi"""
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/call/{call_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception as e:
        return None

def analyze_transcript(transcript_text, agent_name):
    """Analyze transcript for AI-tells"""
    if not transcript_text:
        return {"ai_tells": 0, "word_count": 0, "status": "NO_TRANSCRIPT"}
    
    text_lower = transcript_text.lower()
    ai_tells_found = 0
    
    for tell in AI_TELLS:
        if tell.lower() in text_lower:
            ai_tells_found += 1
    
    word_count = len(transcript_text.split())
    
    # Flag if too long (humans don't ramble on cold calls)
    if word_count > 150:
        ai_tells_found += 1
    
    status = "PASS" if ai_tells_found == 0 else "NEEDS_FIX"
    
    return {
        "ai_tells": ai_tells_found,
        "word_count": word_count,
        "status": status
    }

def generate_report(results):
    """Generate final test report"""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  GHOST ARMY v3.0 — TEST REPORT                             ║")
    print(f"║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    created = sum(1 for r in results if r.get('created'))
    calls = sum(1 for r in results if r.get('call_launched'))
    
    print(f"📊 AGENTS CREATED: {created}/16")
    print(f"📞 TEST CALLS LAUNCHED: {calls}/16")
    print()
    
    print("🤖 AGENT STATUS:")
    for r in results:
        name = r['name']
        if r.get('analysis'):
            status = r['analysis']['status']
            ai_tells = r['analysis']['ai_tells']
            words = r['analysis']['word_count']
            
            if status == "PASS":
                icon = "✅"
            elif status == "NO_TRANSCRIPT":
                icon = "⏳"
            else:
                icon = "⚠️"
            
            print(f"   {icon} {name:8s} — {status} ({ai_tells} AI-tells, {words} words)")
        else:
            print(f"   ❓ {name:8s} — No analysis yet")
    
    print()
    print("🎧 MJ'S MANUAL LISTENING REQUIRED:")
    print("   You need to answer the calls and score each agent 1-10 on:")
    print("   • Speed (1=slow, 10=perfect)")
    print("   • Naturalness (1=robot, 10=human)")
    print("   • Smartness (1=dumb, 10=sharp)")
    print("   • Overall (1=garbage, 10=deploy)")
    print()
    print("   Text me your scores and I'll fix any under 7/10.")
    print()

def main():
    print_banner()
    check_api_key()
    
    results = []
    
    # ===================================================================
    # STEP 1: Create all 16 assistants
    # ===================================================================
    print("📋 STEP 1/5: Creating 16 AI Voice Agents...")
    print()
    
    for agent in AGENTS:
        print(f"  🤖 Creating {agent['name']} ({agent['squad']} — {agent['specialty']})...")
        
        result = create_assistant(agent)
        result['name'] = agent['name']
        result['squad'] = agent['squad']
        result['specialty'] = agent['specialty']
        result['leads'] = agent['leads']
        
        if result['success']:
            result['created'] = True
        else:
            result['created'] = False
        
        results.append(result)
        time.sleep(0.5)  # Rate limiting
    
    created_count = sum(1 for r in results if r.get('created'))
    print()
    print(f"📊 STEP 1 COMPLETE: {created_count}/16 agents created")
    print()
    
    # ===================================================================
    # STEP 2: Launch test calls
    # ===================================================================
    if created_count > 0:
        print("📞 STEP 2/5: Launching test calls to your phone...")
        print(f"   Target: {TEST_PHONE}")
        print("   ⚠️  MJ — answer your phone! 16 calls coming in...")
        print()
        
        for r in results:
            if r.get('created'):
                print(f"  📲 Calling from {r['name']} → {TEST_PHONE}...")
                call_result = launch_test_call(r['id'], r['name'])
                
                if call_result['success']:
                    r['call_id'] = call_result['id']
                    r['call_launched'] = True
                else:
                    r['call_launched'] = False
                
                time.sleep(1)
        
        calls_count = sum(1 for r in results if r.get('call_launched'))
        print()
        print(f"📊 STEP 2 COMPLETE: {calls_count}/16 test calls launched")
        print()
    
    # ===================================================================
    # STEP 3: Wait for calls to complete
    # ===================================================================
    print("⏳ STEP 3/5: Waiting 3 minutes for calls to complete...")
    print("   (Answer your phone now!)")
    
    for i in range(18):
        time.sleep(10)
        print(f"   ... {i+1}/18 ({(i+1)*10} seconds)")
    
    print()
    print("📊 STEP 3 COMPLETE: Calls should be done")
    print()
    
    # ===================================================================
    # STEP 4: Retrieve and analyze transcripts
    # ===================================================================
    print("🔍 STEP 4/5: Analyzing call transcripts...")
    print()
    
    for r in results:
        if r.get('call_launched') and r.get('call_id'):
            print(f"  📄 {r['name']} — retrieving transcript...")
            
            transcript_data = get_call_transcript(r['call_id'])
            
            if transcript_data:
                # Extract transcript text
                transcript_text = ""
                if 'transcript' in transcript_data:
                    transcript_text = transcript_data['transcript']
                elif 'messages' in transcript_data:
                    for msg in transcript_data['messages']:
                        if msg.get('role') == 'assistant':
                            transcript_text += msg.get('content', '') + " "
                
                analysis = analyze_transcript(transcript_text, r['name'])
                r['analysis'] = analysis
                
                if analysis['status'] == "PASS":
                    print(f"    ✅ NO AI-tells — sounds human!")
                elif analysis['status'] == "NO_TRANSCRIPT":
                    print(f"    ⏳ Transcript not ready yet")
                else:
                    print(f"    ⚠️  {analysis['ai_tells']} AI-tells detected — needs tuning")
            else:
                r['analysis'] = {"ai_tells": 0, "word_count": 0, "status": "NO_TRANSCRIPT"}
                print(f"    ⏳ Transcript not available yet")
        
        time.sleep(0.5)
    
    print()
    print("📊 STEP 4 COMPLETE: Transcript analysis done")
    print()
    
    # ===================================================================
    # STEP 5: Generate report
    # ===================================================================
    generate_report(results)
    
    # Save results to file
    with open('/tmp/vapi-deployment-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📁 Results saved to: /tmp/vapi-deployment-results.json")
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  AUTOMATION COMPLETE                                       ║")
    print("║  Next: MJ listens to calls → Scores → I fix → Deploy     ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

if __name__ == "__main__":
    main()
