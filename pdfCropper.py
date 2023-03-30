#!/usr/bin/env python3
import re,copy
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

file_path = Path()
print("initiating...at ".join(str(file_path)))

pdf_merger = PdfMerger()
print("merger created")
merge_list = (i for i in file_path.glob("*.pdf"))
for pdf_file in merge_list:
    pdf_merger.append(str(pdf_file))

if pdf_merger.inputs == []:
    print("Pdf not Found")
else:
    print("merge completed")
    with Path(file_path, "temp.pdf").open(mode="wb") as f:
        pdf_merger.write(f)
    print("merged file generated")

def x2(path):
    reader = PdfReader(str(path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
        writer.add_page(copy.copy(page))
    return writer
    
def alter_pdf(path):
    reader = PdfReader(str(path))
    for page in reader.pages:
        yield page
    
def chunks(lst):
    for i in range(0,len(lst),2):
        yield lst[i:i+2]

fwriter = PdfWriter()

for page_pair in list(chunks(x2(str(Path(file_path, "temp.pdf"))).pages)):
    page1 = page_pair[0]
    page2 = page_pair[1]
    origin_width, origin_height = page1.mediabox.upperRight  # original size
    if (origin_height > 500) and (len(re.findall("打印次数", page1.extract_text())) > 1):
        upper_half = page1
        lower_half = page2
        upper_half.mediabox.lower_left = (0, origin_height / 2)
        lower_half.mediabox.upper_left = (0, origin_height / 2)
        fwriter.add_page(upper_half)
        fwriter.add_page(lower_half)
    elif (origin_height > 500) and (len(re.findall("打印次数", page1.extract_text())) == 1):
        upper_half = page1
        upper_half.mediabox.lower_left = (0, origin_height / 2)
        fwriter.add_page(upper_half)
    else:
        pass

print("cropping finished")
with Path(file_path, "concate.pdf").open(mode="wb") as f:
    fwriter.write(f)
print("Auto-cleaning...")
Path(file_path, "temp.pdf").unlink()
print("End")