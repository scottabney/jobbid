# 🏭 Smart Job Bid Generator

The **ultimate** smart job bid generator for metal welding and fabrication shops! This powerful tool uses AI to analyze job photos, calculate pricing from your custom pricing sheets, and generate professional bid documents automatically.

## 🌟 Features

### 🤖 AI-Powered Image Analysis
- Upload job site photos and let AI analyze the work required
- Automatically identifies materials (steel, aluminum, stainless, etc.)
- Detects welding processes needed (MIG, TIG, Stick, etc.)
- Estimates complexity and labor hours
- Recognizes fabrication operations (cutting, bending, assembly, etc.)

### 💰 Smart Pricing Calculator
- Upload your custom pricing sheets (Excel or CSV)
- Automatic cost calculation for materials and labor
- Support for multiple material types and processes
- Configurable profit margins and overhead rates
- Detailed cost breakdowns

### 📄 Professional Bid Generation
- Beautiful, professional PDF bid documents
- Customizable company information
- Detailed scope of work
- Cost breakdowns with transparency
- Terms and conditions
- Client signature section

### 🖥️ Multiple Interfaces
- **Web Application**: User-friendly web interface
- **Command Line**: Powerful CLI for automation
- **API**: Programmatic access for integration

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/scottabney/jobbid.git
cd jobbid
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional):
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
COMPANY_NAME=Your Company Name
COMPANY_ADDRESS=123 Industrial Way, City, ST 12345
COMPANY_PHONE=(555) 123-4567
COMPANY_EMAIL=bids@yourcompany.com
PROFIT_MARGIN=0.25
OVERHEAD_RATE=0.15
EOF
```

### Usage

#### Web Interface

Start the web application:
```bash
python app.py
```

Then open your browser to `http://localhost:5000`

#### Command Line Interface

Generate a bid from the command line:
```bash
python cli.py --project "Steel Gate Fabrication" \
              --images gate1.jpg gate2.jpg \
              --client "John Smith" \
              --client-email "john@example.com"
```

#### Python API

Use programmatically in your own code:
```python
from job_bid_manager import JobBidManager

# Initialize
manager = JobBidManager()

# Generate complete bid
result = manager.generate_complete_bid(
    project_name="Custom Railing",
    image_paths=["railing1.jpg", "railing2.jpg"],
    client_info={
        'name': 'Jane Doe',
        'email': 'jane@example.com'
    }
)

print(f"Bid generated: {result['bid_path']}")
print(f"Total: ${result['cost_breakdown']['final_price']}")
```

## 📋 Pricing Sheets

The system supports custom pricing sheets in Excel or CSV format. Example formats are provided:

- `sample_pricing_materials.csv` - Material pricing
- `sample_pricing_labor.csv` - Labor rates

### Material Pricing Format
```csv
Material,Unit,Price
Steel,lb,0.75
Aluminum,lb,2.50
Steel Plate 1/4",sheet,120.00
```

### Labor Pricing Format
```csv
Position,HourlyRate
Master Welder,75.00
Welder,55.00
Fabricator,50.00
```

Upload through the web interface or specify with `--pricing` flag in CLI.

## 🏗️ Architecture

### Core Components

1. **Image Analyzer** (`image_analyzer.py`)
   - Uses OpenAI GPT-4 Vision API
   - Analyzes job photos for materials, processes, and complexity
   - Falls back to mock analysis if API not configured

2. **Pricing Calculator** (`pricing_calculator.py`)
   - Loads and parses pricing sheets
   - Calculates material, labor, and process costs
   - Applies overhead and profit margins

3. **Bid Generator** (`bid_generator.py`)
   - Creates professional PDF documents
   - Uses ReportLab for document generation
   - Customizable templates and styling

4. **Job Bid Manager** (`job_bid_manager.py`)
   - Orchestrates the complete workflow
   - Integrates all components
   - Provides high-level API

## 🎨 Web Interface Features

- **Dashboard**: Upload pricing sheets, view summary
- **Create Bid**: Upload images, enter project details
- **View Bids**: Browse and download past bids
- **Responsive Design**: Works on desktop and mobile

## 🔧 Configuration

Edit `config.py` or set environment variables:

- `OPENAI_API_KEY` - Required for AI image analysis
- `COMPANY_NAME` - Your company name
- `COMPANY_ADDRESS` - Your address
- `COMPANY_PHONE` - Contact phone
- `COMPANY_EMAIL` - Contact email
- `PROFIT_MARGIN` - Default profit margin (0.25 = 25%)
- `OVERHEAD_RATE` - Default overhead rate (0.15 = 15%)
- `TAX_RATE` - Sales tax rate if applicable

## 📊 Example Output

The system generates:
1. **PDF Bid Document** - Professional, ready-to-send bid
2. **JSON Data File** - Structured bid data for record-keeping
3. **Console Summary** - Quick overview of the bid

### Sample Bid Summary
```
JOB BID SUMMARY
============================================================
Project: Custom Steel Railing
Complexity: Moderate
Estimated Hours: 16

Materials: Steel, Stainless Steel
Processes: MIG Welding, Cutting, Grinding, Assembly

PRICING:
  Materials: $450.00
  Labor: $1,040.00
  Processes: $520.00
  Overhead: $301.50
  Profit: $577.88
  
  TOTAL BID: $2,889.38
============================================================
```

## 🔐 Security

- No credentials stored in code
- Environment variables for sensitive data
- File upload validation
- Secure filename handling

## 🛠️ Development

### Project Structure
```
jobbid/
├── app.py                    # Flask web application
├── cli.py                    # Command line interface
├── config.py                 # Configuration management
├── job_bid_manager.py        # Main orchestration
├── image_analyzer.py         # AI image analysis
├── pricing_calculator.py     # Cost calculations
├── bid_generator.py          # PDF generation
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── create_bid.html
│   ├── bid_result.html
│   └── view_bids.html
├── static/                   # CSS and assets
│   └── css/
│       └── style.css
├── uploads/                  # Upload directory
│   ├── images/
│   └── pricing_sheets/
└── generated_bids/           # Output directory
```

## 🤝 Contributing

This is a powerful, production-ready system for job bidding. Feel free to:
- Add new features
- Improve AI analysis
- Enhance bid templates
- Add new export formats

## 📝 License

MIT License - Feel free to use for your business!

## 🎯 Future Enhancements

Potential improvements:
- Multiple bid templates
- Historical bid analytics
- Customer database integration
- Email sending capability
- Mobile app
- Multi-language support
- CAD file analysis
- Material quantity estimation from dimensions

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ for metal fabrication professionals**