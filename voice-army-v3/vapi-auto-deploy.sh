#!/bin/bash
# VAPI AUTOMATED DEPLOYMENT SCRIPT
# MJ's Ghost Army — v3.0 Human Upgrade
# Created: 2026-04-26
# Purpose: Create all 16 agents, test them, analyze, fix, deploy

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  GHOST ARMY v3.0 — AUTOMATED VAPI DEPLOYMENT               ║"
echo "║  Creating 16 agents • Testing • Analyzing • Deploying    ║"
echo "╚════════════════════════════════════════════════════════════╝"

# CONFIGURATION — MJ fills these in
VAPI_API_KEY="${VAPI_API_KEY:-YOUR_VAPI_KEY_HERE}"
ELEVENLABS_API_KEY="${ELEVENLABS_API_KEY:-OPTIONAL}"
TEST_PHONE="+13066308369"
WEBHOOK_URL="https://ag-automation.app.n8n.cloud/webhook/vapi-call-ended"

# Check if VAPI key is set
if [ "$VAPI_API_KEY" = "YOUR_VAPI_KEY_HERE" ]; then
    echo "❌ ERROR: Please set VAPI_API_KEY environment variable"
    echo "   export VAPI_API_KEY='your-key-here'"
    exit 1
fi

echo ""
echo "📋 STEP 1/6: Creating 16 AI Voice Agents..."
echo ""

# Agent definitions
# Format: NAME|VOICE_ID|SPEED|STYLE|STABILITY|SIMILARITY|SQUAD|SPECIALTY|LEADS|SYSTEM_PROMPT_FILE

declare -a AGENTS=(
    "Sarah|Bella|1.15|0.60|0.30|0.80|Sarah Squad|HVAC|25|sarah-01"
    "Riley|Jessica|1.10|0.55|0.30|0.80|Sarah Squad|HVAC|25|riley-02"
    "Jordan|Josh|1.20|0.65|0.30|0.80|Sarah Squad|HVAC|25|jordan-03"
    "Morgan|Laura|1.15|0.60|0.30|0.80|Sarah Squad|HVAC|25|morgan-04"
    "Mike|Josh|1.15|0.60|0.30|0.80|Mike Squad|Plumbing|24|mike-01"
    "Danny|Josh|1.20|0.65|0.30|0.80|Mike Squad|Plumbing|24|danny-02"
    "Frank|Josh|1.10|0.55|0.30|0.80|Mike Squad|Plumbing|24|frank-03"
    "Terry|Josh|1.15|0.60|0.30|0.80|Mike Squad|Plumbing|25|terry-04"
    "Emma|Bella|1.15|0.60|0.30|0.80|Emma Squad|Electrical|22|emma-01"
    "Chloe|Bella|1.10|0.55|0.30|0.80|Emma Squad|Electrical|22|chloe-02"
    "Alex|Josh|1.20|0.65|0.30|0.80|Emma Squad|Electrical|22|alex-03"
    "Sam|Bella|1.15|0.60|0.30|0.80|Emma Squad|Electrical|22|sam-04"
    "David|Josh|1.15|0.60|0.30|0.80|David Squad|General|45|david-01"
    "Chris|Josh|1.20|0.65|0.30|0.80|David Squad|General|45|chris-02"
    "Pat|Bella|1.15|0.60|0.30|0.80|David Squad|General|45|pat-03"
    "Taylor|Josh|1.10|0.55|0.30|0.80|David Squad|General|44|taylor-04"
)

# Counter
CREATED=0
FAILED=0

# Create each agent
for agent in "${AGENTS[@]}"; do
    IFS='|' read -r NAME VOICE SPEED STYLE STABILITY SIMILARITY SQUAD SPECIALTY LEADS ID <<< "$agent"
    
    echo "  🤖 Creating $NAME ($SQUAD — $SPECIALTY)..."
    
    # Build the API payload
    cat > "/tmp/vapi-payload-${NAME,,}.json" <<EOF
{
  "name": "${NAME} v3.0 — ${SPECIALTY} Specialist",
  "voice": {
    "provider": "11labs",
    "voiceId": "${VOICE}",
    "model": "eleven_turbo_v2_5",
    "settings": {
      "stability": ${STABILITY},
      "similarityBoost": ${SIMILARITY},
      "style": ${STYLE},
      "speed": ${SPEED},
      "speakerBoost": true
    }
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "maxTokens": 75,
    "temperature": 0.8
  },
  "firstMessage": "Hey there, quick question — do you lose calls when you're on a job?",
  "endCallPhrases": ["bye", "thanks", "talk later", "not interested", "take me off your list", "stop calling"],
  "recordingEnabled": true,
  "silenceTimeoutSeconds": 10,
  "responseDelaySeconds": 0.5,
  "maxDurationSeconds": 180,
  "backgroundSound": "office-ambience",
  "webhook": "${WEBHOOK_URL}"
}
EOF
    
    # Call Vapi API to create assistant
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Authorization: Bearer ${VAPI_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "@/tmp/vapi-payload-${NAME,,}.json" \
        "https://api.vapi.ai/assistant" 2>/dev/null)
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
        ASSISTANT_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
        echo "    ✅ Created — ID: ${ASSISTANT_ID:0:20}..."
        echo "${NAME}|${ASSISTANT_ID}|${SQUAD}|${SPECIALTY}|${LEADS}" >> /tmp/vapi-agent-registry.txt
        ((CREATED++))
    else
        echo "    ❌ FAILED — HTTP ${HTTP_CODE}"
        echo "       Error: ${BODY:0:100}"
        ((FAILED++))
    fi
    
    # Small delay to avoid rate limiting
    sleep 0.5
done

echo ""
echo "📊 STEP 1 COMPLETE: ${CREATED} created, ${FAILED} failed"
echo ""

# ===================================================================
# STEP 2: Launch Test Calls
# ===================================================================

if [ $CREATED -gt 0 ]; then
    echo "📞 STEP 2/6: Launching test calls to ${TEST_PHONE}..."
    echo ""
    
    CALL_COUNT=0
    while IFS='|' read -r NAME ASSISTANT_ID SQUAD SPECIALTY LEADS; do
        echo "  📲 Calling from $NAME → ${TEST_PHONE}..."
        
        cat > "/tmp/vapi-call-${NAME,,}.json" <<EOF
{
  "assistantId": "${ASSISTANT_ID}",
  "phoneNumber": {
    "number": "${TEST_PHONE}"
  }
}
EOF
        
        # Initiate call
        CALL_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Authorization: Bearer ${VAPI_API_KEY}" \
            -H "Content-Type: application/json" \
            -d "@/tmp/vapi-call-${NAME,,}.json" \
            "https://api.vapi.ai/call" 2>/dev/null)
        
        CALL_HTTP=$(echo "$CALL_RESPONSE" | tail -n1)
        CALL_BODY=$(echo "$CALL_RESPONSE" | sed '$d')
        
        if [ "$CALL_HTTP" = "200" ] || [ "$CALL_HTTP" = "201" ]; then
            CALL_ID=$(echo "$CALL_BODY" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
            echo "    ✅ Call initiated — ID: ${CALL_ID:0:20}..."
            echo "${NAME}|${ASSISTANT_ID}|${CALL_ID}" >> /tmp/vapi-call-log.txt
            ((CALL_COUNT++))
        else
            echo "    ❌ Call failed — HTTP ${CALL_HTTP}"
        fi
        
        sleep 1
    done < /tmp/vapi-agent-registry.txt
    
    echo ""
    echo "📊 STEP 2 COMPLETE: ${CALL_COUNT} test calls launched"
    echo ""
fi

# ===================================================================
# STEP 3: Wait for calls to complete & retrieve transcripts
# ===================================================================

echo "⏳ STEP 3/6: Waiting 5 minutes for calls to complete..."
echo "   (MJ — answer your phone! The calls are coming in now)"
sleep 300

echo ""
echo "📊 STEP 3 COMPLETE: Calls should be done"
echo ""

# ===================================================================
# STEP 4: Analyze transcripts for AI-tells
# ===================================================================

echo "🔍 STEP 4/6: Analyzing call transcripts for AI-tells..."
echo ""

if [ -f /tmp/vapi-call-log.txt ]; then
    while IFS='|' read -r NAME ASSISTANT_ID CALL_ID; do
        echo "  📄 Analyzing $NAME's call..."
        
        # Get transcript
        TRANSCRIPT=$(curl -s -X GET \
            -H "Authorization: Bearer ${VAPI_API_KEY}" \
            "https://api.vapi.ai/call/${CALL_ID}" 2>/dev/null)
        
        # Check for AI-tells
        AI_TELLS=0
        
        if echo "$TRANSCRIPT" | grep -qi "I understand"; then ((AI_TELLS++)); fi
        if echo "$TRANSCRIPT" | grep -qi "I'm here to help"; then ((AI_TELLS++)); fi
        if echo "$TRANSCRIPT" | grep -qi "As an AI"; then ((AI_TELLS++)); fi
        if echo "$TRANSCRIPT" | grep -qi "Let me assist you"; then ((AI_TELLS++)); fi
        if echo "$TRANSCRIPT" | grep -qi "I appreciate your time"; then ((AI_TELLS++)); fi
        
        # Check response lengths
        WORD_COUNT=$(echo "$TRANSCRIPT" | wc -w)
        if [ "$WORD_COUNT" -gt 100 ]; then ((AI_TELLS++)); fi
        
        if [ $AI_TELLS -eq 0 ]; then
            echo "    ✅ NO AI-tells detected — sounds human!"
        else
            echo "    ⚠️  ${AI_TELLS} AI-tells detected — needs fixing"
            echo "       (Long responses or robotic phrases found)"
        fi
        
        echo "${NAME}|${AI_TELLS}|${WORD_COUNT}" >> /tmp/vapi-analysis.txt
    done < /tmp/vapi-call-log.txt
fi

echo ""
echo "📊 STEP 4 COMPLETE: Transcript analysis done"
echo ""

# ===================================================================
# STEP 5: Generate Report for MJ
# ===================================================================

echo "📋 STEP 5/6: Generating test report..."
echo ""

cat > /tmp/vapi-test-report.txt <<EOF
╔════════════════════════════════════════════════════════════╗
║  GHOST ARMY v3.0 — TEST REPORT                             ║
║  Generated: $(date)                                        ║
╚════════════════════════════════════════════════════════════╝

AGENTS CREATED: ${CREATED}/16
CALLS LAUNCHED: ${CALL_COUNT}/16

TRANSCRIPT ANALYSIS:
EOF

if [ -f /tmp/vapi-analysis.txt ]; then
    while IFS='|' read -r NAME AI_TELLS WORD_COUNT; do
        STATUS="✅ PASS"
        if [ "$AI_TELLS" -gt 0 ]; then STATUS="⚠️ NEEDS FIX"; fi
        echo "  ${NAME}: ${STATUS} (${AI_TELLS} AI-tells, ${WORD_COUNT} words)" >> /tmp/vapi-test-report.txt
    done < /tmp/vapi-analysis.txt
fi

cat >> /tmp/vapi-test-report.txt <<EOF

🎧 MJ'S MANUAL LISTENING REQUIRED:
You need to answer the calls and score each agent 1-10 on:
- Speed (1=slow, 10=perfect)
- Naturalness (1=robot, 10=human)
- Smartness (1=dumb, 10=sharp)
- Overall (1=garbage, 10=deploy)

Text me your scores and I'll fix any under 7/10.

EOF

cat /tmp/vapi-test-report.txt

echo ""
echo "📊 STEP 5 COMPLETE: Report generated"
echo ""

# ===================================================================
# STEP 6: Deploy approved agents (manual approval required)
# ===================================================================

echo "🚀 STEP 6/6: READY TO DEPLOY"
echo ""
echo "Once MJ approves all 16 agents, run:"
echo "  ./deploy-approved-agents.sh"
echo ""
echo "This will:"
echo "  • Activate all 16 agents for live calling"
echo "  • Upload 562 leads to Vapi"
echo "  • Start the campaign"
echo "  • Begin calling Calgary trade businesses"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  AUTOMATION COMPLETE                                       ║"
echo "║  Next: MJ answers calls → Scores agents → I fix → Deploy ║"
echo "╚════════════════════════════════════════════════════════════╝"
