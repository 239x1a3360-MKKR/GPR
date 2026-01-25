# Commands to Run the Application

## Quick Start (If Already Set Up)

```powershell
# Navigate to project directory
cd "C:\Users\A.Lokeswar Reddy\OneDrive\Desktop\Karthik"

# Run the server
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## Complete Setup (First Time)

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\A.Lokeswar Reddy\OneDrive\Desktop\Karthik"
```

### Step 2: Activate Virtual Environment (if using one)
```powershell
# If you created a virtual environment
venv\Scripts\activate
```

### Step 3: Install Dependencies (if not already installed)
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Set Up Database
```powershell
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 5: Create Admin User (if not already created)
```powershell
python setup.py
```

### Step 6: Run the Server
```powershell
python manage.py runserver
```

---

## Alternative: Run on Custom Port

```powershell
# Run on port 8080
python manage.py runserver 8080

# Run on specific IP and port
python manage.py runserver 0.0.0.0:8000
```

---

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Access URLs

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/

---

## Login Credentials

**Admin:**
- Username: `admin`
- Password: `gprec@1985`

**Note:** Student registration requires email from `@gprec.ac.in` domain.

---

## Troubleshooting

### Port Already in Use
```powershell
# Use a different port
python manage.py runserver 8080
```

### Database Errors
```powershell
python manage.py migrate
```

### Static Files Not Loading
```powershell
python manage.py collectstatic --noinput
```

