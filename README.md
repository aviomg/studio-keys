
# Studio Keys

A Python-based tool designed to enables the easy retrieval and recovery of otherwise inaccessible UI/UX designs created with the now-extinct Invision prototyping tool.

[Access the web application!](https://studio-keys.onrender.com/)
[View the Github repo](https://github.com/aviomg/studio-keys) to view my code or access sample materials for the demo.

## Motivation
My mom is a painter, and she gave me an interesting analogy. Imagine you were an artist who has spent endless man-hours developing this diverse portfolio of oil paintings. You kept these valuable pieces in a temperature-controlled storage locker, where they'd be safe but easily accessible when you need them.

One day, you come home to a flood, everything in your home soaked in water, if not fully washed away. Your locker is waterproof, though, so your paintings are okay, thank god. Only then, you realize that the key, which is usually sitting on your desk, the kitchen table, or some other absentminded counter, was washed away. Now what?

Despite having the storage locker right in front of your eyes, your paintings are, for all intents and purposes, lost. But what if you could get them back?  

InVision Studio, once a popular prototyping tool for creating UI/UX designs (think Figma, Sketch, etc.), is like that waterproof locker. With its abrupt discontinuation of all services (read about it [here](https://www.feedme.design/invisions-prototyping-tool-the-unexpected-reappearance-and-abrupt-goodbye/), [here](https://support.invisionapp.com/), or [here](https://dorve.c.om/blog/ux-news-articles-archive/invision-shutting-down/)), many designers and developers found themselves unable to access their designs, all of which are saved by default in an InVision-specific file extension, `.studio`, that can't be opened without the desktop application. Studio Keys was developed to address this need by providing an reliable way to convert these once-inaccessible files into SVGs, ensuring that valuable design work is not lost and can be reused in other projects or platforms.  

## Project Overview

Studio Keys is a Python program that:
- Processes `.studio` files to extract the necessary data in JSON format.
- Parses and processes the JSON files to convert the design elements (e.g., rectangles, text, images) into SVG format, rendering one SVG for each "artboard".
- Locates, processes, and encodes images to base-64.
- Outputs the SVG files, maintaining the correct layering and structure of the original design.

Users upload `.studio` files through an intuitive web interface and receive a downloadable .zip containing the SVGs.

## Key Features
- **Effortless Conversion Process**: Users can upload `.studio` files and download neatly packaged SVG mockups with a single click, simplifying the process of turning design files into web-compatible assets.
- **Intuitive Web Interface**: A user-friendly Flask-powered web interface ensures a smooth user experience, making it simple for users of all technical backgrounds to upload files and retrieve SVG outputs.
- **Scalable and Modular Codebase**: Designed with scalability in mind, the project’s modular code structure makes it easy to extend functionality, accommodating future enhancements and customizations.
- **Customizable for Diverse Needs**: The program can be tailored to meet specific requirements, whether by adjusting SVG layouts or tweaking conversion settings, offering flexibility for various design workflows.
## Usage
- Navigate to the web application at https://studio-keys.onrender.com, and follow the instructions to upload a .studio file from your computer. The program will output a .zip file to a folder containing an SVG for each artboard rendered from the file. 

## Examples
- I owe the motivation for this entire project to my manager, who tasked me with it to recover ~600 mockups that he possessed. He was kind enough to allow me to provide some of the mockups that I rendered for examples.
- To try the program out for yourself, download one of the sample `.studio` files from /resources/sample_studio_files and upload it to the [web application](https://studio-keys.onrender.com/).
- View some sample generated mockups in /resources/sample_generated_svgs

## Known Issues & Limitations
#### 1. File Size Constraints:
- Currently, Studio Keys reliably handles `.studio` files of size up to **36.3 MB**.
- Files larger than **43.7 MB** consistently result in memory-related errors in the deployment environment (_e.g., SIGKILL_).
- Files between **36.3 MB and 43.7 MB** are untested and may yield unpredictable results. 
#### 2. The smaller the file, the faster the output generation
- Please allow up to 16 seconds for the program to output your mockups, particularly for larger `.studio` files.
#### 3. Text Alignment:
- Occasional inaccuracies in text alignment may occur, particularly with complex layouts.
#### 4. Image Scaling:
- Images occasionally fail to scale correctly within their bounding boxes, either appearing too small or extending outside their intended areas.

## Future work
#### 1. Resolve Memory Management Issues:
Refactor code to optimize memory usage and improve support for larger .studio files.
#### 2. Enhance Text Alignment:
Investigate and correct text alignment issues to ensure accuracy across all artboards.
#### 3. Improve Image Scaling:
Address inconsistencies in image fitting and scaling within design boxes.
#### 4. Expanded Testing:
Test with a broader range of .studio files to ensure robust functionality across various file sizes and complexities.
#### 5. New Features:
Add support for additional file formats or export options beyond SVG.
Incorporate a progress tracker for uploads and conversions in the web interface.

## Call for Contributors
- Want to be part of the process of improving this awesome program? I am in the continuous process of improving the program to create more precise, refined mockups, and the key to this is my database of diverse .studio files that I use to gain a better understanding of the logic behind the now-extinct Invision app. If you would like to volunteer your .studio files for this cause, please do so at [this google form](https://forms.gle/Cyv3TL1Z477RxHBcA).

### License
### Acknowledgements
### The Process/Lessons Learned
### Technical Details
### How it Works


 





