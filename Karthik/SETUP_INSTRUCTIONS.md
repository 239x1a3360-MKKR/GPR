# Quick Setup Instructions

## Step 1: Install Prerequisites

### Python Dependencies
```bash
pip install -r requirements.txt
```

### System Compilers/Interpreters

**Windows:**
- Install MinGW-w64 for GCC (C/C++)
- Install JDK for Java
- Python should already be installed

**Linux:**
```bash
sudo apt-get update
sudo apt-get install gcc g++ python3 default-jdk
```

**macOS:**
```bash
xcode-select --install  # For GCC
brew install openjdk    # For Java
```

## Step 2: Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Admin User (Optional)

You can either:
- Run the setup script: `python setup.py`
- Or manually: `python manage.py createsuperuser`

## Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 5: Run the Server

```bash
python manage.py runserver
```

## Step 6: Access the Application

Open your browser and go to: **http://127.0.0.1:8000/**

### Default Admin Credentials (if using setup.py)
- Username: `admin`
- Password: `gprec@1985`
- Email: `admin@gprec.ac.in`

## Troubleshooting

### "gcc: command not found"
- Install GCC compiler (see Step 1)

### "javac: command not found"
- Install Java JDK (see Step 1)

### Static files not loading
- Run: `python manage.py collectstatic --noinput`

### Database errors
- Run: `python manage.py migrate`

## Testing Code Execution

Try these sample programs:

### Python
```python
print("Hello, World!")
for i in range(5):
    print(i)
```

### C
```c
#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    return 0;
}
```

### C++
```cpp
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```

### Java
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

