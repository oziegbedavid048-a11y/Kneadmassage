# Knead Hushed Massage — Django Backend & Admin

This directory contains the Django backend and admin interface for managing bookings and appointments.

## 🚀 How to Run the Django Server

1. Open your terminal in the `backend/` folder:
   ```bash
   cd c:\Users\David\Desktop\KNEADMASSAGE\backend
   ```

2. Activate the virtual environment (Windows PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

   The server will start at: `http://127.0.0.1:8000/`

---

## 🔑 Django Admin Login Credentials

- **Admin URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@kneadmassage.com`

---

## 📊 Features Built in Django Admin

- **Booking Table View**:
  - View Customer Full Name, Email, Phone, Zipcode, Service, Date, Time, Duration, Status, and Timestamp.
- **Inline Status Editing**:
  - Update any booking's status (`Pending`, `Confirmed`, `Completed`, `Cancelled`) directly from the table list view.
- **Bulk Actions**:
  - Select multiple bookings and bulk update them as **Confirmed**, **Completed**, or **Cancelled**.
- **Filters & Search**:
  - Filter by Status, Service, Date, or Creation time.
  - Search by Name, Email, Phone, Zipcode, or Notes.
- **API Endpoint**:
  - `POST http://127.0.0.1:8000/api/bookings/create/` receives live form submissions from `book-now.html`.
