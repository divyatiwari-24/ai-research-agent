from llm import call_llm

def multi_agent_system(query):
    prompt = f"""
You are a multi-agent AI system.

Return ONLY valid JSON. No markdown, no explanation.

Format:
{{
  "plan": "Step 1... Step 2... Step 3...",
  "research": "Detailed explanation...",
  "answer": "Final answer..."
}}

Question: {query}
"""
    return call_llm(prompt)