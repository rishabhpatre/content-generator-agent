import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.arxiv_client import search_papers
from src.llm_processor import ContentGenerator
from src.email_client import send_email
from src.rss_client import fetch_rss_items
from src.image_generator import generate_infographic

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Arxiv to LinkedIn Agent")
    parser.add_argument("--email", action="store_true", help="Send the result via email instead of just printing")
    args = parser.parse_args()

    console.print(Panel.fit("[bold blue]Arxiv to LinkedIn Agent[/bold blue]", subtitle="AI Research & News Content Generator"))

    # Check API Key
    if not os.getenv("GOOGLE_API_KEY"):
        console.print("[bold red]Error:[/bold red] GOOGLE_API_KEY not set. Please create a .env file with your API key.")
        return

    try:
        generator = ContentGenerator()
        
        # --- PART 1: ARXIV ---
        with console.status("[bold green]Fetching recent AI papers from Arxiv...[/bold green]"):
            papers = search_papers(max_results=7)
            console.print(f"[bold green]Found {len(papers)} papers.[/bold green]")

        with console.status("[bold yellow]Analyzing papers...[/bold yellow]"):
            best_paper = generator.analyze_and_pick_best(papers)
        
        console.print(Panel(f"[bold]{best_paper.title}[/bold]\n\n{best_paper.summary[:200]}...", title="Best Paper Selected", border_style="green"))

        with console.status("[bold magenta]Generating LinkedIn post for Paper...[/bold magenta]"):
            paper_post = generator.generate_linkedin_post(best_paper)

        console.print("\n[bold]Generated LinkedIn Post (Arxiv):[/bold]\n")
        console.print(Panel(Markdown(paper_post), border_style="blue"))


        # --- PART 2: RSS FEEDS ---
        with console.status("[bold green]Fetching AI News from RSS Feeds...[/bold green]"):
            news_items = fetch_rss_items(max_items_per_feed=2)
            console.print(f"[bold green]Found {len(news_items)} news items.[/bold green]")

        best_news = None
        news_post = ""
        
        if news_items:
            with console.status("[bold yellow]Analyzing news items...[/bold yellow]"):
                best_news = generator.analyze_and_pick_best(news_items)
            
            console.print(Panel(f"[bold]{best_news.title}[/bold]\n\n{best_news.summary[:200]}...", title="Best News Item Selected", border_style="cyan"))

            with console.status("[bold magenta]Generating LinkedIn post for News...[/bold magenta]"):
                news_post = generator.generate_linkedin_post(best_news)

            console.print("\n[bold]Generated LinkedIn Post (RSS News):[/bold]\n")
            console.print(Panel(Markdown(news_post), border_style="cyan"))
        else:
            console.print("[bold red]No RSS items found![/bold red]")


        # --- PART 3: AI CONCEPT INFOGRAPHIC ---
        with console.status("[bold cyan]Generating AI Concept Concept...[/bold cyan]"):
            concept_data = generator.generate_ai_concept()
        
        console.print(Panel(f"[bold]{concept_data['title']}[/bold]\n\n{concept_data['explanation']}\n\n[dim]Mermaid Code:[/dim]\n{concept_data['mermaid_code']}", title="AI Concept Generated", border_style="magenta"))

        infographic_path = "daily_concept.png"
        with console.status("[bold magenta]Fetching Mermaid Diagram...[/bold magenta]"):
            from src.image_generator import generate_mermaid_diagram
            # We use the new mermaid generator
            path = generate_mermaid_diagram(concept_data['mermaid_code'], infographic_path)
            if path:
                console.print(f"[bold green]Diagram saved to {infographic_path}[/bold green]")
            else:
                console.print("[bold red]Failed to generate diagram![/bold red]")


        # --- PART 4: EMAIL ---
        if args.email:
            with console.status("[bold cyan]Sending email...[/bold cyan]"):
                email_subject = f"Daily AI Digest: {best_paper.title[:30]}... & More"
                
                email_body = f"""Here are your daily LinkedIn posts:

========================================
RESEARCH PAPER
========================================
Based on: {best_paper.title}

{paper_post}

========================================
AI NEWS
========================================
Based on: {best_news.title if best_news else 'N/A'}

{news_post}

========================================
DAILY AI CONCEPT
========================================
{concept_data['title']}

{concept_data['explanation']}

(See attached concept diagram)
"""
                send_email(subject=email_subject, body=email_body, image_path=infographic_path)

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
