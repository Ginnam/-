from PIL import Image
import os


def create_image_grid(image_paths, grid_size):
    images = [Image.open(img_path) for img_path in image_paths]

    # Calculate the size of each thumbnail
    thumb_width, thumb_height = images[0].size
    new_im = Image.new('RGB', (thumb_width * grid_size[0], thumb_height * grid_size[1]))

    x_offset = 0
    y_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, y_offset))
        x_offset += thumb_width
        if x_offset >= thumb_width * grid_size[0]:
            x_offset = 0
            y_offset += thumb_height

    return new_im


def main():
    directory = 'movie_posters'
    image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]

    if not image_files:
        print("No .jpg files found in the specified directory.")
        return

    # Determine the number of rows and columns for the grid
    num_images = len(image_files)
    grid_size = (int(num_images ** 0.5), int(num_images / int(num_images ** 0.5)) + 1)

    poster_wall = create_image_grid(image_files, grid_size)
    poster_wall.save('poster_wall.jpg')
    print("Poster wall created and saved as 'poster_wall.jpg'.")


if __name__ == "__main__":
    main()



