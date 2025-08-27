"""
Beautiful CLI for the AI-Powered Resume System using Typer and Rich.

This module provides a comprehensive command-line interface with rich formatting,
progress indicators, and intuitive commands for managing your resume as infrastructure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from . import __version__
from .config import config

# Initialize Rich console
console = Console()
app = typer.Typer(
    name="resume",
    help="🚀 AI-Powered DevOps Resume System - Resume as Infrastructure",
    add_completion=False,
    rich_markup_mode="rich",
)

# Subcommands
ai_app = typer.Typer(
    name="ai",
    help="🤖 AI-powered content enhancement and automation",
    rich_markup_mode="rich",
)
build_app = typer.Typer(
    name="build",
    help="🔨 Build resume in multiple formats",
    rich_markup_mode="rich",
)
serve_app = typer.Typer(
    name="serve",
    help="🌐 Development server with live preview",
    rich_markup_mode="rich",
)

app.add_typer(ai_app)
app.add_typer(build_app)
app.add_typer(serve_app)


def version_callback(show_version: bool):
    """Show version information."""
    if show_version:
        rprint(f"[bold blue]Tom Drake Resume System[/bold blue] v{__version__}")
        rprint(f"[dim]AI-Powered DevOps Resume Management[/dim]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose output"
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Override default config file",
        exists=True,
    ),
):
    """
    🚀 AI-Powered DevOps Resume System
    
    Transform your resume management with modern DevOps practices, AI enhancement,
    and comprehensive automation. Build, deploy, and maintain your resume like
    infrastructure code.
    """
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
    
    # Validate configuration
    config.validate_ai_config()


@app.command()
def status():
    """📊 Show system status and configuration."""
    console.print("\n[bold blue]System Status[/bold blue]\n")
    
    # Create status table
    table = Table(title="Configuration Status", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", width=25)
    table.add_column("Status", width=15)
    table.add_column("Details", style="dim")
    
    # Check file existence
    resume_exists = config.resume_file.exists()
    schema_exists = config.schema_file.exists()
    
    table.add_row(
        "Resume Data",
        "✅ Found" if resume_exists else "❌ Missing",
        str(config.resume_file)
    )
    
    table.add_row(
        "Schema File", 
        "✅ Found" if schema_exists else "❌ Missing",
        str(config.schema_file)
    )
    
    table.add_row(
        "AI Provider",
        "✅ Claude" if config.claude_api_key else 
        "✅ OpenAI" if config.openai_api_key else "❌ None",
        f"Model: {config.claude_model if config.claude_api_key else config.openai_model if config.openai_api_key else 'N/A'}"
    )
    
    table.add_row(
        "Output Directory",
        "✅ Ready" if config.output_dir.exists() else "📁 Created",
        str(config.output_dir)
    )
    
    console.print(table)
    
    # Show available formats
    console.print(f"\n[bold]Available Formats:[/bold] {', '.join(config.formats)}")
    
    if not config.has_ai_api_key:
        console.print("\n[yellow]⚠️  AI features disabled - configure CLAUDE_API_KEY or OPENAI_API_KEY[/yellow]")


@app.command()
def validate(
    schema: bool = typer.Option(
        True,
        help="Validate against JSON schema"
    ),
    fix_formatting: bool = typer.Option(
        False,
        "--fix",
        help="Automatically fix formatting issues"
    )
):
    """✅ Validate resume data against schema and best practices."""
    with console.status("[bold green]Validating resume data...") as status:
        try:
            # Import here to avoid circular imports
            from .validators.schema import validate_resume_file
            
            status.update("[bold green]Loading resume data...")
            result = validate_resume_file(config.resume_file, config.schema_file)
            
            if result.is_valid:
                console.print("✅ [bold green]Resume validation passed![/bold green]")
                
                # Show summary
                table = Table(title="Validation Summary", show_header=False)
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="bold")
                
                table.add_row("Experience Entries", str(len(result.data.experience)))
                table.add_row("Skills Categories", str(len(result.data.skills.categories)))
                table.add_row("Total Skills", str(sum(len(cat.skills) for cat in result.data.skills.categories.values())))
                table.add_row("Certifications", str(len(result.data.certifications or [])))
                table.add_row("Projects", str(len(result.data.projects or [])))
                
                console.print(table)
                
            else:
                console.print("❌ [bold red]Validation failed![/bold red]")
                for error in result.errors:
                    console.print(f"  • {error}")
                raise typer.Exit(1)
                
        except Exception as e:
            console.print(f"❌ [bold red]Validation error:[/bold red] {e}")
            raise typer.Exit(1)


# Build commands
@build_app.command()
def all(
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory (default: from config)"
    ),
    formats: Optional[List[str]] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output formats (default: all configured)"
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Clean output directory first"
    )
):
    """🔨 Build resume in all configured formats."""
    output_dir = output or config.output_dir
    build_formats = formats or config.formats
    
    if clean and output_dir.exists():
        console.print(f"🧹 Cleaning output directory: {output_dir}")
        import shutil
        shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Load and validate data
        task = progress.add_task("Loading resume data...", total=None)
        try:
            from .validators.schema import validate_resume_file
            result = validate_resume_file(config.resume_file, config.schema_file)
            
            if not result.is_valid:
                console.print("❌ [bold red]Cannot build: Resume data validation failed[/bold red]")
                for error in result.errors:
                    console.print(f"  • {error}")
                raise typer.Exit(1)
                
        except Exception as e:
            console.print(f"❌ [bold red]Error loading resume data:[/bold red] {e}")
            raise typer.Exit(1)
        
        progress.remove_task(task)
        
        # Build each format
        built_files = []
        for fmt in build_formats:
            task = progress.add_task(f"Building {fmt.upper()} format...", total=None)
            
            try:
                # Import builder dynamically
                if fmt == "html":
                    from .builders.html import HtmlBuilder
                    builder = HtmlBuilder(result.data, output_dir)
                elif fmt == "pdf":
                    from .builders.pdf import PdfBuilder
                    builder = PdfBuilder(result.data, output_dir)
                elif fmt == "json":
                    from .builders.json_builder import JsonBuilder
                    builder = JsonBuilder(result.data, output_dir)
                elif fmt == "markdown":
                    from .builders.markdown import MarkdownBuilder
                    builder = MarkdownBuilder(result.data, output_dir)
                else:
                    console.print(f"❌ Unknown format: {fmt}")
                    continue
                
                file_path = builder.build()
                built_files.append((fmt.upper(), file_path))
                
            except Exception as e:
                console.print(f"❌ [bold red]Error building {fmt}:[/bold red] {e}")
                
            progress.remove_task(task)
    
    # Show results
    if built_files:
        console.print("\n✅ [bold green]Build completed successfully![/bold green]\n")
        
        table = Table(title="Generated Files", show_header=True, header_style="bold magenta")
        table.add_column("Format", style="cyan", width=10)
        table.add_column("File", style="bright_white")
        table.add_column("Size", style="dim", justify="right")
        
        for fmt, file_path in built_files:
            file_size = file_path.stat().st_size if file_path.exists() else 0
            size_str = f"{file_size:,} bytes" if file_size < 1024 else f"{file_size/1024:.1f} KB"
            table.add_row(fmt, str(file_path.name), size_str)
        
        console.print(table)
        console.print(f"\n📁 Output directory: {output_dir}")
    else:
        console.print("❌ [bold red]No files were built successfully[/bold red]")
        raise typer.Exit(1)


# AI commands
@ai_app.command()
def enhance(
    field: Optional[str] = typer.Option(
        None,
        "--field",
        "-f",
        help="Specific field to enhance (achievements, summary, skills)"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be enhanced without making changes"
    )
):
    """🤖 Enhance resume content using AI."""
    if not config.has_ai_api_key:
        console.print("❌ [bold red]AI features require CLAUDE_API_KEY or OPENAI_API_KEY[/bold red]")
        console.print("Set your API key in the .env file")
        raise typer.Exit(1)
    
    console.print("🤖 [bold blue]AI Content Enhancement[/bold blue]")
    
    if dry_run:
        console.print("[yellow]Running in dry-run mode - no changes will be made[/yellow]\n")
    
    with console.status("[bold green]Analyzing resume content...") as status:
        try:
            from .ai.claude import enhance_resume_content
            
            status.update("[bold green]Loading resume data...")
            from .validators.schema import validate_resume_file
            result = validate_resume_file(config.resume_file, config.schema_file)
            
            if not result.is_valid:
                console.print("❌ Cannot enhance: Resume validation failed")
                raise typer.Exit(1)
            
            status.update("[bold green]Enhancing content with AI...")
            enhanced_data = enhance_resume_content(result.data, field)
            
            if dry_run:
                console.print("✨ [bold green]AI enhancement preview:[/bold green]")
                # Show preview of changes
                console.print("[dim]Changes would be applied to resume.yml[/dim]")
            else:
                # Save enhanced data
                import yaml
                with open(config.resume_file, 'w') as f:
                    yaml.dump(enhanced_data.dict(), f, default_flow_style=False, sort_keys=False)
                
                console.print("✅ [bold green]Resume enhanced successfully![/bold green]")
                console.print(f"📝 Updated: {config.resume_file}")
                
        except Exception as e:
            console.print(f"❌ [bold red]Enhancement failed:[/bold red] {e}")
            raise typer.Exit(1)


@ai_app.command()
def commit_message(
    files: Optional[List[str]] = typer.Option(
        None,
        "--files",
        help="Files that were changed"
    )
):
    """🤖 Generate AI-powered commit message."""
    if not config.has_ai_api_key:
        console.print("❌ [bold red]AI features require API key configuration[/bold red]")
        raise typer.Exit(1)
    
    with console.status("[bold green]Generating commit message...") as status:
        try:
            from .ai.claude import generate_commit_message
            
            # Get git diff if no files specified
            changed_files = files or ["resume.yml"]  # Default assumption
            
            message = generate_commit_message(changed_files)
            
            console.print("✨ [bold green]Generated commit message:[/bold green]\n")
            
            panel = Panel(
                message,
                title="📝 Commit Message",
                border_style="blue"
            )
            console.print(panel)
            
            if typer.confirm("\nUse this commit message?"):
                import subprocess
                try:
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "commit", "-m", message], check=True)
                    console.print("✅ [bold green]Committed successfully![/bold green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"❌ Git command failed: {e}")
            
        except Exception as e:
            console.print(f"❌ [bold red]Failed to generate commit message:[/bold red] {e}")
            raise typer.Exit(1)


# Serve commands
@serve_app.command()
def dev(
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to serve on"
    ),
    host: str = typer.Option(
        "localhost",
        "--host",
        "-h",
        help="Host to bind to"
    ),
    watch: bool = typer.Option(
        True,
        "--watch/--no-watch",
        help="Enable file watching for auto-reload"
    )
):
    """🌐 Start development server with live preview."""
    console.print(f"🌐 [bold blue]Starting development server...[/bold blue]")
    console.print(f"📡 Server will be available at: http://{host}:{port}")
    
    if watch:
        console.print("👀 File watching enabled - changes will trigger rebuilds")
    
    try:
        # This would start a development server
        # For now, just show what would happen
        console.print("\n[dim]Development server functionality coming soon...[/dim]")
        console.print("[dim]This would start a live preview server with auto-reload[/dim]")
        
    except KeyboardInterrupt:
        console.print("\n👋 Development server stopped")


@app.command()
def init(
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite existing files"
    )
):
    """🚀 Initialize a new resume project."""
    console.print("🚀 [bold blue]Initializing Resume Project[/bold blue]\n")
    
    # Create .env.example
    if not Path(".env.example").exists() or force:
        from .config import Config
        Config.create_example_env()
        console.print("✅ Created .env.example")
    
    # Create basic directory structure
    dirs_to_create = [
        "templates/html",
        "templates/latex", 
        "templates/markdown",
        "dist",
        "tests",
        ".github/workflows"
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    console.print("✅ Created directory structure")
    
    # Show next steps
    panel = Panel(
        """[bold]Next Steps:[/bold]

1. Copy .env.example to .env and add your API keys
2. Update resume.yml with your information  
3. Run: [cyan]resume validate[/cyan] to check your data
4. Run: [cyan]resume build all[/cyan] to generate your resume
5. Run: [cyan]resume ai enhance[/cyan] to improve content with AI

[dim]For help: resume --help[/dim]""",
        title="🎯 Getting Started",
        border_style="green"
    )
    
    console.print(panel)


if __name__ == "__main__":
    app()