#!/usr/bin/env python3
"""
GHOST ARMY v4.0 — NORTH AMERICAN UPGRADE
Auto-deploy with MJ's latest feedback:
- Canadian/American accent
- "Hey this is [name], do you got a minute to chat"
- 3-service pitch (calls + SMS + email)
- Chloe settings (speed 1.10, style 0.55) as baseline
"""

import os, json, requests, time

VAPI_KEY = os.environ.get('VAPI_API_KEY', '')
PHONE_ID = 'ed889b06-010e-4d86-9f70-d1fd50dcb2fb'
BASE = 'https://api.vapi.ai'

# Only use voices that sound North American
VOICES = {
    "Bella": "XB0fDUnXU5powFXDhCwa",    # Female, North American
    "Josh": "TxGEqnHWrfWFTfGW9XjX",     # Male, North American
    "Rachel": "21m00Tcm4TlvDq8ikWAM",   # Female, American
    "Adam": "pNInz6obpgDQGcFmaJgB"      # Male, American
}

AGENTS = [
    {"name": "Sarah", "voice": "Bella", "industry": "HVAC", "leads": 25},
    {"name": "Riley", "voice": "Rachel", "industry": "HVAC", "leads": 25},
    {"name": "Jordan", "voice": "Adam", "industry": "HVAC", "leads": 25},
    {"name": "Morgan", "voice": "Bella", "industry": "HVAC", "leads": 25},
    {"name": "Mike", "voice": "Josh", "industry": "Plumbing", "leads": 24},
    {"name": "Danny", "voice": "Adam", "industry": "Plumbing", "leads": 24},
    {"name": "Frank", "voice": "Josh", "industry": "Plumbing", "leads": 24},
    {"name": "Terry", "voice": "Josh", "industry": "Plumbing", "leads": 25},
    {"name": "Emma", "voice": "Bella", "industry": "Electrical", "leads": 22},
    {"name": "Chloe", "voice": "Rachel", "industry": "Electrical", "leads": 22},
    {"name": "Alex", "voice": "Adam", "industry": "Electrical", "leads": 22},
    {"name": "Sam", "voice": "Bella", "industry": "Electrical", "leads": 22},
    {"name": "David", "voice": "Josh", "industry": "General", "leads": 45},
    {"name": "Chris", "voice": "Adam", "industry": "General", "leads": 45},
    {"name": "Pat", "voice": "Josh", "industry": "General", "leads": 45},
    {"name": "Taylor", "voice": "Rachel", "industry": "General", "leads": 44},
]

SYSTEM_PROMPT = """You are {name}, a {industry} specialist. You sound like you're from Calgary or Montana — direct, busy, no time to waste.

CRITICAL — NEVER BREAK:
1. NEVER say "I understand", "I'm here to help", "As an AI", "Let me assist you"
2. Use contractions: "I'm", "don't", "can't", "gonna", "wanna", "ya", "got"
3. Keep responses under 15 seconds. 1-2 sentences MAX.
4. Natural filler: "um", "hmm", "yeah", "so", "listen", "right"
5. If "not interested" → "Fair enough. Have a good one." HANG UP.
6. Canadian/American accent — sound natural, not posh
7. Get to the POINT in first 5 words.
8. INTERRUPT yourself: "Actually — no wait"
9. DON'T be too polite. You're busy too.
10. If rude → match energy. Short. Direct. Move on.

OPENING:
"Hey this is {name}, do you got a minute to chat?"

PITCH (if they say yes):
"Cool. So we do three things: AI answers your calls 24/7, auto-SMS goes out with your demo links, and email sequences follow up. All while you're on the job. You never lose another lead."

CLOSE:
"Wanna see it? Takes 15 minutes. MJ's free Thursday at 4 or Friday at 10. Which works?"

OBJECTIONS:
- "Too expensive" → "One lost job pays for the whole year."
- "Already have a website" → "This isn't a website — it's a lead machine."
- "Too busy" → "That's exactly why you need this."
- "Send info" → "Yeah for sure — what's your email?"
- "Call back" → "What time works?"
"""

def create_agent(agent):
    headers = {"Authorization": f"Bearer {VAPI_KEY}", "Content-Type": "application/json"}
    voice_id = VOICES[agent['voice']]
    prompt = SYSTEM_PROMPT.format(name=agent['name'], industry=agent['industry'])
    
    payload = {
        "name": f"{agent['name']} v4.0 — {agent['industry']}",
        "voice": {
            "provider": "11labs", "voiceId": voice_id, "model": "eleven_turbo_v2_5",
            "stability": 0.30, "similarityBoost": 0.80, "style": 0.55, "speed": 1.10
        },
        "model": {
            "provider": "openai", "model": "gpt-4o-mini", "maxTokens": 75, "temperature": 0.8,
            "messages": [{"role": "system", "content": prompt}]
        },
        "firstMessage": f"Hey this is {agent['name']}, do you got a minute to chat?",
        "silenceTimeoutSeconds": 10, "backgroundDenoisingEnabled": True,
        "transcriber": {"provider": "deepgram", "model": "nova-3", "language": "en"}
    }
    
    resp = requests.post(f"{BASE}/assistant", headers=headers, json=payload, timeout=30)
    if resp.status_code in [200, 201]:
        return {"success": True, "id": resp.json()['id']}
    return {"success": False, "error": resp.text}

def launch_call(assistant_id, name):
    headers = {"Authorization": f"Bearer {VAPI_KEY}", "Content-Type": "application/json"}
    payload = {
        "assistantId": assistant_id,
        "phoneNumberId": PHONE_ID,
        "customer": {"number": "+13066308369"}
    }
    resp = requests.post(f"{BASE}/call/phone", headers=headers, json=payload, timeout=30)
    return resp.status_code in [200, 201]

if __name__ == "__main__":
    print("🔥 GHOST ARMY v4.0 — NORTH AMERICAN UPGRADE")
    print("=" * 50)
    
    results = []
    for agent in AGENTS:
        print(f"Creating {agent['name']}...", end=" ")
        r = create_agent(agent)
        if r['success']:
            print(f"✅ {r['id'][:20]}...")
            results.append({"name": agent['name'], "id": r['id'], "ok": True})
        else:
            print(f"❌ {r['error'][:80]}")
            results.append({"name": agent['name'], "ok": False})
        time.sleep(0.5)
    
    created = sum(1 for r in results if r['ok'])
    print(f"\n📊 {created}/16 agents created")
    
    # Save IDs
    with open('/tmp/vapi-v4-ids.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ v4.0 DEPLOYMENT COMPLETE")
    print("IDs saved to /tmp/vapi-v4-ids.json")
