import random

adjectives = [
    "Old", "Young", "Fast", "Slow", "Bright",
    "Dark", "Small", "Big", "Tall", "Short",
    "Smart", "Dumb", "Weak", "Strong", "Soft",
    "Hard", "Cold", "Warm", "Light", "Heavy",
    "Clean", "Dirty", "High", "Low", "Green",
    "Dry", "Wet", "Quick", "Dead", "Sharp"
]

activities = [
    "Running", "Jumping", "Swimming", "Singing", "Hiking",
    "Drawing", "Skiing", "Cooking", "Painting", "Dancing",
    "Golfing", "Reading", "Climbing", "Baking", "Fishing",
    "Sailing", "Typing", "Riding", "Coding", "Kiting",
    "Knitting", "Chatting", "Grilling", "Skating", "Surfing",
    "Flying", "Acting", "Bowling", "Camping", "Driving"
]

animals = [
    "Cat", "Dog", "Bat", "Rat", "Cow",
    "Pig", "Bee", "Ant", "Fish", "Duck",
    "Bear", "Wolf", "Lion", "Frog", "Bird",
    "Crab", "Fox", "Goat", "Moth", "Snail",
    "Mule", "Elk", "Gull", "Hare", "Toad",
    "Seal", "Shark", "Squid", "Swan", "Wasp"
]


def generate_id():
    return f"{random.choice(adjectives)}{random.choice(activities)}{random.choice(animals)}"


if __name__ == '__main__':
    [print(generate_id()) for _ in range(10)]
