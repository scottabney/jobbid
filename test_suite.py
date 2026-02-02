#!/usr/bin/env python3
"""
Comprehensive test suite for Job Bid Generator
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from job_bid_manager import JobBidManager
        from pricing_calculator import PricingCalculator
        from bid_generator import BidGenerator
        from image_analyzer import ImageAnalyzer
        import config
        print("  ✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_pricing_calculator():
    """Test pricing calculator functionality"""
    print("\nTesting pricing calculator...")
    try:
        from pricing_calculator import PricingCalculator
        
        calc = PricingCalculator()
        
        # Test material cost calculation
        materials = [
            {'material': 'Steel', 'quantity': 100, 'unit': 'lb'},
            {'material': 'Aluminum', 'quantity': 50, 'unit': 'lb'}
        ]
        
        processes = {
            'MIG Welding': 4,
            'Cutting': 2
        }
        
        cost = calc.generate_cost_breakdown(materials, 8, processes)
        
        assert cost['material_cost'] > 0, "Material cost should be greater than 0"
        assert cost['labor_cost'] > 0, "Labor cost should be greater than 0"
        assert cost['final_price'] > 0, "Final price should be greater than 0"
        
        print(f"  ✓ Cost calculation works: ${cost['final_price']:.2f}")
        return True
        
    except Exception as e:
        print(f"  ✗ Pricing calculator error: {e}")
        return False


def test_bid_generator():
    """Test bid document generation"""
    print("\nTesting bid generator...")
    try:
        from bid_generator import BidGenerator
        import tempfile
        
        gen = BidGenerator()
        
        # Create a test bid
        bid_data = {
            'project_name': 'Test Project',
            'project_description': 'Test description',
            'materials': ['Steel', 'Aluminum'],
            'processes': ['MIG Welding', 'Cutting'],
            'cost_breakdown': {
                'material_cost': 200.00,
                'labor_cost': 400.00,
                'process_cost': 100.00,
                'subtotal': 700.00,
                'overhead': 105.00,
                'overhead_rate': 0.15,
                'profit': 201.25,
                'profit_margin': 0.25,
                'final_price': 1006.25,
                'breakdown': {
                    'labor_hours': 8
                }
            }
        }
        
        # Generate to temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            output_path = f.name
        
        result = gen.generate_bid(bid_data, output_path)
        
        assert Path(result).exists(), "PDF should be created"
        assert Path(result).stat().st_size > 0, "PDF should not be empty"
        
        # Clean up
        Path(result).unlink()
        
        print("  ✓ Bid generation works")
        return True
        
    except Exception as e:
        print(f"  ✗ Bid generator error: {e}")
        return False


def test_job_bid_manager():
    """Test the main job bid manager"""
    print("\nTesting job bid manager...")
    try:
        from job_bid_manager import JobBidManager
        
        manager = JobBidManager()
        
        # Test pricing summary
        summary = manager.get_pricing_summary()
        assert 'material_count' in summary
        assert summary['material_count'] > 0
        
        print(f"  ✓ Manager initialized with {summary['material_count']} materials")
        return True
        
    except Exception as e:
        print(f"  ✗ Job bid manager error: {e}")
        return False


def test_custom_pricing_sheet():
    """Test loading custom pricing sheets"""
    print("\nTesting custom pricing sheet...")
    try:
        from pricing_calculator import PricingCalculator
        
        # Test with sample CSV
        calc = PricingCalculator('sample_pricing_materials.csv')
        
        summary = calc.get_pricing_summary()
        assert summary['material_count'] > 0, "Should load materials"
        
        print(f"  ✓ Loaded {summary['material_count']} materials from CSV")
        return True
        
    except Exception as e:
        print(f"  ✗ Custom pricing sheet error: {e}")
        return False


def test_complete_workflow():
    """Test complete workflow without images"""
    print("\nTesting complete workflow...")
    try:
        from job_bid_manager import JobBidManager
        import tempfile
        
        manager = JobBidManager()
        
        # Define test data
        materials = [
            {'material': 'Steel', 'quantity': 100, 'unit': 'lb'}
        ]
        
        processes = {
            'MIG Welding': 4,
            'Cutting': 2
        }
        
        # Calculate costs
        cost = manager.estimate_costs(
            materials=materials,
            labor_hours=6,
            processes=processes
        )
        
        # Generate bid
        with tempfile.TemporaryDirectory() as tmpdir:
            config_backup = __import__('config').OUTPUT_FOLDER
            __import__('config').OUTPUT_FOLDER = Path(tmpdir)
            
            bid_path = manager.create_bid(
                project_name="Test Workflow",
                cost_breakdown=cost
            )
            
            assert Path(bid_path).exists(), "Bid PDF should be created"
            
            __import__('config').OUTPUT_FOLDER = config_backup
        
        print(f"  ✓ Complete workflow successful: ${cost['final_price']:.2f}")
        return True
        
    except Exception as e:
        print(f"  ✗ Workflow error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Job Bid Generator - Test Suite")
    print("="*60)
    
    tests = [
        test_imports,
        test_pricing_calculator,
        test_bid_generator,
        test_job_bid_manager,
        test_custom_pricing_sheet,
        test_complete_workflow
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} of {total} tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
