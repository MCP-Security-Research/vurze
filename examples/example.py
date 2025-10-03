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

# Test the add_decorators_to_functions function
def test_decorator_addition():
    """Test the add_decorators_to_functions function with this current file."""
    import os
    
    # Get the current file path
    current_file = __file__
    print(f"Testing add_decorators_to_functions with: {current_file}")
    print(f"Adding decorator: @my_decorator")
    
    try:
        # Call the Rust function to add decorators to all functions in this file
        modified_code = vurze.add_decorators_to_functions(current_file, "my_decorator")
        
        print("\n" + "="*80)
        print("MODIFIED PYTHON CODE WITH DECORATORS:")
        print("="*80)
        print(modified_code)
        print("="*80)
        
        # Count how many @my_decorator occurrences we added
        decorator_count = modified_code.count("@my_decorator")
        print(f"\n✅ Successfully added {decorator_count} '@my_decorator' decorators!")
        
        # Show which functions should have received decorators
        expected_functions = ["greet", "calculate_area", "fetch_user_data", "test_decorator_addition"]
        print(f"Expected to decorate functions: {expected_functions}")
            
    except Exception as e:
        print(f"❌ Error testing add_decorators_to_functions: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing vurze.add_decorators_to_functions function")
    print("=" * 50)
    test_decorator_addition()
