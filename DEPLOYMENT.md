# 🚀 Deployment Guide

## Quick Start (Local Development)

### Method 1: Using the Start Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This script will:
1. Create a virtual environment if needed
2. Install all dependencies
3. Start the web server on http://localhost:5000

### Method 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

### Required Configuration

1. **OpenAI API Key** (for AI image analysis):
   - Get your API key from https://platform.openai.com/api-keys
   - Set it in `.env` file or as environment variable

### Optional Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` with your values:
- Company information
- Pricing defaults (profit margin, overhead)
- Flask secret key

## Production Deployment

### Using Gunicorn (Recommended for Production)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t jobbid .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key jobbid
```

### Environment Variables for Production

Set these environment variables:

```bash
export OPENAI_API_KEY="your_api_key"
export SECRET_KEY="generate_random_secret_key"
export DEBUG="False"
export COMPANY_NAME="Your Company"
export COMPANY_ADDRESS="Your Address"
export COMPANY_PHONE="Your Phone"
export COMPANY_EMAIL="Your Email"
```

### Nginx Reverse Proxy

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Cloud Deployment

### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### AWS EC2

1. Launch an EC2 instance (Ubuntu)
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

3. Clone and setup:
```bash
git clone your-repo
cd jobbid
./start.sh
```

4. Use systemd to run as a service

### Railway / Render

These platforms work with minimal configuration:
1. Connect your GitHub repository
2. Set environment variables
3. Deploy!

## Security Considerations

### For Production:

1. **Always set a strong SECRET_KEY**
2. **Set DEBUG=False**
3. **Use HTTPS** (Let's Encrypt for free SSL)
4. **Restrict file uploads**:
   - Keep MAX_IMAGE_SIZE reasonable
   - Validate file types
5. **Secure API keys**:
   - Never commit API keys to git
   - Use environment variables or secret managers
6. **Database** (if adding one):
   - Use PostgreSQL for production
   - Enable backup

## Monitoring

Add monitoring for production:
- Application logs
- Error tracking (Sentry)
- Uptime monitoring
- Performance metrics

## Backup

Important directories to backup:
- `generated_bids/` - All generated PDFs
- `uploads/pricing_sheets/` - Custom pricing sheets
- Database (if implemented)

## Scaling

For high traffic:
1. Use multiple Gunicorn workers
2. Add Redis for caching
3. Use CDN for static files
4. Consider load balancer
5. Database connection pooling

## Troubleshooting

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### Permission denied
```bash
chmod +x start.sh
chmod +x cli.py
```

### Module not found
```bash
pip install -r requirements.txt
```

### OpenAI API errors
- Check your API key is set correctly
- Verify you have credits in your OpenAI account
- System works with mock analysis if API is not configured

## Updates

To update the application:
```bash
git pull
pip install -r requirements.txt --upgrade
# Restart the service
```

## Support

For issues:
1. Check logs in console
2. Verify environment variables
3. Test with sample data
4. Open GitHub issue if problem persists
