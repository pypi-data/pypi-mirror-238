import requests
import json


def action(server, command, player='FF:FF:FF:FF', id='squeeze-jrpc'):
    host, port = server
    data = dict(id=id,
                method='slim.request',
                params=[player, command])
    # print(json.dumps(data))
    return requests.post(
            f'http://{host}:{port}/jsonrpc.js',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data),
            timeout=30).json()['result']


def request(server, command, start, items_per_response, result_loop_field,
            result_count_field, player='FF:FF:FF:FF', id='squeeze-jrpc',
            tags=None, params=[]):
    host, port = server
    results = []
    while True:
        data = dict(id=id,
                    method='slim.request',
                    params=[player,
                            [command, start, items_per_response] + params
                            + ([f'tags:{tags}'] if tags else [])])
        # print(json.dumps(data))
        r = requests.post(
                f'http://{host}:{port}/jsonrpc.js',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data),
                timeout=30).json()['result']
        results += r.get(result_loop_field, [])
        if len(results) >= r[result_count_field]:
            r[result_loop_field] = results
            return r
        start += items_per_response
