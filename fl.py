from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

HEADERS = {
    'accept': '*/*',
    'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    'x-asbd-id': '129477',
    'x-csrftoken': 'mFcLz5S7aKKvWLBOWjTVqtpJAGYmjgqg',
    'x-ig-app-id': '936619743392459',
    'x-requested-with': 'XMLHttpRequest',
}

API_URL = 'https://www.instagram.com/api/v1/users/web_profile_info/'

@app.route('/instagram', methods=['GET'])
def get_instagram_info():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    params = {'username': username}
    response = requests.get(API_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data', 'status_code': response.status_code}), response.status_code

    try:
        info = response.json()['data']['user']
        result = {
            'name': info['full_name'],
            'username': info['username'],
            'verified': info['is_verified'],
            'private': info['is_private'],
            'followers': info["edge_followed_by"]["count"],
            'following': info["edge_follow"]["count"],
            'bio': info['biography'],
            'profile_picture': info["profile_pic_url_hd"]
        }
        return jsonify(result)
    except KeyError:                                                            return jsonify({'error': 'Invalid response structure'}), 500    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)