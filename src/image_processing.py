
import os
import base64
import svgwrite

class ImageHandler:
    def __init__(self, json_data, json_files_folder_path):
        self.json_files_folder_path = json_files_folder_path
        self.href_table = self.create_href_table(json_data, json_files_folder_path)
        self.size_table = self.create_size_table(json_data)

    def create_href_table(self, json_data, json_files_folder_path):
      # Logic from image_dict function
          ans = {}
          if "resources" in json_data:
               resources = json_data['resources']
               if "images" in resources:
                    for img in resources['images']:
                         if "fileType" in img:
                              ext = img['fileType'].lower()
                              if "png" in ext or "jpeg" in ext:
                                   hash = img['hash']
                                   id = img['id']
                                   if "png" in ext:
                                        fileName = hash + ".png"
                                   if "jpeg" in ext:
                                        fileName = hash + ".jpg"
                                   filePath = self.find_file(json_files_folder_path,fileName)
                                   #print(f"Searching for image with ID {id}: expected path {filePath}")
                                   if filePath:
                                        img_b64 = self.convert_img_base_64(filePath)
                                        if "png" in ext:
                                             img_href = f"data:image/png;base64,{img_b64}"
                                        if "jpeg" in ext:
                                             img_href = f"data:image/jpeg;base64,{img_b64}"
                                        ans[id] = img_href
                                   else:
                                        print(f"no file path found for image ID {id} with file name {fileName}")
                              else:
                                   print("file is of type " + ext)
               else:
                    print("no images")
          else:
               print("no resources")
          return ans

    def create_size_table(self, json_data):
         # Logic from size_dict function
        ans = {}
        if "resources" in json_data:
             resources = json_data['resources']
             if "images" in resources:
                  for img in resources['images']:
                       id = img['id']
                       width = img['width']
                       height = img['height']
                       ans[id] = (width,height)
             else:
                  print("no images")
        return ans
     
    def find_file(self, start_dir, hash_filename):
         # Logic from find_file function
        lc_target = hash_filename.lower()
        for dirpath, dirnames, filenames in os.walk(start_dir):
             lc_filenames = [filename.lower() for filename in filenames]
             #if hash_filename in filenames:
             if lc_target in lc_filenames:
                  index = lc_filenames.index(lc_target)
                  filepath = os.path.join(dirpath,filenames[index])
                 # print(f"File found: {filepath}")
                  return filepath
        print(f"File {hash_filename} not found in {start_dir}")
        return None
    
    def convert_img_base_64(self, image_path):
         try:
              with open(image_path, "rb") as image_file:
                   return base64.b64encode(image_file.read()).decode('utf-8')
         except Exception as e:
              print(f"Error encoding image: {e}")
              return None
     

    def create_image(self, ch):
     # Logic from create_image function
     img = 0
     resourceID = ch['resourceId'] #this is the same as the "ID" of the image dict
    # print(f"Creating image for resourceID: {resourceID}")
     if "fills" in ch:
          if "image" in ch['fills'][0]:
               if "fit" in ch['fills'][0]['image'] and ch['fills'][0]['image']['fit'] != "fill":
                         print("not fill")
     if resourceID in self.href_table:
          href = self.href_table.get(resourceID) 
          x = ch['x']['value']
          y = ch['y']['value']
          width = ch['width']['value']
          height = ch['height']['value']
          img = svgwrite.image.Image(href=href, insert=(x,y),size=(width,height))   
       #   print(f"Image created with href., position: ({x}, {y}), size: ({width}, {height})")     
          if (ch['isFixedAspectRatio']):
                         img.fit(horiz='center',vert='middle', scale='meet')  
     else:
          print(f"Image with resourceID {resourceID} not found in href table.")
     if ch['isVisible']:
          return img
     elif not ch['isVisible']:
         # print(f"image with resourceID {resourceID} was not visible") 
          return 0     
       
    def get_image_data(self, id):
        return self.href_table.get(id)
        # Retrieve image data from href_table

    def get_image_size(self, id):
        return self.size_table.get(id)
        # Retrieve image size from size_table