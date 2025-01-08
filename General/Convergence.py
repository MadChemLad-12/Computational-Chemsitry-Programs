import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import sys


# Function to dynamically parse each line and extract column names and values
def parse_lines(lines):
    # Use regular expressions to find and extract key-value pairs
    pattern = re.compile(r"(\S+)=\s*([-.\dE+]+)") #Here it looks for characters like "E" "+" "=" in a specific order
    
    # List to store dictionaries of parsed data
    data = []

    for line in lines:  # Going through each line the E.txt
        try: 
            # Extract the index
            line_parts = line.split()   #Split each line
            index = int(line_parts[0])  #Index is always first on the E.txt file
            
        except (ValueError, IndexError) as e: ### Error catching
            print(f"Error parsing index from line: '{line.strip()}'. Error: {e}")
            continue    
        
        # Find all key-value pairs in the line
        matches = pattern.findall(line)  # Using the specific characters to find values for each column
        if matches:
            entry = {'Index': index}
            for key, value in matches:
                try:
                    entry[key] = float(value)
                except ValueError as e:
                    print(f"Error converting value '{value}' for key '{key}' in line: '{line.strip()}'. Error: {e}")
            data.append(entry)
    
    return data

# Read the data from the file
try:
    with open("E.txt", "r") as file:
        lines = file.readlines()
except FileNotFoundError as e:
    print(f"Error: The file 'E.txt' was not found. Please check the file path. Error: {e}")
    quit()
except IOError as e:
    print(f"Error reading the file 'E.txt'. Error: {e}")
    quit()    

# Parse the lines to extract the data
data = parse_lines(lines)

#Check if any data is present
if not data:
    print("No valid data was parsed from the file. Exiting.")
    quit()
    
# Create a pandas DataFrame from the parsed data
try:
    df = pd.DataFrame(data)
except ValueError as e:
    print(f"Error creating DataFrame from parsed data. Error: {e}")
    quit()

# Display the DataFrame
#print(df)

# Optionally, save the cleaned data to a new CSV file
#df.to_csv("cleaned_E.csv", index=False)

x_axis = 'Index'
y_axis = 'E0'

### Plotting data 
###Define function for plotting figure
#Things needed, size, color, convergence checker
def conv_plot(size, col):
    #create plot
    plt.figure(figsize =( 1.5*size, size))
    plt.plot(df[x_axis], df[y_axis], marker='o', linestyle='-', color=col)
    #Add title and lables
    plt.title(f'Plot of {y_axis} vs {x_axis}')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    # Show grid
    plt.grid(True)

conv_plot(10, 'red')
# Display the plot
#plt.show()   

# Get the output directory from the command line arguments
output_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

# Save the plot in the specified directory
output_path = os.path.join(output_dir, 'energy_plot.jpg')
plt.savefig(output_path, format='jpg')
plt.close()

print(f"Plot saved to {output_path}")

quit()
