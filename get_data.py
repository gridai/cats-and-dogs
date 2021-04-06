from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

URL = 'https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip'


def download_zip_data(url, path="data/"):
    with urlopen(url) as resp:
        with ZipFile(BytesIO(resp.read())) as file:
            file.extractall(path)


def remove_bad_images(bad_images_path='bad_images.txt', image_folder='cats_and_dogs_data/'):
    bad_img_filepaths = Path(bad_images_path).open().readlines()
    deleted_files = []
    for bad_img_file in bad_img_filepaths:
        file_to_delete = Path(image_folder) / Path(bad_img_file.strip())
        if file_to_delete.exists():
            deleted_files.append(file_to_delete.as_posix())
            file_to_delete.unlink()
    print(f"Deleted {len(deleted_files)} corrupted files! :)")


def main():
    if not Path('cats_and_dogs/').exists():
        download_zip_data(URL, 'cats_and_dogs_data/')
    remove_bad_images()


if __name__ == '__main__':
    main()
