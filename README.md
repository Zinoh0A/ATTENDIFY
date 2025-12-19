# Attendify – Facial Recognition Attendance System

A modern Python desktop application for automated student attendance tracking using face recognition. Built with Tkinter, OpenCV, and dlib for intelligent facial identification.

---

## Key Features

✓ **Facial Recognition** — Dual-pipeline support (OpenCV LBPH + dlib-based encoding)  
✓ **Live Detection** — Real-time face detection and attendance marking  
✓ **Desktop GUI** — Clean Tkinter interface with intuitive card layout  
✓ **AI Chatbot** — Integrated Ollama-powered assistant for help  
✓ **Flexible Storage** — MySQL support or CSV fallback  
✓ **Model Training** — Built-in pipeline to train and update recognition models  
✓ **Student Management** — Add, modify, and manage student records  
✓ **Attendance Reports** — Export and view attendance logs

---

## Tech Stack

| Component       | Library                    | Notes                                          |
| --------------- | -------------------------- | ---------------------------------------------- |
| **Language**    | Python 3.8+                | Main runtime                                   |
| **GUI**         | Tkinter                    | Desktop interface                              |
| **Images**      | Pillow (PIL)               | Image handling & display                       |
| **Vision**      | OpenCV                     | Face detection (Haar cascades) & LBPH training |
| **Recognition** | dlib, imutils              | Advanced facial encoding & recognition         |
| **Database**    | MySQL                      | Optional persistent storage                    |
| **Fallback**    | CSV                        | Simple attendance logging                      |
| **Chatbot**     | Ollama                     | Local LLM integration                          |
| **Utilities**   | NumPy, threading, datetime | Core helpers                                   |

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Zinoh0A/ATTENDIFY.git
cd ATTENDIFY
```

### 2. Create a virtual environment (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install opencv-python pillow numpy mysql-connector-python imutils ollama
```

**Special Notes:**

- **dlib** — Install separately: `pip install dlib`. On Windows, you may need Visual Studio Build Tools or a prebuilt wheel. If installation fails, the app will still run using OpenCV-only mode.
- **Ollama** — Download and install from [ollama.ai](https://ollama.ai). Models are loaded locally for the chatbot feature.

### 4. Set up directories & configuration

- Create `data/` folder for LBPH training images
- Create `known_faces/<student_id>/` folders with sample face images
- Edit `database.py` to set MySQL credentials (or skip for CSV mode)
- Place dlib model files in `pretrained_model/`:
  - `shape_predictor_68_face_landmarks.dat`
  - `dlib_face_recognition_resnet_model_v1.dat`

---

## Quick Start

### Run the Application

```powershell
python main.py
```

Or use the login UI:

```powershell
python login.py
```

### Train a Face Model (LBPH)

1. Prepare images in `data/` with naming: `user.STUDENT_ID.NUMBER.jpg`
2. Run:

```powershell
python train.py
```

3. Model is saved to `classifier/trainer.xml`

### Start Recognition (Live)

1. Open the app: `python main.py`
2. Click **Face Detector** card
3. Click **Start Recognition**
4. Attendance is logged to `attendance.csv`

---

## Project Structure

```
ATTENDIFY/
├── main.py                    # Application dashboard
├── login.py                   # Login/authentication UI
├── train.py                   # LBPH model training
├── face_recognition.py        # Live recognition GUI
├── attendance.py              # Attendance management
├── database.py                # MySQL helper functions
├── chatbot.py                 # Ollama chatbot UI
├── dlib_face_recognition.py   # dlib encoder/recognizer
├── Student.py                 # Student class & utilities
├── attendmodify.py            # Modify attendance records
├── data/                      # Training images (LBPH)
├── known_faces/               # Known face encodings (dlib)
├── classifier/                # Trained LBPH models
├── pretrained_model/          # dlib pretrained models & encodings.pickle
├── attendance.csv             # Attendance log
├── icones/                    # UI icons & images
├── chatbot_images/            # Chatbot assets
├── help_images/               # Help/documentation images
└── conversations/             # Saved chatbot conversations
```

---

## Configuration

### MySQL Setup (Optional)

Edit `database.py`:

```python
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # Change this
    "database": "face_recognition_system"
}
```

### Ollama Models

Install a model locally:

```bash
ollama pull llama2
# or other available models: mistral, phi3, deepseek-r1
```

The chatbot will automatically detect available models.

---

## Usage Guide

### Add a Student

1. Click **Student Details**
2. Fill in name, ID, department, course, year, etc.
3. Capture or upload a photo
4. Save

### Train Recognition Model

1. Collect ~10+ clear face photos per student
2. Organize in `data/` as `user.ID.1.jpg`, `user.ID.2.jpg`, etc.
3. Click **Train Data** (or run `python train.py`)
4. Wait for training to complete

### Mark Attendance

1. Click **Face Detector** → **Start Recognition**
2. Position face in front of webcam
3. System auto-detects and logs attendance
4. View logs in **Attendance** or export `attendance.csv`

### Chat with AI

1. Click **ChatBot**
2. Ask questions about the system
3. Responses powered by local Ollama model

---

## Troubleshooting

| Issue                        | Solution                                                     |
| ---------------------------- | ------------------------------------------------------------ |
| **Camera not detected**      | Check device permissions; try index 0 or 1 in code           |
| **dlib import error**        | Install Visual Studio Build Tools or use prebuilt wheels     |
| **Poor recognition**         | Add more training images; ensure good lighting               |
| **Ollama errors**            | Install Ollama from ollama.ai; verify a model is pulled      |
| **MySQL connection failed**  | Check credentials in `database.py`; ensure server is running |
| **No models in classifier/** | Run `python train.py` first to generate models               |

---

## Key Files Explained

| File                       | Purpose                                           |
| -------------------------- | ------------------------------------------------- |
| `main.py`                  | Central dashboard; launches other modules         |
| `face_recognition.py`      | Live recognition loop; uses `DlibFaceRecognition` |
| `dlib_face_recognition.py` | Encodes faces to embeddings; saves to `.pickle`   |
| `train.py`                 | LBPH trainer for OpenCV-based recognition         |
| `chatbot.py`               | Ollama chatbot with multi-conversation UI         |
| `database.py`              | MySQL CRUD operations                             |
| `attendance.py`            | View/export attendance records                    |

---

## Development Notes

- **Dual pipelines**: The app tries dlib first; if unavailable, falls back to OpenCV LBPH
- **Threading**: Face recognition runs in background threads to avoid UI freeze
- **Encodings**: dlib embeddings stored in `pretrained_model/encodings.pickle`
- **CSV fallback**: Attendance marked even if MySQL is unavailable
- **Ollama integration**: Chatbot requires local Ollama server or API endpoint

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

MIT License — See `LICENSE` file for details.

---

## Contact & Support

For questions, issues, or suggestions:

- Open an issue on GitHub
- Check `developper.py` for maintainer contact info
- Review inline code comments for implementation details

---

**Last Updated:** December 2025
