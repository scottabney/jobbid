#!/usr/bin/env python3
"""
Demo script to showcase the Job Bid Generator capabilities
"""
from job_bid_manager import JobBidManager
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def demo_quick_bid():
    """Demo: Generate a quick bid without images"""
    print_header("DEMO 1: Quick Bid Generation (No Images)")
    
    print("Scenario: Customer calls about a steel railing job")
    print("We need a quick estimate...")
    print()
    
    # Initialize manager
    manager = JobBidManager()
    
    # Define the job
    materials = [
        {'material': 'Steel Tube 2"', 'quantity': 30, 'unit': 'ft'},
        {'material': 'Steel Angle 2x2', 'quantity': 15, 'unit': 'ft'},
        {'material': 'Welding Wire', 'quantity': 2, 'unit': 'spool'},
        {'material': 'Paint/Coating', 'quantity': 1, 'unit': 'gallon'}
    ]
    
    processes = {
        'MIG Welding': 6,
        'Cutting': 2,
        'Grinding/Finishing': 2,
        'Assembly': 2
    }
    
    print("📋 Job Details:")
    print("  • 30 feet of 2\" steel tubing")
    print("  • 15 feet of 2x2 angle iron")
    print("  • MIG welding, cutting, finishing")
    print("  • Estimated 12 hours total")
    print()
    
    # Calculate costs
    cost = manager.estimate_costs(
        materials=materials,
        labor_hours=12,
        processes=processes
    )
    
    print("💰 Cost Breakdown:")
    print(f"  Materials:  ${cost['material_cost']:>8,.2f}")
    print(f"  Labor:      ${cost['labor_cost']:>8,.2f}")
    print(f"  Processes:  ${cost['process_cost']:>8,.2f}")
    print(f"  Overhead:   ${cost['overhead']:>8,.2f}")
    print(f"  Profit:     ${cost['profit']:>8,.2f}")
    print(f"  {'─'*25}")
    print(f"  TOTAL:      ${cost['final_price']:>8,.2f}")
    print()
    
    # Generate bid
    bid_path = manager.create_bid(
        project_name="Residential Steel Railing",
        cost_breakdown=cost,
        client_info={
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'phone': '(555) 123-4567',
            'address': '123 Main St, Anytown, ST 12345'
        },
        project_description="""
        Custom steel railing fabrication for residential deck.
        30 linear feet of 2" steel tube top rail with 2x2 angle iron posts.
        Includes fabrication, powder coat finishing, and installation hardware.
        All work performed to code specifications.
        """
    )
    
    print(f"✅ Bid generated: {Path(bid_path).name}")
    print(f"📄 Location: {bid_path}")
    
    return bid_path


def demo_complex_bid():
    """Demo: Generate a complex commercial bid"""
    print_header("DEMO 2: Complex Commercial Project")
    
    print("Scenario: Large commercial fabrication project")
    print("Multiple materials and processes required...")
    print()
    
    manager = JobBidManager()
    
    materials = [
        {'material': 'Steel Plate 1/2"', 'quantity': 5, 'unit': 'sheet'},
        {'material': 'Steel I-Beam 6"', 'quantity': 40, 'unit': 'ft'},
        {'material': 'Stainless Steel', 'quantity': 200, 'unit': 'lb'},
        {'material': 'Aluminum', 'quantity': 100, 'unit': 'lb'},
        {'material': 'Welding Gas', 'quantity': 3, 'unit': 'tank'},
        {'material': 'Welding Wire', 'quantity': 5, 'unit': 'spool'},
        {'material': 'Hardware Kit', 'quantity': 10, 'unit': 'set'}
    ]
    
    processes = {
        'TIG Welding': 20,
        'MIG Welding': 15,
        'Plasma Cutting': 8,
        'Grinding/Finishing': 12,
        'Assembly': 10,
        'Design/Engineering': 5
    }
    
    print("📋 Job Details:")
    print("  • Custom structural steel framework")
    print("  • Mixed materials (steel, stainless, aluminum)")
    print("  • Precision TIG and MIG welding")
    print("  • Engineering design included")
    print("  • Estimated 70 hours total")
    print()
    
    cost = manager.estimate_costs(
        materials=materials,
        labor_hours=70,
        processes=processes,
        profit_margin=0.30,  # Higher margin for complex work
        overhead_rate=0.18
    )
    
    print("💰 Cost Breakdown:")
    print(f"  Materials:  ${cost['material_cost']:>9,.2f}")
    print(f"  Labor:      ${cost['labor_cost']:>9,.2f}")
    print(f"  Processes:  ${cost['process_cost']:>9,.2f}")
    print(f"  Overhead:   ${cost['overhead']:>9,.2f} (18%)")
    print(f"  Profit:     ${cost['profit']:>9,.2f} (30%)")
    print(f"  {'─'*30}")
    print(f"  TOTAL:      ${cost['final_price']:>9,.2f}")
    print()
    
    bid_path = manager.create_bid(
        project_name="Commercial Steel Framework",
        cost_breakdown=cost,
        client_info={
            'name': 'ABC Construction Corp',
            'email': 'contracts@abcconstruction.com',
            'phone': '(555) 987-6543',
            'address': '456 Industrial Pkwy, Metro City, ST 54321'
        },
        project_description="""
        Custom structural steel framework for commercial building renovation.
        Includes engineering design, material procurement, precision fabrication,
        welding, finishing, and quality inspection. Mixed material construction
        with steel, stainless steel, and aluminum components. All work performed
        to commercial building codes and industry standards.
        """
    )
    
    print(f"✅ Bid generated: {Path(bid_path).name}")
    print(f"📄 Location: {bid_path}")
    
    return bid_path


def demo_pricing_comparison():
    """Demo: Show pricing with different margins"""
    print_header("DEMO 3: Pricing Strategy Comparison")
    
    print("Scenario: Same job with different pricing strategies")
    print()
    
    manager = JobBidManager()
    
    materials = [
        {'material': 'Steel', 'quantity': 200, 'unit': 'lb'}
    ]
    
    processes = {
        'MIG Welding': 10,
        'Cutting': 3,
        'Finishing': 2
    }
    
    strategies = [
        ('Competitive', 0.20, 0.15),
        ('Standard', 0.25, 0.15),
        ('Premium', 0.35, 0.20)
    ]
    
    print("Same job, different strategies:")
    print()
    
    results = []
    for name, profit, overhead in strategies:
        cost = manager.estimate_costs(
            materials=materials,
            labor_hours=15,
            processes=processes,
            profit_margin=profit,
            overhead_rate=overhead
        )
        results.append((name, cost['final_price'], profit, overhead))
    
    print(f"{'Strategy':<15} {'Price':>10}  {'Profit %':>9}  {'Overhead %':>11}")
    print("─" * 55)
    for name, price, profit, overhead in results:
        print(f"{name:<15} ${price:>9,.2f}  {profit*100:>8.0f}%  {overhead*100:>10.0f}%")
    
    diff = results[-1][1] - results[0][1]
    print()
    print(f"💡 Price difference between Competitive and Premium: ${diff:,.2f}")


def demo_summary():
    """Show summary of capabilities"""
    print_header("Job Bid Generator - Capabilities Summary")
    
    print("✨ What This System Can Do:")
    print()
    print("  🤖 AI-Powered Analysis")
    print("     • Analyze job photos with GPT-4 Vision")
    print("     • Identify materials automatically")
    print("     • Detect processes and complexity")
    print("     • Estimate labor hours")
    print()
    print("  💰 Smart Pricing")
    print("     • Custom pricing sheets (Excel/CSV)")
    print("     • 27+ default materials")
    print("     • 10+ labor positions")
    print("     • Multiple welding processes")
    print("     • Configurable margins")
    print()
    print("  📄 Professional Output")
    print("     • Beautiful PDF documents")
    print("     • Detailed cost breakdowns")
    print("     • Company branding")
    print("     • Terms and conditions")
    print("     • Client signatures")
    print()
    print("  🖥️ Multiple Interfaces")
    print("     • Web application (Flask)")
    print("     • Command-line tool")
    print("     • Python API")
    print("     • REST endpoints")
    print()
    print("  🔧 Designed For:")
    print("     • Metal fabrication shops")
    print("     • Welding companies")
    print("     • Steel manufacturers")
    print("     • Custom metal work")
    print()


def main():
    """Run all demos"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + " "*15 + "JOB BID GENERATOR - DEMO" + " "*29 + "█")
    print("█" + " "*12 + "Smart Bidding for Metal Fabrication" + " "*21 + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    demo_summary()
    
    # Run demos
    bid1 = demo_quick_bid()
    bid2 = demo_complex_bid()
    demo_pricing_comparison()
    
    print_header("DEMO COMPLETE")
    
    print("Generated bid documents:")
    print(f"  1. {Path(bid1).name}")
    print(f"  2. {Path(bid2).name}")
    print()
    print("📂 All bids saved to: generated_bids/")
    print()
    print("🚀 Try it yourself:")
    print("   • Web UI:  python app.py")
    print("   • CLI:     python cli.py --help")
    print("   • Python:  See example_usage.py")
    print()
    print("✨ This is the GREATEST job bid generator you've ever seen!")
    print()


if __name__ == '__main__':
    main()
