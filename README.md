# Welcome to ISHACARE! 🚀

Hey there! ISHACARE is your friendly AI-powered health monitoring buddy. We take those confusing medical documents and turn them into clear insights about your health. Think of us as your personal health detective - we analyze PDFs, spot risks, calculate scores, and even send alerts when something needs attention.

## What Makes ISHACARE Special? ✨

We're all about making health monitoring smarter and easier:

- **Smart Document Reading**: We can pull text from PDF reports using OCR magic
- **Data Cleanup Crew**: Automatically organizes messy medical data into something useful
- **Risk Detective**: Uses machine learning to predict potential health risks
- **Health Score Calculator**: Gives you a comprehensive health score based on your data
- **Alert System**: Sends notifications for important health stuff you shouldn't miss
- **Easy API**: Built with FastAPI so developers can integrate it anywhere

## Getting Started - Let's Get You Up and Running! 🛠️

Don't worry, we've got you covered. Here's how to get ISHACARE running on your machine:

### 1. Grab the Code
First, let's clone this repository:
```bash
git clone <your-repo-url-here>
cd ISHACARE
```

### 2. Install the Good Stuff
Now, let's get all the dependencies installed. You have two options:

**Option A: Using pip (easiest)**
```bash
pip install -r REQUIRMENTS.TXT
```

**Option B: Using poetry (if you're fancy)**
```bash
poetry install
```

### 3. Set Up OCR (for reading images in PDFs)
ISHACARE uses Tesseract for reading text from images. Here's how to get it:
- **Windows users**: Head over to [Tesseract's GitHub page](https://github.com/UB-Mannheim/tesseract/wiki) and download the installer
- **Other OS**: Check their installation guide - it's pretty straightforward!

Make sure to add Tesseract to your system's PATH so we can find it.

## Time to Play! 🎮

Ready to see ISHACARE in action? Let's fire it up:

1. **Start the server**:
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

2. **Check it out**: Open your browser and go to `http://127.0.0.1:8000`
   - You'll see a simple welcome message

3. **Explore the API**: Visit `http://127.0.0.1:8000/docs` for the interactive documentation
   - This is where the magic happens! You can test endpoints right from your browser

## How to Use the API 📡

We've kept it simple - just two main endpoints:

- **`GET /`** - A quick health check. Returns a friendly message confirming everything's working
- **`POST /analyze/`** - The star of the show! Upload a PDF medical document and get back:
  - Clean, structured medical data
  - Health risk predictions
  - Your overall health score
  - Any important alerts

**Quick example**: Upload a medical report PDF to `/analyze/` and boom - you get insights that actually make sense!

## Under the Hood: Project Structure 🏗️

Curious about how we organized everything? Here's the breakdown:

```
ISHACARE/
├── Backend/                 # Where the magic happens
│   ├── main.py             # The main FastAPI app - our entry point
│   ├── Models/
│   │   └── ml_model.py     # Our machine learning brain
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── pipeline.py     # The main processing workflow
│   ├── routes/
│   │   ├── __init__.py
│   │   └── analyze.py      # API routes and endpoints
│   └── services/           # All our helper functions
│       ├── __init__.py
│       ├── alerts.py       # Alert generation logic
│       ├── automation.py   # Automation features
│       ├── cleaner.py      # Data cleaning utilities
│       ├── confidence.py   # Confidence scoring
│       ├── extractor.py    # Text and data extraction
│       ├── predictor.py    # Risk prediction models
│       └── scorer.py       # Health scoring algorithms
├── pyproject.toml          # Project configuration
├── REQUIRMENTS.TXT         # List of what we need to run
└── README.md               # This friendly guide!
```

## What We Use (Our Tech Stack) 🔧

ISHACARE runs on some awesome open-source tools:

- **FastAPI** - Our speedy web framework
- **Uvicorn** - The server that makes FastAPI fly
- **pdfplumber** - Expert PDF text extraction
- **pytesseract** - OCR for reading images
- **Pillow** - Image processing wizardry
- **NumPy & Pandas** - Data crunching powerhouses
- **Scikit-learn** - Machine learning magic
- **python-multipart** - Handles file uploads like a pro

## Want to Help Make ISHACARE Better? 🤝

We'd love your contributions! Whether you're fixing bugs, adding features, or improving documentation:

1. Fork this repository
2. Create a branch for your changes (`git checkout -b amazing-new-feature`)
3. Make your improvements
4. Test everything works
5. Submit a pull request

Got questions? Found a bug? Open an issue - we're here to help!

## What's Next? 🚀

We're just getting started! Future plans include:
- Mobile app integration
- More advanced ML models
- Integration with electronic health records
- Real-time monitoring capabilities

Stay tuned - ISHACARE is growing fast!

---

*Built with love for better health insights*

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[MIT LICENSE ]
