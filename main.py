#!/usr/bin/env python3
"""
Bifrost - Bridge between Apple Music and Spotify
Main entry point for the application
"""

import sys
from pathlib import Path

# Add the current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from cli.cli import cli

def main():
    """Main entry point for the Bifrost application"""
    cli()

if __name__ == "__main__":
    main()
