import os
import google.generativeai as genai
from typing import List, Optional
from src.arxiv_client import Paper
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env or pass it to the constructor.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_and_pick_best(self, papers: List[Paper]) -> Paper:
        """
        Analyzes a list of papers and picks the most interesting one for a LinkedIn post.
        """
        prompt = "You are an expert AI curator. Analyze the following research papers and identify the ONE most interesting topic for a broad audience of AI enthusiasts (from beginners to experts).\n"
        prompt += "Choose the paper that is most likely to be a 'cool' or 'big' discovery. Avoid extremely niche mathematical proofs unless they have huge implications. We want papers that make people say 'Wow'.\n\n"
        
        for i, paper in enumerate(papers):
            prompt += f"Paper {i+1}:\nTitle: {paper.title}\nSummary: {paper.summary}\n\n"
        
        prompt += "Return ONLY the index number (e.g., '1', '2', etc.) of the best paper. Do not explain."

        response = self.model.generate_content(prompt)
        try:
            index = int(response.text.strip()) - 1
            if 0 <= index < len(papers):
                return papers[index]
            else:
                return papers[0] # Fallback
        except:
            return papers[0] # Fallback if parsing fails

    def generate_linkedin_post(self, paper: Paper) -> str:
        """
        Generates a LinkedIn post for the given paper.
        """
        prompt = f"""
        You are an expert ghostwriter for a tech thought leader on LinkedIn.
        
        Write a LinkedIn post about this research paper that matches the following specific style instructions EXACTLY.

        STYLE INSTRUCTIONS:
        - Tone: Enthusiastic but grounded. Professional curiosity.
        - Perspective: Write as if I just read this paper and found it genuinely interesting.
        - Audience: Accessible to AI beginners but respecting the intelligence of experts.
        - No corporate jargon, no stiff language. Use natural, punchy sentences.
        - Avoid over-the-top hype like "my jaw is on the floor", "mind blown", or "game over".
        - You CAN use a few relevant emojis (like 🚀, 💡) but don't overdo it.
        - Focus on the "Big Idea" – why does this matter? What is the core innovation?
        - Keep it concise (under 150 words).
        - Do NOT summarize abstract-style. Tell a story.
        - Include the paper URL at the very end.

        EXAMPLE OF DESIRED STYLE:
        I just finished reading "Large Causal Models" and this is a fascinating direction.

        We’ve all seen LLMs predict text, but this paper shows them building actual maps of cause and effect. It’s not just guessing patterns anymore; it’s attempting to understand *why* things happen.

        They treat the LLM like a scientist—asking it to spot conflicts, fix its own logic, and ask "what if?" until it builds a stable explanation.

        This feels like a significant shift. We’re moving from models that just "know" things to systems that can actually explain how the world works.

        If this scales, it could impact everything from debugging code to scientific discovery. Definitely worth a read. 💡

        PAPER DETAILS:
        This paper might be the most important shift in how we use LLMs this entire year.

        “Large Causal Models from Large Language Models.”

        It shows that an LLM can build a clear map of cause and effect on its own, letting us ask “what if,” predict what happens when we change something, and check whether those explanations actually make sense.

        And the way they do it is surprisingly simple.

        They do not train a new complex model.
        They treat the LLM like a curious scientist.

        They ask it to:

        → pull cause-and-effect clues from text
        → check which things really depend on each other
        → spot conflicts in its own explanations
        → fix the story
        → ask “what if we change this?”
        → repeat until the explanation stops breaking

        The result is something new.

        A system where the LLM builds its own explanation of how the world works, using what it already knows.

        Not just statistics.
        Not just patterns.

        Understanding.

        Across many tests, including messy real-world topics, this approach beats older methods because it uses common sense and background knowledge, not just numbers in a table.

        And the “what if” answers?

        Surprisingly strong.

        It can answer questions that normal algorithms fail at, simply because it already understands how the world usually behaves.

        This points to a future where LLMs are not just text predictors.

        They become systems that explain.

        If this scales, fields like medicine, economics, policy, and science will change fast.

        LLMs will not just tell you 𝘄𝗵𝗮𝘁 happens.

        They will tell you 𝘄𝗵𝘆.

        PAPER DETAILS:
        Title: {paper.title}
        Authors: {", ".join(paper.authors[:3])} {"et al." if len(paper.authors) > 3 else ""}
        Summary: {paper.summary}
        URL: {paper.url}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
