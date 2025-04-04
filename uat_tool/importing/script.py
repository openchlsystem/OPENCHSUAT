#!/usr/bin/env python3
import requests
import json
import sys
import time

def print_debug(message):
    """Print debug message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_functionality(base_url, auth_token, functionality_data):
    """Create a functionality and return its ID"""
    url = f"{base_url}/functionalities/"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    print_debug(f"Creating functionality: {functionality_data['name']}")
    response = requests.post(url, json=functionality_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print_debug(f"Successfully created functionality: {response.json()}")
        return response.json()["id"]
    else:
        print_debug(f"Failed to create functionality. Status code: {response.status_code}")
        print_debug(f"Response: {response.text}")
        return None

def create_test_case(base_url, auth_token, test_case_data):
    """Create a test case and return its ID"""
    url = f"{base_url}/test-cases/"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    print_debug(f"Creating test case: {test_case_data['title']}")
    response = requests.post(url, json=test_case_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print_debug(f"Successfully created test case: {response.json()}")
        return response.json()["id"]
    else:
        print_debug(f"Failed to create test case. Status code: {response.status_code}")
        print_debug(f"Response: {response.text}")
        return None

def create_test_step(base_url, auth_token, test_step_data):
    """Create a test step"""
    url = f"{base_url}/test-steps/"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"  # Added content type
    }
    
    print_debug(f"Creating test step {test_step_data['step_number']} for test case ID {test_step_data['test_case']}")
    response = requests.post(url, json=test_step_data, headers=headers)  # Changed data to json
    
    if response.status_code in [200, 201]:
        print_debug(f"Successfully created test step: {response.json()}")
        return response.json()["id"]
    else:
        print_debug(f"Failed to create test step. Status code: {response.status_code}")
        print_debug(f"Response: {response.text}")
        return None

def process_json_file(file_path, base_url, auth_token, system_id):
    """Process a JSON file containing test data"""
    try:
        print_debug(f"Reading test data from {file_path}")
        with open(file_path, 'r') as file:
            test_data = json.load(file)
            
        # Create functionality
        functionality_data = {
            "id": None,
            "name": test_data.get("functionality", "Unnamed Functionality"),
            "description": test_data.get("functionality", "No description provided"),
            "system": system_id
        }
        
        functionality_id = create_functionality(base_url, auth_token, functionality_data)
        if not functionality_id:
            print_debug("Failed to create functionality. Exiting.")
            return False
            
        # Create test cases and their steps
        for test_case in test_data.get("testCases", []):
            # Create test case
            test_case_data = {
                "title": test_case.get("title", "Unnamed Test Case"),
                "functionality_id": functionality_id,
                "description": test_case.get("description", "No description provided"),
                "expected_result": "See individual test steps"
            }
            
            test_case_id = create_test_case(base_url, auth_token, test_case_data)
            if not test_case_id:
                print_debug(f"Failed to create test case {test_case_data['title']}. Skipping its steps.")
                continue
                
            # Create test steps
            for step in test_case.get("steps", []):
                test_step_data = {
                    "step_number": step.get("stepNumber", 1),
                    "description": step.get("stepDescription", "No description provided"),
                    "expected_result": step.get("expectedResult", "No expected result provided"),
                    "test_case": test_case_id
                }
                
                step_id = create_test_step(base_url, auth_token, test_step_data)
                if not step_id:
                    print_debug(f"Failed to create test step {test_step_data['step_number']} for test case {test_case_id}.")
                
            # Add a small delay to avoid overloading the server
            time.sleep(0.5)
                
        print_debug("Successfully processed the JSON file.")
        return True
            
    except FileNotFoundError:
        print_debug(f"Error: File {file_path} not found.")
        return False
    except json.JSONDecodeError:
        print_debug(f"Error: File {file_path} is not a valid JSON file.")
        return False
    except Exception as e:
        print_debug(f"Error: An unexpected error occurred: {str(e)}")
        return False

def main():
    """Main function to run the script"""
    if len(sys.argv) < 5:
        print("Usage: python script.py <base_url> <auth_token> <system_id> <json_file> [json_file2 ...]")
        print("Example: python script.py http://127.0.0.1:8000 your_auth_token 1 test_data.json")
        return
        
    base_url = sys.argv[1].rstrip('/')
    auth_token = sys.argv[2]
    system_id = int(sys.argv[3])
    json_files = sys.argv[4:]
    
    print_debug(f"Starting test setup script")
    print_debug(f"Base URL: {base_url}")
    print_debug(f"System ID: {system_id}")
    print_debug(f"Number of JSON files to process: {len(json_files)}")
    
    success_count = 0
    for file_path in json_files:
        print_debug(f"Processing file: {file_path}")
        if process_json_file(file_path, base_url, auth_token, system_id):
            success_count += 1
            
    print_debug(f"Completed processing {success_count} out of {len(json_files)} files successfully.")

if __name__ == "__main__":
    main()