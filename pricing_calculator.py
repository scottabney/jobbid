"""
Pricing Calculator - Handles pricing sheets and cost calculations
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import csv


class PricingCalculator:
    """Calculate job costs based on uploaded pricing sheets and job details"""
    
    def __init__(self, pricing_sheet_path: Optional[str] = None):
        """Initialize with optional pricing sheet"""
        self.pricing_data = None
        self.material_prices = {}
        self.labor_rates = {}
        self.process_rates = {}
        
        if pricing_sheet_path:
            self.load_pricing_sheet(pricing_sheet_path)
        else:
            self._load_default_pricing()
    
    def load_pricing_sheet(self, file_path: str) -> bool:
        """
        Load pricing data from Excel or CSV file
        
        Expected format:
        - Sheet/section for materials with columns: Material, Unit, Price
        - Sheet/section for labor with columns: Position, HourlyRate
        - Sheet/section for processes with columns: Process, Rate
        """
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                # Load Excel file
                excel_file = pd.ExcelFile(file_path)
                
                # Try to find materials sheet
                for sheet_name in excel_file.sheet_names:
                    if 'material' in sheet_name.lower():
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)
                        self._parse_materials(df)
                    elif 'labor' in sheet_name.lower():
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)
                        self._parse_labor(df)
                    elif 'process' in sheet_name.lower():
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)
                        self._parse_processes(df)
                
            elif file_path.suffix.lower() == '.csv':
                # Load CSV file
                df = pd.read_csv(file_path)
                self._parse_pricing_csv(df)
            
            return True
            
        except Exception as e:
            print(f"Error loading pricing sheet: {str(e)}")
            self._load_default_pricing()
            return False
    
    def _parse_materials(self, df: pd.DataFrame):
        """Parse materials pricing from DataFrame"""
        try:
            # Look for relevant columns
            material_col = None
            price_col = None
            unit_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'material' in col_lower or 'item' in col_lower:
                    material_col = col
                elif 'price' in col_lower or 'cost' in col_lower:
                    price_col = col
                elif 'unit' in col_lower:
                    unit_col = col
            
            if material_col and price_col:
                for _, row in df.iterrows():
                    material = str(row[material_col]).strip()
                    try:
                        price = float(row[price_col])
                        unit = str(row[unit_col]).strip() if unit_col else 'unit'
                        self.material_prices[material] = {'price': price, 'unit': unit}
                    except (ValueError, TypeError):
                        continue
                        
        except Exception as e:
            print(f"Error parsing materials: {str(e)}")
    
    def _parse_labor(self, df: pd.DataFrame):
        """Parse labor rates from DataFrame"""
        try:
            position_col = None
            rate_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'position' in col_lower or 'role' in col_lower or 'title' in col_lower:
                    position_col = col
                elif 'rate' in col_lower or 'hourly' in col_lower:
                    rate_col = col
            
            if position_col and rate_col:
                for _, row in df.iterrows():
                    position = str(row[position_col]).strip()
                    try:
                        rate = float(row[rate_col])
                        self.labor_rates[position] = rate
                    except (ValueError, TypeError):
                        continue
                        
        except Exception as e:
            print(f"Error parsing labor: {str(e)}")
    
    def _parse_processes(self, df: pd.DataFrame):
        """Parse process rates from DataFrame"""
        try:
            process_col = None
            rate_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'process' in col_lower or 'service' in col_lower:
                    process_col = col
                elif 'rate' in col_lower or 'cost' in col_lower:
                    rate_col = col
            
            if process_col and rate_col:
                for _, row in df.iterrows():
                    process = str(row[process_col]).strip()
                    try:
                        rate = float(row[rate_col])
                        self.process_rates[process] = rate
                    except (ValueError, TypeError):
                        continue
                        
        except Exception as e:
            print(f"Error parsing processes: {str(e)}")
    
    def _parse_pricing_csv(self, df: pd.DataFrame):
        """Parse a general pricing CSV"""
        # Try to intelligently parse the CSV
        if 'Material' in df.columns or 'material' in df.columns:
            self._parse_materials(df)
        elif 'Position' in df.columns or 'position' in df.columns:
            self._parse_labor(df)
        elif 'Process' in df.columns or 'process' in df.columns:
            self._parse_processes(df)
    
    def _load_default_pricing(self):
        """Load default pricing data"""
        # Default material prices (per unit)
        self.material_prices = {
            'Steel': {'price': 0.75, 'unit': 'lb'},
            'Aluminum': {'price': 2.50, 'unit': 'lb'},
            'Stainless Steel': {'price': 3.00, 'unit': 'lb'},
            'Steel Plate 1/4"': {'price': 120.00, 'unit': 'sheet'},
            'Steel Plate 1/2"': {'price': 240.00, 'unit': 'sheet'},
            'Steel Tube 2"': {'price': 15.00, 'unit': 'ft'},
            'Steel Angle 2x2': {'price': 8.00, 'unit': 'ft'},
            'Welding Gas': {'price': 25.00, 'unit': 'tank'},
            'Welding Wire': {'price': 50.00, 'unit': 'spool'},
            'Electrodes': {'price': 30.00, 'unit': 'box'},
        }
        
        # Default labor rates (per hour)
        self.labor_rates = {
            'Master Welder': 75.00,
            'Welder': 55.00,
            'Fabricator': 50.00,
            'Helper': 35.00,
            'Shop Rate': 65.00
        }
        
        # Default process rates
        self.process_rates = {
            'MIG Welding': 65.00,
            'TIG Welding': 85.00,
            'Stick Welding': 60.00,
            'Plasma Cutting': 45.00,
            'Grinding/Finishing': 40.00,
            'Assembly': 50.00,
            'Design/Engineering': 95.00
        }
    
    def calculate_material_cost(self, materials: List[Dict]) -> float:
        """
        Calculate total material costs
        
        Args:
            materials: List of dicts with 'material', 'quantity', 'unit'
        """
        total = 0.0
        
        for item in materials:
            material_name = item.get('material', '')
            quantity = item.get('quantity', 0)
            
            # Find matching material in pricing
            price_info = self._find_material_price(material_name)
            if price_info:
                total += price_info['price'] * quantity
        
        return total
    
    def calculate_labor_cost(self, hours: float, position: str = 'Shop Rate') -> float:
        """Calculate labor cost based on hours and position"""
        rate = self.labor_rates.get(position, self.labor_rates.get('Shop Rate', 65.00))
        return hours * rate
    
    def calculate_process_cost(self, processes: List[str], hours_per_process: Dict[str, float]) -> float:
        """
        Calculate cost for specific processes
        
        Args:
            processes: List of process names
            hours_per_process: Dict mapping process to hours
        """
        total = 0.0
        
        for process in processes:
            hours = hours_per_process.get(process, 0)
            rate = self.process_rates.get(process, 50.00)
            total += hours * rate
        
        return total
    
    def _find_material_price(self, material_name: str) -> Optional[Dict]:
        """Find material price by name (fuzzy matching)"""
        material_lower = material_name.lower()
        
        # Exact match
        if material_name in self.material_prices:
            return self.material_prices[material_name]
        
        # Fuzzy match
        for key, value in self.material_prices.items():
            if material_lower in key.lower() or key.lower() in material_lower:
                return value
        
        # Default fallback
        return {'price': 50.00, 'unit': 'unit'}
    
    def generate_cost_breakdown(self, 
                                materials: List[Dict],
                                labor_hours: float,
                                processes: Dict[str, float],
                                profit_margin: float = 0.25,
                                overhead_rate: float = 0.15) -> Dict:
        """
        Generate complete cost breakdown
        
        Returns:
            Dictionary with detailed cost breakdown
        """
        # Calculate base costs
        material_cost = self.calculate_material_cost(materials)
        labor_cost = self.calculate_labor_cost(labor_hours)
        process_cost = self.calculate_process_cost(list(processes.keys()), processes)
        
        # Subtotal
        subtotal = material_cost + labor_cost + process_cost
        
        # Overhead
        overhead = subtotal * overhead_rate
        
        # Total before profit
        total_cost = subtotal + overhead
        
        # Profit
        profit = total_cost * profit_margin
        
        # Final price
        final_price = total_cost + profit
        
        return {
            'material_cost': round(material_cost, 2),
            'labor_cost': round(labor_cost, 2),
            'process_cost': round(process_cost, 2),
            'subtotal': round(subtotal, 2),
            'overhead': round(overhead, 2),
            'overhead_rate': overhead_rate,
            'total_cost': round(total_cost, 2),
            'profit': round(profit, 2),
            'profit_margin': profit_margin,
            'final_price': round(final_price, 2),
            'breakdown': {
                'materials': materials,
                'labor_hours': labor_hours,
                'processes': processes
            }
        }
    
    def get_pricing_summary(self) -> Dict:
        """Get summary of loaded pricing data"""
        return {
            'material_count': len(self.material_prices),
            'materials': list(self.material_prices.keys()),
            'labor_positions': list(self.labor_rates.keys()),
            'processes': list(self.process_rates.keys())
        }
