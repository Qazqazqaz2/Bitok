import requests

from proxy import Proxy_get
from bs4 import BeautifulSoup as BS

import random
import json
import re

session, http = Proxy_get().get_session()

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, '', str(raw_html))
    return cleantext

def get_info_item(lst='["4557628"]'):
    ip = random.randint(0, len(http) - 1)
    url = 'https://zaycev.net/api/external/track/filezmeta'
    headers = {
            'authority': 'zaycev.net',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://zaycev.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://zaycev.net/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'user_id=588de01e-aaf3-48e7-b22e-23f2042398f9; provider=; sid=fe036537-8065-410c-a1ff-1f88a2071254; _ns_clientId=709713870090328021; _ns_abVar=DoubleStep.A; _ym_uid=1651829290928590430; _ym_d=1651829290; tmr_lvid=b7806b8915dc53dbbf335c41f5b99288; tmr_lvidTS=1651829290176; _ym_visorc=b; _ym_isad=2; _ga=GA1.2.1230947326.1651829294; _gid=GA1.2.1681764552.1651829294; adBoxFirst=1; firstPageSession=1; notsy_session_counter=1; notsy_interstitial_shown=1; tmr_detect=0%7C1651829971980; tmr_reqNum=34; isMobile=1'
        }
    lst = str(lst).replace("'", '"')
    data = '{"trackIds":'+str(lst)+',"subscription":false}'
    r = session.request('POST', url=url, headers=headers, data=data, proxies={
    'http': http[ip]}).json()
    items = r['tracks']
    links = get_links_tracks(items)
    return get_tracks_results(links)

def get_tracks_results(links):
    results = set()
    for link in links:
        link = session.get(link).text
        results.add(link)
    return results

def get_links_tracks(items):
    set_links = set()
    for item in items:
        download = item["download"]
        if download != False:
            link = 'https://zaycev.net/api/external/track/download/'+ download
            set_links.add(link)
        else:
            print(False)
    return set_links

def get_art_tracks(query='', page=1):
    url = f'https://zaycev.net/api/external/pages/artist/{query}/tracks?page={page}&sort=popularity&limit=10'
    print(url)
    headers = {
        'authority': 'zaycev.net',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://zaycev.net/artist/{query}',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'user_id=588de01e-aaf3-48e7-b22e-23f2042398f9; provider=; sid=fe036537-8065-410c-a1ff-1f88a2071254; _ns_clientId=709713870090328021; _ns_abVar=DoubleStep.A; _ym_uid=1651829290928590430; _ym_d=1651829290; tmr_lvid=b7806b8915dc53dbbf335c41f5b99288; tmr_lvidTS=1651829290176; _ga=GA1.2.1230947326.1651829294; adBoxFirst=1; notsy_session_counter=1; isMobile=0; _gid=GA1.2.84675349.1652083659; notsy_interstitial_shown=1; tmr_detect=0%7C1652083670016; _ym_isad=2; tmr_reqNum=143'
    }
    req = session.request("GET", url=url, headers=headers).json()
    pagesCount = req["pagesCount"]
    datas = req['tracksInfo']
    res = []
    artists = []
    names = []
    for data in datas:
        print(data)
        block = datas[data]
        artist = block['artistName']
        track_name = block['track']
        res.append(data)
        artists.append(artist)
        names.append(track_name)
    res = str(res)
    return list(get_info_item(res)), artists, names, [page, pagesCount]


def get_tracks(query='', page=1):
    query = query.replace(' ', '%20')
    headers = {
        'authority': 'zaycev.net',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://zaycev.net/search.html?query_search={query}',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'user_id=588de01e-aaf3-48e7-b22e-23f2042398f9; provider=; sid=fe036537-8065-410c-a1ff-1f88a2071254; _ns_clientId=709713870090328021; _ns_abVar=DoubleStep.A; _ym_uid=1651829290928590430; _ym_d=1651829290; tmr_lvid=b7806b8915dc53dbbf335c41f5b99288; tmr_lvidTS=1651829290176; _ga=GA1.2.1230947326.1651829294; adBoxFirst=1; notsy_session_counter=1; _ym_isad=1; isMobile=1; firstPageSession=1; tmr_reqNum=85; notsy_interstitial_shown=1; _ym_visorc=b; _gid=GA1.2.1338723432.1651929737; _gat_gtag_UA_39219306_1=1; tmr_detect=0%7C1651929739048'
        }
    req = session.request('GET', url=f'https://zaycev.net/api/external/pages/search/tracks?q={query}&page={page}&limit=10', headers=headers).text
    req = json.loads(cleanhtml(req))
    datas = req['tracksInfo']
    res = []
    artists = []
    names = []
    for data in datas:
        block = datas[data]
        artist = block['artistName']
        track_name = block['track']
        res.append(data)
        artists.append(artist)
        names.append(track_name)
    res = str(res)
    return list(get_info_item(res)), artists, names, page, query

def get_artists(query='',art_page=0):
    headers = {
        'authority': 'zaycev.net',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://zaycev.net/search.html?query_search={query}',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'user_id=588de01e-aaf3-48e7-b22e-23f2042398f9; provider=; sid=fe036537-8065-410c-a1ff-1f88a2071254; _ns_clientId=709713870090328021; _ns_abVar=DoubleStep.A; _ym_uid=1651829290928590430; _ym_d=1651829290; tmr_lvid=b7806b8915dc53dbbf335c41f5b99288; tmr_lvidTS=1651829290176; _ga=GA1.2.1230947326.1651829294; adBoxFirst=1; notsy_session_counter=1; _ym_isad=1; isMobile=1; firstPageSession=1; tmr_reqNum=85; notsy_interstitial_shown=1; _ym_visorc=b; _gid=GA1.2.1338723432.1651929737; _gat_gtag_UA_39219306_1=1; tmr_detect=0%7C1651929739048'
        }
    req_artists = session.request('GET', url=f"https://zaycev.net/api/external/pages/search/artists?q={query}&page={art_page}", headers=headers).json()
    blocks = req_artists['list']
    art_ids = []
    art_names = []
    art_tracks = []
    for block in blocks:
        art_tracks.append(block['trackCount'])
        art_names.append(block['name'])
        art_ids.append(block['id'])
    return art_ids, art_names, art_tracks

if __name__ == '__main__':
    print(get_tracks('squore'))