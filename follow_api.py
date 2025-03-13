from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Follow API is running!"

@app.route('/isfollowing', methods=['GET'])
def is_following():
    follower_id = request.args.get('followerId')
    followee_id = request.args.get('followeeId')

    if not follower_id or not followee_id:
        return jsonify({'error': 'Missing followerId or followeeId'}), 400

    # Roblox endpoint for followers
    url = f'https://friends.roblox.com/v1/users/{follower_id}/followings?limit=100'

    try:
        response = requests.get(url)
        data = response.json()

        following_list = data.get('data', [])
        
        # Check if followee is in the following list
        for user in following_list:
            if str(user['id']) == followee_id:
                return jsonify({'isFollowing': True})

        return jsonify({'isFollowing': False})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
