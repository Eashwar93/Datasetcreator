import os, glob
import argparse 
import imutils
import cv2

def CreateRotatedDataset(datapath, trainimagespath, trainlabelspath, evalimagespath, evallabelspath):

	modes = ["train","eval"]
	for mode in modes:

		if mode == "train":
			imgspath = trainimagespath
			labelspath = trainlabelspath
			
		elif mode == "eval":
			imgspath = evalimagespath
			labelspath = evallabelspath
			
		imgs=[]
		lbls=[]
		lbls_id=[]
	
		for file in glob.glob1(datapath+imgspath, "*.png"):
			img = os.path.splitext(file)[0]
			imgs.append(img)
			
			
		for file in glob.glob1(datapath+labelspath, "*_id.png"):
			lbl_id = os.path.splitext(file)[0]
			lbl = lbl_id.split("_")[0]
			lbls .append(lbl)
			lbls_id.append(lbl_id)

			
		if(set(imgs).difference(lbls)):
			print("Missing labels for images:",(set(imgs).difference(lbls)))
			
		elif(set(lbls).difference(imgs)):
			print("Missing images for labels:",(set(lbls).difference(imgs)))
				
		else:
			if mode == "train":
				print("Sanity check complete."+str(len(imgs))+" training-images found training-label_id images")
	
			elif mode == "eval":
				print("Sanity check complete."+str(len(imgs))+" evaluation-images found training-label_id images")
		
	dirs = ["train_img","train_label","eval_img", "eval_label"]
	for di in dirs:
		if di == "train_img":
			rotate_dir_path = "/images/train_rotated"
			dir_path = trainimagespath
			os.mkdir(datapath+rotate_dir_path)
			os.chdir(datapath+rotate_dir_path)
			search_string = "*.png"
		
		elif di == "train_label":
			rotate_dir_path = "/labels/train_rotated"
			dir_path = trainlabelspath
			os.mkdir(datapath+rotate_dir_path)
			os.chdir(datapath+rotate_dir_path)
			search_string = "*_id.png"
			
		elif di == "eval_img":
			rotate_dir_path = "/images/eval_rotated"
			dir_path = evalimagespath
			os.mkdir(datapath+rotate_dir_path)
			os.chdir(datapath+rotate_dir_path)
			search_string = "*.png"
			
		elif di == "eval_label":
			rotate_dir_path = "/labels/eval_rotated"
			dir_path = evallabelspath
			os.mkdir(datapath+rotate_dir_path)
			os.chdir(datapath+rotate_dir_path)
			search_string = "*_id.png"
		
		for file in glob.glob1(datapath+dir_path,search_string):
			print("Rotating"+file)
			img_no = os.path.splitext(file)[0]
			if di == "train_img" or "eval_img":
				print(di)
				print(datapath+dir_path+file)
				img = cv2.imread(datapath+dir_path+file)
			elif di == "train_label" or "eval_label":
				print(di)
				img = cv2.imread(datapath+dir_path+file,0)
			rotated=imutils.rotate_bound(img, -90)
			cv2.imwrite(img_no+".png",rotated)
				
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("datapath", type=str, help="Absolute path to the root of the custom dataset")
	parser.add_argument("trainimagespath", type=str, help="Relative path to the training images directory from the root of the custom dataset")
	parser.add_argument("trainlabelspath", type=str, help="Relative path to the training label images directory from the root of the custom dataset")
	parser.add_argument("evalimagespath", type=str, help="Relative path to the training images directory from the root of the custom dataset")
	parser.add_argument("evallabelspath", type=str, help="Relative path to the training label images directory from the root of the custom dataset")
	args = parser.parse_args()
	CreateRotatedDataset(args.datapath, args.trainimagespath, args.trainlabelspath, args.evalimagespath, args.evallabelspath)

		
	
