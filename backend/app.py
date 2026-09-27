from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


app = Flask(__name__)
CORS(app)


# =========================================================
# MYSQL CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# =========================================================
# UI PAGES
# =========================================================

@app.route("/")
def home():
    return render_template("main.html")


# ---------------- FOOD PAGE ----------------

@app.route("/food-page")
def food_page():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                food_id,
                center_name,
                location,
                phone,
                latitude,
                longitude
            FROM food_centers
        """)

        food_centers = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "foodpg.html",
            food_centers=food_centers
        )

    except Exception as e:

        print("Food page error:", e)

        return render_template(
            "foodpg.html",
            food_centers=[]
        )


# ---------------- JOBS PAGE ----------------

@app.route("/jobs-page")
def jobs_page():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                job_id,
                job_title,
                company,
                location,
                contact
            FROM jobs
        """)

        jobs = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "jobs.html",
            jobs=jobs
        )

    except Exception as e:

        print("Jobs page error:", e)

        return render_template(
            "jobs.html",
            jobs=[]
        )


# ---------------- HEALTH PAGE ----------------

@app.route("/health-page")
def health_page():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                hospital_id,
                hospital_name,
                location,
                phone,
                latitude,
                longitude
            FROM hospitals
        """)

        hospitals = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "healthhpage.html",
            hospitals=hospitals
        )

    except Exception as e:

        print("Health page error:", e)

        return render_template(
            "healthhpage.html",
            hospitals=[]
        )


# ---------------- SCHEMES PAGE ----------------

@app.route("/schemes-page")
def schemes_page():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM schemes
        """)

        schemes = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "schemes.html",
            schemes=schemes
        )

    except Exception as e:

        print("Schemes page error:", e)

        return render_template(
            "schemes.html",
            schemes=[]
        )


# ---------------- NEARBY PAGE ----------------

@app.route("/nearby")
def nearby_page():
    return render_template("nearby.html")


# ---------------- PROFILE PAGE ----------------

@app.route("/profile-page")
def profile_page():
    return render_template("profilepage.html")


# =========================================================
# PROFILE API
# =========================================================

@app.route("/profile", methods=["POST"])
def save_profile():

    data = request.get_json() or {}

    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    if not name or not phone or not location:

        return jsonify({
            "success": False,
            "message": "Please fill all fields"
        }), 400

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users
            (name, phone, location)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, phone, location)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Profile saved successfully"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# GET PROFILE API
# =========================================================

@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:

            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        return jsonify({
            "success": True,
            "user": user
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# FOOD API
# =========================================================

@app.route("/food", methods=["GET"])
def get_food():

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM food_centers"
        )

        food = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "food_centers": food
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SINGLE FOOD API
# =========================================================

@app.route("/food/<int:food_id>", methods=["GET"])
def get_single_food(food_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM food_centers
            WHERE food_id = %s
            """,
            (food_id,)
        )

        food = cursor.fetchone()

        cursor.close()
        conn.close()

        if not food:

            return jsonify({
                "success": False,
                "message": "Food center not found"
            }), 404

        return jsonify({
            "success": True,
            "food": food
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# HOSPITALS API
# =========================================================

@app.route("/hospitals", methods=["GET"])
def get_hospitals():

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM hospitals"
        )

        hospitals = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "hospitals": hospitals
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SINGLE HOSPITAL API
# =========================================================

@app.route("/hospitals/<int:hospital_id>", methods=["GET"])
def get_single_hospital(hospital_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM hospitals
            WHERE hospital_id = %s
            """,
            (hospital_id,)
        )

        hospital = cursor.fetchone()

        cursor.close()
        conn.close()

        if not hospital:

            return jsonify({
                "success": False,
                "message": "Hospital not found"
            }), 404

        return jsonify({
            "success": True,
            "hospital": hospital
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# JOBS API
# =========================================================

@app.route("/jobs", methods=["GET"])
def get_jobs():

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM jobs"
        )

        jobs = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "jobs": jobs
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SINGLE JOB API
# =========================================================

@app.route("/jobs/<int:job_id>", methods=["GET"])
def get_single_job(job_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM jobs
            WHERE job_id = %s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        cursor.close()
        conn.close()

        if not job:

            return jsonify({
                "success": False,
                "message": "Job not found"
            }), 404

        return jsonify({
            "success": True,
            "job": job
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SCHEMES API
# =========================================================

@app.route("/schemes", methods=["GET"])
def get_schemes():

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM schemes"
        )

        schemes = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "schemes": schemes
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SINGLE SCHEME API
# =========================================================

@app.route("/schemes/<int:scheme_id>", methods=["GET"])
def get_single_scheme(scheme_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM schemes
            WHERE scheme_id = %s
            """,
            (scheme_id,)
        )

        scheme = cursor.fetchone()

        cursor.close()
        conn.close()

        if not scheme:

            return jsonify({
                "success": False,
                "message": "Scheme not found"
            }), 404

        return jsonify({
            "success": True,
            "scheme": scheme
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# SAVE ITEM API
# =========================================================

@app.route("/saved", methods=["POST"])
def save_item():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    item_type = data.get("item_type")
    item_id = data.get("item_id")

    if not user_id or not item_type or not item_id:

        return jsonify({
            "success": False,
            "message": "user_id, item_type and item_id are required"
        }), 400

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT saved_id
            FROM saved_items
            WHERE user_id = %s
            AND item_type = %s
            AND item_id = %s
            """,
            (user_id, item_type, item_id)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Item already saved"
            }), 409

        cursor.execute(
            """
            INSERT INTO saved_items
            (user_id, item_type, item_id)
            VALUES (%s, %s, %s)
            """,
            (user_id, item_type, item_id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Item saved successfully"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# GET SAVED ITEMS API
# =========================================================

@app.route("/saved/<int:user_id>", methods=["GET"])
def get_saved_items(user_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM saved_items
            WHERE user_id = %s
            ORDER BY saved_id DESC
            """,
            (user_id,)
        )

        saved = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "saved_items": saved
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# DELETE SAVED ITEM API
# =========================================================

@app.route("/saved/<int:saved_id>", methods=["DELETE"])
def delete_saved_item(saved_id):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM saved_items
            WHERE saved_id = %s
            """,
            (saved_id,)
        )

        conn.commit()

        deleted = cursor.rowcount

        cursor.close()
        conn.close()

        if deleted == 0:

            return jsonify({
                "success": False,
                "message": "Saved item not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Saved item removed"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)