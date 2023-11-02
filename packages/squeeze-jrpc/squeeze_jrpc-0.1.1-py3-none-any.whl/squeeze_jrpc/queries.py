import squeeze_jrpc.protocol.slim as slim


def albums(server, params):
    r = slim.request(server, 'albums', 0, 50, 'albums_loop', 'count',
                     tags='lajSy',
                     params=[f'{k}:{v}' for k, v in params.items()])
    return r['albums_loop']


def artists(server, params):
    r = slim.request(server, 'artists', 0, 50, 'artists_loop', 'count',
                     params=[f'{k}:{v}' for k, v in params.items()])
    return r['artists_loop']


def tracks(server, params):
    r = slim.request(server, 'tracks', 0, 50, 'titles_loop', 'count',
                     tags='aJlcesy',
                     params=[f'{k}:{v}' for k, v in params.items()])
    return r['titles_loop']
