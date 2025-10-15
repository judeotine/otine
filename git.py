import os
import random
import sys
from datetime import datetime, date, timedelta


print("=" * 60)

def parse_date(date_str):
    """Parse date from MM/DD/YYYY format"""
    try:
        month, day, year = map(int, date_str.split('/'))
        return date(year, month, day)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Please use MM/DD/YYYY format (e.g., 08/24/2025)")
        exit(1)

# Check if command-line arguments are provided
if len(sys.argv) == 4:
    # Command-line mode: python git.py <num_commits> <start_date> <end_date>
    try:
        NUM_COMMITS = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number of commits.")
        exit(1)
    
    start_date = parse_date(sys.argv[2])
    end_date = parse_date(sys.argv[3])
else:
    # Interactive mode
    try:
        NUM_COMMITS = int(input("\nEnter the number of commits to create: "))
    except ValueError:
        print("Please enter a valid integer for the number of commits.")
        exit(1)
    
    def get_date_input(prompt):
        """Get and validate date input from user"""
        while True:
            try:
                date_str = input(prompt)
                return parse_date(date_str)
            except SystemExit:
                continue
    
    print("\nEnter the date range for commits:")
    start_date = get_date_input("Start date (MM/DD/YYYY): ")
    end_date = get_date_input("End date (MM/DD/YYYY): ")

# Validate date range
current_date = date.today()
if start_date > end_date:
    print("Error: Start date must be before or equal to end date.")
    exit(1)
if end_date > current_date:
    print(f"Error: End date cannot be in the future. Today is {current_date}.")
    exit(1)

print(f"\nCreating {NUM_COMMITS} commits between {start_date} and {end_date}...")
print("=" * 60)

# Create a file for dummy commits
file_path = 'test.txt'
with open(file_path, 'a') as file:
    file.write('Initial commit\n')

# Check if we're in a git repository
if os.system('git status') != 0:
    print("Error: Not in a git repository. Please run 'git init' first.")
    exit(1)

# Add and commit initial file
add_result = os.system('git add test.txt')
if add_result != 0:
    print("Error adding initial file")
    exit(1)

commit_result = os.system('git commit -m "Initial commit"')
if commit_result != 0:
    print("Error creating initial commit")
    exit(1)

print("Initial commit created successfully")

for i in range(NUM_COMMITS):
    # Generate random date within the specified range
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    commit_date = start_date + timedelta(days=random_days)
    
    # Add random time (hour and minute)
    random_hour = random.randint(9, 20)
    random_minute = random.randint(0, 59)
    
    # Construct the commit date string
    commit_date_str = f"{commit_date.year}-{commit_date.month:02d}-{commit_date.day:02d} {random_hour:02d}:{random_minute:02d}:00"

    print(f"Creating commit {i+1}/{NUM_COMMITS} for {commit_date}...")

    # Write to file to create a change
    with open(file_path, 'a') as file:
        file.write(f'Commit for {commit_date_str}\n')
    
    # Add and commit changes with the specified date
    add_result = os.system('git add test.txt')
    if add_result != 0:
        print(f"Error adding file for commit {i+1}")
        continue
    
    commit_result = os.system(f'git commit --date="{commit_date_str}" -m "Commit #{i+1}"')
    if commit_result != 0:
        print(f"Error during commit {i+1}")
    else:
        print(f"✓ Created commit {i+1} for {commit_date}")

# Push commits to the remote repository
push_result = os.system('git push -u origin main')
if push_result != 0:
    print("Error pushing to repository")


#git commit --amend --no-edit --date="Fri Nov 6 20:00:00 2015 -0600" 
#git fetch origin master
#git rebase origin/master
