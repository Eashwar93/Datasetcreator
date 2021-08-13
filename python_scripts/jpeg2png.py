import glob, os
import shutil, random
from PIL import Image
import argparse


def converttopng(datapath):
	print ("Specified dataset path:",datapath)
	count = len(glob.glob1(datapath,"*.jpg"))
	print ("number of images files to be converted:",str(count))


		
	for file in glob.glob1(datapath,"*.jpg"):
		iml = Image.open(datapath+file)
		file_png = os.path.splitext(file)[0]+".png"
		iml.save(datapath+file_png)
		os.remove(datapath+file)
		count -= 1
		if count%100 == 0:
			print(count,"Images left to convert")			

	

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("jpegdatapath", type=str, help="Absolute path to the saved images in jpeg format and their coressponding json label files generateed with labelme")
	args = parser.parse_args()
	converttopng(args.jpegdatapath)

	






	
	





	
