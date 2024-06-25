import tkinter as tk
import math
import random
from acc import edgeDetection

readings = [
    [0.0, 'inf'], [0.1, 'inf'], [0.2, 'inf'], [0.3, 'inf'], [0.4, 'inf'],
    [0.5, 'inf'], [0.6, 'inf'], [0.7, 'inf'], [0.8, 'inf'], [0.9, 'inf'], [1.0, 'inf'],
    [1.1, 'inf'], [1.2, 'inf'], [1.3, 'inf'], [1.4, 'inf'], [1.5, 'inf'], [1.6, 'inf'],
    [1.7, 'inf'], [1.8, 'inf'], [1.9, 'inf'], [2.0, 'inf'], [2.1, '30'], [2.2, '35'],
    [2.3, '33'], [2.4, '30'], [2.5, '35'], [2.6, '32'], [2.7, '30'], [2.8, '34'], [2.9, '35'],
    [3.0, '17'], [3.1, '15'], [3.2, 'inf'], [3.3, 'inf'], [3.4, 'inf'], [3.5, 'inf'],
    [3.6, 'inf'], [3.7, 'inf'], [3.8, 'inf'], [3.9, 'inf'], [4.0, 'inf'], [4.1, 'inf'], [4.2, 'inf'],
    [4.3, 'inf'], [4.4, 'inf'], [4.5, 'inf'], [4.6, 'inf'], [4.7, 'inf'], [4.8, 'inf'], [4.9, 'inf'],
    [5.0, 'inf'], [5.1, 'inf'], [5.2, 'inf'], [5.3, 'inf'], [5.4, 'inf'], [5.5, 'inf'], [5.6, 'inf'], [5.7, 'inf'],
    [5.8, 'inf'], [5.9, 'inf'], [6.0, 'inf'], [6.1, 'inf'], [6.2, 'inf'], [6.3, 'inf'], [6.4, 'inf'],
    [6.5, 'inf'], [6.6, 'inf'], [6.7, 'inf'], [6.8, 'inf'], [6.9, 'inf'], [7.0, 'inf'], [7.1, 'inf'],
    [7.2, 'inf'], [7.3, 'inf'], [7.4, 'inf'], [7.5, 'inf'], [7.6, 'inf'], [7.7, 'inf'], [7.8, 'inf'], [7.9, 'inf']
]


def plot_radar_data(canvas, all_data, subset_data):
    # Clear previous plot
    canvas.delete("all")

    # Define center and scale
    center_x, center_y = 250, 250
    scale = 5

    # Plot the radar data as points
    for angle, length in all_data:
        x = center_x + length * scale * math.cos(math.radians(angle*10))
        y = center_y - length * scale * math.sin(math.radians(angle*10))
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='black')

    for angle, length in subset_data:
        x = center_x + length * scale * math.cos(math.radians(angle*10))
        y = center_y - length * scale * math.sin(math.radians(angle*10))
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='red')

    # Add labels
    canvas.create_text(20, 20, anchor='nw', text='All Data', fill='black')
    canvas.create_text(20, 40, anchor='nw', text='Subset Data', fill='red')

def update_plot():
    global all_data
    global subset_data

    plot_radar_data(canvas, all_data, subset_data)

    ranNum = random.randint(0, len(all_data) - 1)
    all_data[ranNum][1] += 1
    print(ranNum)

    # Schedule the next update
    root.after(100, update_plot)  # Update every 100 milliseconds

# Define your radar data lists
subset_data = []
edgeDetection(readings,subset_data)
all_data = readings

# Create the main window
root = tk.Tk()
root.title("Radar Plot")

# Create a canvas for plotting
canvas = tk.Canvas(root, width=500, height=500, bg='white')
canvas.pack()

# Plot the initial radar data
plot_radar_data(canvas, all_data, subset_data)

# Start updating the plot
update_plot()

# Start the Tkinter event loop
root.mainloop()
