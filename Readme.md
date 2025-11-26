# Canteen Reservation System

API for managing canteen reservations, made for the '5 dana u oblacima' hackaton, by levi9.

## Technologies and Versions

### Technologies
- **Python**: 3.13.7
- **Pip**: 25.3
- **Docker**: 28.3.3, build 980b856
- **Docker Compose**: 2.40.3

### Python packages
- **annotated-doc**==0.0.4
- **annotated-types**==0.7.0
- **anyio**==4.11.0
- **certifi**==2025.11.12
- **charset-normalizer**==3.4.4
- **click**==8.3.1
- **dataclasses**==0.6
- **DateTime**==6.0
- **fastapi**==0.122.0
- **h11**==0.16.0
- **httpcore**==1.0.9
- **httpx**==0.28.1
- **idna**==3.11
- **iniconfig**==2.3.0
- **packaging**==25.0
- **pluggy**==1.6.0
- **pydantic**==2.12.4
- **pydantic_core**==2.41.5
- **Pygments**==2.19.2
- **pytest**==9.0.1
- **pytz**==2025.2
- **requests**==2.32.5
- **sniffio**==1.3.1
- **starlette**==0.50.0
- **typing**==3.7.4.3
- **typing-inspection**==0.4.2
- **typing_extensions**==4.15.0
- **urllib3**==2.5.0
- **uvicorn**==0.38.0
- **zope.interface**==8.1.1

## Environment Setup

### Local Setup

1. **Install Python 3.13.7**
   - Download from [python.org](https://www.python.org/downloads/)

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Building the Application

### Python doesn't need building lmao

```bash
:^)
```

### Build with Docker

```bash
docker build -t canteen-api .
```

### Build with Docker Compose

```bash
docker-compose build
```

## Running the Application

### Local execution

```bash
uvicorn handlers:app --reload --port 8000
```

Application will be available at: `http://localhost:8000`

### Running with Docker

**Option 1: Docker run**
```bash
docker run -p 8000:8000 canteen-api
```

**Option 2: Docker Compose**
```bash
docker compose up app
```

Application will be available at: `http://localhost:8000`

## Running Unit Tests

### Local test execution

```bash
# cd into the root of the project
# run all tests
pytest
```

### Running tests with Docker

**Option 1: Docker run**
```bash
docker run canteen-api pytest
```

**Option 2: Docker Compose**
```bash
# Run all tests
docker-compose run test

