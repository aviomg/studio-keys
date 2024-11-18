import svgwrite
import os
import json
from collections import namedtuple
from text_processing import TextProcessor
from image_processing import ImageHandler
import logging
import resource

logging.basicConfig(level=logging.INFO)  # Change to DEBUG for even more detail
logger = logging.getLogger(__name__)

def create_mockups(src_path,dest_path, json_files_folder_path):
     """Runs the program to create all of the mockups in a single .studio file.
          src_path = path of the JSON source file
          dest_path = the location of where to store the output mockups"""
     logger.info("about to open the src path and load the json data")
     log_resource_usage()
     with open(src_path, 'r', encoding='utf-8') as f:
          data = json.load(f)
     logger.info("about to instantiate imagehandler object")
     log_resource_usage()
     global image_handler
     image_handler = ImageHandler(data,json_files_folder_path,src_path)
     logger.info("image handler instantiated")
     log_resource_usage()

     print(f"generating mockups from src: {studio_file_name(src_path)}:")
     if "children" in data:
          if (data['children'][0]['type'] == "page"):
               page = data['children'][0]
     if "children" in page:
          for ch in page['children']: #Creates a separate SVG file for each artboard, each of which represent 1 mockup.
               if ch['type'] == "artboard":
                    artboard = ch
                    name1 = artboard['name'] + ".svg"
                    #ACCOUNTING FOR THE ARTBOARD NAME INCLUDING A SLASH:
                    name = name1.replace("/","-")
                    #if name == "branch-guest-1280.svg":
                    #print("creating " + name)
                    create_artboard(artboard,name, dest_path)

def create_artboard(artboard, name,save_to):
    """Creates a singular mockup (an "artboard").
          artboard = the object representing a JSON child element named 'artboard' (see function above). Each JSON file representing a .studio file
               contains a parent element, "page", with one or more children of type "artboard".
          name = the file name ([name].svg) where the generated mockup will be stored.
          dest_path = the destination folder to store the output mockup. """
    global attributes
    global imageTable
    attributes = namedtuple('Attributes',['x','y','width','height'])
    imageTable = {}   
    height = artboard['height']['value']
    width = (artboard['width']['value'])
    dwg = svgwrite.Drawing(os.path.join(save_to, name),size=(width,height))
    dwg.viewbox(width=width, height=height)
    abcolor = ""
     #Creating the artboard viewport:
    if "viewportWidth" in artboard:
         vpwidth = str(artboard['viewportWidth']['value']) + "px"
    else:
         vpwidth = width
    if "viewportHeight" in artboard and (artboard['viewportHeight']['unit'] == "pixel"):
        vpheight = str(artboard['viewportHeight']['value']) + "px"
    else:
         vpheight = height
    if "fills" in artboard and "color" in artboard['fills'][0]:
         color = artboard['fills'][0]['color']
         abcolor = format_color(color)
    else:
         abcolor = 'white'
    rect = dwg.add(dwg.rect(insert=(0,0),size=(vpwidth, vpheight), fill=abcolor))
    g1 = dwg.add(dwg.g())
    #Creating and adding the elements/contents of the artboard (Base rectangles are added first to ensure correct layering):
    for ch in artboard['children']:
         if ch['type'] == 'rectangle':
              r = create_rectangle(ch)
              dwg.add(r)  
    logger.info("about to call process element many times")
    log_resource_usage
    for ch in artboard['children']:
         if ch['type'] != 'rectangle':
          process_element(dwg,dwg,ch)
    logger.info("done calling process element many times")
    log_resource_usage
    dwg.save()

def process_element(dwg, parent_group, element):
     
     """Creates each SVG element and adds it to the given SVG. Handles nested elements, which are labeled in the JSON file as children of type 'group'.
          dwg = the base SVG drawing onto which all created elements are directly or indirectly added.
          parent_group = the SVG group element onto which elements of a group are added (parent_group is eventually added to "dwg".) Used for handling JSON children of type 'group'.
          element = the actual element (text, rectangle, etc.) being processed at a given call of the function.
          """
     hasImg = False
     hasRec = False
     image = 0
     rectangle = 0
     if element['type'] == 'group':
        group = dwg.g()
        tgroup = dwg.g()
        group_children = element['children']
     #Handling image addition, sizing, placement by cross referencing 'image' children with 
     # 'rectangle' children (representing 'image backgrounds') who have the same JSON parent of type 'group'.
        if len(group_children) == 3 or len(group_children) == 2:
             #print(f"ground group {element['name']} with length {len(group_children)}")
             for ch in group_children:
                  if ch['type'] == "image" and (ch['isVisible']):
                       hasImg = True
                       image = ch
                  if ch['type'] == "rectangle":
                       #if "isVisible" in ch and (ch['isVisible']) and ("bg" in ch['name']):
                       if "isVisible" in ch and (ch['isVisible']):
                         hasRec = True
                         n2 = ch['name']
                         rectangle = ch
             if hasRec and hasImg and image != 0 and rectangle !=0:
                 # print(f"found a group. name={element['name']}. id={element['id']}")
                  #for ch in group_children:
                      # if ch['type'] == 'rectangle':
                       #      print(f"child: name={ch['name']},type={ch['type']}, color={ch['fills'][0]['type']},{format_color(ch['fills'][0]['color'])}")
                       #else:
                        #    print(f"child: name={ch['name']},type={ch['type']}")
                       #if len(group_children) != 2:
                        #    print(f"group of size {len(group_children)}")
                 
                  id = image['resourceId']
                  x = rectangle['x']['value']
                  y = rectangle['y']['value']
                  width = rectangle['width']['value']
                  height = rectangle['height']['value']
                  imgx = image['x']['value']
                  imgy = image['y']['value']
                  imgw = image['width']['value']
                  imgh = image['height']['value']
               #   print(f"x(img,rect): {imgx},{x}....y: {imgy},{y}....width:{imgw},{width}...height:{imgh},{height}")
                #  print("\n")
                  imageTable[id] = attributes(x, y, width, height)
                 # print(f"added image id {id} to table with width={width} and height={height}")
     #Handles children of type 'group' by recursively calling process_element on each child of the group:
        for ch in group_children:
            if ch['type'] == 'rectangle' and "container" in ch['name']:
                 process_element(dwg, group, ch)
        for ch in group_children:
            if ch['type'] == 'rectangle' and  "container" not in ch['name']:
                 process_element(dwg, group, ch)
        for ch in group_children:
            if ch['type'] != 'rectangle':
                 process_element(dwg,tgroup,ch) 
        group.add(tgroup)
        parent_group.add(group)
     else:
          if element['type'] == 'rectangle':
               rect = create_rectangle(element)
               parent_group.add(rect)
          elif element['type'] == 'text':
               el = final_create_text(element)
               if el:
                    if isinstance(el, list):
                         for line in el:
                              parent_group.add(line)
                    else:
                         parent_group.add(el)
          elif element['type'] == 'image':
              # print(f"processing image with name {element['name']}")
              # logger.info("about to call image handler for an image")
               #log_resource_usage()
               img = image_handler.create_image(element,imageTable)
               #log_resource_usage()
               if img != 0:
                    parent_group.add(img)

def final_create_text(element):
     text_processor = TextProcessor()
     el = text_processor.create_text(element)
     if el != 0:
          visible = True
          if "isVisible" in element:
               visible = element['isVisible']
          if (visible):
               return el
     return None

def create_rectangle(rect):
     rx = 0
     ry = 0
     if "cornerRadius" in rect:
          rx = rect['cornerRadius']['left']
          ry = rect['cornerRadius']['top']
     MCU = "userSpaceOnUse"
     maskUnits = "userSpaceOnUse"
     rect_x = rect['x']['value']
     rect_y = rect['y']['value']
     rect_width = rect['width']['value']
     rect_height = rect['height']['value']
     rect_id = rect['id']
     ans = svgwrite.shapes.Rect(insert=(rect_x, rect_y),rx=rx, ry=ry, size=(rect_width,rect_height), fill='none', id=rect_id)
     enabled = True
     enabledb = False
     isVisible = True
     if "isVisible" in rect:
          isVisible = rect['isVisible']
     if (isVisible):
          if "fills" in rect and isinstance(rect['fills'],list):
               if (len(rect['fills'])>0) and rect['fills'][0]['type'] == 'solid':
                    if "isEnabled" in rect['fills'][0]:
                         enabled = rect['fills'][0]['isEnabled']
                    if (enabled):
                         color = rect['fills'][0]['color']
                         formatted_color = format_color(color)
                         ans = svgwrite.shapes.Rect(insert=(rect_x,rect_y),rx=rx,ry=ry,size=(rect_width,rect_height),
                                                    fill=formatted_color,fill_opacity=(color['a']))
          if "borders" in rect and isinstance(rect['borders'],list): 
               if ((len(rect['borders'])>0)) and rect['borders'][0]['type'] == 'solid':
                    if "isEnabled" in rect['borders'][0]:
                         enabledb = rect['borders'][0]['isEnabled']
                    if(enabledb):
                         color = rect['borders'][0]['color']
                         rect_border = format_color(color)
                         rect_border_width = rect['borders'][0]['width']
                         ans.stroke(rect_border)
                         ans.attribs['stroke-width'] = rect_border_width
     return ans

def format_color(colorElement):
     return f"rgb({colorElement['r']},{colorElement['g']},{colorElement['b']})"
def studio_file_name(src_path):
     dir_name = os.path.dirname(src_path)
     return os.path.basename(dir_name) + ".studio"

def log_resource_usage():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    logger.info(f"Memory usage: {usage.ru_maxrss} KB")
    logger.info(f"User time: {usage.ru_utime} seconds")
    logger.info(f"System time: {usage.ru_stime} seconds")