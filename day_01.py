# Day 1 — Variables, lists and dictionaries
# These are the same structures you'll use later to handle JSON responses from AI APIs

# Simple variable
name = "Damian"
print("Hello,", name)

# List — same concept as an array in Java
trails = ["Nahuelbuta", "Huerquehue", "Torres del Paine"]
print("Available trails:", trails)
print("First trail:", trails[0])

# Dictionary — key/value pairs, exactly like the JSON that AI APIs return
trail = {
    "name": "Nahuelbuta",
    "distance_km": 12,
    "difficulty": "medium"
}
print("Name:", trail["name"])
print("Distance:", trail["distance_km"], "km")
