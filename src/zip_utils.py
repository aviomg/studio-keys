import os
import zipfile

def create_zip(output_path, studio_file_name,zip_folder,session_output_folder):
    #if not any(os.scandir(output_path)):
    if not any(os.scandir(session_output_folder)):
        print("No files found in the output directory.")
    else:
        print("Files found; proceeding with zipping.")

    """Creates a zip file containing SVG mockups generated from the .studio file."""
    zip_filename = f"{os.path.splitext(studio_file_name)[0]}.zip"
    zip_path = os.path.join(zip_folder,zip_filename)

    #output_svg_path = os.path.join(output_path, "Studio Keys - Output")

#THIS IS THE FIX THAT REMOVES THE JSON FOLDER FROM ALSO BEING SAVED W IT. The commented out chunk below is what i was using
#before
    svg_output_path = os.path.join(session_output_folder, "Studio Keys - Output/SVG Mockups")
    with zipfile.ZipFile(zip_path,'w') as zipf: 
        for root,_,files in os.walk(svg_output_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path, os.path.relpath(file_path, session_output_folder))


    '''with zipfile.ZipFile(zip_path,'w') as zipf: 
           #for root, _, files in os.walk(output_svg_path):
           for root, dirs, files in os.walk(session_output_folder):
               for file in files:
                   file_path = os.path.join(root,file)
                   zipf.write(file_path, os.path.relpath(file_path,session_output_folder))'''



    '''    bname = os.path.splitext(studio_file_name)[0]
        print(f"bname is {bname}")
        mockups_path = os.path.join(output_path,"Studio Keys - Output","SVG Mockups",bname)
        print(f"mockups path is {mockups_path}")
        for root, dirs, files in os.walk(mockups_path):
            for file in files:
                zipf.write(os.path.join(root,file),
                           os.path.relpath(os.path.join(root,file),
                                           os.path.join(output_path,'..'))) '''
    return zip_path

