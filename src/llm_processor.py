import os
import google.generativeai as genai
from typing import List, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env or pass it to the constructor.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_and_pick_best(self, items: List[Any]) -> Any:
        """
        Analyzes a list of papers or news items and picks the most interesting one for a LinkedIn post.
        """
        prompt = "You are an expert AI curator. Analyze the following content items (research papers or news articles) and identify the ONE most interesting topic for a broad audience of AI enthusiasts (from beginners to experts).\n"
        prompt += "Choose the item that is most likely to be a 'cool' or 'big' discovery/news. Avoid extremely niche topics unless they have huge implications. We want content that makes people say 'Wow'.\n\n"
        
        for i, item in enumerate(items):
            prompt += f"Item {i+1}:\nTitle: {item.title}\nSummary: {item.summary}\n\n"
        
        prompt += "Return ONLY the index number (e.g., '1', '2', etc.) of the best item. Do not explain."

        response = self.model.generate_content(prompt)
        try:
            index = int(response.text.strip()) - 1
            if 0 <= index < len(items):
                return items[index]
            else:
                return items[0] # Fallback
        except:
            return items[0] # Fallback if parsing fails

    def generate_linkedin_post(self, item: Any) -> str:
        """
        Generates a LinkedIn post for the given paper or news item.
        """
        prompt = f"""
        You are an expert ghostwriter for a tech thought leader on LinkedIn.
        
        Write a LinkedIn post about this content (research paper or news article) that matches the following specific style instructions EXACTLY.

        STYLE INSTRUCTIONS:
        - Tone: Enthusiastic but grounded. Professional curiosity.
        - Perspective: Write as if I just read this and found it genuinely interesting.
        - Audience: Accessible to AI beginners but respecting the intelligence of experts.
        - No corporate jargon, no stiff language. Use natural, punchy sentences.
        - Avoid over-the-top hype like "my jaw is on the floor", "mind blown", or "game over".
        - You CAN use a few relevant emojis (like 🚀, 💡) but don't overdo it.
        - Focus on the "Big Idea" – why does this matter? What is the core innovation/news?
        - Keep it concise (under 150 words).
        - Do NOT summarize abstract-style. Tell a story.
        - Include the URL at the very end.

        EXAMPLE OF DESIRED STYLE:
        I just finished reading about "Large Causal Models" and this is a fascinating direction.

        We’ve all seen LLMs predict text, but this new work shows them building actual maps of cause and effect. It’s not just guessing patterns anymore; it’s attempting to understand *why* things happen.

        They treat the LLM like a scientist—asking it to spot conflicts, fix its own logic, and ask "what if?" until it builds a stable explanation.

        This feels like a significant shift. We’re moving from models that just "know" things to systems that can actually explain how the world works.

        If this scales, it could impact everything from debugging code to scientific discovery. Definitely worth a read. 💡

        CONTENT DETAILS:
        Title: {item.title}
        Authors/Source: {", ".join(item.authors[:3]) if hasattr(item, 'authors') else getattr(item, 'source', 'Unknown')}
        Summary: {item.summary}
        URL: {item.url}
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_ai_concept(self) -> dict:
        """
        Generates a 'Concept of the Day' with a title, explanation, and Mermaid diagram code.
        """
        prompt = """
        Select a specific, **Intermediate to Advanced** technical concept from Artificial Intelligence, Machine Learning, or Generative AI.
        
        DO NOT choose basic concepts like "What is AI?", "Chatbots", or "Machine Learning vs AI".
        INSTEAD, choose technical topics like:
        - Low-Rank Adaptation (LoRA)
        - Proximal Policy Optimization (PPO)
        - Vision Transformers (ViT)
        - Retrieval Augmented Generation (RAG) Architecture
        - Latent Diffusion
        - KV Cache
        - Flash Attention
        
        Provide three things:
        1. A catchy Title (max 5-7 words).
        2. A high-quality, educational LinkedIn post (150-200 words). 
           - **Goal**: Teach the concept simply but deeply.
           - **Style**: Start with a hook (why it matters). Use an ANALOGY if helpful. Break it down step-by-step.
           - **Tone**: Professional, insightful, like a senior engineer mentoring a junior.
           - Complement the diagram (mention "As shown in the diagram...").
        3. A valid Mermaid.js graph definition (e.g., `graph TD; A-->B;`) that visually explains the concept.
           - **CRITICAL**: Use semicolons (;) after EVERY statement.
           - **KEEP IT SIMPLE**: Max 5-8 nodes. DO NOT use `subgraph` or `linkStyle`.
           - Example: `graph TD; A[Input] --> B{Process}; B -- Yes --> C[Output]; B -- No --> D[Retrying];`
           - Do not use special characters in node labels that break Mermaid syntax.
        
        Format the output EXACTLY like this (don't use markdown code blocks):
        TITLE: [The Title]
        EXPLANATION: [The Explanation text]
        MERMAID: [The Mermaid code, on one line or multiple lines]
        """
        
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        
        # Simple parsing
        title = "Unknown Concept"
        explanation = "Check back tomorrow!"
        mermaid_code = "graph TD; A[Error] --> B[No Code];"
        
        current_section = None
        mermaid_lines = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line: continue
            
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
                current_section = "title"
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
                current_section = "explanation"
            elif line.startswith("MERMAID:"):
                mermaid_lines.append(line.replace("MERMAID:", "").strip())
                current_section = "mermaid"
            elif current_section == "explanation":
                explanation += " " + line
            elif current_section == "mermaid":
                mermaid_lines.append(line)
        
        mermaid_code = "\n".join(mermaid_lines)
        # Clean up any markdown code blocks if the model ignored instructions
        mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
        
        return {"title": title, "explanation": explanation, "mermaid_code": mermaid_code}
