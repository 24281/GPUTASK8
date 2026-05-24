import sqlite3
import os

def test_database_connection():
    # Automatically finds the folder your main.py file is sitting in (H:\GPUTASK8)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Target the correct file name seen in your sidebar
    database_name = 'GPUTASK8.db' 
    database_path = os.path.join(script_dir, database_name)
    
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        
        print(" Successfully connected to the GPU database!")
        print("-" * 50)
        
        # Pull your data
        cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus")
        all_gpus = cursor.fetchall()
        
        for gpu in all_gpus:
            gpu_id, model_name, brand, price, speed = gpu
            print(f"ID: {gpu_id} | {brand} {model_name} | ${price:.2f} NZD | {speed}MHz")
            
        print("-" * 50)
        print("Connection test complete. Everything works!")
        connection.close()
        
    except sqlite3.Error as error:
        print(f"❌ Database error occurred: {error}")

# test_database_connection()

def get_db_connection():
    """Helper function to cleanly connect to your database file"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, 'GPUTASK8.db')
    return sqlite3.connect(database_path)

def show_all_gpus():
    """Feature 1: Displays everything in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus")
    rows = cursor.fetchall()
    
    print("\n--- ALL AVAILABLE GRAPHICS CARDS ---")
    for row in rows:
        print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
    print("-" * 36)
    
    conn.close()

def search_by_manufacturer():
    """Feature 2: Filters GPUs by brand name with case-insensitive protection"""
    brand_input = input("\nEnter manufacturer name (NVIDIA, AMD, or Intel): ").strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Using the SQL 'LIKE' operator makes the search case-insensitive
    cursor.execute("""
        SELECT gpu_id, model_name, manufacturer, price, clock_speed 
        FROM gpus 
        WHERE manufacturer LIKE ?
    """, (brand_input,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # If the database found matches, print them out
    if rows:
        print(f"\n--- MATCHING {brand_input.upper()} GRAPHICS CARDS ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
        print("-" * 40)
    else:
        print(f"\n❌ No graphics cards found matching manufacturer: '{brand_input}'")

def main():
    """Main Program Menu Loop"""
    while True:
        print("\n=== GPU DATABASE MANAGEMENT SYSTEM ===")
        print("1. View All Graphics Cards")
        print("2. Search by Manufacturer (NVIDIA/AMD/Intel)")
        print("3. Search by Budget (Max Price)")
        print("4. Sort by Clock Speed")
        print("5. Exit Program")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            show_all_gpus()
        elif choice == "2":
            search_by_manufacturer()
        elif choice == "3":
            print("\n[System]: Budget filter function coming next!")
        elif choice == "4":
            print("\n[System]: Sorting function coming next!")
        elif choice == "5":
            print("\nThank you for using the GPU Database App. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 5.")

# This line starts the menu loop when you run python main.py
if __name__ == "__main__":
    main()