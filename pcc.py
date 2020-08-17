import sys
sys.path.append('/Users/thomas/Library/Python/3.7/lib/python/site-packages')

from operator import add
from PIL import Image
from pdf2image import convert_from_path
import re


# Decides color based on input arguments
def get_black(args):
	if len(args) >= 5 and args[3] == "-c":
		valid_colors = {"p":(50, 0, 100), "g":(0, 100, 0), "b":(0, 0, 100), "r":(100, 0, 0)}
		ret = valid_colors.get(args[4])
		if ret != None:
			return ret
		else:
			raise Exception("Invalid choice of colors")
	else:
		return (0, 0, 100) # Dark blue is default color choice

# Removes black from an image by converting it to greyscale but with input
#	BLACK as black instead of RGB (0, 0, 0)
def deblack(im, BLACK):
	WLIM = 240 # threshold above which we accept it's white
	
	px = im.load()

	w, h = im.size
	print(str(w) + ' by ' + str(h))

	blue_im = Image.new("RGB", (w,h), "white")
	blue_px = blue_im.load()

	for x in range(w):
		for y in range(h):
			cc = px[x, y]

			if (cc[0] > WLIM and cc[1] > WLIM and cc[2] > WLIM):
				# pixel is white
				blue_px[x, y] = cc
			else:
				# pixel is color and should get greyscaled
				frac = (0.299 * cc[0] + 0.587 * cc[1] + 0.114 * cc[2]) / 255
				val = [int((255 - x) * frac) for x in BLACK]

				blue_px[x, y] = tuple(map(add, BLACK, val))

	return blue_im
	
# Reads in file based on extension
#	acceptable types: pdf, any single image PIL can open
def read_file(name):
	if bool(re.match(r"(?i).*\.(pdf)", name)):
		images = convert_from_path(name)
	else:
		images = [Image.open(name)]
	return images

# Saves to resulting file to pdf
# 	may save to 2 files if given flag -d for double sided printing
def save_file(ims, name, args):
	if "-d" in args:
		
		# Pad to even number of pages
		if len(ims) % 2 == 1 and len(ims) != 1:
			w, h = ims[0].size
			ims.append(Image.new('RGB', (w, h), (255, 255, 255)))
	
		# Save to 2 files
		front = ims[0::2]
		back = ims[1::2]
		back.reverse()

		front[0].save(args[2] + "1.pdf", save_all=True, append_images=front[1:])
		if back:
			back[0].save(args[2] + "2.pdf", save_all=True, append_images=back[1:])
	else:
		ims[0].save(args[2] + ".pdf", save_all=True, append_images=ims[1:])


########################
# MAIN for pcc.py
#	correct usage: python3 pcc.py inputImage saveToName
#		optional: -c to select color (p for purple, g for green, b for blue)

assert(len(sys.argv) >= 3)
BLACK = get_black(sys.argv)

images = read_file(sys.argv[1])

dcimgs = [deblack(x, BLACK) for x in images]

save_file(dcimgs, sys.argv[2], sys.argv)
# dcimgs[0].save(sys.argv[2] + ".pdf", save_all=True, append_images=dcimgs[1:])


