"""
TicketBook — учебный API для интеграционного тестирования
Модули: M1 Auth | M2 Catalog | M3 Booking | M4 Payment
Запуск: python ticketbook_server.py
Адрес: http://localhost:5000
"""

from flask import Flask, request, jsonify
import uuid, time

app = Flask(__name__)

# ──────────────────────────────────────────────
# БД в памяти
# ──────────────────────────────────────────────
USERS = {
    "user@test.com": {"password": "Test1234!", "name": "Test User"}
}

SESSIONS = {}   # token -> email

EVENTS = {
    1: {"id": 1, "title": "Концерт Ария",       "date": "2025-08-10", "category": "concert", "price": 5000},
    2: {"id": 2, "title": "Театр. Гамлет",       "date": "2025-08-15", "category": "theatre", "price": 3500},
    3: {"id": 3, "title": "Кино. Дюна 3",        "date": "2025-08-20", "category": "cinema",  "price": 1800},
    4: {"id": 4, "title": "Концерт Кино",        "date": "2025-09-01", "category": "concert", "price": 6000},
    5: {"id": 5, "title": "Фестиваль Jazz",      "date": "2025-09-12", "category": "concert", "price": 4200},
}

BOOKINGS = {}   # booking_id -> {event_id, user, status}
_booking_counter = [1]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def get_token(req):
    auth = req.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None

def validate_token(req):
    token = get_token(req)
    if not token or token not in SESSIONS:
        return None, jsonify({"error": "Unauthorized", "message": "Invalid or missing session token"}), 401
    return SESSIONS[token], None, None


# ──────────────────────────────────────────────
# M1 AUTH
# ──────────────────────────────────────────────
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "User")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    if email in USERS:
        return jsonify({"error": "User already exists"}), 409

    USERS[email] = {"password": password, "name": name}
    return jsonify({"message": "User registered successfully", "email": email}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "")
    password = data.get("password", "")

    user = USERS.get(email)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = "tok_" + str(uuid.uuid4()).replace("-", "")
    SESSIONS[token] = email
    return jsonify({
        "message": "Login successful",
        "session_token": token,
        "user": {"email": email, "name": user["name"]}
    }), 200


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    token = get_token(request)
    if token and token in SESSIONS:
        del SESSIONS[token]
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"error": "No active session"}), 400


# ──────────────────────────────────────────────
# M2 CATALOG
# ──────────────────────────────────────────────
@app.route("/api/catalog/events", methods=["GET"])
def get_events():
    category = request.args.get("category")
    date = request.args.get("date")
    events = list(EVENTS.values())
    if category:
        events = [e for e in events if e["category"] == category]
    if date:
        events = [e for e in events if e["date"] == date]
    return jsonify({"events": events, "total": len(events)}), 200


@app.route("/api/catalog/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = EVENTS.get(event_id)
    if not event:
        return jsonify({"error": "Event not found", "event_id": event_id}), 404
    return jsonify(event), 200


# ──────────────────────────────────────────────
# M3 BOOKING
# ──────────────────────────────────────────────
@app.route("/api/booking/create", methods=["POST"])
def create_booking():
    email, err, code = validate_token(request)
    if err:
        return err, code

    data = request.get_json() or {}
    event_id = data.get("event_id")

    if not event_id:
        return jsonify({"error": "event_id is required"}), 400

    if event_id not in EVENTS:
        return jsonify({"error": "Event not found", "event_id": event_id}), 404

    booking_id = _booking_counter[0]
    _booking_counter[0] += 1
    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "event_id": event_id,
        "user": email,
        "status": "pending",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    return jsonify({
        "message": "Booking created",
        "booking_id": booking_id,
        "event_id": event_id,
        "status": "pending"
    }), 200


@app.route("/api/booking/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    email, err, code = validate_token(request)
    if err:
        return err, code

    booking = BOOKINGS.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify(booking), 200


@app.route("/api/booking/cancel", methods=["POST"])
def cancel_booking():
    email, err, code = validate_token(request)
    if err:
        return err, code

    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    booking = BOOKINGS.get(booking_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    if booking["status"] == "paid":
        return jsonify({"error": "Cannot cancel a paid booking"}), 409

    booking["status"] = "cancelled"
    return jsonify({"message": "Booking cancelled", "booking_id": booking_id, "status": "cancelled"}), 200


@app.route("/api/booking/list", methods=["GET"])
def list_bookings():
    email, err, code = validate_token(request)
    if err:
        return err, code

    user_bookings = [b for b in BOOKINGS.values() if b["user"] == email]
    return jsonify({"bookings": user_bookings, "total": len(user_bookings)}), 200


# ──────────────────────────────────────────────
# M4 PAYMENT
# ──────────────────────────────────────────────
@app.route("/api/payment/pay", methods=["POST"])
def pay():
    email, err, code = validate_token(request)
    if err:
        return err, code

    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    card_token = data.get("card_token", "")

    booking = BOOKINGS.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # TC-INT-05: двойная оплата
    if booking["status"] == "paid":
        return jsonify({"error": "Booking already paid", "booking_id": booking_id}), 409

    if booking["status"] == "cancelled":
        return jsonify({"error": "Cannot pay for a cancelled booking"}), 409

    # TC-INT-06: карта отклонена
    if card_token == "tok_test_decline":
        booking["status"] = "failed"
        return jsonify({
            "payment_status": "declined",
            "booking_id": booking_id,
            "message": "Card declined by payment provider"
        }), 402

    # TC-INT-04: успешная оплата
    booking["status"] = "paid"
    return jsonify({
        "payment_status": "success",
        "booking_id": booking_id,
        "message": "Payment successful",
        "status": "paid"
    }), 200


# ──────────────────────────────────────────────
# Запуск
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🎫 TicketBook API запущен!")
    print("📍 http://localhost:5000\n")
    print("Модули:")
    print("  M1 Auth    → /api/auth/...")
    print("  M2 Catalog → /api/catalog/...")
    print("  M3 Booking → /api/booking/...")
    print("  M4 Payment → /api/payment/...\n")
    app.run(debug=True, port=5000)
