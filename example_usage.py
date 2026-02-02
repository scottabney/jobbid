"""
Example script showing how to use the Job Bid Manager
"""
from job_bid_manager import JobBidManager
from pathlib import Path

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===\n")
    
    # Initialize the manager
    manager = JobBidManager()
    
    # Example: Generate a bid from images
    # (Replace with actual image paths)
    image_paths = [
        'path/to/your/image1.jpg',
        'path/to/your/image2.jpg'
    ]
    
    # Note: This is just an example - you'll need actual images
    # For testing without images, see example_without_images() below
    
    try:
        result = manager.generate_complete_bid(
            project_name="Custom Steel Railing",
            image_paths=image_paths,
            client_info={
                'name': 'John Smith',
                'email': 'john@example.com',
                'phone': '(555) 123-4567',
                'address': '456 Oak Street, City, ST 12345'
            }
        )
        
        print(f"Success! Bid generated: {result['bid_path']}")
        print(f"Total Price: ${result['cost_breakdown']['final_price']:,.2f}")
        
    except Exception as e:
        print(f"Note: {e}")
        print("This is expected if you don't have actual images yet.")


def example_without_images():
    """Example showing manual bid creation without image analysis"""
    print("\n=== Manual Bid Creation (No Images) ===\n")
    
    manager = JobBidManager()
    
    # Define materials manually
    materials = [
        {'material': 'Steel', 'quantity': 150, 'unit': 'lb'},
        {'material': 'Steel Tube 2"', 'quantity': 20, 'unit': 'ft'},
        {'material': 'Welding Wire', 'quantity': 2, 'unit': 'spool'},
    ]
    
    # Define processes and hours
    processes = {
        'MIG Welding': 8,
        'Cutting': 3,
        'Grinding/Finishing': 2,
        'Assembly': 3
    }
    
    # Calculate costs
    cost_breakdown = manager.estimate_costs(
        materials=materials,
        labor_hours=16,
        processes=processes,
        profit_margin=0.25,
        overhead_rate=0.15
    )
    
    print("Cost Breakdown:")
    print(f"  Materials: ${cost_breakdown['material_cost']:,.2f}")
    print(f"  Labor: ${cost_breakdown['labor_cost']:,.2f}")
    print(f"  Processes: ${cost_breakdown['process_cost']:,.2f}")
    print(f"  Overhead: ${cost_breakdown['overhead']:,.2f}")
    print(f"  Profit: ${cost_breakdown['profit']:,.2f}")
    print(f"  TOTAL: ${cost_breakdown['final_price']:,.2f}")
    
    # Create bid document
    bid_path = manager.create_bid(
        project_name="Steel Railing Project",
        cost_breakdown=cost_breakdown,
        client_info={
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        },
        project_description="""
        Custom steel railing fabrication for residential deck.
        Includes 20 feet of 2" steel tube railing with posts,
        powder-coated finish, and professional installation.
        """
    )
    
    print(f"\nBid document created: {bid_path}")


def example_with_custom_pricing():
    """Example using custom pricing sheet"""
    print("\n=== Custom Pricing Example ===\n")
    
    # Initialize with custom pricing sheet
    # (You can create your own Excel or CSV file)
    pricing_sheet = 'sample_pricing_materials.csv'
    
    manager = JobBidManager(pricing_sheet_path=pricing_sheet)
    
    # Show loaded pricing
    summary = manager.get_pricing_summary()
    print(f"Loaded {summary['material_count']} materials")
    print(f"Available materials: {', '.join(summary['materials'][:5])}...")
    
    # Continue with bid generation...
    print("\nYou can now use this manager with your custom pricing!")


def example_quick_estimate():
    """Quick cost estimate"""
    print("\n=== Quick Estimate ===\n")
    
    manager = JobBidManager()
    
    # Quick estimate for a simple job
    materials = [
        {'material': 'Steel', 'quantity': 100, 'unit': 'lb'}
    ]
    
    processes = {
        'MIG Welding': 4,
        'Cutting': 2
    }
    
    cost = manager.estimate_costs(
        materials=materials,
        labor_hours=6,
        processes=processes
    )
    
    print(f"Quick estimate for 6 hours of work with 100 lbs steel:")
    print(f"Total Price: ${cost['final_price']:,.2f}")


if __name__ == '__main__':
    print("Job Bid Generator - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_without_images()
    example_quick_estimate()
    example_with_custom_pricing()
    
    print("\n" + "=" * 60)
    print("For image-based analysis, set up your OPENAI_API_KEY")
    print("and use actual job photos!")
