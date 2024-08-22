import svgwrite
from collections import namedtuple

class TextProcessor:
    StyleSettings = namedtuple('StyleSettings',['fontFamily', 'fontSize','fontWeight','fontStyle', 'fontFill','dy'])

    def create_text(self,ch):
     width = self.extract_width(ch)
     if width:
          if "\n" not in ch['content']:
               lines = self.handle_no_line_breaks(ch,width)
               if lines:
                    return lines
          elif "\n" in ch['content']:
               lines = self.handle_prebroken_text(ch,width)
               if lines:
                    return lines
     lines = self.handle_multiline_text(ch)
     if lines:
          return lines
     lines = self.handle_multiple_text_attributes(ch)
     if lines:
          return lines
     return self.create_default_text(ch)
    
    def extract_width(self,ch):
     if "textAttributes" in ch and "attributes" in ch['textAttributes'][0] and "font" in ch['textAttributes'][0]['attributes']:
          width = self.textwidth(ch['content'],14)
          return width
     return None
    
    def handle_no_line_breaks(self,ch, width):
     words = ch['content'].split(' ')
     if(len(words)>1)and (width > (ch['width']['value'] + 5)): 
          lines = self.longer_text(ch, width) 
          if lines != 0:
               return lines
     return None
    
    def handle_prebroken_text(self,ch, width):
     lines = ch['content'].split('\n')
     still_too_long = False
     for line in lines:
          line_width = self.textwidth(line,14)
          words = line.split(' ')
          if(len(words)>4) and (line_width > (ch['width']['value'] + 15)):
               still_too_long = True
     if (still_too_long):
          removed_line_breaks = ch['content'].replace("\n"," ")
          broken_lines = self.longer_text(ch, width, removed_line_breaks)
          if broken_lines != 0:
               return broken_lines
     return None
    
    def handle_multiline_text(self,ch):
        words = ch['content'].split('\n')
        if(len(words) > 1):
            return self.mult_lines(ch, words)
        return None
    
    def handle_multiple_text_attributes(self,ch):
        if "textAttributes" in ch and isinstance(ch['textAttributes'],list) and len(ch['textAttributes'])>1:
            return self.range(ch, len(ch['textAttributes']))
        return None
    
    def create_default_text(self,ch):
     text = self.create_basic_text(ch,0)
     if text != 0:
          return text
     return None
    
    def longer_text(self,ch, currLength, newcont="a0"):
     lines = 0
     desLength = ch['width']['value']
     content = ch['content']
     curr = ""
     ans = ""
     fsize = ch['textAttributes'][0]['attributes']['font']['size']
     realwords = content.split(' ')
     for w in realwords:
          word = w + ' ' 
          temp = curr + word 
          width = self.textwidth(temp,fsize)
          if width >= (ch['width']['value']):
               ans = ans + curr + "\n"    
               curr = word    
          else:
               curr = curr + word
     ans = ans + curr
     lines1 = ans.split('\n')
     if (len(lines1) > 1):
          lines = self.mult_lines(ch,lines1)
     return lines
    
    def textwidth(self,text, fontsize=14):
        try:
            import cairo
        except:
            return len(text) * fontsize
        surface = cairo.SVGSurface('undefined.svg', 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(fontsize)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
        return width
    
    def mult_lines(self,text,lines="a0"):
       if lines == "ao":
          l = text['content'].split('\n')
       else:
            l = lines
       ranges = {}
       start = 0
       end = 0
       for line in l:
            end = start + len(line)
            ranges[line] =(start,end)
            start = start + len(line) + 1
       yfactor=0
       x = text['x']['value']
       y = text['y']['value']
       fS = self.getStyle(text,0)
       if "textAttributes" in text and "attributes" in text['textAttributes'][0]:
            attribs = text['textAttributes'][0]['attributes']
            if "lineHeight" in attribs:
               yfactor = attribs['lineHeight'] 
            if "lineHeight" not in attribs:
                 yfactor = attribs['font']['defaultLineHeight']
       elements= []
       t = svgwrite.text.Text("")
       t.add(svgwrite.text.TSpan(lines[0],insert=(text['x']['value'],text['y']['value'] + yfactor),font_family=fS.fontFamily,font_weight=fS.fontWeight,
                                 font_size=fS.fontSize,font_style=fS.fontStyle,fill=fS.fontFill))
       elements.append(t)
       lines.pop(0)
       i = 2
       if "textAttributes" in text:
           if isinstance(text['textAttributes'],list) and len(text['textAttributes'])>1:
                for line in lines:
                     j = 0
                     for index, ch in enumerate(text['textAttributes']):
                          current_index = int(index)
                          if ranges[line][0] >= ch['range'][0] and ranges[line][1] <= ch['range'][1]:
                               fS = self.getStyle(text,current_index)
                     t = svgwrite.text.Text("")
                     t.add(svgwrite.text.TSpan(line,insert=(x,(y+(yfactor * i))),font_family=fS.fontFamily, font_weight=fS.fontWeight,
                     font_size=fS.fontSize,font_style=fS.fontStyle,fill=fS.fontFill))
                     i+=1
                     elements.append(t)
                return elements
           else:
                fS = self.getStyle(text,0)
                for line in lines:
                    t = svgwrite.text.Text("")
                    t.add(svgwrite.text.TSpan(line,insert=(x,(y+(yfactor * i))),font_family=fS.fontFamily, font_weight=fS.fontWeight,
                    font_size=fS.fontSize,font_style=fS.fontStyle,fill=fS.fontFill))
                    i+=1
                    elements.append(t)
                return elements
    
    def create_basic_text(self,text,index, cont="a0", xfactor=0):
       t_x = text['x']['value'] + xfactor
       t_y = text['y']['value']
       fS = self.getStyle(text,index)
       if cont == "a0":
            content = text['content']
       else:
            content = cont
       t = svgwrite.text.Text("")
       span =svgwrite.text.TSpan(content, insert=(t_x,t_y), dy=[fS.dy], 
                                 font_family= fS.fontFamily,font_weight = fS.fontWeight, font_size=fS.fontSize,font_style=fS.fontStyle, fill=fS.fontFill )
       t.add(span)
       return t  
    
    def range(self,text, num):
     ans = []
     content = text['content']
     i = 0
     xfactor = 0
     mainText = svgwrite.text.Text("", insert=(text['x']['value'], text['y']['value']))
     for ch in text['textAttributes']:
          start = ch['range'][0]
          end = ch['range'][1]
          substr = content[start:(end + 1)]
          t = self.create_tspan(text, i, substr)
          mainText.add(t)
          i +=1
     return mainText
    
    def create_tspan(self,text,index,cont="a0"):
     content = cont
     fS = self.getStyle(text,index)
     if index == 0:
          dy1 = fS.dy
     elif index != 0:
          dy1 = 0
     span =svgwrite.text.TSpan(content, dy=[dy1],font_family= fS.fontFamily,font_weight = fS.fontWeight, font_size=fS.fontSize,font_style=fS.fontStyle , fill=fS.fontFill)
     return span
    
    def getStyle(self,ch, index):
      fontFam = "Arial"
      style="normal"
      weight = 400
      fill = 'blue'
      lineHeight = 0
      defLineHeight = 0
      t_height = ch['height']['value']
      if "textAttributes" in ch and "attributes" in ch['textAttributes'][index]:
           attribs = ch['textAttributes'][index]['attributes']
           if "lineHeight" in attribs:
                lineHeight = attribs['lineHeight']
           if "color" in attribs:
                fill = self.format_color(attribs['color'])
           if "color" not in attribs:
               print("no color given")
           if "font" in attribs:
                font = attribs['font']
           if "defaultLineHeight" in font:
                defLineHeight = font['defaultLineHeight']
           if "family" in font:
               if "Open Sans" in font['family']:
                    fontFam = "Open Sans"
               else:
                    fontFam = font['family']
           if "size" in font:
                size = font['size']
           if "weight" in font:
                if font['weight'] == "Regular":
                     if "weightNum" in font:
                          weight = font['weightNum']
                     else:
                          weight = "normal"
                if font['weight'] == "Bold":
                     weight = "bold"
                if font['weight'] != "Regular" and font['weight'] != "Bold":
                     if font['weight'] == "Italic":
                          style = "italic"
                     if "weightNum" in font:
                          weight = font['weightNum']
           if "weight" not in font:
                if "weightNum" in font:
                     weight = font['weightNum']
           if "italic" in font:
                if (font['italic']):
                     style = "italic"
      else:
           print("textAttributes not in text element")
      dy1 = self.get_dy(lineHeight, defLineHeight, t_height)
      ans = self.StyleSettings(fontFamily=fontFam,fontSize=size,fontWeight=weight,fontStyle=style, fontFill=fill, dy=[dy1])
      return ans 

    def format_color(self,colorElement):
     return f"rgb({colorElement['r']},{colorElement['g']},{colorElement['b']})" 

    def get_dy(self,lineHeight, defLineHeight, t_height=0):
      dy = t_height
      if (lineHeight == 24) and (defLineHeight == 22):
            dy = 17
      if (lineHeight == 40) and (defLineHeight == 38):
            dy=29
      if (lineHeight == 28) and (defLineHeight == 27):
            dy=21
      if lineHeight == 16 and defLineHeight == 16:
            dy=12
      if lineHeight == 36 and defLineHeight == 33:
            dy=26
      if lineHeight == 24 and defLineHeight == 19:
            dy = 17
      if lineHeight == 16 and defLineHeight == 19:
            dy = 13
      if lineHeight == 16 and defLineHeight == 20:
            dy = 13
      if lineHeight == 40 and defLineHeight == 44:
            dy = 31
      if lineHeight == 24 and defLineHeight == 16:
            dy = 16
      if defLineHeight == 19 and lineHeight == 0:
            dy = 14
      return dy 
  






    
    

