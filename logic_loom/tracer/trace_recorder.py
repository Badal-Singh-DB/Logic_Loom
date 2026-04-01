import json
import os
from typing import Optional
from logic_loom.tracer.trace_schema import ReasoningTrace, TraceStep, TraceMetadata

class TraceRecorder:
    def __init__(self, task_id: str, task_description: str):
        self.trace_obj = ReasoningTrace(task_id=task_id, task_description=task_description)
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "recorded_traces")
        os.makedirs(self.output_dir, exist_ok=True)

    def current_step_count(self) -> int:
        return len(self.trace_obj.trace) + 1

    def record_planning(self, thought: str, rationale: str):
        step = TraceStep(
            step=self.current_step_count(),
            type="planning",
            thought=thought,
            decision_rationale=rationale
        )
        self.trace_obj.trace.append(step)
        self.trace_obj.metadata.planning_steps += 1

    def record_tool_use(self, tool_name: str, tool_input: str, tool_output: str, observation: Optional[str] = None):
        step = TraceStep(
            step=self.current_step_count(),
            type="tool_use",
            tool=tool_name,
            input=tool_input,
            output=tool_output,
            observation=observation
        )
        self.trace_obj.trace.append(step)
        self.trace_obj.metadata.tool_use_steps += 1
        if tool_name not in self.trace_obj.metadata.tools_used:
            self.trace_obj.metadata.tools_used.append(tool_name)

    def record_reasoning(self, thought: str, alternatives: list[str], chosen: str):
        step = TraceStep(
            step=self.current_step_count(),
            type="reasoning",
            thought=thought,
            alternatives_considered=alternatives,
            chosen_approach=chosen
        )
        self.trace_obj.trace.append(step)
        self.trace_obj.metadata.reasoning_steps += 1

    def finalize(self, success: bool, score: float = 0.0) -> str:
        self.trace_obj.metadata.total_steps = len(self.trace_obj.trace)
        self.trace_obj.metadata.success = success
        self.trace_obj.metadata.quality_score = score
        
        json_output = self.trace_obj.to_json()
        filepath = os.path.join(self.output_dir, f"{self.trace_obj.task_id}.json")
        with open(filepath, "w") as f:
            f.write(json_output)
            
        return json_output
