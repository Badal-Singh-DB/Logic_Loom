import os
import requests

class TextGenerationAgent:
    def __init__(self):
        self.invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.api_key = os.environ.get("NVIDIA_API_KEY")
        
    def generate_trace(self, prompt, stream=True):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream" if stream else "application/json"
        }
        
        payload = {
            "model": "qwen/qwen3.5-122b-a10b",
            "messages": [{"role":"user","content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.60,
            "top_p": 0.95,
            "stream": stream,
        }
        
        response = requests.post(self.invoke_url, headers=headers, json=payload, stream=stream)
        
        if stream:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        print(decoded_line[6:]) 
        else:
            return response.json()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    agent = TextGenerationAgent()
    agent.generate_trace("Plan steps to parse an Apache log file and count error frequency.")
