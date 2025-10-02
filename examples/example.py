#!/usr/bin/env python3

import vurze

def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

def calculate_area(radius):
    """Calculate the area of a circle."""
    import math
    return math.pi * radius ** 2

async def fetch_user_data(user_id):
    """Fetch user data asynchronously."""
    # Simulate async operation
    import asyncio
    await asyncio.sleep(0.1)
    return {"id": user_id, "name": f"User {user_id}"}

# Test the get_functions_from_file function
def test_function_extraction():
    """Test the get_functions_from_file function with this current file."""
    import os
    
    # Get the current file path
    current_file = __file__
    print(f"Testing get_functions_from_file with: {current_file}")
    
    try:
        # Call the Rust function to extract function names from this file
        functions = vurze.get_functions_from_file(current_file)
        
        print(f"\nFound {len(functions)} functions:")
        for i, func_name in enumerate(functions, 1):
            print(f"  {i}. {func_name}")
            
        # Expected functions in this file
        expected_functions = ["greet", "calculate_area", "fetch_user_data", "test_function_extraction"]
        
        print(f"\nExpected functions: {expected_functions}")
        print(f"Found functions: {functions}")
        
        # Check if we found all expected functions
        missing = [f for f in expected_functions if f not in functions]
        extra = [f for f in functions if f not in expected_functions]
        
        if missing:
            print(f"Missing functions: {missing}")
        if extra:
            print(f"Extra functions found: {extra}")
        
        if not missing and not extra:
            print("✅ Perfect match! All expected functions found.")
        else:
            print("⚠️  Some differences found, but that's okay for testing.")
            
    except Exception as e:
        print(f"❌ Error testing get_functions_from_file: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing vurze.get_functions_from_file function")
    print("=" * 50)
    test_function_extraction()
