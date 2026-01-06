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
