from flask import Blueprint, request, current_app
import urllib.parse
import squeeze_jrpc.commands

bp = Blueprint('player', __name__, url_prefix='/players')


@bp.route('', methods=['GET'])
def players():
    player_names = squeeze_jrpc.commands.get_players(server())
    return {name: player_from_jrpc(
        squeeze_jrpc.commands.get_player_status(server(), name))
            for name in player_names}


@bp.route('/<name>', methods=['GET'])
def player_by_name(name):
    return player_from_jrpc(squeeze_jrpc.commands.get_player_status(
            server(), urllib.parse.unquote(name)))


@bp.route('/<name>', methods=['PATCH'])
def player_control(name):
    name = urllib.parse.unquote(name)
    changes = request.get_json()
    for key, value in changes.items():
        match key:
            case 'playback':
                if value not in ['play', 'pause']:
                    return {key: value}, 422
                status = squeeze_jrpc.commands.get_player_status(
                        server(), name)
                if value != status['mode']:
                    squeeze_jrpc.commands.player_pause(server(), name)
            case 'volume':
                squeeze_jrpc.commands.player_volume(server(), name, value)
            case 'current_track_index':
                match value:
                    case '+1':
                        squeeze_jrpc.commands.player_next(server(), name)
                    case '-1':
                        squeeze_jrpc.commands.player_prev(server(), name)
                    case _:
                        squeeze_jrpc.commands.player_playlist_index(
                                server(), name, value)
    return '', 204


@bp.route('/<name>/playlist', methods=['GET'])
def player_playlist(name):
    player_status = squeeze_jrpc.commands.get_player_status(server(), name)
    return {
            'current_track_index': int(player_status['playlist_cur_index']),
            'tracks': [track_from_jrpc(t)
                       for t in sorted(
                           player_status['playlist_loop'],
                           key=lambda t: t['playlist index'])]
            }


@bp.route('/<name>/playlist', methods=['PUT'])
def player_playlist_replace(name):
    squeeze_jrpc.commands.player_playlist_play(
            server(),
            name,
            album=int_or_none(request.args.get('album_id')),
            artist=int_or_none(request.args.get('artist_id')),
            tracks=(None if request.args.get('track_id') is None
                    else [int_or_none(t)
                          for t in request.args.getlist('track_id')]))
    return '', 204


def int_or_none(id):
    return None if id is None else int(id)


@bp.route('/<name>/playlist/<int:index>', methods=['DELETE'])
def player_playlist_index_delete(name, index):
    squeeze_jrpc.commands.player_playlist_remove(server(), name, index)
    return '', 204


@bp.route('/<name>/playlist/<int:index>', methods=['GET'])
def player_playlist_index(name, index):
    player_status = squeeze_jrpc.commands.get_player_status(server(), name)
    try:
        return track_from_jrpc(
                sorted(
                    player_status['playlist_loop'],
                    key=lambda t: t['playlist index'])[index])
    except IndexError:
        return '', 404


def server():
    return (current_app.config['LMS_HOST'], current_app.config['LMS_PORT'])


def track_from_jrpc(jrpc):
    return {
            'title': jrpc['title'],
            'album': jrpc['album'],
            'artist': jrpc['artist'],
            'id': jrpc['id'],
            }


repeat_states = ['none', 'track', 'playlist']
shuffle_states = ['none', 'tracks', 'albums']


def player_from_jrpc(jrpc):
    playlist_cur_index = jrpc.get('playlist_cur_index')
    playlist_cur_index = (None if playlist_cur_index is None
                          else int(playlist_cur_index))
    player = {
            'volume': jrpc.get('mixer volume'),
            'name': jrpc.get('player_name'),
            'playback': jrpc.get('mode'),
            'repeat': repeat_states[jrpc.get('playlist repeat')],
            'shuffle': shuffle_states[jrpc.get('playlist shuffle')],
            'playlist_tracks': jrpc.get('playlist_tracks'),
            'current_track_index': playlist_cur_index,
            'current_track': current_track_from_jrpc(jrpc),
            }
    return player


def current_track_from_jrpc(jrpc):
    playlist = jrpc.get('playlist_loop')
    if not playlist:
        return None
    cur_index = int(jrpc.get('playlist_cur_index'))
    cur_track = playlist[cur_index]
    return {
            'duration': jrpc.get('duration'),
            'elapsed_time': jrpc.get('time'),
            'id': cur_track['id'],
            'title': cur_track['title'],
            'album': cur_track['album'],
            'artist': cur_track['artist'],
            }
