# Day 2 — Loops and JSON
# JSON is the standard format used by all AI APIs to send and receive data
# If you can read and write JSON, you can talk to any AI API

import json  # built-in Python library, no installation needed

# --- PART 1: For loops ---
# Iterate over a list, same concept as Java's for-each

trails = ["Nahuelbuta", "Huerquehue", "Conguillio", "Torres del Paine"]

print("--- All trails ---")
for trail in trails:
    print("-", trail)

# Loop with index (when you need the position too)
print("\n--- Trails with index ---")
for i, trail in enumerate(trails):
    print(f"{i + 1}. {trail}")  # f-string: cleaner way to build strings


# --- PART 2: List of dictionaries ---
# This is exactly how an AI API returns a list of results

trail_list = [
    {"name": "Nahuelbuta",     "distance_km": 12, "difficulty": "medium"},
    {"name": "Huerquehue",     "distance_km": 8,  "difficulty": "easy"},
    {"name": "Conguillio",     "distance_km": 15, "difficulty": "hard"},
]

print("\n--- Trail details ---")
for trail in trail_list:
    print(f"{trail['name']} — {trail['distance_km']} km — {trail['difficulty']}")


# --- PART 3: Filter with conditions ---
# Show only easy or medium trails (useful for a search feature)

print("\n--- Trails for beginners (easy or medium) ---")
for trail in trail_list:
    if trail["difficulty"] != "hard":
        print(f"  {trail['name']} ({trail['difficulty']})")


# --- PART 4: Read and write JSON ---
# This is exactly what happens when an AI API responds to your request

# Convert Python dictionary to JSON string (what you SEND to an API)
request_data = {
    "user": "Damian",
    "query": "trails near Nahuelbuta",
    "max_results": 3
}
json_string = json.dumps(request_data, indent=2)
print("\n--- JSON you would SEND to an AI API ---")
print(json_string)

# Convert JSON string back to Python dictionary (what you RECEIVE from an API)
api_response = '{"trail": "Nahuelbuta", "distance_km": 12, "rating": 4.8}'
parsed = json.loads(api_response)
print("\n--- JSON you would RECEIVE from an AI API ---")
print(f"Trail: {parsed['trail']}, Rating: {parsed['rating']}")
