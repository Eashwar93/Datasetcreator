import os, glob
import shutil
import argparse

def add_data(source_path, dest_path, file_format):
	existing_names = []
	for file in glob.glob1(dest_path,"*"+file_format):
		existing_name = os.path.splitext(file)[0]
		existing_names.append(int(existing_name))
		existing_names.sort()
	if len(existing_names) >= 1:
		file_number = existing_names[-1]
	else:
		file_number = 0
	print ("Images will be written sequentially starting from: "+str(file_number+1)+file_format+"\n")
	confirm = input("Please confirm by typing \"agree\":\n")
	
	if str(confirm) != "agree":
		print("Exiting without copying the new data to the existing dataset")
		return
		
	else:
		for file in glob.glob1(source_path,"*"+file_format):
			shutil.copy(source_path+file, dest_path+str(file_number+1)+file_format)
			file_number += 1
	
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--source_path", type=str, help="Ablsolute path to the source ditrectory")
	parser.add_argument("--dest_path", type=str, help="Absolute path to the existing dataset directory")
	parser.add_argument("--file_format", type=str, help="image extension .png or .jpg with .")
	args = parser.parse_args()
	if args.source_path and args.dest_path and args.file_format is not None:
		add_data(args.source_path, args.dest_path, args.file_format)
	else:
		print("missing arguments or too-many arguments")
		parser.print_help()
		exit(1)
	
