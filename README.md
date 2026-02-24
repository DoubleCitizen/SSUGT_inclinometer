<div align="center">
  <h1>🎯 SSUGT Inclinometer Software</h1>
  <p><strong>Developed within the framework of the Novosibirsk university SSUGT: software for a high-precision inclinometer, capable of replacing expensive analogues.</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://wiki.qt.io/Qt_for_Python)
  [![OpenCV](https://img.shields.io/badge/OpenCV-4.9-red.svg)](https://opencv.org/)
</div>

---

## 📖 About The Project

This software is designed for a high-precision inclinometer, developed as a highly precise yet cost-effective alternative to expensive commercial counterparts. The project is a proud part of research and development at **SSUGT** (Siberian State University of Geosystems and Technologies, Novosibirsk).

It provides a modern graphical user interface, real-time video stream processing, visual segmentation, and specific hardware integration to deliver accurate tilt, level, and inclination measurements.

## ✨ Key Features

- 🖥️ **Modern GUI:** Built with PySide6 (Qt) for a responsive and intuitive user experience.
- 📹 **Real-time Video Processing:** Integrates OpenCV for visual data stream segmentation and analysis.
- 🔌 **Hardware Integration:** Communicates with external sensors and inclinometer devices via serial connections (`pyserial`).
- 📊 **Advanced Analytics:** Uses NumPy, SciPy, Matplotlib, and SymPy for high-performance mathematical computations and interactive data visualization.
- 📦 **Standalone Executable:** Ready to be packaged with PyInstaller for quick deployment without requiring a local Python environment.

## 🛠️ Technologies & Libraries

- **Core:** Python 3
- **GUI Framework:** PySide6
- **Computer Vision:** OpenCV (`opencv-python`)
- **Math & Data Visualization:** NumPy, SciPy, Matplotlib, SymPy
- **Hardware & Networking:** PySerial, Scapy, Requests
- **Packaging:** PyInstaller

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system. 

### Installation

1. **Clone the repository** (or download the source code):
   ```bash
   git clone https://github.com/DoubleCitizen/SSUGT_inclinometer
   cd SSUGT_inclinometer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

To run the software, ensure your virtual environment is activated and execute the main script:

```bash
python run.py
```

### 📦 Building the Executable

To build a standalone executable for Windows using PyInstaller, use the included `.spec` files (e.g., `vim_cmd.spec`):

```bash
pyinstaller vim_cmd.spec
```

## 📁 Project Structure

```text
SSUGT_inclinometer/
│
├── classes/          # Core logic classes and stream controllers
├── controllers/      # UI controllers (e.g., Start Menu logic)
├── data/             # Application configs and output data
├── dialogs/          # Modal UI dialog windows
├── logs/             # Runtime execution logs
├── ui/               # RAW Qt Designer interfaces (.ui)
├── widgets/          # Custom graphical widget components
│
├── run.py            # Main application entry point
├── requirements.txt  # Python environment dependencies
└── resource_rc.py    # Compiled UI resources
```

## 🎓 Acknowledgments

- Developed within the curriculum and research scope of the **[Siberian State University of Geosystems and Technologies (SSUGT)](https://sgugit.ru/)**, Novosibirsk.

---
<div align="center">
  <i>Developed with ❤️ for precise measurements.</i>
</div>
