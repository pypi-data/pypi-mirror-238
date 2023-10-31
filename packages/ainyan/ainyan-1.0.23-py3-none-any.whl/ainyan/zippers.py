import zipfile
import os

def zip_folder(src_folder, output_filename):
    """Zip the folder 'src_folder' with the output zip file name
    """
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_STORED) as zipf:
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, src_folder)
                zipf.write(file_path, arcname)


def unzip_folder(zip_file, folder_path):
    """
    Unzip folder
    :param zip_file: the zip file to unzip
    :param folder_path: path where to extract the content of the zip file
    :return: nothing
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
