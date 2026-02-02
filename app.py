"""
Web Application for Job Bid Generator
"""
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import json

import config
from job_bid_manager import JobBidManager


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = str(config.UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = max(config.MAX_IMAGE_SIZE, config.MAX_PRICING_SIZE)

# Initialize the job bid manager
bid_manager = JobBidManager()


# Template filters
@app.template_filter('basename')
def basename_filter(path):
    """Get basename of a path"""
    return Path(path).name


@app.template_filter('timestamp_to_date')
def timestamp_to_date_filter(timestamp):
    """Convert timestamp to readable date"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%B %d, %Y at %I:%M %p')


@app.template_filter('filesizeformat')
def filesizeformat_filter(size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', 
                         company_name=config.COMPANY_NAME,
                         pricing_summary=bid_manager.get_pricing_summary())


@app.route('/upload_pricing', methods=['POST'])
def upload_pricing():
    """Upload pricing sheet"""
    if 'pricing_file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['pricing_file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename, config.ALLOWED_PRICING_EXTENSIONS):
        filename = secure_filename(file.filename)
        filepath = config.PRICING_SHEET_FOLDER / filename
        file.save(str(filepath))
        
        # Load the pricing sheet
        success = bid_manager.load_pricing_sheet(str(filepath))
        
        if success:
            flash('Pricing sheet uploaded and loaded successfully!', 'success')
        else:
            flash('Pricing sheet uploaded but there were issues loading it. Using defaults.', 'warning')
        
        return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload Excel (.xlsx, .xls) or CSV file.', 'error')
    return redirect(url_for('index'))


@app.route('/create_bid', methods=['GET', 'POST'])
def create_bid():
    """Create a new bid"""
    if request.method == 'GET':
        return render_template('create_bid.html')
    
    # Handle POST request
    try:
        # Get form data
        project_name = request.form.get('project_name', 'Unnamed Project')
        client_name = request.form.get('client_name', '')
        client_email = request.form.get('client_email', '')
        client_phone = request.form.get('client_phone', '')
        client_address = request.form.get('client_address', '')
        project_description = request.form.get('project_description', '')
        
        # Get uploaded images
        image_files = request.files.getlist('images')
        image_paths = []
        
        for file in image_files:
            if file and file.filename and allowed_file(file.filename, config.ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(file.filename)
                filepath = config.IMAGE_FOLDER / filename
                file.save(str(filepath))
                image_paths.append(str(filepath))
        
        if not image_paths:
            flash('Please upload at least one image', 'error')
            return redirect(url_for('create_bid'))
        
        # Prepare client info
        client_info = None
        if client_name:
            client_info = {
                'name': client_name,
                'email': client_email,
                'phone': client_phone,
                'address': client_address
            }
        
        # Generate bid
        result = bid_manager.generate_complete_bid(
            project_name=project_name,
            image_paths=image_paths,
            client_info=client_info,
            project_description=project_description or None
        )
        
        # Save bid data
        bid_data_path = config.OUTPUT_FOLDER / f"{Path(result['bid_path']).stem}_data.json"
        bid_manager.save_bid_data(str(bid_data_path))
        
        return render_template('bid_result.html',
                             result=result,
                             bid_filename=Path(result['bid_path']).name)
    
    except Exception as e:
        flash(f'Error generating bid: {str(e)}', 'error')
        return redirect(url_for('create_bid'))


@app.route('/download_bid/<filename>')
def download_bid(filename):
    """Download a generated bid"""
    filepath = config.OUTPUT_FOLDER / secure_filename(filename)
    
    if not filepath.exists():
        flash('Bid file not found', 'error')
        return redirect(url_for('index'))
    
    return send_file(str(filepath), as_attachment=True)


@app.route('/view_bids')
def view_bids():
    """View all generated bids"""
    bids = []
    
    for pdf_file in config.OUTPUT_FOLDER.glob('*.pdf'):
        json_file = pdf_file.parent / f"{pdf_file.stem}_data.json"
        
        bid_info = {
            'filename': pdf_file.name,
            'created': pdf_file.stat().st_mtime,
            'size': pdf_file.stat().st_size
        }
        
        # Try to load additional data
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    bid_info['project_name'] = data.get('project_name', 'Unknown')
                    bid_info['total'] = data.get('cost_breakdown', {}).get('final_price', 0)
            except:
                pass
        
        bids.append(bid_info)
    
    # Sort by creation time, newest first
    bids.sort(key=lambda x: x['created'], reverse=True)
    
    return render_template('view_bids.html', bids=bids)


@app.route('/api/analyze_image', methods=['POST'])
def api_analyze_image():
    """API endpoint to analyze a single image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    if not allowed_file(file.filename, config.ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save and analyze
    filename = secure_filename(file.filename)
    filepath = config.IMAGE_FOLDER / filename
    file.save(str(filepath))
    
    analysis = bid_manager.image_analyzer.analyze_image(str(filepath))
    
    return jsonify(analysis)


@app.route('/api/estimate_cost', methods=['POST'])
def api_estimate_cost():
    """API endpoint to estimate costs"""
    data = request.get_json()
    
    materials = data.get('materials', [])
    labor_hours = data.get('labor_hours', 8)
    processes = data.get('processes', {})
    
    cost_breakdown = bid_manager.estimate_costs(
        materials=materials,
        labor_hours=labor_hours,
        processes=processes
    )
    
    return jsonify(cost_breakdown)


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
