from bs4 import BeautifulSoup
import numpy as np
import csv
from pathlib import Path
from typing import List, Dict, Optional

# Constants for CSS Selectors
# These classes are based on the specific e-commerce site structure (Flipkart/Amazon etc.)
PRODUCT_NAME_CLASS = "RG5Slk"
PRODUCT_SPECS_CLASS = "CMXw7N"
PRODUCT_PRICE_CLASS = "hZ3P6w DeU9vF"

class ParseData:
    """
    Parses HTML files to extract product information such as name, specifications,
    ratings, and price. Optimized to use lists for collection and proper error handling.
    """

    def __init__(self, file_path: str):
        """
        Initialize the parser with the directory path containing HTML files.

        Args:
            file_path (str): Path to the directory containing HTML files.
        """
        # Convert string path to Path object for better handling
        self.file_path = Path(file_path)
        
        # Initialize lists for O(1) appending during parsing
        self.product_names: List[str] = []
        self.product_specs: List[str] = []
        self.ratings: List[str] = []
        self.prices: List[str] = []

    def parse_data(self) -> Dict[str, np.ndarray]:
        """
        Fetches product information from available HTML files in the directory.

        Returns:
            Dict[str, np.ndarray]: A dictionary containing numpy arrays of 
            product names, specs, ratings, and prices.
        """
        if not self.file_path.exists():
            print(f"Warning: Directory {self.file_path} does not exist.")
            return self.get_data_as_numpy()

        # Iterate over all files in the directory
        for file_path in self.file_path.iterdir():
            # Process only .html files
            if file_path.suffix != '.html':
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as file_reader:
                    html_docs = file_reader.read()
            except IOError as e:
                print(f"Error reading {file_path}: {e}")
                continue
            
            soup = BeautifulSoup(html_docs, 'html.parser')
            self._extract_product_from_soup(soup)

        return self.get_data_as_numpy()

    def _extract_product_from_soup(self, soup: BeautifulSoup) -> None:
        """Helper method to extract individual fields from the soup object."""
        
        # 1. Product Name
        product_elem = soup.find("div", class_=PRODUCT_NAME_CLASS)
        if product_elem:
            # Extract text and take the part before the first hyphen
            name = product_elem.get_text(strip=True).split("-")[0].strip()
            self.product_names.append(name)
        else:
            self.product_names.append("Unknown")

        # 2. Specifications
        specs_elem = soup.find("div", class_=PRODUCT_SPECS_CLASS)
        if specs_elem:
            self.product_specs.append(specs_elem.get_text(strip=True))
        else:
            self.product_specs.append("N/A")

        # 3. Ratings
        # Finds the text node containing "Ratings"
        rating_elem = soup.find(string=lambda text: text and "Ratings" in text)
        if rating_elem:
            # Example format: "1,234 Ratings & ..." -> extract "1,234"
            rating_val = rating_elem.strip().split(" ")[0]
            self.ratings.append(rating_val)
        else:
            self.ratings.append("null")

        # 4. Price
        price_elem = soup.find("div", class_=PRODUCT_PRICE_CLASS)
        if price_elem:
            self.prices.append(price_elem.get_text(strip=True))
        else:
            self.prices.append("0")

    def get_data_as_numpy(self) -> Dict[str, np.ndarray]:
        """
        Converts the accumulated lists into NumPy arrays.
        
        Returns:
            Dict[str, np.ndarray]: Dictionary with keys 'product_names', 'product_specs', 
            'ratings', 'prices'.
        """
        return {
            "product_names": np.array(self.product_names),
            "product_specs": np.array(self.product_specs),
            "ratings": np.array(self.ratings),
            "prices": np.array(self.prices)
        }

    def save_to_csv(self, filename: str) -> None:
        """
        Saves the parsed data to a CSV file.

        Args:
            filename (str): The name (or path) of the CSV file to write to.
        """
        if not self.product_names:
            print("No data collected to save to CSV.")
            return

        print(f"Saving data to {filename}...")
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Product Name", "Specifications", "Ratings", "Price"])
                
                # Zip the lists to write row by row
                rows = zip(self.product_names, self.product_specs, self.ratings, self.prices)
                writer.writerows(rows)
                
            print(f"Successfully saved {len(self.product_names)} records to {filename}.")
        except IOError as e:
            print(f"Failed to save CSV: {e}")

    # Legacy method name for backward compatibility if needed, but updated logic
    def parse_data_to_list(self) -> tuple:
        """
        Legacy wrapper to match previous interface returning a tuple.
        Triggers parsing and returns tuple of numpy arrays/lists.
        """
        data = self.parse_data()
        return (data['product_names'], data['product_specs'], 
                data['prices'], data['ratings'])