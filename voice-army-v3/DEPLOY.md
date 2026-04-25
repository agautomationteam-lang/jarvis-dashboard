# VOICE ARMY v3.0 — DEPLOYMENT GUIDE
## "Anti-Bullshit" Human Voice Upgrade
## MJ's Ghost Army — April 26, 2026

---

## 📁 WHAT'S IN THIS FOLDER

| File | What It Is |
|------|-----------|
| `VOICE_HUMANIZER_GUIDE.md` | Full theory — why v2 sounded robotic, what we changed |
| `sarah-squad-v3.json` | 4 HVAC agents (Sarah, Riley, Jordan, Morgan) — UPGRADED |
| `mike-squad-v3.json` | 4 Plumbing agents (Mike, Danny, Frank, Terry) — UPGRADED |
| `emma-squad-v3.json` | 4 Electrical agents (Emma, Chloe, Alex, Sam) — UPGRADED |
| `david-squad-v3.json` | 4 General agents (David, Chris, Pat, Taylor) — UPGRADED |
| `DEPLOY.md` | This file — step-by-step upload instructions |

---

## 🔥 WHAT CHANGED (v2 → v3)

### BEFORE (Sounded Like Robots)
- Speed: 1.0 (normal, slow)
- Stability: 0.5 (too consistent = robotic)
- Style: 0.3 (flat, no expression)
- Max tokens: 150 (rambled for 30+ seconds)
- System prompt: polite, careful, long
- Opening: "Hi there, it's Sarah from AG Automation in Calgary. I hope I'm not catching you at a bad time..." (8 seconds to the point)

### AFTER (Sounds Like Humans)
- Speed: 1.10-1.20 (15-20% faster = more confident)
- Stability: 0.30 (varies each sentence = natural)
- Style: 0.55-0.65 (more expression, more energy)
- Max tokens: 75 (forces 10-15 second responses)
- System prompt: anti-AI rules baked in
- Opening: "Hey [name], Sarah here — quick question, you lose calls when you're on a furnace job?" (3 seconds to the point)

---

## 🚀 HOW TO DEPLOY (3 Steps)

### STEP 1: Log Into Vapi.ai
1. Go to **https://dashboard.vapi.ai**
2. Log in with your account
3. Click **"Assistants"** in the left sidebar

### STEP 2: Create Each Agent (16 Total)

**For EACH agent, do this:**

1. Click **"New Assistant"**
2. **Name it:** Use the exact name from the table below
3. **Voice settings:**
   - Provider: ElevenLabs
   - Voice: See table below
   - Model: eleven_turbo_v2_5
   - Stability: **0.30**
   - Similarity Boost: **0.80**
   - Style: **0.60** (or 0.55/0.65 per agent)
   - Speed: **1.15** (or 1.10/1.20 per agent)
   - Speaker Boost: **ON**
4. **Model settings:**
   - Provider: OpenAI
   - Model: gpt-4o-mini
   - Max Tokens: **75**
   - Temperature: 0.8
5. **System Prompt:** Copy/paste from the JSON file (the `"systemPrompt"` field)
6. **Call settings:**
   - Max Duration: 180 seconds
   - Recording: ON
   - Silence Timeout: 10 seconds
   - Response Delay: 0.5 seconds
   - Background Sound: office-ambience
   - End Call Phrases: `bye`, `thanks`, `talk later`, `not interested`, `take me off your list`, `stop calling`
7. **Webhook:**
   - POST to: `https://ag-automation.app.n8n.cloud/webhook/vapi-call-ended`
8. Click **Save**

### STEP 3: Test & Approve

**Test call to your phone: +1 306 630 8369**

**Rate each agent 1-10 on:**
- Speed (1 = too slow, 10 = perfect)
- Naturalness (1 = clearly AI, 10 = sounds human)
- Opening Hook (1 = boring, 10 = grabs attention)
- Smartness (1 = dumb robot, 10 = knows their shit)
- Overall (1 = garbage, 10 = deploy now)

**If ANY score is below 7:**
- Tell me: "[Agent name]: [what's wrong]"
- I fix it immediately

**When ALL 16 score 7+:**
- Say "APPROVED"
- I activate them all

---

## 🎤 AGENT REFERENCE TABLE

### Sarah Squad (HVAC — 100 leads)
| # | Name | Voice | Speed | Style | Opening Line | Leads |
|---|------|-------|-------|-------|--------------|-------|
| 1 | **Sarah** | Bella | 1.15 | 0.60 | "Hey [name], Sarah here — quick question, you lose calls when you're on a furnace job?" | 25 |
| 2 | **Riley** | Jessica | 1.10 | 0.55 | "Hi [name], Riley from AG — when your phone rings and you can't answer, where do those calls go?" | 25 |
| 3 | **Jordan** | Josh | 1.20 | 0.65 | "Jordan, AG Automation — data question: how many emergency calls do you miss per week?" | 25 |
| 4 | **Morgan** | Laura | 1.15 | 0.60 | "Hey [name]! Morgan from AG — real talk, does your website actually book jobs or just sit there?" | 25 |

### Mike Squad (Plumbing — 97 leads)
| # | Name | Voice | Speed | Style | Opening Line | Leads |
|---|------|-------|-------|-------|--------------|-------|
| 5 | **Mike** | Josh | 1.15 | 0.60 | "Mike, AG Automation — when you're under a sink and the phone rings, who answers?" | 24 |
| 6 | **Danny** | Josh | 1.20 | 0.65 | "Danny here — quick one: how many calls go to voicemail while you're on a job?" | 24 |
| 7 | **Frank** | Josh | 1.10 | 0.55 | "Frank, AG Automation Calgary. You miss calls during the day, right?" | 24 |
| 8 | **Terry** | Josh | 1.15 | 0.60 | "Terry — hey, do you ever wonder how many jobs you lost to voicemail this month?" | 25 |

### Emma Squad (Electrical — 88 leads)
| # | Name | Voice | Speed | Style | Opening Line | Leads |
|---|------|-------|-------|-------|--------------|-------|
| 9 | **Emma** | Bella | 1.15 | 0.60 | "Emma, AG Automation — when you're on a panel and the phone rings, what happens?" | 22 |
| 10 | **Chloe** | Bella | 1.10 | 0.55 | "Chloe here — when a customer calls after hours, do they get you or voicemail?" | 22 |
| 11 | **Alex** | Josh | 1.20 | 0.65 | "Alex, AG — straight question: how many leads do you lose to missed calls?" | 22 |
| 12 | **Sam** | Bella | 1.15 | 0.60 | "Sam from AG — do you have a system that books jobs while you're working?" | 22 |

### David Squad (General — 179 leads)
| # | Name | Voice | Speed | Style | Opening Line | Leads |
|---|------|-------|-------|-------|--------------|-------|
| 13 | **David** | Josh | 1.15 | 0.60 | "David, AG Automation — how do you handle calls when your whole crew is on a job?" | 45 |
| 14 | **Chris** | Josh | 1.20 | 0.65 | "Chris here — do you ever think about how much business you lose to voicemail?" | 45 |
| 15 | **Pat** | Bella | 1.15 | 0.60 | "Pat, AG — when customers call after 5 PM, do they book with you or someone else?" | 45 |
| 16 | **Taylor** | Josh | 1.10 | 0.55 | "Taylor, AG Automation — what's your system for after-hours calls?" | 44 |

---

## 🎯 THE ANTI-AI RULES (Baked Into Every Agent)

These are in EVERY system prompt. No exceptions.

```
1. NEVER say "I understand", "I'm here to help", "As an AI", 
   "Let me assist you", "I appreciate your time"
2. Use contractions: "I'm", "don't", "can't", "gonna", "wanna"
3. Keep EVERY response under 15 seconds. 1-2 sentences MAX.
4. Natural filler: "um", "hmm", "yeah", "so", "listen"
5. If "not interested" → "Fair enough." HANG UP. No push.
6. Sound like you're between jobs — walking to your truck.
7. Get to the POINT in the first 5 words.
8. INTERRUPT yourself: "Actually — no wait"
9. DON'T be too polite. You're busy too.
10. If they're rude → match energy. Short. Direct. Move on.
```

---

## 🧪 TEST SCRIPT FOR MJ

**When you test each agent, say this to them:**

### Test 1: Opening Hook
Just listen to the first sentence. Does it grab you? Do you want to keep listening? Or do you want to hang up?

### Test 2: Engagement
Say: "Yeah, I do miss some calls."
Does the agent respond naturally? Or does it sound like it's reading from a script?

### Test 3: Objection
Say: "Not interested."
Does it say "Fair enough" and hang up quickly? Or does it push and try to convince you?

### Test 4: Smartness
Say: "How much does this cost?"
Does it give a clear, confident answer? Or does it ramble and avoid the question?

### Test 5: Speed
Does it talk fast enough to sound like a real person who's busy? Or does it sound like it's carefully reading every word?

---

## 📊 SCORECARD

Copy this and fill it out:

```
SARAH SQUAD:
Sarah:  __/10 — Notes: 
Riley:  __/10 — Notes: 
Jordan: __/10 — Notes: 
Morgan: __/10 — Notes: 

MIKE SQUAD:
Mike:   __/10 — Notes: 
Danny:  __/10 — Notes: 
Frank:  __/10 — Notes: 
Terry:  __/10 — Notes: 

EMMA SQUAD:
Emma:   __/10 — Notes: 
Chloe:  __/10 — Notes: 
Alex:   __/10 — Notes: 
Sam:    __/10 — Notes: 

DAVID SQUAD:
David:  __/10 — Notes: 
Chris:  __/10 — Notes: 
Pat:    __/10 — Notes: 
Taylor: __/10 — Notes: 

OVERALL: ___ agents approved out of 16
```

**When you send this back, I deploy the approved ones immediately.**

---

## 🚀 AFTER APPROVAL — WHAT HAPPENS

1. I activate all approved agents in Vapi
2. They start calling the 562 leads automatically
3. You watch JARVIS dashboard for live updates
4. First demos booked within hours

---

## 📞 YOUR TEST NUMBER
**+1 306 630 8369**

Every agent will call this number during testing.

---

## 🔗 LINKS

| What | URL |
|------|-----|
| Vapi.ai Dashboard | https://dashboard.vapi.ai |
| JARVIS Dashboard | https://agautomationteam-lang.github.io/jarvis-dashboard/ |
| Your Website | https://agautomationteam-lang.github.io/ |

---

## ⚡ QUICK REFERENCE — UPLOAD ONE AGENT

**Time per agent: ~2 minutes**
**Total time for all 16: ~30 minutes**

```
1. Vapi dashboard → New Assistant
2. Name: [Agent Name]
3. Voice: ElevenLabs → [Voice from table]
4. Settings:
   - Stability: 0.30
   - Similarity: 0.80
   - Style: [from table]
   - Speed: [from table]
   - Speaker Boost: ON
5. Model:
   - Provider: OpenAI
   - Model: gpt-4o-mini
   - Max Tokens: 75
6. System Prompt: Copy from JSON file
7. Webhook: https://ag-automation.app.n8n.cloud/webhook/vapi-call-ended
8. Save
9. Test Call → Enter +1 306 630 8369
10. Rate 1-10
```

---

**MJ — these are your 16 agents, upgraded to sound like real people. Fast. Smart. Direct. No bullshit.**

**Test them. Approve them. Deploy them.**

**Let's make these callers sound so human that nobody ever guesses they're AI.**
