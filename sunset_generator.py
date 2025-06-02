import matplotlib.pyplot as plt
import numpy as np

def generate_sunset_image(width=800, height=600, filename="sunset.png"):
    """
    Generates an image of a sunset with a simple gradient and saves it.
    """
    image = np.zeros((height, width, 3))

    # Define key colors for the sunset gradient (RGB, 0-1 range)
    color_sky = np.array([0.1, 0.1, 0.4])          # Dark blue/purple for the top
    color_horizon_upper = np.array([0.8, 0.3, 0.1]) # Reddish orange
    color_sun_glow_middle = np.array([1.0, 0.6, 0.2]) # Bright orange
    color_sun_glow_lower = np.array([1.0, 0.8, 0.4])  # Yellowish orange for near horizon

    for y in range(height):
        t = y / height  # Normalized position (0 at top, 1 at bottom)

        if t < 0.5: # Upper half: transition from sky to horizon_upper
            local_t = t * 2
            current_color = (1 - local_t) * color_sky + local_t * color_horizon_upper
        elif t < 0.75: # Middle-lower: transition from horizon_upper to sun_glow_middle
            local_t = (t - 0.5) * 4 
            current_color = (1 - local_t) * color_horizon_upper + local_t * color_sun_glow_middle
        else: # Lower part: transition from sun_glow_middle to sun_glow_lower
            local_t = (t - 0.75) * 4
            current_color = (1 - local_t) * color_sun_glow_middle + local_t * color_sun_glow_lower
        
        image[y, :, :] = np.clip(current_color, 0, 1)

    # Create figure with exact pixel dimensions
    fig = plt.figure(figsize=(width/100, height/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]) # Fill the entire figure
    ax.imshow(image)
    ax.axis('off')
    
    plt.savefig(filename)
    print(f"Sunset image saved as {filename}")

if __name__ == "__main__":
    generate_sunset_image() 