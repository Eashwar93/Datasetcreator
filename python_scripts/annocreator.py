import os, glob
import argparse 

def createtrainanno(datapath, trainimagespath, trainlabelspath, trainanno):
	
	imgs=[]
	lbls=[]
	lbls_id=[]
	
	for file in glob.glob1(datapath+trainimagespath, "*.png"):
		img = os.path.splitext(file)[0]
		imgs.append(img)
	
	for file in glob.glob1(datapath+trainlabelspath, "*_id.png"):
		lbl_id = os.path.splitext(file)[0]
		lbl = lbl_id.split("_")[0]
		lbls .append(lbl)
		lbls_id.append(lbl_id)
		
	if(set(imgs).difference(lbls)):
		print("Missing labels for images:",(set(imgs).difference(lbls)))
		return
		
	elif(set(lbls).difference(imgs)):
		print("Missing images for labels:",(set(lbls).difference(imgs)))
		return
			
	else:
		print("Sanity check complete all training-images have training-label_id images")
		
	os.chdir(datapath)
	train_txt = open(trainanno, "w")
	for img in imgs:
		train_txt.write(trainimagespath+img+".png,"+trainlabelspath+img+"_id.png\n")
	train_txt.close()
	
def createtestanno(datapath, testimagespath, testlabelspath, testanno):
	
	imgs=[]
	lbls=[]
	lbls_id=[]
	
	for file in glob.glob1(datapath+testimagespath, "*.png"):
		img = os.path.splitext(file)[0]
		imgs.append(img)
	
	for file in glob.glob1(datapath+testlabelspath, "*_id.png"):
		lbl_id = os.path.splitext(file)[0]
		lbl = lbl_id.split("_")[0]
		lbls .append(lbl)
		lbls_id.append(lbl_id)
		
	if(set(imgs).difference(lbls)):
		print("Missing labels for images:",(set(imgs).difference(lbls)))
		return
		
	elif(set(lbls).difference(imgs)):
		print("Missing images for labels:",(set(lbls).difference(imgs)))
		return
			
	else:
		print("Sanity check complete all test-images have test-label_id images")
		
	os.chdir(datapath)
	test_txt = open(testanno, "w")
	for img in imgs:
		test_txt.write(testimagespath+img+".png,"+testlabelspath+img+"_id.png\n")
	test_txt.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--datapath", type=str, help="Absolute path to the root of the custom dataset")
	parser.add_argument("--trainimagespath", type=str, help="Relative path to the training images directory from the root of the custom dataset")
	parser.add_argument("--trainlabelspath", type=str, help="Relative path to the training label images directory from the root of the custom dataset")
	parser.add_argument("--testimagespath", type=str, help="Relative path to the training images directory from the root of the custom dataset")
	parser.add_argument("--testlabelspath", type=str, help="Relative path to the training label images directory from the root of the custom dataset")
	parser.add_argument("--trainanno", type=str, help="Name of the train annotation file")
	parser.add_argument("--testanno", type=str, help="Name of the test annotation file")
	parser.add_argument("--evalimagespath", type=str, help="Relative path to the evaluation images directory from the root of the custom dataset")
	parser.add_argument("--evallabelspath", type=str,
						help="Relative path to the evaluation label images directory from the root of the custom dataset")
	parser.add_argument("--evalanno", type=str, help="Name of the train annotation file")
	parser.add_argument("--eval", type=bool,default=False, help="True if evaluation dataset preparation and False if train or test dataset preparation")
	args = parser.parse_args()
	if args.datapath and args.trainimagespath and args.trainlabelspath and args.trainanno and args.testimagespath and args.testlabelspath and args.testanno is not None:
		createtrainanno(args.datapath, args.trainimagespath, args.trainlabelspath, args.trainanno)
		createtestanno(args.datapath, args.testimagespath, args.testlabelspath, args.testanno)
	elif args.datapath and args.evalimagespath and args.evallabelspath and args.evalanno and args.eval is not False:
		createtrainanno(args.datapath, args.evalimagespath, args.evallabelspath, args.evalanno)
	else:
		print("Wrong usage detected")
		parser.print_help()
		
	
