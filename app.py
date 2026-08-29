import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def fetch_one(query, params=()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# ---------- WEB PAGES ----------

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/food")
def food_page():
    try:
        return render_template("foodpg.html", food_centers=fetch_all(
            "SELECT * FROM food_centers ORDER BY food_id DESC"
        ))
    except Error as e:
        return render_template("foodpg.html", food_centers=[])

@app.route("/jobs")
def jobs_page():
    try:
        return render_template("jobs.html", jobs=fetch_all(
            "SELECT * FROM jobs ORDER BY job_id DESC"
        ))
    except Error:
        return render_template("jobs.html", jobs=[])

@app.route("/health")
def health_page():
    try:
        return render_template("healthhpage.html", hospitals=fetch_all(
            "SELECT * FROM hospitals ORDER BY hospital_id DESC"
        ))
    except Error:
        return render_template("healthhpage.html", hospitals=[])

@app.route("/schemes")
def schemes_page():
    try:
        return render_template("schemes.html", schemes=fetch_all(
            "SELECT * FROM schemes ORDER BY scheme_id DESC"
        ))
    except Error:
        return render_template("schemes.html", schemes=[])

@app.route("/nearby")
def nearby_page():
    return render_template("nearby.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profilepage.html")

    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    if not all([name, phone, location]):
        return jsonify(success=False, message="Please fill all fields"), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, phone, location) VALUES (%s, %s, %s)",
            (name.strip(), phone.strip(), location.strip())
        )
        conn.commit()
        return jsonify(success=True, message="Profile saved successfully",
                       user_id=cursor.lastrowid)
    except Error as e:
        if conn:
            conn.rollback()
        return jsonify(success=False, message="Database error. Check MySQL setup."), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ---------- API ----------

@app.get("/api/status")
def api_status():
    try:
        conn = get_connection()
        conn.close()
        return jsonify(success=True, message="Survival Hub Backend + MySQL are connected!")
    except Error:
        return jsonify(success=False, message="Backend is running, but MySQL is not connected."), 500

@app.get("/api/food")
def api_food():
    return jsonify(success=True, food_centers=fetch_all("SELECT * FROM food_centers"))

@app.get("/api/food/<int:food_id>")
def api_single_food(food_id):
    item = fetch_one("SELECT * FROM food_centers WHERE food_id=%s", (food_id,))
    if not item:
        return jsonify(success=False, message="Food center not found"), 404
    return jsonify(success=True, food=item)

@app.get("/api/hospitals")
def api_hospitals():
    return jsonify(success=True, hospitals=fetch_all("SELECT * FROM hospitals"))

@app.get("/api/hospitals/<int:hospital_id>")
def api_single_hospital(hospital_id):
    item = fetch_one("SELECT * FROM hospitals WHERE hospital_id=%s", (hospital_id,))
    if not item:
        return jsonify(success=False, message="Hospital not found"), 404
    return jsonify(success=True, hospital=item)

@app.get("/api/jobs")
def api_jobs():
    return jsonify(success=True, jobs=fetch_all("SELECT * FROM jobs"))

@app.get("/api/jobs/<int:job_id>")
def api_single_job(job_id):
    item = fetch_one("SELECT * FROM jobs WHERE job_id=%s", (job_id,))
    if not item:
        return jsonify(success=False, message="Job not found"), 404
    return jsonify(success=True, job=item)

@app.get("/api/schemes")
def api_schemes():
    return jsonify(success=True, schemes=fetch_all("SELECT * FROM schemes"))

@app.get("/api/schemes/<int:scheme_id>")
def api_single_scheme(scheme_id):
    item = fetch_one("SELECT * FROM schemes WHERE scheme_id=%s", (scheme_id,))
    if not item:
        return jsonify(success=False, message="Scheme not found"), 404
    return jsonify(success=True, scheme=item)

@app.post("/api/saved")
def api_save_item():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    item_type = data.get("item_type")
    item_id = data.get("item_id")
    if not all([user_id, item_type, item_id]):
        return jsonify(success=False, message="user_id, item_type and item_id are required"), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT saved_id FROM saved_items
               WHERE user_id=%s AND item_type=%s AND item_id=%s""",
            (user_id, item_type, item_id)
        )
        if cursor.fetchone():
            return jsonify(success=False, message="Item already saved"), 409
        cursor.execute(
            "INSERT INTO saved_items (user_id,item_type,item_id) VALUES (%s,%s,%s)",
            (user_id, item_type, item_id)
        )
        conn.commit()
        return jsonify(success=True, message="Item saved successfully")
    except Error:
        if conn: conn.rollback()
        return jsonify(success=False, message="Database error"), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.get("/api/saved/<int:user_id>")
def api_get_saved(user_id):
    return jsonify(success=True, saved_items=fetch_all(
        "SELECT * FROM saved_items WHERE user_id=%s ORDER BY saved_id DESC",
        (user_id,)
    ))

@app.delete("/api/saved/<int:saved_id>")
def api_delete_saved(saved_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM saved_items WHERE saved_id=%s", (saved_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(success=False, message="Saved item not found"), 404
        return jsonify(success=True, message="Saved item removed")
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
