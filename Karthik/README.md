# Cloud-Based Virtual Lab for Programming Practice

A locally hosted web-based virtual programming lab that allows users to write, compile, and execute programs in multiple programming languages (C, C++, Java, Python) using a browser-based interface.

## Features

- 🌐 **Web-based Code Editor** - Modern, syntax-highlighted code editor with CodeMirror
- 🔐 **User Authentication** - Login/Registration system with Admin and Student roles
- 💻 **Multi-language Support** - Execute code in C, C++, Java, and Python
- ⚡ **Real-time Execution** - Instant code execution with output and error feedback
- 📊 **Submission Tracking** - View submission history and execution results
- 👨‍💼 **Admin Panel** - Manage users and review all submissions
- 🔒 **Secure Execution** - Timeout protection and isolated execution environment

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+**
- **Django 4.2+**
- **GCC** (for C and C++ compilation)
- **Java JDK** (for Java compilation)
- **Python Interpreter** (for Python execution)

### Installing Compilers/Interpreters

#### Windows
- **GCC**: Install [MinGW-w64](https://www.mingw-w64.org/) or [TDM-GCC](https://jmeubank.github.io/tdm-gcc/)
- **Java**: Install [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
- **Python**: Usually pre-installed or download from [python.org](https://www.python.org/)

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install gcc g++ python3 default-jdk
```

#### macOS
```bash
# Install Xcode Command Line Tools (includes GCC)
xcode-select --install

# Install Java
brew install openjdk

# Python is usually pre-installed
```

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser** (optional, for admin access):
```bash
python manage.py createsuperuser
```

6. **Collect static files**:
```bash
python manage.py collectstatic --noinput
```

## Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Accessing the Application

- **Main Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/

## Usage

### For Students

1. **Register/Login**: Create an account or login with existing credentials
   - **Note**: Registration requires an email from `@gprec.ac.in` domain
2. **Select Language**: Choose from C, C++, Java, or Python
3. **Write Code**: Use the code editor to write your program
4. **Add Input** (optional): Provide input data if your program requires it
5. **Run Code**: Click "Run Code" to execute your program
6. **View Results**: See output or error messages in real-time
7. **Check History**: View your submission history

### For Administrators

1. **Login**: Use admin credentials to access the system
2. **View All Submissions**: Access submission history of all users
3. **Admin Panel**: Use Django admin panel to manage users and submissions
4. **Monitor Activity**: Track user activity and code executions

## Project Structure

```
virtuallab/
├── lab/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── code_executor.py   # Code execution logic
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── virtuallab/            # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
│   └── lab/
├── static/                # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## API Endpoints

- `POST /api/execute/` - Execute code
  - Body: `{ "language": "python", "code": "...", "input": "..." }`
  - Returns: Execution results with output/error

- `GET /api/submissions/` - Get submission history
  - Returns: List of user's submissions

- `GET /api/submissions/<id>/` - Get submission details
  - Returns: Detailed submission information

## Security Features

- **Timeout Protection**: Code execution times out after 10 seconds (configurable)
- **Code Length Limit**: Maximum 100,000 characters per submission
- **Isolated Execution**: Each execution runs in a temporary directory
- **User Authentication**: Only authenticated users can execute code
- **Role-based Access**: Admin and Student roles with different permissions

## Configuration

You can modify settings in `virtuallab/settings.py`:

- `CODE_EXECUTION_TIMEOUT`: Execution timeout in seconds (default: 10)
- `MAX_CODE_LENGTH`: Maximum code length (default: 100000)
- `EXECUTION_DIR`: Directory for temporary code execution files

## Troubleshooting

### Code Execution Fails

1. **Check compiler installation**: Ensure GCC, Java, and Python are installed and in PATH
2. **Verify permissions**: Ensure the execution directory is writable
3. **Check logs**: Review Django server logs for error messages

### Static Files Not Loading

Run: `python manage.py collectstatic --noinput`

### Database Errors

Run migrations: `python manage.py migrate`

## Future Enhancements

- [ ] Support for additional programming languages (JavaScript, Go, Rust)
- [ ] Code sharing and collaboration features
- [ ] Advanced code analysis and linting
- [ ] Test case execution and automated grading
- [ ] Docker containerization for easier deployment
- [ ] Enhanced security with sandboxing (Docker containers)
- [ ] Real-time collaboration features
- [ ] Code templates and examples library

## License

This project is developed for educational purposes.

## Support

For issues or questions, please check the Django documentation or create an issue in the repository.

---

**Note**: This is a locally hosted implementation. For production deployment, consider:
- Using a production-grade web server (Nginx + Gunicorn)
- Implementing proper security measures (HTTPS, stronger authentication)
- Using containerization (Docker) for code execution isolation
- Setting up proper database (PostgreSQL instead of SQLite)
- Implementing rate limiting and resource quotas

