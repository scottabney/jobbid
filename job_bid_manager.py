"""
Main Job Bid Application - Integrates all components
"""
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from image_analyzer import ImageAnalyzer
from pricing_calculator import PricingCalculator
from bid_generator import BidGenerator
import config


class JobBidManager:
    """Main class that orchestrates the bid generation process"""
    
    def __init__(self, openai_api_key: Optional[str] = None, pricing_sheet_path: Optional[str] = None):
        """
        Initialize the Job Bid Manager
        
        Args:
            openai_api_key: OpenAI API key for image analysis
            pricing_sheet_path: Path to pricing sheet (Excel/CSV)
        """
        self.image_analyzer = ImageAnalyzer(openai_api_key or config.OPENAI_API_KEY)
        self.pricing_calculator = PricingCalculator(pricing_sheet_path)
        self.bid_generator = BidGenerator({
            'name': config.COMPANY_NAME,
            'address': config.COMPANY_ADDRESS,
            'phone': config.COMPANY_PHONE,
            'email': config.COMPANY_EMAIL
        })
        
        self.current_analysis = None
        self.current_bid_data = None
    
    def analyze_job_from_images(self, image_paths: List[str]) -> Dict:
        """
        Analyze job from one or more images
        
        Args:
            image_paths: List of paths to job site images
            
        Returns:
            Analysis results dictionary
        """
        print(f"Analyzing {len(image_paths)} image(s)...")
        
        if len(image_paths) == 1:
            analysis = self.image_analyzer.analyze_image(image_paths[0])
        else:
            analysis = self.image_analyzer.analyze_multiple_images(image_paths)
        
        self.current_analysis = analysis
        return analysis
    
    def estimate_costs(self, 
                      analysis: Optional[Dict] = None,
                      materials: Optional[List[Dict]] = None,
                      labor_hours: Optional[float] = None,
                      processes: Optional[Dict[str, float]] = None,
                      profit_margin: Optional[float] = None,
                      overhead_rate: Optional[float] = None) -> Dict:
        """
        Estimate costs based on analysis or manual input
        
        Args:
            analysis: Analysis from image analyzer (optional)
            materials: List of materials (optional, extracted from analysis if not provided)
            labor_hours: Total labor hours (optional, extracted from analysis if not provided)
            processes: Dict of process to hours (optional, extracted from analysis if not provided)
            profit_margin: Profit margin percentage (optional, uses default if not provided)
            overhead_rate: Overhead rate percentage (optional, uses default if not provided)
            
        Returns:
            Cost breakdown dictionary
        """
        # Use current analysis if not provided
        if analysis is None:
            analysis = self.current_analysis or {}
        
        # Extract materials
        if materials is None:
            materials = self._extract_materials_from_analysis(analysis)
        
        # Extract labor hours
        if labor_hours is None:
            if 'total_estimated_hours' in analysis:
                labor_hours = analysis['total_estimated_hours']
            elif 'estimated_hours' in analysis:
                labor_hours = analysis['estimated_hours']
            else:
                labor_hours = 8  # Default
        
        # Extract processes
        if processes is None:
            processes = self._extract_processes_from_analysis(analysis, labor_hours)
        
        # Use defaults for margin and overhead if not provided
        profit_margin = profit_margin or config.DEFAULT_PROFIT_MARGIN
        overhead_rate = overhead_rate or config.DEFAULT_OVERHEAD_RATE
        
        # Calculate costs
        cost_breakdown = self.pricing_calculator.generate_cost_breakdown(
            materials=materials,
            labor_hours=labor_hours,
            processes=processes,
            profit_margin=profit_margin,
            overhead_rate=overhead_rate
        )
        
        return cost_breakdown
    
    def create_bid(self,
                  project_name: str,
                  cost_breakdown: Optional[Dict] = None,
                  analysis: Optional[Dict] = None,
                  client_info: Optional[Dict] = None,
                  output_filename: Optional[str] = None,
                  **kwargs) -> str:
        """
        Create a complete bid document
        
        Args:
            project_name: Name of the project
            cost_breakdown: Cost breakdown (if None, will calculate from analysis)
            analysis: Analysis data (if None, uses current analysis)
            client_info: Client information dictionary
            output_filename: Custom output filename (optional)
            **kwargs: Additional bid data (project_description, scope_of_work, terms, etc.)
            
        Returns:
            Path to generated bid PDF
        """
        # Use current analysis if not provided
        if analysis is None:
            analysis = self.current_analysis or {}
        
        # Calculate costs if not provided
        if cost_breakdown is None:
            cost_breakdown = self.estimate_costs(analysis)
        
        # Prepare bid data
        bid_data = {
            'project_name': project_name,
            'project_description': kwargs.get('project_description', self._generate_project_description(analysis)),
            'materials': self._get_materials_list(analysis),
            'processes': self._get_processes_list(analysis),
            'scope_of_work': kwargs.get('scope_of_work', self._generate_scope_of_work(analysis)),
            'cost_breakdown': cost_breakdown,
            'bid_number': kwargs.get('bid_number', f"BID-{datetime.now().strftime('%Y%m%d-%H%M%S')}"),
            'date': kwargs.get('date', datetime.now().strftime('%B %d, %Y')),
            'valid_until': kwargs.get('valid_until', (datetime.now() + timedelta(days=30)).strftime('%B %d, %Y')),
            'terms': kwargs.get('terms')
        }
        
        # Generate output filename
        if output_filename is None:
            safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"bid_{safe_name}_{timestamp}.pdf"
        
        output_path = config.OUTPUT_FOLDER / output_filename
        
        # Generate bid
        print(f"Generating bid document: {output_path}")
        self.bid_generator.generate_bid(bid_data, str(output_path), client_info)
        
        self.current_bid_data = bid_data
        
        return str(output_path)
    
    def generate_complete_bid(self,
                            project_name: str,
                            image_paths: List[str],
                            client_info: Optional[Dict] = None,
                            **kwargs) -> Dict:
        """
        Complete end-to-end bid generation from images to PDF
        
        Args:
            project_name: Name of the project
            image_paths: List of image paths to analyze
            client_info: Client information
            **kwargs: Additional parameters for customization
            
        Returns:
            Dictionary with analysis, costs, and PDF path
        """
        # Step 1: Analyze images
        print("\n=== Step 1: Analyzing Images ===")
        analysis = self.analyze_job_from_images(image_paths)
        
        # Step 2: Estimate costs
        print("\n=== Step 2: Estimating Costs ===")
        cost_breakdown = self.estimate_costs(analysis, **kwargs)
        
        # Step 3: Generate bid document
        print("\n=== Step 3: Generating Bid Document ===")
        bid_path = self.create_bid(
            project_name=project_name,
            cost_breakdown=cost_breakdown,
            analysis=analysis,
            client_info=client_info,
            **kwargs
        )
        
        # Return complete results
        results = {
            'analysis': analysis,
            'cost_breakdown': cost_breakdown,
            'bid_path': bid_path,
            'summary': self._create_summary(project_name, analysis, cost_breakdown, bid_path)
        }
        
        print("\n=== Bid Generation Complete ===")
        print(results['summary'])
        
        return results
    
    def _extract_materials_from_analysis(self, analysis: Dict) -> List[Dict]:
        """Extract materials list from analysis"""
        materials_list = []
        
        # Get materials from analysis
        materials = analysis.get('materials', [])
        if isinstance(materials, str):
            materials = [materials]
        
        # Create material entries with default quantities
        for material in materials:
            materials_list.append({
                'material': material,
                'quantity': 100,  # Default quantity in lbs
                'unit': 'lb'
            })
        
        return materials_list
    
    def _extract_processes_from_analysis(self, analysis: Dict, total_hours: float) -> Dict[str, float]:
        """Extract processes and estimate hours for each"""
        processes = analysis.get('processes', [])
        if not processes:
            return {'MIG Welding': total_hours * 0.5, 'Assembly': total_hours * 0.3, 'Finishing': total_hours * 0.2}
        
        # Distribute hours among processes
        hours_per_process = total_hours / len(processes)
        return {process: hours_per_process for process in processes}
    
    def _get_materials_list(self, analysis: Dict) -> List[str]:
        """Get simple materials list"""
        materials = analysis.get('materials', [])
        if isinstance(materials, str):
            return [materials]
        return materials
    
    def _get_processes_list(self, analysis: Dict) -> List[str]:
        """Get simple processes list"""
        processes = analysis.get('processes', [])
        if isinstance(processes, str):
            return [processes]
        return processes
    
    def _generate_project_description(self, analysis: Dict) -> str:
        """Generate project description from analysis"""
        if 'recommendations' in analysis:
            return analysis['recommendations'][:500]  # First 500 chars
        
        materials = self._get_materials_list(analysis)
        processes = self._get_processes_list(analysis)
        complexity = analysis.get('complexity', 'Moderate')
        
        desc = f"This is a {complexity.lower()} complexity metal fabrication project involving {', '.join(materials)}. "
        desc += f"Required processes include: {', '.join(processes)}. "
        desc += "All work will be performed to industry standards with quality materials and skilled craftsmanship."
        
        return desc
    
    def _generate_scope_of_work(self, analysis: Dict) -> List[str]:
        """Generate scope of work from analysis"""
        scope = []
        
        materials = self._get_materials_list(analysis)
        processes = self._get_processes_list(analysis)
        
        scope.append(f"Material procurement: {', '.join(materials)}")
        
        for process in processes:
            scope.append(f"{process} operations")
        
        scope.extend([
            'Quality control and inspection',
            'Surface finishing and preparation',
            'Final assembly and testing'
        ])
        
        return scope
    
    def _create_summary(self, project_name: str, analysis: Dict, cost_breakdown: Dict, bid_path: str) -> str:
        """Create a summary of the bid"""
        summary = f"""
JOB BID SUMMARY
{'=' * 60}
Project: {project_name}
Complexity: {analysis.get('complexity', 'N/A')}
Estimated Hours: {analysis.get('total_estimated_hours', analysis.get('estimated_hours', 'N/A'))}

Materials: {', '.join(self._get_materials_list(analysis))}
Processes: {', '.join(self._get_processes_list(analysis))}

PRICING:
  Materials: ${cost_breakdown['material_cost']:,.2f}
  Labor: ${cost_breakdown['labor_cost']:,.2f}
  Processes: ${cost_breakdown['process_cost']:,.2f}
  Overhead: ${cost_breakdown['overhead']:,.2f}
  Profit: ${cost_breakdown['profit']:,.2f}
  
  TOTAL BID: ${cost_breakdown['final_price']:,.2f}

Bid document saved to: {bid_path}
{'=' * 60}
        """
        return summary.strip()
    
    def load_pricing_sheet(self, file_path: str) -> bool:
        """Load a new pricing sheet"""
        return self.pricing_calculator.load_pricing_sheet(file_path)
    
    def get_pricing_summary(self) -> Dict:
        """Get summary of current pricing data"""
        return self.pricing_calculator.get_pricing_summary()
    
    def save_bid_data(self, output_path: str) -> str:
        """Save current bid data to JSON"""
        if self.current_bid_data is None:
            raise ValueError("No bid data to save")
        
        with open(output_path, 'w') as f:
            json.dump(self.current_bid_data, f, indent=2)
        
        return output_path
