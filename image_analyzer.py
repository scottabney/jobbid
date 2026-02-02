"""
Image Analysis Module - Analyzes job site photos using AI vision
"""
import base64
from pathlib import Path
from typing import Dict, List, Optional
import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ImageAnalyzer:
    """Analyzes images to extract job details for welding and fabrication work"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the image analyzer with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '')
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze a single image and extract fabrication details
        
        Returns:
            Dictionary containing:
            - materials: List of materials identified
            - dimensions: Estimated dimensions
            - complexity: Job complexity assessment
            - processes: Welding/fabrication processes needed
            - recommendations: Additional notes and recommendations
        """
        if not self.client:
            return self._mock_analysis(image_path)
        
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Create the analysis prompt
            prompt = """Analyze this image for a metal welding and fabrication job bid. 
            
            Please identify:
            1. Materials visible (steel, aluminum, stainless steel, etc.)
            2. Approximate dimensions and scale
            3. Complexity level (simple, moderate, complex, very complex)
            4. Required welding processes (MIG, TIG, Stick, etc.)
            5. Fabrication work needed (cutting, bending, grinding, assembly, etc.)
            6. Any special considerations or challenges
            7. Estimated labor hours needed
            
            Provide detailed, specific observations that will help create an accurate bid."""
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the response into structured data
            return self._parse_analysis(analysis_text, image_path)
            
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return self._mock_analysis(image_path)
    
    def analyze_multiple_images(self, image_paths: List[str]) -> Dict:
        """
        Analyze multiple images and combine the results
        
        Returns:
            Combined analysis with aggregated information
        """
        analyses = []
        for image_path in image_paths:
            analysis = self.analyze_image(image_path)
            analyses.append(analysis)
        
        # Combine analyses
        combined = {
            'images_analyzed': len(analyses),
            'individual_analyses': analyses,
            'materials': self._merge_lists([a.get('materials', []) for a in analyses]),
            'processes': self._merge_lists([a.get('processes', []) for a in analyses]),
            'complexity': max([a.get('complexity_score', 1) for a in analyses]),
            'total_estimated_hours': sum([a.get('estimated_hours', 0) for a in analyses]),
            'combined_recommendations': self._merge_recommendations(analyses)
        }
        
        return combined
    
    def _parse_analysis(self, analysis_text: str, image_path: str) -> Dict:
        """Parse the AI response into structured data"""
        # Extract key information from the text
        result = {
            'image_path': image_path,
            'raw_analysis': analysis_text,
            'materials': self._extract_materials(analysis_text),
            'dimensions': self._extract_dimensions(analysis_text),
            'complexity': self._extract_complexity(analysis_text),
            'complexity_score': self._calculate_complexity_score(analysis_text),
            'processes': self._extract_processes(analysis_text),
            'estimated_hours': self._extract_hours(analysis_text),
            'recommendations': analysis_text
        }
        
        return result
    
    def _extract_materials(self, text: str) -> List[str]:
        """Extract material types from analysis text"""
        materials = []
        keywords = ['steel', 'aluminum', 'stainless', 'iron', 'metal', 'alloy']
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                materials.append(keyword.title())
        
        return list(set(materials)) if materials else ['Steel']
    
    def _extract_dimensions(self, text: str) -> str:
        """Extract dimension information"""
        # Look for dimension patterns
        import re
        patterns = [r'\d+\s*[xX]\s*\d+', r'\d+\s*ft', r'\d+\s*in', r'\d+\s*cm']
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return "To be measured on-site"
    
    def _extract_complexity(self, text: str) -> str:
        """Extract complexity level"""
        text_lower = text.lower()
        if 'very complex' in text_lower or 'extremely complex' in text_lower:
            return 'Very Complex'
        elif 'complex' in text_lower:
            return 'Complex'
        elif 'moderate' in text_lower:
            return 'Moderate'
        else:
            return 'Simple'
    
    def _calculate_complexity_score(self, text: str) -> int:
        """Calculate numerical complexity score (1-5)"""
        complexity = self._extract_complexity(text)
        complexity_map = {
            'Simple': 1,
            'Moderate': 2,
            'Complex': 3,
            'Very Complex': 4
        }
        return complexity_map.get(complexity, 2)
    
    def _extract_processes(self, text: str) -> List[str]:
        """Extract welding and fabrication processes"""
        processes = []
        keywords = {
            'MIG': ['mig', 'gmaw'],
            'TIG': ['tig', 'gtaw'],
            'Stick': ['stick', 'smaw'],
            'Cutting': ['cutting', 'plasma', 'torch'],
            'Bending': ['bending', 'brake'],
            'Grinding': ['grinding', 'finishing'],
            'Assembly': ['assembly', 'fitting']
        }
        
        text_lower = text.lower()
        for process, keywords_list in keywords.items():
            if any(kw in text_lower for kw in keywords_list):
                processes.append(process)
        
        return processes if processes else ['MIG Welding', 'Cutting', 'Assembly']
    
    def _extract_hours(self, text: str) -> float:
        """Extract estimated hours from analysis"""
        import re
        
        # Look for hour estimates
        patterns = [
            r'(\d+\.?\d*)\s*hours?',
            r'(\d+\.?\d*)\s*hrs?',
            r'(\d+)-(\d+)\s*hours?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    if len(match.groups()) > 1 and match.group(2):
                        # Range found, take average
                        return (float(match.group(1)) + float(match.group(2))) / 2
                    return float(match.group(1))
                except:
                    pass
        
        # Default estimate based on complexity
        complexity = self._extract_complexity(text)
        hours_map = {
            'Simple': 4,
            'Moderate': 8,
            'Complex': 16,
            'Very Complex': 24
        }
        return hours_map.get(complexity, 8)
    
    def _mock_analysis(self, image_path: str) -> Dict:
        """Provide mock analysis when API is not available"""
        return {
            'image_path': image_path,
            'raw_analysis': 'Mock analysis - OpenAI API not configured',
            'materials': ['Steel'],
            'dimensions': 'To be measured on-site',
            'complexity': 'Moderate',
            'complexity_score': 2,
            'processes': ['MIG Welding', 'Cutting', 'Grinding', 'Assembly'],
            'estimated_hours': 8,
            'recommendations': 'Professional analysis requires OpenAI API key configuration. This is a sample analysis for demonstration purposes.'
        }
    
    def _merge_lists(self, lists: List[List]) -> List:
        """Merge multiple lists and remove duplicates"""
        merged = []
        for lst in lists:
            merged.extend(lst)
        return list(set(merged))
    
    def _merge_recommendations(self, analyses: List[Dict]) -> str:
        """Combine recommendations from multiple analyses"""
        recommendations = []
        for idx, analysis in enumerate(analyses, 1):
            rec = analysis.get('recommendations', '')
            if rec:
                recommendations.append(f"Image {idx}: {rec}")
        
        return "\n\n".join(recommendations)
