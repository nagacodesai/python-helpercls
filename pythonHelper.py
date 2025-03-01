import os
import json
import csv
import logging
import random
import string
import requests
import pandas as pd
from datetime import datetime, timedelta

class PythonHelper:
    
    def __init__(self, log_file="app.log"):
        """Initialize the helper class and set up logging."""
        self.setup_logging(log_file)

    # ============== File Handling Methods ==============
    
    @staticmethod
    def getkeyvalueByNameFromEnvVaribles(keyName):
        return os.getenv(keyName)

    @staticmethod
    def read_json(file_path):
        """Read a JSON file and return data."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON file: {e}")
            return None

    @staticmethod
    def write_json(file_path, data):
        """Write data to a JSON file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.info(f"JSON file saved: {file_path}")
        except Exception as e:
            logging.error(f"Error writing JSON file: {e}")

    @staticmethod
    def read_csv(file_path):
        """Read a CSV file into a Pandas DataFrame."""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")
            return None

    @staticmethod
    def write_csv(file_path, data):
        """Write a Pandas DataFrame to a CSV file."""
        try:
            data.to_csv(file_path, index=False)
            logging.info(f"CSV file saved: {file_path}")
        except Exception as e:
            logging.error(f"Error writing CSV file: {e}")

    # ============== Logging Setup ==============

    @staticmethod
    def setup_logging(log_file):
        """Set up logging to a file and console."""
        logging.basicConfig(
            filename=log_file,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)

    # ============== Date & Time Methods ==============

    @staticmethod
    def get_current_timestamp():
        """Return the current timestamp in YYYY-MM-DD HH:MM:SS format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convert_date_format(date_str, input_format="%Y-%m-%d", output_format="%d-%m-%Y"):
        """Convert date format from input format to output format."""
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except ValueError as e:
            logging.error(f"Error in date conversion: {e}")
            return None

    @staticmethod
    def get_future_date(days=1):
        """Return a future date from today based on given days."""
        return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    # ============== API Request Methods ==============

    @staticmethod
    def send_get_request(url, params=None, headers=None):
        """Send a GET request and return the response."""
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"GET request error: {e}")
            return None

    @staticmethod
    def send_post_request(url, data=None, headers=None):
        """Send a POST request and return the response."""
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"POST request error: {e}")
            return None

    # ============== Data Processing Methods ==============

    @staticmethod
    def remove_duplicates(data):
        """Remove duplicate entries from a list."""
        return list(set(data))

    @staticmethod
    def fill_missing_values(df, column_name, fill_value="Unknown"):
        """Fill missing values in a specified column of a DataFrame."""
        if column_name in df.columns:
            df[column_name].fillna(fill_value, inplace=True)
            logging.info(f"Missing values in column '{column_name}' filled with '{fill_value}'")
        return df

    # ============== String Utility Methods ==============

    @staticmethod
    def generate_random_string(length=8):
        """Generate a random alphanumeric string."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def to_uppercase(text):
        """Convert a string to uppercase."""
        return text.upper()

    @staticmethod
    def to_lowercase(text):
        """Convert a string to lowercase."""
        return text.lower()

    # ============== Environment Variables ==============

    @staticmethod
    def get_env_variable(var_name, default_value=None):
        """Retrieve an environment variable."""
        return os.getenv(var_name, default_value)

# ============== Usage Example ==============
if __name__ == "__main__":
    helper = PythonHelper()

    # Example: Read & Write JSON
    sample_data = {"name": "Helium V2", "status": "Active"}
    helper.write_json("sample.json", sample_data)
    print(helper.read_json("sample.json"))

    # Example: Logging & API Calls
    logging.info("Helper class initialized successfully.")
    response = helper.send_get_request("https://jsonplaceholder.typicode.com/todos/1")
    print(response)

    # Example: Date and String Operations
    print(helper.get_current_timestamp())
    print(helper.generate_random_string(12))
