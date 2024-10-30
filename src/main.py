from file_utils import FileUtils
import os

def main():
  #input_path = r"/Users/avikumar/Desktop/studio keys/studio-keys/10-28/about-us.studio"
  #output_path = r"/Users/avikumar/Desktop/studio keys/studio-keys/10-28/about-us"
  multiple_files = input("Do you have multiple .studio files you'd like to convert? (y/n): ").strip().lower()
  if multiple_files == 'y':
        input_path = input("Please provide the full path to the folder containing all .studio files: ").strip()
        if not os.path.isdir(input_path):
            print(f"The folder path '{input_path}' is not a valid path. Please try again.")
            exit(1)
        if not contains_studio_files(input_path):
            print(f"The folder you provided does not contain .studio files, or contains files which are not .studio files. Please provide a valid folder.")
            exit(1)
  elif multiple_files == 'n':
        input_path = input("Please provide the full path to the single .studio file: ").strip()
        if not os.path.isfile(input_path):
            print(f"The file path '{input_path}' is not valid. Please try again.")
            exit(1)
        if not input_path.endswith(".studio"):
            print(f"The file '{input_path}' is not a .studio file. Please provide a valid .studio file.")
            exit(1)
  else:
        print("Invalid input. Please enter 'y' or 'n'.")
        exit(1)
  output_path = input("Please provide the full path to where you'd like the output folder of mockups to be placed: ").strip()
  if not os.path.isdir(output_path):
        print(f"The folder path '{output_path}' is not valid. Please try again.")
        exit(1)
  file_processor = FileUtils(input_path,output_path)
  file_processor.run_studio_keys()


def is_valid_path(path, is_file=False):
    if is_file:
        return os.path.isfile(path)
    else:
        return os.path.isdir(path)
def contains_studio_files(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.endswith(".studio"):
            return False
    return True

if __name__ == '__main__':
    main()

