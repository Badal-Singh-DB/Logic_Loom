<div align="center">
  <img src="https://raw.githubusercontent.com/TheDudeThatCode/TheDudeThatCode/master/Assets/Developer.gif" alt="Animated Developer coding" width="400">
  
  <h1>LogicLoom</h1>
  <p><b>Observable, no-magic LLM agents and tooling</b></p>

  <a href="#"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python" alt="Python 3.10+"></a>
  <a href="#"><img src="https://img.shields.io/badge/Maintenance-Active-success.svg?style=flat-square" alt="Maintenance"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square" alt="License"></a>
</div>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#setup">Setup</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a>
</p>

LogicLoom is a lightweight toolkit for building and tracing LLM agents. I got tired of massive, opaque frameworks that swallow errors and make it impossible to see exactly *why* an agent made a decision. This project focuses on explicit traces, simple tool integrations, and a built-in UI for human review.

If you're looking for a massive, fully autonomous AGI framework, this isn't it. If you want readable code and clear logs for tool-calling agents, you're in the right place.

## Features

- **Transparent Tracing**: The `tracer` module logs every thought, tool call, and response to a strict schema.
- **Built-in Annotator UI**: A local frontend (`annotator.annotation_ui`) to review traces and provide human feedback. Great for debugging or logging RLHF data.
- **Standard Tools**: Comes with `code_executor` and `calculator` out of the box, but defining your own takes zero boilerplate.
- **Lightweight**: Minimal dependencies, avoiding the "dependency hell" of typical LLM wrappers.

## Setup

Requires Python 3.10 or higher.

```bash
git clone https://github.com/yourusername/LogicLoom.git
cd LogicLoom
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

*(Note: Don't forget to set your API keys in the `.env` file first. Copy the `.env.example` if available.)*

## Quick Start

Here's how to spin up a basic agent equipped with a calculator and code executor:

```python
from logic_loom.agent.tool_agent import ToolAgent
from logic_loom.agent.tools.calculator import CalculatorTool
from logic_loom.tracer.trace_recorder import TraceRecorder

# Initialize the recorder to explicitly track all agent reasoning
tracer = TraceRecorder()

agent = ToolAgent(
    tools=[CalculatorTool()],
    tracer=tracer
)

response = agent.run("What is 15% of 850?")
print(response)

# Later, view the trace in the annotator UI
# python -m logic_loom.annotator.annotation_ui
```

## Architecture Map

- `logic_loom/agent/` - The core agent loops (`tool_agent.py`) and standard tool definitions (`tools/`).
- `logic_loom/annotator/` - The interactive UI app for reviewing past agent runs and traces.
- `logic_loom/tracer/` - Defines the strict JSON standard (`trace_schema.py`) and handles logging execution graphs (`trace_recorder.py`).
- `logic_loom/examples/` - Working scripts to get you started immediately.

## Contributing

PRs are welcome. If you modify the agent loop, please ensure you update the trace schema accordingly so the annotator UI doesn't break. I try to review PRs within a few days.

## License

MIT
