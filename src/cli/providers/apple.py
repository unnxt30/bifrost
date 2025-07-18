import click 
from src.services.apple import AppleManager
import json


@click.group()
def apple():
    """Apple Music Operations"""
    pass

@apple.command()
@click.argument('url')
@click.option('--output', '-o', type=click.Choice(['json', 'pretty']), default='pretty', 
              help='Output format (json or pretty)')
def track_info(url, output):
    """Get track information from Apple Music URL"""
    try:
        apple_manager = AppleManager(url)

        # Extract track ID
        if not apple_manager.extract_track_id():
            click.echo("Failed to extract track ID from URL", err=True)
            return
        
        click.echo(f"Extracted track ID: {apple_manager.track_id}")
        
        # Get iTunes data
        click.echo("Fetching track information...")
        itunes_data = apple_manager.get_itunes_url()
        
        if not itunes_data:
            click.echo("Failed to fetch track information", err=True)
            return
        
        if output == 'json':
            click.echo(json.dumps(itunes_data, indent=2))
        else:
            # Pretty print the track information
            results = itunes_data.get('results', [])
            if results:
                track = results[0]
                click.echo("\nTrack Information:")
                click.echo(f"  Title: {track.get('trackName', 'N/A')}")
                click.echo(f"  Artist: {track.get('artistName', 'N/A')}")
                click.echo(f"  Album: {track.get('collectionName', 'N/A')}")
                click.echo(f"  Genre: {track.get('primaryGenreName', 'N/A')}")
                click.echo(f"  Release Date: {track.get('releaseDate', 'N/A')}")
                click.echo(f"  Duration: {track.get('trackTimeMillis', 0) // 1000} seconds")
                click.echo(f"  Preview URL: {track.get('previewUrl', 'N/A')}")
            else:
                click.echo("No track information found")
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)