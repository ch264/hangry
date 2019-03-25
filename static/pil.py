from PIL import Image
import argparse
import os


# create const and set to tuple
DEFAULT_SIZE = (128, 128)

# img = Image.open('klara-avsenik-1365422-unsplash.jpg')
# print(img.size)
# print(img.format)

dir = os.getcwd()
input_dir = (dir + '/700')
output_dir = dir + '/' + '300'
size = DEFAULT_SIZE

def thumbnail_image(input_dir, infile, output_dir='thumbnail', size=DEFAULT_SIZE):
  outfile = os.path.splitext(infile)[0] + '.thumbnail' 
  extension = os.path.splitext(infile)[1]

  try:
    img = Image.open(input_dir + '/' + infile)
    # LANCZOS is a high quality downsampling filter
    img = img.thumbnail((size[0], size[1]), Image.LANCZOS)

    new_file = output_dir + '/' + outfile + extension
    img.save(new_file)
  except IOError:
    print('cannot resize')


# # passing in values for each resize
# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--input_dir', help='Full Input Path')
# parser.add_argument('-o', '--output_dir', help='Full Output Path')
# parser.add_argument('-w', '--width', help='Resized Width')
# parser.add_argument('-t', '--height', help='Resized Height')
# args = parser.parse_args()

# # pass width height, otherwise display default
# if args.width and args.height:
#   size = (int(args.width), int(args.height))
# else: 
#   size = DEFAULT_SIZE

# print(args)

# define input and output folder
# if args.input_dir:
#   input_dir = args.input_dir
# else: 
  input_dir = (dir + '/700')

# if args.output_dir:
#   output_dir = args.output_dir
# else:
  output_dir = dir + '/' + '300'


if not os.path.exists(os.path.join(dir, output_dir)):
  os.mkdir(output_dir)
try:
  for file in os.listdir(input_dir):
    thumbnail_image(input_dir, file, output_dir, size=size)
except OSError:
    print('file not found')

