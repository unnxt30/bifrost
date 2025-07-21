import click
import sys
from pathlib import Path
from src.cli.providers.apple import apple
from src.cli.providers.spotify import spotify
# Add the parent directory to sys.path so we can import services
sys.path.insert(0, str(Path(__file__).parent.parent))

@click.group()
def bifrost():
    "Bifrost 🥶"
    pass

bifrost.add_command(apple)
bifrost.add_command(spotify)

if __name__ == '__main__':
    bifrost()
