import numpy as np

# Set the random seed for reproducibility
np.random.seed(6401)

# Number of samples
num_samples = 1000

# Create a normally distributed random variable x
# Mean = 0, Variance = 1 (so, standard deviation = 1)
mean_x = 0
std_dev_x = np.sqrt(1)
x = np.random.normal(loc=mean_x, scale=std_dev_x, size=num_samples)

# Create a normally distributed random variable y
# Mean = 5, Variance = 2 (so, standard deviation = sqrt(2))
mean_y = 5
std_dev_y = np.sqrt(2)
y = np.random.normal(loc=mean_y, scale=std_dev_y, size=num_samples)

# Display the first 5 observations of x and y
print("First 5 observations of x:")
print(x[:5])
print("\nFirst 5 observations of y:")
print(y[:5])
