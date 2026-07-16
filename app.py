import streamlit as st
import os
from google import genai

# 1. New Upgraded Client Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 2. UI Frontend Design
st.set_page_config(page_title="DoDo Blueprint Generator", layout="centered")

st.title("🦤 DoDo: Automation Blueprint Generator")
st.write("Turn confusing apps into simple, one-page execution roadmaps for small businesses.")

st.divider()

# 3. User Input Fields
app_name = st.text_input("1. What app do they need help with?", placeholder="e.g., Notion, Excel, QuickBooks")
user_goal = st.text_input("2. What repetitive task do they want to solve?", placeholder="e.g., auto-saving customer emails into a sheet")

# Move 3 Implementation: Dynamic Target Audience Selection
audience = st.selectbox(
    "3. Who is this execution blueprint for?",
    options=["Absolute Beginner / Non-Tech Business Owner", "Virtual Assistant / Operations Admin", "Junior Software Developer"]
)

st.divider()

# 4. Trigger Action Button
if st.button("Generate My Blueprint", type="primary"):
    if not app_name or not user_goal:
        st.warning("Please fill out both fields to generate the roadmap!")
    else:
        # Sleek professional loading wrapper
        with st.spinner(f"🧠 DoDo is customizing a blueprint tailored for a {audience}..."):
            try:
                # 5. System Instructions + Dynamic Audience Prompt Engineering
                engineered_prompt = f"""
                The user needs an structured execution blueprint for the software app "{app_name}" to achieve this goal: "{user_goal}".
                
                CRITICAL CONTEXT: The target audience reading this blueprint is a {audience}. Adjust the depth, terminology, and technical detail of your steps so it perfectly matches their skill level.
                
                Do not write any introductory text. Output the response strictly using markdown with these sections:
                
                ### 📍 Section 1: The UI Interface Map
                (Where are the main buttons they need located on the screen?)
                
                ### ⚡ Section 2: The Step-by-Step Action Flow
                (Numbered list of exact clicks needed to finish the task. Short, actionable sentences.)
                
                ### ⚠️ Section 3: The Beginner "Gotcha"
                (What specific mistake or point of confusion does a user at this level always hit here?)
                """
                
                # Execution call to the production engine
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=engineered_prompt,
                    config={"system_instruction": "You are an expert automation engineer named DoDo who excels at making complex technical tasks clear."}
                )
                
                # 6. Display the result on the webpage cleanly
                st.success("Blueprint Rendered Successfully!")
                st.markdown(response.text)
                
                st.markdown("---")
                
                # 7. Dynamic Two-Column Action Layout (Download & Paywall Shortcut)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Download Blueprint as Markdown",
                        data=response.text,
                        file_name=f"{app_name.lower().replace(' ', '_')}_blueprint.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                with col2:
                    # ⚠️ ACTION ITEM: Replace the URL below with your actual Gumroad page link
                    gumroad_payment_url = "https://yourusername.gumroad.com/l/your-product-id"
                    
                    st.link_button(
                        label="⚡ Get Pre-built Template & Code (RM25)",
                        url=gumroad_payment_url,
                        type="primary",
                        use_container_width=True
                    )
                
                st.caption(
                    "💡 **Why build from scratch?** Click the premium link above to instantly download the "
                    "fully configured system architecture, plug-and-play scripts, and ready-to-import templates "
                    "generated for this exact workflow."
                )
                
            except Exception as e:
                st.error(f"Engine connection issue: {e}")
