import random, argparse
from os.path import join, isfile, split, splitext
parser = argparse.ArgumentParser(description='Random shuffle a txt list.')
parser.add_argument('--txt', type=str, help='txt list file', default='list.txt')
args = parser.parse_args()

assert isfile(args.txt), "txt file(%s) not exists!"%args.txt
with open(args.txt, 'r') as f:
  lines = f.readlines()
random.shuffle(lines)
fdir, fullfn = split(args.txt)
fn, ext = splitext(fullfn)
new_txt = open(join(fdir, fn + "_shuffled" + ext ), 'w')
for l in lines:
  new_txt.write("%s"%l)
new_txt.close()
  
