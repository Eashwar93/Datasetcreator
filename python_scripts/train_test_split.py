import glob, os
import shutil, random
from PIL import Image
import argparse


def traintestsplit(datapath, destpath, ratio):
	
	print("Specified dataset path:",datapath)
	print("number of images files:",len(glob.glob1(datapath,"*.png")))
	print("number of json files:",len(glob.glob1(datapath,"*.json")))
	
	imgs = []
	lbls = []

	for file in glob.glob1(datapath,"*.png"):
		img = os.path.splitext(file)[0]
		imgs.append(img)
		
	for file in glob.glob1(datapath, "*.json"):
		lbl = os.path.splitext(file)[0]
		lbls.append(lbl)
		
	if(set(imgs).difference(lbls)):
		print("Missing labels for images:",(set(imgs).difference(lbls)))
		
	elif(set(lbls).difference(imgs)):
		print("Missing images for labels:",(set(lbls).difference(imgs)))
			
	else:
		print("Sanity check complete all images have labels")
		
	imgs_traindir = destpath+"images/train/"
	labels_traindir = destpath+"labels/train/"
	
	imgs_testdir = destpath+"images/test/"
	labels_testdir = destpath+"labels/test/"

	try:
		os.makedirs(imgs_traindir)
	except OSError:
		print("Creation of %s failed, the path probably already exists, skipping creation" % imgs_traindir)
	else:
		print("Creation of %s succeeded" % imgs_traindir)
	
	try:
		os.makedirs(labels_traindir)
	except OSError:
		print("Creation of %s failed, the path probably already exists, skipping creation" % labels_traindir)
	else:
		print("Creation of %s succeeded" % labels_traindir)
		
	try:
		os.mkdir(imgs_testdir)
	except OSError:
		print("Creation of %s failed, the path probably already exists, skipping creation" % imgs_testdir)
	else:
		print("Creation of %s succeeded" % imgs_testdir)
	
	try:
		os.mkdir(labels_testdir)
	except OSError:
		print("Creation of %s failed, the path probably already exists, skipping creation" % labels_testdir)
	else:
		print("Creation of %s succeeded" % labels_testdir)
		
	total_data = len(glob.glob1(datapath, "*.png"))
	train_data_count = round(ratio*total_data)
	test_data_count = total_data - train_data_count
	print("Planned number of training images:", train_data_count)
	print("Planned number of testuation images:", test_data_count)
	
	train_data = random.sample(glob.glob1(datapath,"*.png"),train_data_count)
	for f in enumerate (train_data, 1):
		shutil.copy(datapath+f[1], imgs_traindir)
		shutil.move(datapath+f[1], labels_traindir)	
	
	test_data = glob.glob1(datapath,"*.png")
	for f in enumerate (test_data, 1):
		shutil.copy(datapath+f[1], imgs_testdir)
		shutil.move(datapath+f[1], labels_testdir)

	imgs_training = []
	imgs_test = []
		
	for file in glob.glob1(imgs_traindir,"*.png"):
		img = os.path.splitext(file)[0]
		imgs_training.append(img)
		shutil.copy(imgs_traindir+file, datapath+file)
		
	for file in glob.glob1(imgs_testdir,"*.png"):
		img = os.path.splitext(file)[0]
		imgs_test.append(img)
		shutil.copy(imgs_testdir+file, datapath+file)
		
	for img in imgs_training:
		shutil.copy(datapath+img+".json", labels_traindir)
		
	for img in imgs_test:
		shutil.copy(datapath+img+".json", labels_testdir)
		

	
if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--datapath", type=str, help="Absolute path to the saved images in png format and their coressponding json label files generateed with labelme")
	parser.add_argument("--destpath", type=str, help="Absolute path to create the custom dataset")
	parser.add_argument("--ratio", type=float, help="Ratio of images to be assigned for training compared to the total number of images")
	args = parser.parse_args()
	if args.datapath and args.destpath and args.ratio is not None:
		traintestsplit(args.datapath, args.destpath, args.ratio)
	else:
		print("Wrong usage detected")
		parser.print_help()
	






	
	





	
