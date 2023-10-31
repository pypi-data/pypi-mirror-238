from flask import Blueprint, request, current_app
import squeeze_jrpc.queries

bp = Blueprint('library', __name__, url_prefix='/library')


@bp.route('/artists')
def artists_search():
    return squeeze_jrpc.queries.artists(
            server(), sanitise_query_params(request.args))


@bp.route('/tracks')
def tracks_search():
    return squeeze_jrpc.queries.tracks(
            server(), sanitise_query_params(request.args))


@bp.route('/albums')
def albums_search():
    return squeeze_jrpc.queries.albums(
            server(), sanitise_query_params(request.args))


def server():
    return (current_app.config['LMS_HOST'], current_app.config['LMS_PORT'])


def sanitise_query_params(params):
    return {k: v for k, v in params.items()
            if k in ['search', 'track_id', 'album_id', 'artist_id']}
