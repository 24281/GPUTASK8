import sqlite3 # Import the library needed to talk to SQL databases
import os # Import the library needed to find your file paths

# --- CONFIGURATION (Constants) ---
DATABASE_NAME = 'GPUTASK8.db' # Store the filename in a constant for easy updates
SEPARATOR_WIDTH = 40 # Store the UI width in a constant to avoid 'magic numbers'
MENU_EXIT = "5" # Define the exit choice as a constant

def get_db_connection():
    """Helper function to cleanly connect to your database file"""
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Find the folder where this script lives
    return sqlite3.connect(os.path.join(script_dir, DATABASE_NAME)) # Open the database file using the full path

def show_all_gpus():
    """Feature 1: Displays everything in the database"""
    conn = get_db_connection() # Open a connection to the database
    cursor = conn.cursor() # Create a 'cursor' object to run SQL commands
    
    # Send the SQL query to select all columns from the 'gpus' table
    cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus")
    rows = cursor.fetchall() # Grab all the results from the query
    
    print(f"\n{'--- ALL AVAILABLE GRAPHICS CARDS ---':^{SEPARATOR_WIDTH}}") # Print a centered header
    for row in rows: # Loop through every record retrieved from the database
        # Print the data, accessing individual columns using their index [0, 1, 2, 3, 4]
        print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
    print("-" * SEPARATOR_WIDTH) # Print a separator line using the constant width
    
    conn.close() # Close the database connection to free up resources

def search_by_manufacturer():
    """Feature 2: Filters GPUs by brand name"""
    # Ask the user for input and remove extra whitespace
    brand_input = input("\nEnter manufacturer name (NVIDIA, AMD, or Intel): ").strip()
    
    conn = get_db_connection() # Connect to the database
    cursor = conn.cursor() # Create the cursor
    
    # Execute a parameterized query (using '?' for safety) to find the manufacturer
    cursor.execute("""
        SELECT gpu_id, model_name, manufacturer, price, clock_speed
        FROM gpus
        WHERE manufacturer LIKE ?
    """, (brand_input,)) # Pass the user input as a tuple to the query
    
    rows = cursor.fetchall() # Store the matching results
    conn.close() # Close the connection
    
    if rows: # Check if the list 'rows' contains any data
        print(f"\n--- MATCHING {brand_input.upper()} GRAPHICS CARDS ---") # Inform the user
        for row in rows: # Loop through each match
            print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
        print("-" * SEPARATOR_WIDTH)
    else: # If no data was found
        print(f"\n❌ No graphics cards found matching: '{brand_input}'")

def search_by_budget():
    """Feature 3: Filters GPUs by max price with error handling"""
    print("\n--- BUDGET SEARCH ---")
    budget_input = input("Enter your maximum budget (NZD): $").strip() # Get user input
    
    try: # Start an error-checking block
        max_price = float(budget_input) # Attempt to convert input string to a number
    except ValueError: # Catch an error if the user typed text instead of numbers
        print("\n❌ Invalid input! Please enter a real number.") # Notify the user
        return # Stop the function from running further
        
    conn = get_db_connection() # Connect to the database
    cursor = conn.cursor() # Create the cursor
    
    # Select records where price is less than or equal to user input, ordered by price
    cursor.execute("""
        SELECT gpu_id, model_name, manufacturer, price, clock_speed
        FROM gpus
        WHERE price <= ?
        ORDER BY price DESC
    """, (max_price,)) # Pass the converted float to the query
    
    rows = cursor.fetchall() # Retrieve the filtered records
    conn.close() # Close the connection
    
    if rows: # If matches exist
        print(f"\n--- BEST CARDS UNDER ${max_price:.2f} NZD ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
        print("-" * SEPARATOR_WIDTH)
    else: # If no matches exist
        print(f"\n❌ No cards found under ${max_price:.2f} NZD.")

def sort_by_clock_speed():
    """Feature 4: Sorts all GPUs by clock speed"""
    print("\n--- FASTEST TO SLOWEST ---")
    
    conn = get_db_connection() # Connect to the database
    cursor = conn.cursor() # Create the cursor
    
    # Perform a standard select but use SQL's ORDER BY feature for sorting
    cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus ORDER BY clock_speed DESC")
    rows = cursor.fetchall() # Get all results
    conn.close() # Close the connection
    
    if rows: # If the table isn't empty
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | {row[4]}MHz | ${row[3]:.2f} NZD")
        print("-" * SEPARATOR_WIDTH)
    else: # If the table is empty
        print("❌ No data found.")

def main():
    """Main Program Menu Loop"""
    while True: # Keep the program running indefinitely until the user breaks
        print("\n=== GPU DATABASE MANAGEMENT SYSTEM ===")
        print("1. View All Graphics Cards")
        print("2. Search by Manufacturer")
        print("3. Search by Budget")
        print("4. Sort by Clock Speed")
        print(f"{MENU_EXIT}. Exit Program") # Display the exit option using the constant
        
        choice = input("\nEnter your choice (1-5): ").strip() # Get user menu selection
        
        # Branch the program logic based on user choice
        if choice == "1":
            show_all_gpus()
        elif choice == "2":
            search_by_manufacturer()
        elif choice == "3":
            search_by_budget()
        elif choice == "4":
            sort_by_clock_speed()
        elif choice == MENU_EXIT: # Compare input against the constant
            print("\nGoodbye!")
            break # Stop the while loop, effectively ending the program
        else: # Handle input that is not 1-5
            print("\n❌ Invalid choice!")

# Only run the main function if this file is executed directly (standard practice)
if __name__ == "__main__":
    main()