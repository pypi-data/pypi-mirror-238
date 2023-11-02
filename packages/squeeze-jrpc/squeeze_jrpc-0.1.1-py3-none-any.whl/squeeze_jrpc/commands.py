import squeeze_jrpc.protocol.slim as slim


def player_pause(server, name):
    slim.action(server, ['pause'], player=name)


def player_next(server, name):
    slim.action(server, ['playlist', 'index', '+1'], player=name)


def player_prev(server, name):
    slim.action(server, ['playlist', 'index', '-1'], player=name)


def player_playlist_index(server, name, index):
    slim.action(server, ['playlist', 'index', index], player=name)


def player_playlist_remove(server, name, index):
    slim.action(server, ['playlist', 'delete', index], player=name)


def player_playlist_play(server, name, tracks=None, album=None, artist=None):
    return player_playlistcontrol(server, name, 'load', tracks, album, artist)


def player_playlist_add(server, name, tracks=None, album=None, artist=None):
    return player_playlistcontrol(server, name, 'add', tracks, album, artist)


def player_playlist_insert(server, name, tracks=None, album=None, artist=None):
    return player_playlistcontrol(
            server, name, 'insert', tracks, album, artist)


def player_playlist_playnext(
        server, name, tracks=None, album=None, artist=None):
    return player_playlistcontrol(
            server, name, 'insert', tracks, album, artist)


def player_playlistcontrol(server, name, cmd, tracks, album, artist):
    track_id = ([f'track_id:{",".join([f"{t}" for t in tracks])}']
                if tracks else [])
    album_id = [f'album_id:{album}'] if album else []
    artist_id = [f'artist_id:{artist}'] if artist else []
    try:
        return slim.action(server,
                           ['playlistcontrol', f'cmd:{cmd}']
                           + album_id + artist_id + track_id,
                           player=name)['count']
    except Exception:  # TODO: catch a more specific exception?
        return 0


def player_volume(server, name, volume):
    slim.action(server, ['mixer', 'volume', volume], player=name)


def player_shuffle(server, name, mode):
    slim.action(server, ['playlist', 'shuffle', mode], player=name)


def player_repeat(server, name, mode):
    slim.action(server, ['playlist', 'repeat', mode], player=name)


def get_player_status(server, name):
    return slim.request(server, 'status', 0, 10, 'playlist_loop',
                        'playlist_tracks', player=name, tags='aJlces')


def get_players(server):
    r = slim.request(server, 'players', 0, 10, 'players_loop', 'count')
    return [p['name'] for p in r['players_loop']]
