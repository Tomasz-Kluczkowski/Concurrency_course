import urllib.request
import time


NUMBER_OF_IMAGES_TO_DOWNLOAD = 10


def download_image(image_path, file_name):
    print(f'Downloading image from: {image_path}')
    urllib.request.urlretrieve(image_path, file_name)


def main():
    start = time.time()
    for i in range(NUMBER_OF_IMAGES_TO_DOWNLOAD):
        image_name = f'temp/image-{i}.jpg'
        download_image('https://picsum.photos/400/200', image_name)

    stop = time.time()
    total_time = stop - start
    print(f'Tota Excecution time {total_time}')


if __name__ == '__main__':
    main()
