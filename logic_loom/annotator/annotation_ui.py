import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LogicLoom Annotation", page_icon="🛠️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: transparent !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Professional 'Pulse Grid' Animation */
    .ai-universe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -100;
        background-color: #0b0f19;
        background-image: 
            linear-gradient(rgba(30, 41, 59, 0.5) 1px, transparent 1px),
            linear-gradient(90deg, rgba(30, 41, 59, 0.5) 1px, transparent 1px);
        background-size: 40px 40px;
        animation: slowGridPan 30s linear infinite;
    }
    
    .ai-universe::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, transparent 0%, #0b0f19 80%);
        pointer-events: none;
    }

    @keyframes slowGridPan {
        0% { background-position: 0px 0px; }
        100% { background-position: 40px 40px; }
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #0ea5e9;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .trace-card {
        background: #111827;
        border-radius: 8px;
        padding: 24px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        border: 1px solid #1e293b;
    }
    .step-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .badge-planning { background-color: rgba(71, 85, 105, 0.2); color: #94a3b8; border: 1px solid #475569; }
    .badge-tool_use { background-color: rgba(14, 165, 233, 0.1); color: #0ea5e9; border: 1px solid #0284c7; }
    .badge-reasoning { background-color: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #059669; }
</style>
<div class="ai-universe"></div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">LogicLoom Node Active</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">■ STRUCTURE, EVALUATE, AND REFINE EXPERT TRACES</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### Generate Sequence")
    task_id = st.text_input("Task ID", value="task_001")
    prompt = st.text_area("Deploy a complex prompt to trigger real-time inference:", value="A snail is at the bottom of a 20-foot well. Each day, it climbs up 5 feet. Each night, it slides down 4 feet...", height=120)
    
    if st.button("INITIALIZE TRACE GENERATION", use_container_width=True, type="primary"):
        st.info("Reasoning...")
        
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        api_key = os.environ.get("NVIDIA_API_KEY", "")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        system_prompt = '''You are an AI data trainer generating structured reasoning and tool-use traces. 
Output ONLY valid JSON following this exact schema without markdown formatting blocks:
{
  "task_id": "string",
  "task_description": "string",
  "trace": [
    {
      "step": 1,
      "type": "planning | tool_use | reasoning",
      "thought": "string",
      "decision_rationale": "string [if planning]",
      "tool": "string [if tool_use]",
      "input": "string [if tool_use]",
      "output": "string [if tool_use]",
      "observation": "string [if tool_use]",
      "alternatives_considered": ["list of strings [if reasoning]"],
      "chosen_approach": "string [if reasoning]"
    }
  ],
  "metadata": {
    "total_steps": number,
    "tools_used": ["strings"],
    "reasoning_steps": number,
    "planning_steps": number,
    "tool_use_steps": number,
    "success": boolean,
    "quality_score": 0.0
  }
}'''

        payload = {
            "model": "qwen/qwen3.5-122b-a10b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500,
            "temperature": 0.60
        }
        
        with st.spinner("Model is reasoning..."):
            try:
                response = requests.post(invoke_url, headers=headers, json=payload, timeout=45)
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    
                    try:
                        parsed_json = json.loads(content)
                        st.session_state["parsed_trace"] = parsed_json
                        st.session_state["raw_response"] = json.dumps(parsed_json, indent=2)
                        st.success("Trace generated successfully!")
                    except json.JSONDecodeError as de:
                        st.error(f"Failed to parse JSON output: {de}")
                        st.session_state["raw_response"] = content
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"API Error: {str(e)}")

with col2:
    st.subheader("Trace Annotation")
    tabs = st.tabs(["Structured View", "Raw Output", "Export JSON"])
    
    with tabs[1]:
        if "raw_response" in st.session_state:
            st.code(st.session_state["raw_response"], language="json")
        else:
            st.info("Run generation to view raw traces.")
            
    with tabs[0]:
        if "parsed_trace" in st.session_state:
            trace_data = st.session_state["parsed_trace"].get("trace", [])
            for step in trace_data:
                step_type = step.get("type", "unknown")
                if step_type == "planning":
                    st.markdown(f'<div class="trace-card"><span class="step-badge badge-planning">Plan</span> <strong>Step {step.get("step")}:</strong> {step.get("thought", "N/A")}<br><small><i>Rationale: {step.get("decision_rationale", "")}</i></small></div>', unsafe_allow_html=True)
                elif step_type == "tool_use":
                    tool = step.get("tool", "unknown_tool")
                    st.markdown(f'<div class="trace-card"><span class="step-badge badge-tool_use">Tool: {tool}</span> <strong>Step {step.get("step")}:</strong><br><strong>Input:</strong>\n```\n{step.get("input", "")}\n```<br><strong>Output:</strong>\n```\n{step.get("output", "")}\n```<br><strong>Observation:</strong> {step.get("observation", "")}</div>', unsafe_allow_html=True)
                elif step_type == "reasoning":
                    st.markdown(f'<div class="trace-card"><span class="step-badge badge-reasoning">Reasoning</span> <strong>Step {step.get("step")}:</strong> {step.get("thought", "")}<br><strong>Chosen Approach:</strong> {step.get("chosen_approach", "")}</div>', unsafe_allow_html=True)
            
            st.slider("Rate Trace Quality", min_value=1.0, max_value=5.0, value=st.session_state["parsed_trace"].get("metadata", {}).get("quality_score", 4.0), step=0.5)
            st.button("Save Annotation 💾", type="primary")
        else:
            st.markdown('<div class="trace-card">Generate a trace to begin annotation.</div>', unsafe_allow_html=True)


