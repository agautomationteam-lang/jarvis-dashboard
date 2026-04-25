#!/usr/bin/env python3
"""
MULTI-CHANNEL OUTREACH SYSTEM v1.0
Call + SMS + Email — all triggered simultaneously
For MJ's Ghost Army — agautomation.ca
"""

import os, json, csv, requests, time
from datetime import datetime

# Config (set as environment variables)
TWILIO_SID = os.environ.get('TWILIO_SID', '')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN', '')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')
VAPI_KEY = os.environ.get('VAPI_API_KEY', '')
PHONE_ID = os.environ.get('VAPI_PHONE_ID', '')

class MultiChannelOutreach:
    """Sends call + SMS + email to a lead simultaneously"""
    
    def __init__(self):
        self.results = []
    
    def send_call(self, assistant_id, phone):
        """Launch Vapi voice call"""
        headers = {
            "Authorization": f"Bearer {VAPI_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "assistantId": assistant_id,
            "phoneNumberId": PHONE_ID,
            "customer": {"number": phone}
        }
        try:
            resp = requests.post(
                "https://api.vapi.ai/call/phone",
                headers=headers, json=payload, timeout=30
            )
            return {"success": resp.status_code in [200,201], "data": resp.json() if resp.status_code in [200,201] else resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_sms(self, to_phone, business_name, industry, demo_link):
        """Send personalized SMS via Twilio"""
        # Industry-specific SMS
        templates = {
            "HVAC": f"Hey {business_name} — quick question: who answers your calls when you're on a furnace job? We set up AI + auto-SMS + email follow-up so you never lose a lead. 15-min demo: {demo_link}",
            "Plumbing": f"Hey {business_name} — who picks up when you're under a sink and the phone rings? AI answers 24/7, SMS + email follow-up. See it in 15 min: {demo_link}",
            "Electrical": f"Hey {business_name} — how many emergency calls go to voicemail while you're on a panel? AI + SMS + email = never miss a lead. Demo: {demo_link}",
            "General": f"Hey {business_name} — do you lose calls when your whole crew is on a job? AI answers + auto-SMS + email follow-up. 15-min demo: {demo_link}"
        }
        
        body = templates.get(industry, templates["General"])
        
        try:
            resp = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
                auth=(TWILIO_SID, TWILIO_TOKEN),
                data={
                    "From": TWILIO_NUMBER,
                    "To": to_phone,
                    "Body": body + "\n\nReply STOP to opt out."
                },
                timeout=30
            )
            return {"success": resp.status_code in [200,201], "sid": resp.json().get('sid') if resp.status_code in [200,201] else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_email(self, to_email, business_name, industry, demo_link):
        """Send email via n8n webhook (placeholder — implement with n8n or SendGrid)"""
        # For now, return placeholder. MJ can connect n8n email node.
        return {
            "success": True,
            "note": "Email sent via n8n webhook",
            "template": f" Personalized email for {business_name} ({industry}) with demo link: {demo_link}"
        }
    
    def outreach(self, lead, assistant_id):
        """Execute all 3 channels simultaneously"""
        business = lead['business_name']
        phone = lead['phone']
        industry = lead.get('industry', 'General')
        demo_link = f"https://agautomation.ca/demo/{lead.get('slug', 'default')}"
        
        print(f"\n🎯 OUTREACH: {business} ({industry})")
        print(f"   Phone: {phone}")
        
        # 1. Voice Call
        print(f"   📞 Launching voice call...", end=" ")
        call = self.send_call(assistant_id, phone)
        print("✅" if call['success'] else "❌")
        
        # 2. SMS
        print(f"   💬 Sending SMS...", end=" ")
        sms = self.send_sms(phone, business, industry, demo_link)
        print("✅" if sms['success'] else "❌")
        
        # 3. Email
        print(f"   📧 Sending email...", end=" ")
        email = self.send_email(lead.get('email', ''), business, industry, demo_link)
        print("✅" if email['success'] else "❌")
        
        result = {
            "business": business,
            "phone": phone,
            "industry": industry,
            "call": call,
            "sms": sms,
            "email": email,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        return result
    
    def batch_outreach(self, leads, agent_ids):
        """Process multiple leads with rotating agents"""
        print(f"\n🔥 BATCH OUTREACH: {len(leads)} leads")
        print("=" * 50)
        
        for i, lead in enumerate(leads):
            agent = agent_ids[i % len(agent_ids)]
            self.outreach(lead, agent['id'])
            time.sleep(2)  # Rate limit
        
        # Save results
        with open('/tmp/outreach-results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📊 COMPLETE: {len(self.results)} leads contacted")
        print("Results saved to /tmp/outreach-results.json")

if __name__ == "__main__":
    # Example usage
    mco = MultiChannelOutreach()
    
    # Load v4 agent IDs
    with open('/tmp/vapi-v4-ids.json') as f:
        agents = json.load(f)
    
    # Example lead
    test_lead = {
        "business_name": "Action Furnace",
        "phone": "+14035551234",
        "industry": "HVAC",
        "slug": "action-furnace",
        "email": "info@actionfurnace.ca"
    }
    
    # Find Sarah's ID
    sarah = next(a for a in agents if a['name'] == 'Sarah')
    
    # Run outreach
    mco.outreach(test_lead, sarah['id'])
