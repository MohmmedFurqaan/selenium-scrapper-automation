from pathlib import Path
from typing import Union


class PathConfig:
    """Configuration class for managing application paths"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.data = self.project_root / 'data'
        self.scrapped_data = self.data / 'scrapped_data'
        self.html_files = self.scrapped_data / 'html_files'

    def store_scrapped_Outerhtml_files(self, query : str, page : int) -> Path:
        '''
            store all the scrapped outerHTML files into the data/scrapped_data/html_files/
            
            Args:
                query - the content/product to be searched 
                page - page number
            
            Returns:
                Path -> the path of that file

        '''
        
        return self.html_files / f'{query}_{page}.html'


    def validate_paths(self) -> list[str]:
        """
        Validate that all required paths exist
        
        Returns:
            list[str]: List of error messages for missing paths
        """
        required_paths = [
            (self.project_root, "Project root"),
            (self.data, "data directory"),
            (self.scrapped_data, "Scrapped Data"),
            (self.html_files, "html_files")
        ]
        
        errors = []
        for path, name in required_paths:
            if not path.exists():
                errors.append(f"{name} not found at: {path}")
                
        return errors