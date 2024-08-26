import os
import zipfile

def create_zip(output_path, studio_file_name,zip_folder):
    if not any(os.scandir(output_path)):
        print("No files found in the output directory.")
    else:
        print("Files found; proceeding with zipping.")
    """Creates a zip file containing SVG mockups generated from the .studio file."""
    zip_filename = f"{os.path.splitext(studio_file_name)[0]}.zip"
    zip_path = os.path.join(zip_folder,zip_filename)
    with zipfile.ZipFile(zip_path,'w') as zipf: 
        bname = os.path.splitext(studio_file_name)[0]
        print(f"bname is {bname}")
        mockups_path = os.path.join(output_path,"Studio Keys - Output","SVG Mockups",bname)
        print(f"mockups path is {mockups_path}")
        for root, dirs, files in os.walk(mockups_path):
            for file in files:
                zipf.write(os.path.join(root,file),
                           os.path.relpath(os.path.join(root,file),
                                           os.path.join(output_path,'..')))
    return zip_path

