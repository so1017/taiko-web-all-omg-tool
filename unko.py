import requests
import uuid
import json
import threading

session = requests.Session()
cookies = {
    'session': str(uuid.uuid4()),
}
headers = {
    'accept': '*/*',
    'accept-language': 'ja,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://cjdgrevival.com',
    'priority': 'u=1, i',
    'referer': 'https://cjdgrevival.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-csrftoken': '',
}
re = session.get('https://cjdgrevival.com/api/csrftoken',cookies=cookies,headers=headers)
token = re.json()['token']
print('全良ツール(全曲) cjdgrevival.com')
username = input('ユーザー名: ')
password = input('パスワード: ')
headers['x-csrftoken'] = token
json_data = {
    'username': username,
    'password': password,
    'remember': True,
}
response = requests.post('https://cjdgrevival.com/api/login', cookies=session.cookies, headers=headers, json=json_data)
re = requests.get('https://cjdgrevival.com/api/csrftoken',cookies=cookies,headers=headers)
token = re.json()['token']
headers['x-csrftoken'] = token
with open("songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

score_string = "29cd6,1w,0,0,1w,j,1;" * 5
score_string = score_string.rstrip(";")

batch_size = 10
thread_count = 10

def send_batch(batch_index, batch_songs):
    scores = [{"hash": song["hash"], "score": score_string} for song in batch_songs]
    json_data = {"scores": scores}
    try:
        requests.post('https://cjdgrevival.com/api/scores/save', headers=headers, cookies=cookies, json=json_data)
    except requests.exceptions.RequestException as e:
        print(f"エラーが出たよ")

batches = [songs[i:i + batch_size] for i in range(0, len(songs), batch_size)]

threads = []
for i, batch in enumerate(batches):
    t = threading.Thread(target=send_batch, args=(i + 1, batch))
    threads.append(t)
    t.start()
    if len(threads) == thread_count:
        for th in threads:
            th.join()
        threads = []

for th in threads:
    th.join()

print("All done.")