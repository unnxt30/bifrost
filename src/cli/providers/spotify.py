import click 
from src.services.spotify import SpotifyManager
from src.services.apple import AppleManager
import json


@click.group()
def spotify():
    """Spotify Operations"""
    pass

@spotify.command()
@click.argument('url')
@click.option('--output', '-o', type=click.Choice(['json', 'pretty']), default='pretty', 
              help='Output format (json or pretty)')
def track_info(url, output):
    """Get track information from Spotify URL"""
    try:
        spotify_manager = SpotifyManager()
        spotify_data = spotify_manager.get_spotify_track(url)
        
        if not spotify_data:
            click.echo("Failed to fetch track information", err=True)
        
        if output == 'json':
            click.echo(json.dumps(spotify_data, indent=2))
        
        else:
            click.echo("Track Information:")
            click.echo("\nTrack Information:")
            click.echo(f"  Title: {spotify_data.get('name', 'N/A')}")
            click.echo(f"  Artist: {spotify_data.get('artists', [{}])[0].get('name', 'N/A')}")
            click.echo(f"  Album: {spotify_data.get('album', {}).get('name', 'N/A')}")
            click.echo(f"  Release Date: {spotify_data.get('album', {}).get('release_date', 'N/A')}")
            click.echo(f"  Duration: {spotify_data.get('duration_ms', 0) // 1000} seconds")
            click.echo(f"  Preview URL: {spotify_data.get('preview_url', 'N/A')}")

    except Exception as e:
        click.echo(f"erro fetching spotify track info: {e}")
@spotify.command()
@click.argument('url')
def convert(url):
    spotify_manager = SpotifyManager()
    apple_manager = AppleManager()

    spotify_data = spotify_manager.get_spotify_track(url)

    artist_name = spotify_data.get('artists', [{}])[0].get('name', 'N/A')
    track_name = spotify_data.get('name', 'N/A')

    apm_url = apple_manager.get_apple_music_url(track_name, artist_name)

    if not apm_url:
        click.echo("Could not find Apple Music URL", err=True)
        return

    click.echo(apm_url)
    