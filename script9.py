#%%
import numpy as np
import matplotlib.pyplot as plt

mean_x = 0
std_dev_x = 1
mean_y = 5
std_dev_y = np.sqrt(2)

x = np.random.normal(mean_x, std_dev_x, 10000)
y = np.random.normal(mean_y, std_dev_y, 10000)

print(f"observations: {x[:5]}")


#%%
import numpy as np

# Set the random seed for reproducibility
np.random.seed(6401)

# Number of samples
num_samples = 1000

# Create random variables x and y
x = np.random.normal(loc=0, scale=1, size=num_samples)  # Mean = 0, Variance = 1 (std = 1)
y = np.random.normal(loc=5, scale=np.sqrt(2), size=num_samples)  # Mean = 5, Variance = 2 (std = sqrt(2))

# Display the first 5 observations of x and y
print("First 5 observations of x:", x[:5])
print("First 5 observations of y:", y[:5])


#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
URL = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/refs/heads/main/mnist_test.csv"
df = pd.read_csv(URL)

# Display dataset shape
print(f'Dataset shape: {df.shape}')

# Filter out images with labels between 0 and 9
df_filtered = df[df['label'].isin(range(10))]

# Plotting
plt.figure(figsize=(12, 12))

# Loop through the first 100 samples
for i in range(100):  # 10x10 grid for 100 images
    pic = df_filtered.iloc[i, 1:].values.reshape(28, 28)  # Reshape each image
    plt.subplot(10, 10, i + 1)  # 10x10 grid for 100 images
    plt.imshow(pic, cmap='gray')  # Display the image
    plt.axis('off')  # Hide axes for cleaner look

plt.tight_layout()  # Adjust layout
plt.show()

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the MNIST dataset
URL = "https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/refs/heads/main/mnist_test.csv"
df = pd.read_csv(URL)

# Filter out only the digits 0-9
df_filtered = df[df['label'].isin(range(10))]

# Create a figure for plotting
plt.figure(figsize=(12, 12))

# Loop through each digit (0-9) and display 10 images per digit in 10 rows
for i in range(10):
    # Filter data for the current digit (i)
    digit_data = df_filtered[df_filtered['label'] == i]

    # Extract the first 10 observations of the current digit
    for j in range(10):
        # Get the image data (exclude label column)
        pic = digit_data.iloc[j, 1:].values.reshape(28, 28)

        # Create a subplot for each image
        plt.subplot(10, 10, i * 10 + j + 1)
        plt.imshow(pic, cmap='gray')  # Display the image in grayscale
        plt.axis('off')  # Hide the axis

plt.tight_layout()  # Ensure no overlap
plt.show()
