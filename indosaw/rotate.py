from PIL import Image

def rotate_and_save_image(input_path, output_path, angle):
    # Open the original image
    original_image = Image.open(input_path)
    
    # Rotate the image by the specified angle
    rotated_image = original_image.rotate(angle, expand=True)
    
    # Save the rotated image
    rotated_image.save(output_path)
    
    print(f"Image rotated by {angle} degrees and saved to {output_path}")

# Example usage
if __name__ == "__main__":
     # Replace with the desired output file path
    rotation_angle = -90  # Specify the rotation angle in degrees
    for i in range(1,9):
        input_path = str(i)+".Bmp"  # Replace with the path to your input image file
         
        rotate_and_save_image(input_path, input_path, rotation_angle)
