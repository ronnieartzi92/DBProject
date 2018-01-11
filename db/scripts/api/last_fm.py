from urllib.request import urlopen, Request

import db.scripts.api.general as general


def check_connectivity():
    request = Request("http://ws.audioscrobbler.com//2.0/?method=chart.gettoptags&api_key={0}&limit={1}&format=json".format(
                      general.last_fm_creds.get('API_key'), '1000'))

    response_body = urlopen(request).read()
    print(response_body)

check_connectivity()
