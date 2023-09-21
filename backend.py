# backend.py
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define data structures to store votes and squad information
teams = {}
squad_areas = ["Delivering Value", "Operational Stability", "Fun", "Provider Collaboration", "Learning", "Mission", "Pawns or Players", "Speed", "Suitable Process", "Support", "Teamwork"]

# Route to submit votes
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    team_name = data['team_name']
    votes = data['votes']
    teams[team_name] = votes
    return jsonify({"message": "Vote submitted successfully"})


# Route to get vote summary
@app.route('/vote_summary', methods=['GET'])
def vote_summary():
    squad_vote_summary = {}
    for area in squad_areas:
        area_votes = {team: teams[team][area] for team in teams}
        green_count = sum(1 for color in area_votes.values() if color == 'Green')
        yellow_count = sum(1 for color in area_votes.values() if color == 'Yellow')
        red_count = sum(1 for color in area_votes.values() if color == 'Red')

        # Calculate the trend (positive if more Green votes, negative if more Red votes)
        trend = green_count - red_count

        # Determine the color based on the majority of votes
        if green_count > yellow_count and green_count > red_count:
            color = 'Green'
        elif yellow_count > green_count and yellow_count > red_count:
            color = 'Yellow'
        else:
            color = 'Red'

        squad_vote_summary[area] = {
            "color": color,
            "trend": trend
        }

    return jsonify(squad_vote_summary)


@app.route('/')
def index():
    return render_template('index.html', squad_areas=squad_areas)

if __name__ == '__main__':
    app.run(debug=True)
