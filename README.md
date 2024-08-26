# Studio Keys

A Python-based tool designed that enables the easy retrieval and recovery of otherwise inaccessible UI/UX designs created with the now-extinct Invision prototyping tool.

## Motivation
Imagine that you are an artist who has spent countless man-hours developing a rich portfolio of oil paintings. You stored these valuable pieces in a temperature-controlled locker, where they would be safe and easily accessible to you should you ever need them. 

Now imagine that the safelocker was left out in the sun. Your paintings might still be okay, or maybe not. It'd be easy enough to find out...except you've also lost the key. Despite having the safelocker right in front of your eyes, your paintings are, for all intents and purposes, lost. But what if you could get them back?  

InVision Studio was a popular prototyping tool for creating UI/UX designs (think Figma, Sketch, etc.). But with its abrupt discontinuation of all services (read about it [here](https://www.feedme.design/invisions-prototyping-tool-the-unexpected-reappearance-and-abrupt-goodbye/), [here](https://support.invisionapp.com/), or [here](https://dorve.c.om/blog/ux-news-articles-archive/invision-shutting-down/)), many designers and developers found themselves unable to access their designs, all of which are saved by default in an InVision-specific file extension, `.studio`, that can't be opened without the platform. Studio Keys was developed to address this need by providing an reliable way to convert these inaccessible files into SVGs, ensuring that valuable design work is not lost and can be reused in other projects or platforms.  

## Project Overview

Studio Keys is a Python program that:

- Parses and processes `.studio` files, extracting the necessary data.
- Converts the design elements (e.g., rectangles, text, images) into SVG format.
- Outputs the SVG files, maintaining the correct layering and structure of the original design.

The program can handle both individual `.studio` files and folders containing multiple `.studio` files. Users can specify the input and output locations, and the tool will generate the SVG files in the desired directory.

### Key Features

- **Batch Processing**: Convert multiple `.studio` files at once by providing a folder path.
- **Single File Conversion**: Easily convert individual `.studio` files.
- **Output Customization**: Choose where to save the generated SVG mockups.

### Usage/Installation Instructions [unfinished]
### Examples/Demo
### The Process/Lessons Learned
### Future work
### License


 





