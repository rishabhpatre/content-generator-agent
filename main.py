import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.arxiv_client import search_papers
from src.llm_processor import ContentGenerator
from src.email_client import send_email

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Arxiv to LinkedIn Agent")
    parser.add_argument("--email", action="store_true", help="Send the result via email instead of just printing")
    args = parser.parse_args()

    console.print(Panel.fit("[bold blue]Arxiv to LinkedIn Agent[/bold blue]", subtitle="AI Research Content Generator"))

    # Check API Key
    if not os.getenv("GOOGLE_API_KEY"):
        console.print("[bold red]Error:[/bold red] GOOGLE_API_KEY not set. Please create a .env file with your API key.")
        return

    try:
        # 1. Fetch Papers
        with console.status("[bold green]Fetching recent AI papers from Arxiv...[/bold green]"):
            papers = search_papers(max_results=7)
            console.print(f"[bold green]Found {len(papers)} papers.[/bold green]")

        # 2. Analyze
        generator = ContentGenerator()
        with console.status("[bold yellow]Analyzing papers for virality...[/bold yellow]"):
            best_paper = generator.analyze_and_pick_best(papers)
        
        console.print(Panel(f"[bold]{best_paper.title}[/bold]\n\n{best_paper.summary[:200]}...", title="Best Paper Selected", border_style="green"))

        # 3. Generate Post
        with console.status("[bold magenta]Generating LinkedIn post...[/bold magenta]"):
            post_content = generator.generate_linkedin_post(best_paper)

        # 4. Output
        console.print("\n[bold]Generated LinkedIn Post:[/bold]\n")
        console.print(Panel(Markdown(post_content), border_style="blue"))

        # 5. Email (Optional)
        if args.email:
            with console.status("[bold cyan]Sending email...[/bold cyan]"):
                email_body = f"Here is your daily LinkedIn post based on the paper: {best_paper.title}\n\n---\n\n{post_content}"
                send_email(subject=f"Daily LinkedIn Post: {best_paper.title}", body=email_body)

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
