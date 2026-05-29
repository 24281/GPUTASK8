import sqlite3
import os  # Provides tools to interact with the operating system's file paths

DATABASE_NAME = 'GPUTASK8.db'
SEPARATOR_WIDTH = 40
MENU_EXIT = "5"

def get_db_connection():
    # Dynamically locate the database file relative to this script's folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return sqlite3.connect(os.path.join(script_dir, DATABASE_NAME))

def show_all_gpus():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Explicit column selection ensures code stability if the table structure changes
    cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus")
    rows = cursor.fetchall()
    
    print(f"\n{'--- ALL AVAILABLE GRAPHICS CARDS ---':^{SEPARATOR_WIDTH}}")
    for row in rows:
        print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
    print("-" * SEPARATOR_WIDTH)
    
    conn.close()

def search_by_manufacturer():
    # .strip() prevents errors caused by accidental whitespace in user input
    brand_input = input("\nEnter manufacturer name (NVIDIA, AMD, or Intel): ").strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use '?' parameterization to prevent SQL injection and handle user data safely
    cursor.execute("""
        SELECT gpu_id, model_name, manufacturer, price, clock_speed
        FROM gpus
        WHERE manufacturer LIKE ?
    """, (brand_input,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        print(f"\n--- MATCHING {brand_input.upper()} GRAPHICS CARDS ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
        print("-" * SEPARATOR_WIDTH)
    else:
        print(f"\n❌ No graphics cards found matching: '{brand_input}'")

def search_by_budget():
    print("\n--- BUDGET SEARCH ---")
    budget_input = input("Enter your maximum budget (NZD): $").strip()
    
    # Error handling ensures the program gracefully catches non-numeric inputs
    try:
        max_price = float(budget_input)
    except ValueError:
        print("\n❌ Invalid input! Please enter a real number.")
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT gpu_id, model_name, manufacturer, price, clock_speed
        FROM gpus
        WHERE price <= ?
        ORDER BY price DESC
    """, (max_price,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        print(f"\n--- BEST CARDS UNDER ${max_price:.2f} NZD ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | ${row[3]:.2f} NZD | {row[4]}MHz")
        print("-" * SEPARATOR_WIDTH)
    else:
        print(f"\n❌ No cards found under ${max_price:.2f} NZD.")

def sort_by_clock_speed():
    print("\n--- FASTEST TO SLOWEST ---")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT gpu_id, model_name, manufacturer, price, clock_speed FROM gpus ORDER BY clock_speed DESC")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | {row[2]} {row[1]} | {row[4]}MHz | ${row[3]:.2f} NZD")
        print("-" * SEPARATOR_WIDTH)
    else:
        print("❌ No data found.")

def main():
    # Program loop keeps the UI active until the user chooses to exit
    while True:
        print("\n=== GPU DATABASE MANAGEMENT SYSTEM ===")
        print("1. View All Graphics Cards")
        print("2. Search by Manufacturer")
        print("3. Search by Budget")
        print("4. Sort by Clock Speed")
        print(f"{MENU_EXIT}. Exit Program")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        # Route user input to the relevant function
        if choice == "1":
            show_all_gpus()
        elif choice == "2":
            search_by_manufacturer()
        elif choice == "3":
            search_by_budget()
        elif choice == "4":
            sort_by_clock_speed()
        elif choice == MENU_EXIT:
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()