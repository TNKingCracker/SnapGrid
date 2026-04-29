# SnapGrid - Instagram Clone

A production-ready Instagram-style social media application with Android frontend and Python FastAPI backend.

## Tech Stack

### Frontend (Android)
- Kotlin + Jetpack Compose
- Material 3 Design
- MVVM Architecture
- Hilt for DI
- Retrofit for networking
- Coil for image loading

### Backend (Python)
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- WebSocket for real-time features

## Getting Started

### Prerequisites
- Java JDK 17+
- Android Studio
- Python 3.10+
- PostgreSQL

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
# Create .env from .env.example
python main.py
```

### Android Setup

```bash
cd android
# Open in Android Studio
# Or build via command line:
gradlew assembleDebug
```

## Features
- Authentication (Register/Login)
- Home Feed with posts
- Search/Explore
- Reels
- Direct Messages
- Notifications
- Profile Management

## License
MIT