import os, glob
import shutil
import argparse


def sample_images(image_path, sample_rate, file_format, dest_path):
    img_names = []
    for file in glob.glob1(image_path, "*" + file_format):
        camera_img = os.path.splitext(file)[0]
        img_name = camera_img.split("_")[1]
        img_names.append(int(img_name))
        img_names.sort()
    sampled_img_names_cam1 = img_names[::sample_rate]
    sampled_img_names_cam2 = img_names[1::sample_rate]
    sampled_img_names = sampled_img_names_cam1 + sampled_img_names_cam2
    print("Selected Images:", sampled_img_names)
    print("Number of Selected Images:", len(sampled_img_names))

    existing_names = []
    for file in glob.glob1(dest_path, "*" + file_format):
        existing_name = os.path.splitext(file)[0]
        existing_names.append(int(existing_name))
        existing_names.sort()
    if len(existing_names) >= 1:
        file_number = existing_names[-1]
    else:
        file_number = 0
    print("Image start number is:", file_number + 1)

    for sampled_img_name in sampled_img_names:
        for file in glob.glob1(image_path, "*" + str(sampled_img_name) + file_format):
            camera_img = os.path.splitext(file)[0]
            img_name = camera_img.split("_")[1]
            if img_name == str(sampled_img_name):
                shutil.copy(image_path + file, dest_path + str(file_number + 1) + file_format)
                file_number += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--imgs_path", type=str, help="Ablsolute path to the images folder that you want to sample")
    parser.add_argument("--sample_rate", type=int, help="Freequency at which you wan to sample the images")
    parser.add_argument("--file_format", type=str, help="image extension .png or .jpg with .", default=".png")
    parser.add_argument("--dest_path", type=str, help="destination path of the sampled images",
                        default="~/Dataset/recordings/sampled_images")
    args = parser.parse_args()
    if args.imgs_path and args.sample_rate and args.file_format and args.dest_path is not None:
        sample_images(args.imgs_path, args.sample_rate, args.file_format, args.dest_path)
    else:
        print("wrong usage detected")
        parser.print_help()
        exit(1)