import os

stories = {}

# Define the form fields
fields = ["text", "options"]

# Check if the stories file already exists

# If the file doesn't exist, create an empty dictionary
stories = {}

# Loop through the number of stories to create
while True:
    story_num = input("Enter the story number (or q to quit): ")
    if story_num.lower() == "q":
        break
    try:
        i = int(story_num)
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")
        continue
    print(f"Story {i}: ")
    story = {}
    for field in fields:
        if field == "options":
            options = []
            while True:
                num_options = input(
                    "Number of options (or go for Game Over): ")
                if num_options.isdigit() and 1 <= int(num_options) <= 10:
                    num_options = int(num_options)
                    break
                elif num_options.lower() == "go":
                    options = [{"text": "Game Over", "goto": "game_over"}]
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 10.")
                    continue
            if num_options != "go":
                for j in range(num_options):
                    option = {}
                    option["text"] = input(f"Option {j+1} text: ")
                    option["goto"] = input(f"Option {j+1} goto: ")
                    options.append(option)
            story[field] = options
        else:
            story[field] = input(f"{field.capitalize()}: ")
    stories[str(i)] = story

    # Write the stories to the stories.py file
    with open(os.path.join(os.path.dirname(__file__), "stories.py"), "r", encoding="utf-8") as f:
        exec(f.read(), globals())
    with open(os.path.join(os.path.dirname(__file__), "stories.py"), "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("stories.update(" + str({str(i): story}) + ")")
