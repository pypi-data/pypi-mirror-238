
def must(r, return_data=True):
    assert r.status_code == 200, 'http status {}: {}'.format(r.status_code, r.text)
    r = r.json()
    assert r['code'] == 0, 'code not 0: {}'.format(r)
    if return_data:
        return r['data']
    return r



