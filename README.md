# Bifrost 

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://python.org)

**Bifrost** is a powerful command-line utility that bridges the gap between music streaming services. Convert music URLs between Apple Music and Spotify, get detailed track information.

## 🚀 Installation

### Prerequisites

- Python 3.14 or higher
- A Spotify Developer Account (for API access)

### Install from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bifrost.git
   cd bifrost
   ```

2. **Install using uv (recommended):**
   ```bash
   uv sync
   ```

3. **Build and install:**
   ```bash
   make build
   ```

### Alternative Installation

## 🔧 Configuration

### Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note down your `Client ID` and `Client Secret`
4. Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SPOTIFY_CLIENT_ID` | Yes | Your Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Yes | Your Spotify app client secret |

## 📖 Usage

Bifrost provides separate command groups for Apple Music and Spotify operations:

```bash
bifrost --help
```

### Apple Music Commands

#### Get Track Information
```bash
# Pretty output (default)
bifrost apple track-info "https://music.apple.com/us/album/song-name/123456?i=789"

# JSON output
bifrost apple track-info "https://music.apple.com/us/album/song-name/123456?i=789" --output json
```

#### Convert Apple Music to Spotify
```bash
bifrost apple convert "https://music.apple.com/us/album/song-name/123456?i=789"
```

### Spotify Commands

#### Get Track Information
```bash
# Pretty output (default)
bifrost spotify track-info "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh"

# JSON output
bifrost spotify track-info "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh" --output json
```

#### Convert Spotify to Apple Music
```bash
bifrost spotify convert "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh"
```
