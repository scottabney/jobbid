#!/usr/bin/env python3
"""
Command Line Interface for Job Bid Generator
"""
import argparse
import sys
from pathlib import Path

from job_bid_manager import JobBidManager


def main():
    parser = argparse.ArgumentParser(
        description='Smart Job Bid Generator for Metal Welding & Fabrication',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate bid from images
  %(prog)s --project "Steel Gate" --images gate1.jpg gate2.jpg --client "John Smith"
  
  # Use custom pricing sheet
  %(prog)s --project "Railing" --images railing.jpg --pricing my_prices.xlsx
  
  # Set custom margins
  %(prog)s --project "Welding" --images weld.jpg --profit 0.30 --overhead 0.20
        """
    )
    
    # Required arguments
    parser.add_argument('--project', '-p', required=True,
                       help='Project name')
    parser.add_argument('--images', '-i', nargs='+', required=True,
                       help='One or more image files to analyze')
    
    # Optional arguments
    parser.add_argument('--client', '-c',
                       help='Client name')
    parser.add_argument('--client-email',
                       help='Client email')
    parser.add_argument('--client-phone',
                       help='Client phone')
    parser.add_argument('--client-address',
                       help='Client address')
    
    parser.add_argument('--description', '-d',
                       help='Project description')
    parser.add_argument('--pricing',
                       help='Path to pricing sheet (Excel or CSV)')
    
    parser.add_argument('--profit', type=float,
                       help='Profit margin (e.g., 0.25 for 25%%)')
    parser.add_argument('--overhead', type=float,
                       help='Overhead rate (e.g., 0.15 for 15%%)')
    
    parser.add_argument('--output', '-o',
                       help='Output filename for bid PDF')
    
    parser.add_argument('--api-key',
                       help='OpenAI API key (or set OPENAI_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Validate image files
    image_paths = []
    for img in args.images:
        path = Path(img)
        if not path.exists():
            print(f"Error: Image file not found: {img}", file=sys.stderr)
            sys.exit(1)
        image_paths.append(str(path.absolute()))
    
    # Initialize manager
    print("Initializing Job Bid Manager...")
    manager = JobBidManager(
        openai_api_key=args.api_key,
        pricing_sheet_path=args.pricing
    )
    
    # Prepare client info
    client_info = None
    if args.client:
        client_info = {
            'name': args.client,
            'email': args.client_email or '',
            'phone': args.client_phone or '',
            'address': args.client_address or ''
        }
    
    # Prepare kwargs
    kwargs = {}
    if args.description:
        kwargs['project_description'] = args.description
    if args.profit:
        kwargs['profit_margin'] = args.profit
    if args.overhead:
        kwargs['overhead_rate'] = args.overhead
    if args.output:
        kwargs['output_filename'] = args.output
    
    try:
        # Generate bid
        print(f"\nGenerating bid for: {args.project}")
        result = manager.generate_complete_bid(
            project_name=args.project,
            image_paths=image_paths,
            client_info=client_info,
            **kwargs
        )
        
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(f"\nBid document generated: {result['bid_path']}")
        print(f"Total Price: ${result['cost_breakdown']['final_price']:,.2f}")
        
        return 0
        
    except Exception as e:
        print(f"\nError generating bid: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
