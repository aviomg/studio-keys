import os
import shutil
from design_assembly import create_mockups
import uuid
import logging
import resource
import tracemalloc
"""Class for helper functions performing file managing and processing tasks, such as converting the .studio files into zip archives,
    extracting the necessary JSON file, directory organization, etc."""

logging.basicConfig(level=logging.INFO)  # Change to DEBUG for even more detail
logger = logging.getLogger(__name__)
def log_resource_usage():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    logger.info(f"Memory usage: {usage.ru_maxrss} KB")
    logger.info(f"User time: {usage.ru_utime} seconds")
    logger.info(f"System time: {usage.ru_stime} seconds")

class FileUtils:
    output_json_folder_name = "Studio Keys - Output/JSON Data (Ignore)"
    output_studio_folder_name = "Studio Keys - Output/Copy of .studio Files (Ignore)"
    output_svg_folder_name = "Studio Keys - Output" #removed "Studio Keys - Output/SVG Mockups"

    def __init__(self, input_file_path, output_folder_location, unique=True):
        if unique:
            self.output_folder_location = output_folder_location
            self.session_id = str(uuid.uuid4())
            self.session_output_folder = os.path.join(output_folder_location,f"Studio_Keys_Output_{self.session_id}")
            self.output_svg_folder_name = os.path.join(self.session_output_folder,"Studio Keys - Output/SVG Mockups")


            if os.path.isfile(input_file_path):
                temp_dir = os.path.join(self.session_output_folder,"temp_studio_file")
                os.makedirs(temp_dir,exist_ok=True)
                shutil.copy(input_file_path,temp_dir)
                self.input_file_path = temp_dir
            else:
                self.input_file_path = input_file_path
            logger.info("about to call create_jsons_folder_path")
            log_resource_usage()
            self.json_folder_path = self.create_jsons_folder_path()
            logger.info("about to call create_dict")
            log_resource_usage()
            tracemalloc.start()
            self.snapshot_file_dict = self.create_dict(self.input_file_path)
            tracemalloc.stop()
        else:
            self.output_folder_location = output_folder_location
            self.session_output_folder = os.path.join(output_folder_location,f"Studio_Keys_Output")
            self.output_svg_folder_name = os.path.join(self.session_output_folder,"Studio Keys - Output/SVG Mockups")

            if os.path.isfile(input_file_path):
                temp_dir = os.path.join(self.session_output_folder,"temp_studio_file")
                os.makedirs(temp_dir,exist_ok=True)
                shutil.copy(input_file_path,temp_dir)
                self.input_file_path = temp_dir
            else:
                self.input_file_path = input_file_path
        
            self.json_folder_path = self.create_jsons_folder_path()
            self.snapshot_file_dict = self.create_dict(self.input_file_path)
    
    def obtain_json(self,studio_file_path):
        logger.info("obtaining json")
        log_resource_usage()
        """studio_file_path = file path for a .studio mockup file to be converted. 
            Returns the file path of the corresponding extracted JSON file (snapshot.json)."""
        if os.path.isfile(studio_file_path):
            zip_path = self.change_extension(studio_file_path,"zip")
            json_folder_path = self.extract_and_replace_zip(zip_path)
            for filename in os.listdir(json_folder_path):
                if filename == 'snapshot.json':
                    full_path = os.path.join(json_folder_path,filename)
                    return full_path
            print(f"snapshot file not found in the extracted zip folder: {zip_path}")
            return None

    def change_extension(self, file_path, new_extension):
        logger.info("changing extension")
        log_resource_usage()
        """Helper function for obtain_json which converts .studio file into zip archive and extracts contents into a 
            separate subfolder. Creates a copy of original .studio file(s) and stores them in a different folder.
            file_path = file path of the orignal .studio file. new_extension = the desired file type extension"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist!!")
        if os.path.isfile(file_path):
            dest = f"{self.output_folder_location}/{self.output_studio_folder_name}"
            #dest = f"{self.session_output_folder}/{self.output_studio_folder_name}"
            shutil.os.makedirs(dest,exist_ok=True) 
            shutil.copy2(file_path,dest)
            file_name = os.path.basename(file_path) 
            base_name, _ = os.path.splitext(file_name) 
            new_file_name = f"{base_name}.{new_extension}" 
            #new_file_path = os.path.join(self.output_folder_location,self.output_json_folder_name,new_file_name)
            new_file_path = os.path.join(self.session_output_folder,self.output_json_folder_name,new_file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist!!")
            os.rename(file_path, new_file_path)
            return new_file_path
        else:
            print(f"Could not find file: {file_path}")

    def create_jsons_folder_path(self):
        #json_folder_path = os.path.join(self.output_folder_location, self.output_json_folder_name)
        json_folder_path = os.path.join(self.session_output_folder, self.output_json_folder_name)
        os.makedirs(json_folder_path,exist_ok=True)
        return json_folder_path

    def extract_and_replace_zip(self,zip_path):
        logger.info("extracting and replacing zip")
        log_resource_usage()
        """Helper function for obtain_json which extracts the contents of zip archive."""
        if os.path.isfile(zip_path):
            extract_to = os.path.splitext(zip_path)[0]
            try:
                shutil.unpack_archive(zip_path,extract_to,"zip")
                os.remove(zip_path)
                return extract_to
            except shutil.ReadError:
                print(f"{os.path.basename(zip_path)} couldn't be unzipped. Skipping this file.")
        else:
            print(f"Could not find file: {zip_path}")


    def list_json_file_paths(self, folder_path):
        """ Given initial input of .studio mockup files, returns a list of file paths to the JSON files obtained
        from each .studio file. 
        folder_path = file path to folder of .studio files.""" 
        json_file_paths = []
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                json_file_paths.append(self.obtain_json(full_path))
        return json_file_paths

    def create_dict(self,folder_path):
        """Given initial input of .studio mockup files, returns a dictionary of key-value pairs, where key = [file path of key 
            snapshot.json file] and value = [folder name for storing generated mockups]. Output folders of SVG mockups are named
            by the basename of their respective .studio files.
            folder_path = file path to folder of .studio files."""
        mockup_dict = {}
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path,filename)
            base_name, _ = os.path.splitext(filename)
            dest_for_svgs = f"/{base_name}"
            if os.path.isfile(full_path):
                logger.info("Memory before JSON extraction: %s", tracemalloc.get_traced_memory())
                jsonpath = self.obtain_json(full_path)
                logger.info("Memory after JSON extraction: %s", tracemalloc.get_traced_memory())
                if jsonpath:
                    mockup_dict[jsonpath] = dest_for_svgs
                else:
                    print(f"Skipping file {filename} as it couldn't be unzipped or parsed.")
        return mockup_dict

    def create_folder(self,name):
        """Creates a folder to store the generated mockups/artboards of a .studio file
            name = the name of the subfolder, given by create_dict (see above)"""
       # folder_path1 = os.path.join(self.output_folder_location,self.output_svg_folder_name)
        folder_path1 = os.path.join(self.output_svg_folder_name,name.strip("/"))
        #folder_path = f"{folder_path1}/{name}"
        os.makedirs(folder_path1, exist_ok=True)
        return folder_path1
    
    def run_studio_keys(self):
        for srcpath, dest in self.snapshot_file_dict.items():
            dest_path = self.create_folder(dest)
            #(f"sending srcpath as {srcpath} for {dest}")
            create_mockups(srcpath,dest_path, self.json_folder_path)