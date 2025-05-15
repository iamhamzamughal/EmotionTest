
# Emotion Recognition Test

This Python-based GUI application evaluates a user's ability to recognize human emotions from facial expressions. It presents a set of emotion-labeled images for a short time and asks the user to identify the displayed emotion. Responses are recorded and exported to an Excel file for further analysis.

## 🧠 Features

- Displays images showing one of six emotions: `Happy`, `Sad`, `Surprise`, `Fear`, `Disgust`, `Anger`
- User selects gender before starting the test
- Each image is shown briefly to simulate rapid recognition
- A set of buttons allows users to select the emotion they perceived
- Records user response, reaction time, and accuracy
- Automatically saves results to `emotion_data.xlsx`
- Includes a countdown timer for responses (10 seconds)
- Summary generated at the end of the test

## 🖼️ Example Emotions

Images used should follow a consistent naming pattern that reflects the emotion (e.g., `happy123.jpg`, `anger002.jpg`). Digits are ignored while extracting the emotion name.

## 📁 Folder Structure

```
emotion-recognition-test/
│
├── images/                  # Folder containing emotion-labeled images
├── emotion_data.xlsx        # Auto-generated result file
├── main.py                  # Main application script
└── README.md                # Project documentation
```

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/emotion-recognition-test.git
cd emotion-recognition-test
```

2. Install the required Python packages:

```bash
pip install opencv-python pandas pillow openpyxl numpy
```

> **Note**: This app uses `Tkinter`, which is bundled with most Python installations.

## 🚀 Running the Application

Make sure you have a folder named `images/` in the project directory containing emotion images (JPEG/PNG).

```bash
python main.py
```

## 🧪 Test Flow

1. User selects gender
2. Instructions are displayed
3. Upon pressing `START`, images are shown one-by-one
4. After viewing, the user selects the emotion
5. Each response is logged with:
   - Image filename
   - Gender
   - Time taken (in ms)
   - Selected emotion
   - Whether the response was correct
   - Actual emotion extracted from filename

## 📊 Output

Results are saved in `emotion_data.xlsx`, with extra columns showing binary scores for each emotion (useful for analysis).

## 🧩 Dependencies

- Python 3.x
- `opencv-python`
- `pandas`
- `pillow`
- `numpy`
- `openpyxl`
- `tkinter` (built-in for most Python distros)

## 📌 Future Improvements

- Add sound or visual cues for better engagement
- Allow difficulty levels (e.g., faster display time)
- Add support for more nuanced emotions
- Plot real-time or post-test statistics

## 📝 License

MIT License

---

Feel free to fork or contribute!
