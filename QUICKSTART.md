# 🚀 QUICK START GUIDE

Get started with the Smart Job Bid Generator in minutes!

## ⚡ Installation (1 minute)

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/scottabney/jobbid.git
cd jobbid
./start.sh
```

That's it! The script handles everything and starts the web server.

### Option 2: Manual Setup
```bash
# Clone and enter directory
git clone https://github.com/scottabney/jobbid.git
cd jobbid

# Install dependencies
pip install -r requirements.txt

# Start web server
python app.py
```

## 🎯 First Bid in 3 Steps

### Method 1: Web Interface

1. **Open browser**: http://localhost:5000

2. **Click "Create New Bid"**

3. **Fill in the form**:
   - Project name: "Steel Gate"
   - Upload photos of the job
   - Enter client info (optional)
   - Click "Generate Bid"

4. **Done!** Download your professional PDF bid

### Method 2: Command Line

```bash
# Generate a bid from images
python cli.py \
  --project "Custom Railing" \
  --images gate1.jpg gate2.jpg \
  --client "John Smith"
```

### Method 3: Python Code

```python
from job_bid_manager import JobBidManager

# Initialize
manager = JobBidManager()

# Define materials and work
materials = [
    {'material': 'Steel', 'quantity': 100, 'unit': 'lb'}
]

processes = {
    'MIG Welding': 8,
    'Cutting': 2,
    'Finishing': 2
}

# Calculate cost
cost = manager.estimate_costs(
    materials=materials,
    labor_hours=12,
    processes=processes
)

# Generate bid
bid_path = manager.create_bid(
    project_name="Steel Project",
    cost_breakdown=cost
)

print(f"Bid created: {bid_path}")
print(f"Total: ${cost['final_price']:,.2f}")
```

## 🎨 Try the Demo

See the system in action:
```bash
python demo.py
```

This generates sample bids and shows all features.

## 🔧 Optional: Add AI Image Analysis

For AI-powered image analysis (recommended but not required):

1. Get OpenAI API key: https://platform.openai.com/api-keys

2. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

3. That's it! System will now use AI for image analysis

**Note**: System works great without AI too - it uses intelligent defaults.

## 📋 Upload Custom Pricing

1. Create Excel or CSV file with your pricing:

   **Materials** (materials.csv):
   ```csv
   Material,Unit,Price
   Steel,lb,0.75
   Aluminum,lb,2.50
   ```

   **Labor** (labor.csv):
   ```csv
   Position,HourlyRate
   Master Welder,75.00
   Welder,55.00
   ```

2. Upload through web interface (homepage)
   OR
   Use CLI: `python cli.py --pricing your_prices.xlsx`

## ✅ Verify Installation

Run the test suite:
```bash
python test_suite.py
```

You should see: "✅ All 6 tests passed!"

## 🎓 Learn More

- **Full Documentation**: See README.md
- **Usage Examples**: See example_usage.py
- **Deployment Guide**: See DEPLOYMENT.md

## 💡 Common Use Cases

### Quick Phone Quote
```python
from job_bid_manager import JobBidManager
manager = JobBidManager()

cost = manager.estimate_costs(
    materials=[{'material': 'Steel', 'quantity': 50, 'unit': 'lb'}],
    labor_hours=4,
    processes={'MIG Welding': 4}
)
print(f"Quote: ${cost['final_price']:,.2f}")
```

### Batch Process Multiple Jobs
```bash
# Loop through job folders
for job in jobs/*/; do
  python cli.py --project "$job" --images "$job"/*.jpg
done
```

### Custom Margins for Special Customer
```python
cost = manager.estimate_costs(
    materials=materials,
    labor_hours=hours,
    processes=processes,
    profit_margin=0.15,  # 15% instead of default 25%
    overhead_rate=0.10   # 10% instead of default 15%
)
```

## 🆘 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port 5000 already in use"
Change port in app.py or:
```bash
python app.py --port 8000
```

### "No such file or directory"
Make sure you're in the jobbid directory:
```bash
cd /path/to/jobbid
```

## 🎉 You're Ready!

The system is now installed and ready to generate professional bids!

**Next Steps**:
1. Customize company info in `.env`
2. Upload your pricing sheets
3. Start generating bids!

**Need Help?**
- Check README.md for detailed documentation
- Run `python cli.py --help` for CLI options
- Look at example_usage.py for code examples

---

**Pro Tip**: Keep your pricing sheets updated and use the web interface for the best experience. The system gets smarter as you use it!
