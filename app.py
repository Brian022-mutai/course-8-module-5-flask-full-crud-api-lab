from flask import Flask, jsonify, request

app = Flask(__name__)


# ---------------------------
# Event class (simulated model)
# ---------------------------
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# ---------------------------
# In-memory data store
# ---------------------------
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Tracks the next id to assign to a new event
next_id = 3


# ---------------------------
# Helper function: find an event by id
# ---------------------------
def find_event(event_id):
    """Return the Event with the given id, or None if not found."""
    for event in events:
        if event.id == event_id:
            return event
    return None


# ---------------------------
# Root route - welcome message
# ---------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Events API"}), 200


# ---------------------------
# GET /events - list all events
# ---------------------------
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# ---------------------------
# GET /events/<id> - get a single event
# ---------------------------
@app.route("/events/<int:id>", methods=["GET"])
def get_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict()), 200


# ---------------------------
# POST /events - create a new event
# ---------------------------
@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    data = request.get_json(silent=True)

    # Validate that a JSON body with a "title" key was provided
    if not data or not data.get("title"):
        return jsonify({"error": "The 'title' field is required"}), 400

    new_event = Event(next_id, data["title"])
    events.append(new_event)
    next_id += 1

    return jsonify(new_event.to_dict()), 201


# ---------------------------
# PATCH /events/<id> - update an event's title
# ---------------------------
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "The 'title' field is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# ---------------------------
# DELETE /events/<id> - remove an event
# ---------------------------
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return jsonify({"message": f"Event {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)