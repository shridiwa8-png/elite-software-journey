import streamlit as st
import os
import re
import time
from google import genai

# Default key (fallback server key)
DEFAULT_API_KEY = "AQ.Ab8RN6KAbsVtlRrinFIt9JWcqSdahq8XyENzUD_9wGQQ-GzfVQ"

# Inject default key securely into environment as fallback
os.environ["GEMINI_API_KEY"] = DEFAULT_API_KEY

def generate_simulated_blueprint(role, skill, tools, problem):
    """
    Generates a highly contextual, dynamic blueprint programmatically.
    Dissects user tools and problems dynamically to prevent tool-mismatch bugs.
    """
    prob_lower = problem.lower()
    tools_list = [t.strip() for t in re.split(r'[,,;,|]', tools)] if tools else []
    
    # Clean tool names or fallbacks
    primary_tool = tools_list[0].title() if (tools_list and tools_list[0]) else "Simple Tracker"
    secondary_tool = tools_list[1].title() if len(tools_list) > 1 else "Digital Document"
    
    # Classification rules
    is_comm = any(k in prob_lower or any(k in t.lower() for t in tools_list) for k in ["whatsapp", "wa", "email", "gmail", "chat", "message", "lead", "client"])
    is_data = any(k in prob_lower or any(k in t.lower() for t in tools_list) for k in ["excel", "sheet", "csv", "data", "table", "finance", "number"])
    is_notion = any(k in prob_lower or any(k in t.lower() for t in tools_list) for k in ["notion", "clutter", "complex", "system", "workspace", "obsidian", "docs"])
    
    if is_comm:
        domain_title = f"Simple {primary_tool} Reply List"
        bottlenecks = [
            f"Scatter Communication Trap: Client requests get mixed up in different channels in {primary_tool}, leading to delayed response times.",
            "Lack of Status Visibility: No clear tracking of where clients currently stand (e.g., Waiting on Quote, Work In Progress, Paid)."
        ]
        recommended_system = f"A simple list of copy-paste response templates inside {primary_tool} so you can reply in seconds."
        central_hub = f"{primary_tool} + a single plain-text follow-up log"
        
        # Skill-based automation mapping
        if skill == "Beginner":
            automation_upgrade = "None recommended. Use manual status labels to keep setup friction at absolute zero."
            actions = [
                f"Program shortcuts inside {primary_tool}: Create 3 quick-text response templates (e.g., Intro, Pricing, Follow-Up) to reply to clients in 10 seconds.",
                "Dedicate a batch response block: Only check and reply to inbound client inquiries twice a day to protect your deep-work hours.",
                "Build a simple spreadsheet log to map out client statuses in real-time."
            ]
        else:
            automation_upgrade = f"Zapier or Make.com rules to automatically log incoming messages from {primary_tool} into your database."
            actions = [
                f"Configure Webhook integrations inside {primary_tool} to flag high-value client tags.",
                "Automate instant notifications to your central tracker when a client fills out an intake form.",
                "Establish automated trigger replies for after-hours client communications."
            ]
            
        asset_title = f"{primary_tool.upper()} CLIENT RESPONSE SOP"
        asset = f"""===================================================
Hello [Name]! Thanks for reaching out.
I've received your request regarding: "[Topic]".
To help me serve you best, could you reply with:
1. Your project deadline:
2. Your budget estimation:
We will review this and respond with an update shortly!
=================================================== """

    elif is_data:
        domain_title = f"Simple {primary_tool} Table Setup"
        bottlenecks = [
            f"Data Entry Fatigue: Over-engineering columns and formulas inside {primary_tool} causes manual entry friction.",
            "Zero Data Hygiene: Inputting mismatched date formats or leaving incomplete rows makes filtering impossible."
        ]
        recommended_system = f"A clean, straightforward {primary_tool} sheet with only the columns you actually need."
        central_hub = f"{primary_tool} (configured with standard data structures)"
        
        if skill == "Beginner":
            automation_upgrade = "None recommended. Focus purely on consistent, clean manual tracking before attempting automation."
            actions = [
                f"Apply the '3-Column Rule' inside {primary_tool}: Freeze your columns to keep your view simple (e.g., Date, Client, Status, Notes).",
                "Color-code statuses: Set up basic conditional formatting so 'Needs Action' turns soft red and 'Done' turns green.",
                "Set a weekly registry audit: Dedicate 10 minutes every Friday to clear empty rows and update unresolved data."
            ]
        else:
            automation_upgrade = f"Automated scripts to export external transaction/lead data directly into {primary_tool}."
            actions = [
                f"Create data validation dropdown lists inside {primary_tool} to restrict invalid manual text inputs.",
                "Set up conditional formulas to auto-calculate key business metrics.",
                f"Use API integrations to push summary data from {primary_tool} directly to a performance dashboard."
            ]
            
        asset_title = f"{primary_tool.upper()} DATA INPUT CHECKLIST"
        asset = """[ ] Date: [YYYY-MM-DD]
[ ] Category: [Dropdown Option Selected]
[ ] Value/Cost: [Numerical Value]
[ ] Current Status: [Pending / Completed / Cancelled]
[ ] Notes: [Short plain-text description]"""

    elif is_notion:
        domain_title = f"Single-Page {primary_tool} Notebook"
        bottlenecks = [
            f"The Infinite Workspace Trap: Over-complicating {primary_tool} templates with relational databases and tags.",
            "High Maintenance Cost: Spending more time sorting folders and icons than doing actual deep work."
        ]
        recommended_system = f"A single, blank page inside {primary_tool} to brain-dump tasks without any database clutter."
        central_hub = f"{primary_tool} (stripped down to raw plain-text pages)"
        
        if skill == "Beginner":
            automation_upgrade = "None recommended. Keep it fully manual to prevent setup overhead and decision fatigue."
            actions = [
                f"The One-Page Rule: Delete complex database links in {primary_tool}. Create a single blank page called 'Workspace' and do everything there.",
                "Disable flashy configurations: Stick to standard bullet points and toggle lists instead of building complex properties.",
                f"Set up a 'Brain Dump' list at the very top of {primary_tool} to catch stray thoughts instantly."
            ]
        else:
            automation_upgrade = f"Light keyboard shortcuts or web-clipper rules to instantly drop reference links into your central page."
            actions = [
                f"Configure template buttons inside {primary_tool} to spawn clean daily task logs with one click.",
                "Set up synced blocks to make your main priorities visible across all active sub-folders.",
                "Link project logs programmatically to speed up your navigation time."
            ]
            
        asset_title = f"{primary_tool.upper()} MINIMALIST HOME BASE SKELETON"
        asset = """# 🎯 Daily Focus (Max 3 priorities)
- [ ] Priority 1
- [ ] Priority 2

# 📥 Fast Capture Dump
- Log incoming raw ideas here...

# 📂 Reference Hub
- Paste direct links to working files or active tasks here."""

    else:
        # Default fallback scenario (Dynamic standard task pipeline)
        domain_title = f"Simple {primary_tool} Task List"
        bottlenecks = [
            f"The Mental Load Trap: Trying to remember tasks inside {primary_tool} instead of writing them down.",
            f"Friction of Tracking: Setting up a system in {primary_tool} that is too hard to maintain daily."
        ]
        recommended_system = f"A simple 3-step checklist (To Do, Doing, Done) to track your daily progress."
        central_hub = f"{primary_tool} or simple digital checklist"
        
        if skill == "Beginner":
            automation_upgrade = "None recommended. Use raw checklists to build consistent daily workflow habits."
            actions = [
                f"Write everything down: Empty your thoughts into {primary_tool} the moment they appear.",
                "Set your daily Top 3: Never start a workday with more than three priority tasks.",
                "Keep tasks small: Break down big projects into action steps that take under 15 minutes."
            ]
        else:
            automation_upgrade = f"Automated reminders inside {primary_tool} to flag tasks that are overdue."
            actions = [
                "Establish recurring tasks for your daily review blocks.",
                "Integrate your task list with your calendar so project times block out automatically.",
                "Set up automatic archive rules to keep completed tasks out of your immediate workspace."
            ]
            
        asset_title = "DAILY TASK PIPELINE ASSET"
        asset = """[ ] Task Name:
[ ] Estimated Time (mins):
[ ] Due Date:
[ ] Current Stage: [Inbox / Doing / Done]"""

    return f"""# 🎯 Dynamic Problem Analysis

You are operating as a **{role}** with a technology confidence level of **{skill}**.
You currently utilize: `{tools if tools else "No tools specified"}`.
Your custom problem input:
> "{problem}"

Based on your operational profile, we have programmatically identified these main bottlenecks:
* **{bottlenecks[0]}**
* **{bottlenecks[1]}**

---

# 🛠 Recommended System: {domain_title}

{recommended_system}

---

# 📦 Recommended Tools

* **Primary Focus:** `{primary_tool}`
* **Central Tracking Hub:** {central_hub}
* **Automation (Optional upgrade):** {automation_upgrade}

---

# 🔄 Step-by-Step Workflow

1. **Capture:** Every inbound inquiry or data point is immediately written into `{primary_tool}`.
2. **Process:** Move items to your active queue, filtering out unnecessary background steps.
3. **Focus:** Work only on the task at the top of your active columns.
4. **Clean:** Dedicate 10 minutes at the end of every day to archive completed logs.

---

# 🚀 First 3 Actions

1. **{actions[0]}**
2. **{actions[1]}**
3. **{actions[2]}**

---

# 📋 Copy-Paste Asset

```text
===================================================
{asset_title}
===================================================
{asset}
===================================================
```

---

# 🔮 Future Upgrade

Maintain this exact manual operational habit for 2 consecutive weeks. Once the routine is comfortable, look at introducing low-friction scripting options inside your tools to save manual copy-pasting time.
"""

st.set_page_config(
    page_title="DoDo AI Business Systems",
    page_icon="🦤",
    layout="centered"
)

# App Sidebar for Key validation and Sandbox toggle
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0; padding-bottom: 0;'>🦤</h1>", unsafe_allow_html=True)
    st.title("DoDo Controls")
    st.markdown("Use this panel to manage your system settings, API keys, and execution environment.")
    st.divider()
    
    st.subheader("🔑 API Configuration")
    api_source = st.radio(
        "Select Key Source:",
        ["Use Default Server Key", "Enter Custom API Key"]
    )
    
    active_key = DEFAULT_API_KEY
    if api_source == "Enter Custom API Key":
        custom_key = st.text_input("Enter your API Key (Starts with AIza):", type="password")
        if custom_key:
            active_key = custom_key
            st.success("Custom Key Registered!")
        else:
            st.warning("Please provide a valid API Key to use custom generation.")
            active_key = None

    st.divider()
    st.markdown("💡 **Tip:** If your default key gets blocked or experiences a Google `401` bug, toggle to custom mode and provide your own `AIza...` key!")

st.title("🦤 DoDo")
st.subheader("Simple software systems for your business")

st.write(
    "Tell DoDo your problem. Get a personalized workflow, tools, and execution roadmap."
)

st.divider()

role = st.selectbox(
    "Who are you?",
    [
        "Small Business Owner",
        "Freelancer",
        "Virtual Assistant",
        "Student",
        "Creator"
    ]
)

skill = st.selectbox(
    "Your technology confidence level?",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

tools = st.text_input(
    "What tools do you currently use?",
    placeholder="WhatsApp, Gmail, Notion, Excel..."
)

problem = st.text_area(
    "What problem are you trying to solve?",
    placeholder="Example: I forget follow-ups with customers on email."
)

if st.button("🚀 Generate My System", type="primary"):

    if not problem:
        st.warning("Please describe your problem.")

    elif not active_key:
        st.error("Cannot proceed. Please input your API key in the sidebar or select the Default Server Key.")

    else:
        with st.spinner("🧠 DoDo is designing your system..."):

            prompt = f"""
You are DoDo, an AI Business Systems Architect.

User Profile:
Role: {role}
Technical Confidence: {skill}
Current Tools: {tools}
Problem: {problem}

Create a personalized business system.

Rules:
- Make it extremely simple.
- Match the user's technical level.
- Avoid unnecessary coding.
- Focus on real-world execution.
- Give practical steps.

Output structure:
# 🎯 Problem Analysis
# 🛠 Recommended System
# 📦 Recommended Tools
# 🔄 Workflow
# 🚀 First 3 Actions
# 📋 Copy-Paste Asset
# 🔮 Future Upgrade
"""

            response_text = None
            used_fallback = False

            # Attempt live generation
            try:
                client = genai.Client(api_key=active_key)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config={
                        "system_instruction": "You are DoDo. You simplify complex software systems for non-technical people."
                    }
                )
                response_text = response.text
            except Exception as e:
                # Catching any API issue cleanly and letting our hyper-targeted custom mock system take over
                used_fallback = True
                response_text = generate_simulated_blueprint(role, skill, tools, problem)

            # Elegant alert context
            if used_fallback:
                st.info(
                    "💡 **System Note:** Operating in customized Local Sandbox Engine! (To connect the live Gemini brain, verify your credentials in the sidebar)."
                )
            else:
                st.success("🎉 Live System generated with Gemini-2.0-Flash!")

            st.markdown(response_text)
            st.divider()

            # Clean Markdown Download
            st.download_button(
                label="📥 Download Blueprint (Markdown)",
                data=response_text,
                file_name="dodo_blueprint.md",
                mime="text/markdown",
                use_container_width=True
            )