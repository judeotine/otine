import os
import random
import sys
import subprocess
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
print("\n⚠️  NOTE: GitHub's contribution graph may not show all backdated commits.")
print("   Commits must be:")
print("   - Pushed to the default branch (main/master)")
print("   - Made with an email matching your GitHub account")
print("   - Not too far in the past relative to when they were pushed")
print("=" * 60)

# Create a file for dummy commits
file_path = 'test.txt'
with open(file_path, 'a') as file:
    file.write('Initial commit\n')

# Check if we're in a git repository
status_result = subprocess.run(['git', 'status'], capture_output=True, text=True)
if status_result.returncode != 0:
    print("Error: Not in a git repository. Please run 'git init' first.")
    exit(1)

# Add and commit initial file
add_result = subprocess.run(['git', 'add', file_path], capture_output=True, text=True)
if add_result.returncode != 0:
    print(f"Error adding initial file: {add_result.stderr}")
    exit(1)

commit_result = subprocess.run(['git', 'commit', '-m', 'Initial commit'], capture_output=True, text=True)
if commit_result.returncode != 0:
    print(f"Error creating initial commit: {commit_result.stderr}")
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
    
    # Construct the commit date string in RFC2822 format (more reliable for git)
    # Format: "Mon, 1 Jan 2024 12:00:00 +0300"
    commit_datetime = datetime.combine(commit_date, datetime.min.time().replace(hour=random_hour, minute=random_minute))
    weekday = commit_datetime.strftime('%a')
    month_abbr = commit_datetime.strftime('%b')
    day = commit_datetime.day  # Remove leading zero
    commit_date_str = f"{weekday}, {day} {month_abbr} {commit_datetime.year} {commit_datetime.strftime('%H:%M:%S')} +0300"
    
    # Also create ISO format for environment variable (alternative method)
    iso_date_str = commit_datetime.strftime('%Y-%m-%dT%H:%M:%S+03:00')

    print(f"Creating commit {i+1}/{NUM_COMMITS} for {commit_date}...")

    # Write to file to create a change
    with open(file_path, 'a') as file:
        file.write(f'Commit for {iso_date_str}\n')
    
    # Add and commit changes with the specified date
    # Use environment variables for more reliable date setting on Windows
    # Explicitly set author and committer info to match GitHub account
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = commit_date_str
    env['GIT_COMMITTER_DATE'] = commit_date_str
    # Get current git config to ensure email matches GitHub account
    git_email = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True).stdout.strip()
    git_name = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True).stdout.strip()
    env['GIT_AUTHOR_NAME'] = git_name
    env['GIT_AUTHOR_EMAIL'] = git_email
    env['GIT_COMMITTER_NAME'] = git_name
    env['GIT_COMMITTER_EMAIL'] = git_email
    
    add_result = subprocess.run(['git', 'add', file_path], capture_output=True, text=True)
    if add_result.returncode != 0:
        print(f"Error adding file for commit {i+1}: {add_result.stderr}")
        continue
    
    commit_result = subprocess.run(
        ['git', 'commit', '-m', f'Commit #{i+1}'],
        env=env,
        capture_output=True,
        text=True
    )
    if commit_result.returncode != 0:
        print(f"Error during commit {i+1}: {commit_result.stderr}")
    else:
        print(f"✓ Created commit {i+1} for {commit_date}")

# Push commits to the remote repository
push_result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
if push_result.returncode != 0:
    print(f"Error pushing to repository: {push_result.stderr}")


#git commit --amend --no-edit --date="Fri Nov 6 20:00:00 2015 -0600" 
#git fetch origin master
#git rebase origin/master
