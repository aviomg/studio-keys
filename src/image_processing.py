
import os
import base64
import svgwrite
import logging
import resource
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for even more detail
logger = logging.getLogger(__name__)
class ImageHandler:
    def __init__(self, json_data, json_files_folder_path,studio_file_path_name):
        self.json_files_folder_path = json_files_folder_path
        self.studio_file_name = self.get_studio_file_name(studio_file_path_name)
        logger.info("before creating image map table:")
        log_resource_usage()
        self.image_map = self.create_img_file_map(json_data,json_files_folder_path)
        logger.info("Image file map created. about to create size table")
        log_resource_usage()
       # self.href_table = self.create_href_table(json_data, json_files_folder_path)
       # logger.info("after creating href and before creating size table")
        #log_resource_usage()
        self.size_table = self.create_size_table(json_data)
 
        
    def get_studio_file_name(self,studio_file_path_name):
         parts = studio_file_path_name.strip().split(os.sep)
         return parts[-2]

    def create_img_file_map(self,json_data,json_files_folder_path):
         """Map image IDs to their file paths. For each image, we have created a table that associates the id with the 
         file path needed to convert it to base64. self.convert_img_base_64(imagemap[id]) will return the encoding for a given image"""
         imagemap = {}
         if "resources" in json_data and "images" in json_data["resources"]:
              for img in json_data["resources"]["images"]:
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
                                   if not filePath and "jpeg" in ext:
                                        fileName = hash + ".jpeg"
                                        filePath = self.find_file(json_files_folder_path,fileName) 
                                   if filePath:
                                        imagemap[id] = filePath
                                   else:
                                        print(f"No file path found for image ID {img['id']} with file name {fileName} in {self.studio_file_name}")
                              else:
                                   print("Unsupported file type:", ext)
         else:
              print("no images and/or resources found in JSON")
         return imagemap
    
    def get_image_href(self, resource_id):
         """Generate href string for a given image ID on demand."""
         filepath = self.image_map.get(resource_id) #obtains the file path associated with the image
         if not filepath:
              print(f"No file found for resource ID {resource_id}")
              return None
         logger.info("in get_image_href, before calling convertb64")
         log_resource_usage()
         img_b64 = self.convert_img_base_64(filepath)
         logger.info("in get_image_href, after calling convertb64")
         log_resource_usage()
         ext = os.path.splitext(filepath)[1].lower()
         if "png" in ext:
              return f"data:image/png;base64,{img_b64}"
         elif "jpg" in ext or "jpeg" in ext:
              return f"data:image/jpeg;base64,{img_b64}"
         print(f"couldn't generate href for some reason; returning None")
         return None

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
                                   if not filePath and "jpeg" in ext: 
                                        #print("trying again with jpeg")
                                        fileName = hash + ".jpeg"
                                        filePath = self.find_file(json_files_folder_path,fileName)  
                                   #print(f"Searching for image with ID {id}: expected path {filePath}")
                                   if filePath:
                                        #print(f"found img with name {fileName}\n")
                                        img_b64 = self.convert_img_base_64(filePath)
                                        if "png" in ext:
                                             img_href = f"data:image/png;base64,{img_b64}"
                                        if "jpeg" in ext:
                                             img_href = f"data:image/jpeg;base64,{img_b64}"
                                        ans[id] = img_href
                                   else:
                                        print(f"no file path found for image ID {id} with file name {fileName} in {self.studio_file_name}")
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
                  return filepath
        print(f"File {hash_filename} not found in {start_dir}")
        return None
    
    def convert_img_base_64(self, image_path):  
          try:
              base64_chunks = []
              basestr = ""
              with open(image_path, "rb") as image_file:
                 #  return base64.b64encode(image_file.read()).decode('utf-8')
                   while chunk := image_file.read(4002):
                        base64_chunks.append(base64.b64encode(chunk).decode('utf-8'))
                       # basestr += base64.b64encode(chunk).decode('utf-8')
              #return basestr
              result = "".join(base64_chunks)
              return result
          except Exception as e:
              print(f"Error encoding image: {e}")
              return None
              
              """
              with open(image_path, "rb") as image_file:
                   return base64.b64encode(image_file.read()).decode('utf-8')
              """

              
               
    def create_image(self, ch, imageTable):
     # Logic from create_image function
     img = 0
     resourceID = ch['resourceId'] #this is the same as the "ID" of the image dict
    # print(f"Creating image for resourceID: {resourceID}")
     if "fills" in ch:
          if "image" in ch['fills'][0]:
               if "fit" in ch['fills'][0]['image'] and ch['fills'][0]['image']['fit'] != "fill":
                         print("not fill")
    # if resourceID in self.href_table:
    #      href = self.href_table.get(resourceID)
     if resourceID in self.image_map:
          #here is where i'd want to lookup if the image is in "imageTable"
          x = ch['x']['value']
          y = ch['y']['value']
          width = ch['width']['value']
          height = ch['height']['value']
          if resourceID in imageTable:
             #  print(f"found image id {resourceID} in the table")
               attrs = imageTable[resourceID]
               x, y, width, height = attrs.x, attrs.y, attrs.width, attrs.height
               #print(f"Using custom attributes for image")
          logger.info("before generating href:")
          log_resource_usage()
          href = self.get_image_href(resourceID) #generate href on demand
          logger.info("after generating href")
          log_resource_usage() 
          img = svgwrite.image.Image(href=href, insert=(x,y),size=(width,height))   
       #   print(f"Image created with href., position: ({x}, {y}), size: ({width}, {height})")     
          if (ch['isFixedAspectRatio']):
                         img.fit(horiz='center',vert='middle', scale='meet')  
     else:
          print(f"Image with name {ch['name']} not found in href table/ couldn't generate href for it")
          print("\n")
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
def log_resource_usage():
     usage = resource.getrusage(resource.RUSAGE_SELF)
     logger.info(f"Memory usage: {usage.ru_maxrss} KB")
    # logger.info(f"User time: {usage.ru_utime} seconds")
     #logger.info(f"System time: {usage.ru_stime} seconds")