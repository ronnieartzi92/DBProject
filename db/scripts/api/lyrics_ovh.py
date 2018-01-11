from urllib.request import urlopen, Request

def check_connectivity():
    request = Request('https://api.lyrics.ovh/v1/Coldplay/Adventure_of_a_Lifetime')

    response_body = urlopen(request).read()
    print(response_body)

check_connectivity()

