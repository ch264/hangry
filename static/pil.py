from PIL import Image
import argparse
import os


# create const and set to tuple
DEFAULT_SIZE = (320, 180)

# img = Image.open('klara-avsenik-1365422-unsplash.jpg')
# print(img.size)
# print(img.format)

dir = os.getcwd()

def resize_image(input_dir, infile, output_dir='resized', size=DEFAULT_SIZE):
  outfile = os.path.splitext(infile)[0] + '_resized' 
  extension = os.path.splitext(infile)[1]

  try:
    img = Image.open(input_dir + '/' + infile)
    img = img.resize((size[0], size[1]), Image.LANCZOS)

    new_file = output_dir + '/' + outfile + extension
    img.save(new_file)
  except IOError:
    print('cannot resize')

# passing in values for each resize
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_dir', help='Full Input Path')
parser.add_argument('-o', '--output_dir', help='Full Output Path')
parser.add_argument('-w', '--width', help='Resized Width')
parser.add_argument('-t', '--height', help='Resized Height')
args = parser.parse_args()

# pass width height, otherwise display default
if args.width and args.height:
  size = (int(args.width), int(args.height))
else: 
  size = DEFAULT_SIZE

print(args)

# define input and output folder
if args.input_dir:
  input_dir = args.input_dir
else: 
  input_dir = (dir + '/700')

if args.output_dir:
  output_dir = args.output_dir
else:
  output_dir = dir + '/' + '300'


if not os.path.exists(os.path.join(dir, output_dir)):
  os.mkdir(output_dir)

try:
  for file in os.listdir(input_dir):
    resize_image(input_dir, file, output_dir, size=size)
except OSError:
    print('file not found')




# size_300 = (300,300)
# size_700 = (700,700)
# for f in os.listdir('.'):
#     if f.endswith('.jpeg'):
#         i = Image.open(f)
#         fn, fext = os.path.splitext(f)

# 				i.thumbnail(size_700)
#         i.save('700/{}_700{}'.format(fn,fext))

# 				i.thumbnail(size_300)
#         i.save('300/{}_300{}'.format(fn,fext))


# image1 = Image.open('static/lukas-blazek-261682-unsplash.jpg')
# image1.show()
# image1.save('static/lukas-blazek-261682-unsplash.jpg')