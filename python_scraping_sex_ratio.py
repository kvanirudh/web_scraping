"""
WEB SCRAPING SCRIPT

Extract Population Data for Andhra Pradesh & Telangana
"""

# STEP 1: Import the tools we need
import requests  # Download web pages
from bs4 import BeautifulSoup  # Read HTML
import pandas as pd  # Organize data

print("=" * 60)
print("POPULATION DATA SCRAPER")
print("=" * 60)

# ============================================================================
# STEP 2: Download the webpage
# ============================================================================
print("\n  DOWNLOADING WEBPAGE...")

url = "https://en.wikipedia.org/wiki/List_of_Indian_states_and_union_territories_by_population"

# Pretend to be a browser
headers = {'User-Agent': 'Mozilla/5.0'}

# Download the page
response = requests.get(url, headers=headers)
print("✓ Downloaded successfully!")

# ============================================================================
# STEP 3: Parse the HTML (convert to readable format)
# ============================================================================
print("\n  PARSING HTML...")

soup = BeautifulSoup(response.content, 'html.parser')
print("✓ HTML parsed!")

# ============================================================================
# STEP 4: Find the table
# ============================================================================
print("\n  FINDING THE DATA TABLE...")

# Find all tables
tables = soup.find_all('table', {'class': 'wikitable'})
print(f"✓ Found {len(tables)} table(s)")

# Use the first table
table = tables[0]
print("✓ Using first table")

# ============================================================================
# STEP 5: Extract headers
# ============================================================================
print("\n  EXTRACTING HEADERS...")

headers = []
for th in table.find_all('th'):
    header = th.text.strip()
    headers.append(header)
    
print(f"✓ Found {len(headers)} columns:")
for i, h in enumerate(headers, 1):
    print(f"   {i}. {h}")

# ============================================================================
# STEP 6: Extract all rows
# ============================================================================
print("\n  EXTRACTING DATA ROWS...")

all_rows = []
for tr in table.find_all('tr')[1:]:  # Skip header row
    cols = tr.find_all('td')
    if len(cols) > 0:
        row = [col.text.strip() for col in cols]
        all_rows.append(row)

print(f"✓ Extracted {len(all_rows)} rows")

# ============================================================================
# STEP 7: Find our target states
# ============================================================================
print("\n SEARCHING FOR TARGET STATES...")

our_states = ['Andhra Pradesh', 'Telangana']
matching_rows = []

for row in all_rows:
    state_name = row[0]  # First column is state name
    
    # Check if this row is one of our target states
    for target in our_states:
        if target.lower() in state_name.lower():
            matching_rows.append(row)
            print(f"✓ Found: {state_name}")

if len(matching_rows) == 0:
    print(" No states found!")
else:
    print(f"✓ Total found: {len(matching_rows)}")

# ============================================================================
# STEP 8: Convert to table and save
# ============================================================================
print("\n SAVING DATA...")

# Create a nice table (DataFrame)
df = pd.DataFrame(matching_rows, columns=headers[:len(matching_rows[0])])

# Display the table
print("\n" + "=" * 60)
print("RESULTS:")
print("=" * 60)
print(df.to_string(index=False))
print("=" * 60)

# Save to CSV file
df.to_csv('AP_Telangana_Population.csv', index=False)
print("\n File saved: AP_Telangana_Population.csv")

print("\n DONE!")
