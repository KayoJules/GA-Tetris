# Read mode
with open("output.txt", "r") as file:

    for generation in range(20):

        averages = []
        scores = []

        for population in range(80):

            # Read the first 5 lines
            for round in range(5):
                score = float(file.readline().strip())
                scores.append(score)
            
            # Read the next line and store it in the list
            value = float(file.readline().strip())
            averages.append(value)

        
        high_score = max(scores) if scores else None
        highest_avg = max(averages) if averages else None
        print(f"Generation {generation + 1}: Highest Average = {high_score}")

        # Get the 10 highest values from the list
        top_10_values = sorted(scores, reverse=True)[:10]

        # Output the top 10 values
        print("Top 10 Scores:")
        for i, value in enumerate(top_10_values, start=1):
            print(f"{value}")
        print("")

