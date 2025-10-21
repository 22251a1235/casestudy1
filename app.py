from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'music_playlist_secret_key_2025'

# Data storage (in production, use a database)
PLAYLISTS_FILE = 'playlists.json'

def load_playlists():
    """Load playlists from JSON file"""
    if os.path.exists(PLAYLISTS_FILE):
        try:
            with open(PLAYLISTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_playlists(playlists):
    """Save playlists to JSON file"""
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f, indent=2)

@app.route('/')
def index():
    """Home page"""
    playlists = load_playlists()
    total_playlists = len(playlists)
    total_songs = sum(len(p.get('songs', [])) for p in playlists)
    return render_template('index.html', 
                         total_playlists=total_playlists, 
                         total_songs=total_songs)

@app.route('/playlists')
def playlists():
    """View all playlists"""
    all_playlists = load_playlists()
    return render_template('playlists.html', playlists=all_playlists)

@app.route('/create', methods=['GET', 'POST'])
def create_playlist():
    """Create a new playlist"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        genre = request.form.get('genre')
        
        if name:
            playlists = load_playlists()
            new_playlist = {
                'id': len(playlists) + 1,
                'name': name,
                'description': description,
                'genre': genre,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'songs': []
            }
            playlists.append(new_playlist)
            save_playlists(playlists)
            flash(f'Playlist "{name}" created successfully!', 'success')
            return redirect(url_for('playlists'))
        else:
            flash('Playlist name is required!', 'error')
    
    return render_template('create.html')

@app.route('/playlist/<int:playlist_id>')
def view_playlist(playlist_id):
    """View a specific playlist"""
    playlists = load_playlists()
    playlist = next((p for p in playlists if p['id'] == playlist_id), None)
    
    if playlist:
        return render_template('view_playlist.html', playlist=playlist)
    else:
        flash('Playlist not found!', 'error')
        return redirect(url_for('playlists'))

@app.route('/playlist/<int:playlist_id>/add_song', methods=['POST'])
def add_song(playlist_id):
    """Add a song to a playlist"""
    song_title = request.form.get('song_title')
    artist = request.form.get('artist')
    duration = request.form.get('duration')
    
    if song_title and artist:
        playlists = load_playlists()
        playlist = next((p for p in playlists if p['id'] == playlist_id), None)
        
        if playlist:
            new_song = {
                'id': len(playlist.get('songs', [])) + 1,
                'title': song_title,
                'artist': artist,
                'duration': duration if duration else '3:30'
            }
            if 'songs' not in playlist:
                playlist['songs'] = []
            playlist['songs'].append(new_song)
            save_playlists(playlists)
            flash(f'Song "{song_title}" added successfully!', 'success')
        else:
            flash('Playlist not found!', 'error')
    else:
        flash('Song title and artist are required!', 'error')
    
    return redirect(url_for('view_playlist', playlist_id=playlist_id))

@app.route('/playlist/<int:playlist_id>/delete', methods=['POST'])
def delete_playlist(playlist_id):
    """Delete a playlist"""
    playlists = load_playlists()
    playlists = [p for p in playlists if p['id'] != playlist_id]
    save_playlists(playlists)
    flash('Playlist deleted successfully!', 'success')
    return redirect(url_for('playlists'))

@app.route('/search')
def search():
    """Search playlists and songs"""
    query = request.args.get('q', '').lower()
    playlists = load_playlists()
    
    if query:
        results = []
        for playlist in playlists:
            # Check if query matches playlist name or description
            if query in playlist['name'].lower() or query in playlist.get('description', '').lower():
                results.append(playlist)
            else:
                # Check if query matches any song in the playlist
                for song in playlist.get('songs', []):
                    if query in song['title'].lower() or query in song['artist'].lower():
                        results.append(playlist)
                        break
        return render_template('search.html', playlists=results, query=query)
    
    return render_template('search.html', playlists=[], query='')

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return {'status': 'healthy', 'app': 'Music Playlist Manager'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

