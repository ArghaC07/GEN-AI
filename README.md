🧍 User Enters Dialogflow Chatbot
⬇
🔍 User asked for PAN
⬇
✅ PAN Verified (Cloud Function: `pan1`)
⬇
🤔 Ask User: "What do you want to do?"
    → Options: [Create Policy, Update Policy, Track Claim, etc.]
⬇
👤 Call Cloud Function: `pan2`(User selects "Create Policy")
⬇
🎯 Ask for Policy Type (Life, Health, Car)
⬇
📥 Collect All Required Info Step-by-step
    → Age, Gender, Income, Health conditions, etc.
⬇
📤 Call Cloud Function: `pan2`
    → Includes: Underwriting Logic
⬇
🧠 Underwriting Outcome:
    ├─ ✅ Approved → proceed to Premium Calculation
    └─ ❌ Rejected → show reason, END
⬇
🧮 Call `premium_calculator` function
    → Takes approved policy details
    → Returns: ₹Premium
⬇
💬 Ask User:
    "Your calculated premium is ₹____ per year. Do you want to continue?"
⬇
🧍 User Decision:
    ├─ ❌ Decline → Policy not created, END
    └─ ✅ Accept → Insert policy in DB
⬇
🧾 Insert Policy into DB (`policies` table)
⬇
💳 Call `create_initial_payment_record`
    → Insert record in `payments` table
    → status: unpaid
⬇
💬 Ask: "Please complete your payment. Choose a mode (UPI, Card, NetBanking)"
⬇
💳 User selects payment method
⬇
✅ (Mock) Payment Success
⬇
🛠 Update `payments` table → mode = paid
    Update `policies` table → status = active
⬇
🎉 Final Response: "Your policy is now active! Thank you 🎉"
