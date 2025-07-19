import click
import sys
from pathlib import Path
from src.cli.providers.apple import apple

# Add the parent directory to sys.path so we can import services
sys.path.insert(0, str(Path(__file__).parent.parent))

@click.group()
def bifrost():
    "Bifrost 🥶"
    pass



bifrost.add_command(apple)




# @spotify.command()
# @click.option('--client-id', prompt=True, help='Spotify Client ID')
# @click.option('--client-secret', prompt=True, hide_input=True, help='Spotify Client Secret')
# @click.option('--save-credentials', is_flag=True, help='Save credentials to .env file')
# def auth(client_id, client_secret, save_credentials):
#     """Authenticate with Spotify API"""
#     try:
#         spotify_manager = SpotifyManager(client_id, client_secret)
        
#         click.echo("🔄 Authenticating with Spotify...")
#         if spotify_manager.get_auth_token():
#             click.echo("✅ Successfully authenticated with Spotify!")
            
#             if save_credentials:
#                 env_path = Path('.env')
#                 env_content = f"SPOTIFY_CLIENT_ID={client_id}\nSPOTIFY_CLIENT_SECRET={client_secret}\n"
                
#                 if env_path.exists():
#                     with open(env_path, 'r') as f:
#                         existing_content = f.read()
                    
#                     # Remove existing Spotify credentials if they exist
#                     lines = existing_content.split('\n')
#                     lines = [line for line in lines if not line.startswith('SPOTIFY_CLIENT_ID=') and not line.startswith('SPOTIFY_CLIENT_SECRET=')]
#                     env_content = '\n'.join(lines) + '\n' + env_content
                
#                 with open(env_path, 'w') as f:
#                     f.write(env_content)
                
#                 click.echo("💾 Credentials saved to .env file")
#         else:
#             click.echo("❌ Authentication failed", err=True)
            
#     except Exception as e:
#         click.echo(f"❌ Error: {str(e)}", err=True)


# @spotify.command()
# @click.option('--client-id', help='Spotify Client ID (or set SPOTIFY_CLIENT_ID env var)')
# @click.option('--client-secret', help='Spotify Client Secret (or set SPOTIFY_CLIENT_SECRET env var)')
# def test_auth(client_id, client_secret):
#     """Test Spotify authentication with existing credentials"""
#     try:
#         # Try to get credentials from environment variables first
#         if not client_id:
#             client_id = os.getenv('SPOTIFY_CLIENT_ID')
#         if not client_secret:
#             client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
#         if not client_id or not client_secret:
#             click.echo("❌ Please provide client ID and secret via options or environment variables", err=True)
#             click.echo("Environment variables: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET")
#             return
        
#         spotify_manager = SpotifyManager(client_id, client_secret)
        
#         click.echo("🔄 Testing Spotify authentication...")
#         if spotify_manager.get_auth_token():
#             click.echo("✅ Spotify authentication successful!")
#         else:
#             click.echo("❌ Spotify authentication failed", err=True)
            
#     except Exception as e:
#         click.echo(f"❌ Error: {str(e)}", err=True)


# @cli.command()
# def config():
#     """Show current configuration"""
#     click.echo("📋 Current Configuration:")
    
#     # Check for .env file
#     env_path = Path('.env')
#     if env_path.exists():
#         click.echo(f"  .env file: ✅ Found at {env_path.absolute()}")
#         with open(env_path, 'r') as f:
#             content = f.read()
#             if 'SPOTIFY_CLIENT_ID' in content:
#                 click.echo("  Spotify Client ID: ✅ Set in .env")
#             else:
#                 click.echo("  Spotify Client ID: ❌ Not set in .env")
            
#             if 'SPOTIFY_CLIENT_SECRET' in content:
#                 click.echo("  Spotify Client Secret: ✅ Set in .env")
#             else:
#                 click.echo("  Spotify Client Secret: ❌ Not set in .env")
#     else:
#         click.echo("  .env file: ❌ Not found")
    
#     # Check environment variables
#     if os.getenv('SPOTIFY_CLIENT_ID'):
#         click.echo("  SPOTIFY_CLIENT_ID env var: ✅ Set")
#     else:
#         click.echo("  SPOTIFY_CLIENT_ID env var: ❌ Not set")
    
#     if os.getenv('SPOTIFY_CLIENT_SECRET'):
#         click.echo("  SPOTIFY_CLIENT_SECRET env var: ✅ Set")
#     else:
#         click.echo("  SPOTIFY_CLIENT_SECRET env var: ❌ Not set")


if __name__ == '__main__':
    bifrost()
