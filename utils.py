import pandas as pd
import os

def load_menu(file_path):
    """ 
    Loads menu data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: The menu data, or an empty DataFrame if an error occurs.
    """
    try:
        menu_data = pd.read_csv(file_path)
        menu_data.columns = menu_data.columns.str.strip()  # Clean column names
        return menu_data
    except FileNotFoundError:
        print(f"Error: The menu file could not be found at {file_path}. Please check the file path.")
        return pd.DataFrame()  # Return empty DataFrame in case of error
    except Exception as e:
        print(f"Unexpected error loading menu: {e}")
        return pd.DataFrame()

def load_stop_list(file_path):
    """ 
    Loads a list of out-of-stock items from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        list: List of out-of-stock item names, or an empty list if an error occurs.
    """
    try:
        stop_list = pd.read_csv(file_path)
        stop_list.columns = stop_list.columns.str.strip()  # Clean column names
        if 'Name' not in stop_list.columns:
            print(f"Error: The stop list CSV file does not contain expected column ('Name').")
            return []
        stop_list_names = stop_list['Name'].str.strip().tolist()  # Get list of out-of-stock item names
        return stop_list_names
    except FileNotFoundError:
        print(f"Error: The stop list file could not be found at {file_path}. Please check the file path.")
        return []  # Return empty list in case of error
    except Exception as e:
        print(f"Unexpected error loading stop list: {e}")
        return []

def save_to_csv(data, file_path):
    """ 
    Save the data to a CSV file.
    
    Args:
        data (pd.DataFrame): Data to be saved to CSV.
        file_path (str): Path to the CSV file.
    """
    data.to_csv(file_path, index=False)

def save_order_to_csv(order_data, file_path):
    """
    Save the order data to a CSV file. If the file already exists, it appends the data.
    
    Args:
        order_data (dict): Order details (e.g., item name, size, price, etc.)
        file_path (str): Path to the CSV file.
    """
    # Convert order_data to DataFrame
    order_df = pd.DataFrame([order_data])
    
    # Check if file exists to decide whether to append or create new file
    if os.path.exists(file_path):
        order_df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        order_df.to_csv(file_path, mode='w', header=True, index=False)
