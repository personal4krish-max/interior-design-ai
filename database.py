import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = "interior_design.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS design_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_type TEXT,
            room_size TEXT,
            budget TEXT,
            color_theme TEXT,
            furniture_style TEXT,
            lifestyle TEXT,
            special_notes TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            design_id INTEGER,
            designer_name TEXT,
            booking_date TEXT,
            time_slot TEXT,
            service_type TEXT,
            amount REAL,
            payment_status TEXT DEFAULT 'pending',
            booking_status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            booking_id INTEGER,
            amount REAL,
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT DEFAULT 'completed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS designers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            experience TEXT,
            rating REAL DEFAULT 4.5,
            price_per_hour REAL,
            availability TEXT DEFAULT 'Available',
            image_url TEXT
        )
    """)

    # Insert sample designers if empty
    c.execute("SELECT COUNT(*) FROM designers")
    if c.fetchone()[0] == 0:
        designers = [
            ("Sophia Williams", "Modern & Contemporary", "8 Years", 4.9, 120.0, "Available", "https://randomuser.me/api/portraits/women/44.jpg"),
            ("James Carter", "Traditional & Classic", "12 Years", 4.8, 150.0, "Available", "https://randomuser.me/api/portraits/men/32.jpg"),
            ("Priya Sharma", "Minimalist & Zen", "6 Years", 4.7, 100.0, "Available", "https://randomuser.me/api/portraits/women/68.jpg"),
            ("Michael Torres", "Industrial & Rustic", "10 Years", 4.6, 130.0, "Busy", "https://randomuser.me/api/portraits/men/75.jpg"),
            ("Emma Chen", "Bohemian & Eclectic", "5 Years", 4.8, 110.0, "Available", "https://randomuser.me/api/portraits/women/90.jpg"),
        ]
        c.executemany("INSERT INTO designers (name, specialization, experience, rating, price_per_hour, availability, image_url) VALUES (?,?,?,?,?,?,?)", designers)

    # Insert admin user
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                  ("Admin", "admin@interiordesign.com", hash_password("admin123"), "admin"))

    conn.commit()
    conn.close()

def register_user(name, email, password, phone):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password, phone) VALUES (?,?,?,?)",
                  (name, email, hash_password(password), phone))
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Email already registered!"
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def save_design_request(user_id, data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO design_requests 
                 (user_id, room_type, room_size, budget, color_theme, furniture_style, lifestyle, special_notes)
                 VALUES (?,?,?,?,?,?,?,?)""",
              (user_id, data['room_type'], data['room_size'], data['budget'],
               data['color_theme'], data['furniture_style'], data['lifestyle'], data['special_notes']))
    design_id = c.lastrowid
    conn.commit()
    conn.close()
    return design_id

def get_user_designs(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM design_requests WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_all_designers():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM designers ORDER BY rating DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def create_booking(user_id, designer_id, design_id, date, slot, service, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM designers WHERE id=?", (designer_id,))
    designer = c.fetchone()
    import random, string
    txn = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    c.execute("""INSERT INTO bookings (user_id, design_id, designer_name, booking_date, time_slot, service_type, amount, payment_status)
                 VALUES (?,?,?,?,?,?,?,?)""",
              (user_id, design_id, designer['name'] if designer else "TBD", date, slot, service, amount, "completed"))
    booking_id = c.lastrowid
    c.execute("""INSERT INTO payments (user_id, booking_id, amount, payment_method, transaction_id, status)
                 VALUES (?,?,?,?,?,?)""",
              (user_id, booking_id, amount, "Card", txn, "completed"))
    conn.commit()
    conn.close()
    return booking_id, txn

def get_user_bookings(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ── Admin ──
def admin_stats():
    conn = get_connection()
    c = conn.cursor()
    stats = {}
    c.execute("SELECT COUNT(*) FROM users WHERE role='user'"); stats['users'] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM design_requests");         stats['designs'] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bookings");                stats['bookings'] = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM payments"); stats['revenue'] = c.fetchone()[0]
    conn.close()
    return stats

def admin_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id,name,email,phone,role,created_at FROM users ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def admin_all_bookings():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT b.*, u.name as user_name, u.email as user_email 
                 FROM bookings b JOIN users u ON b.user_id=u.id 
                 ORDER BY b.created_at DESC""")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows
# Add this to the bottom of database.py
def update_booking_status(booking_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE bookings SET booking_status=? WHERE id=?", (status, booking_id))
    conn.commit()
    conn.close()
    return True
