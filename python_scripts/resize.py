import cv2
import glob
import argparse

def resize(img_path, resolution):
    for file in glob.glob1(img_path, "*.png"):
        img = cv2.imread(img_path+str(file))
        img = cv2.resize(img, dsize=resolution, interpolation=cv2.INTER_AREA)
        cv2.imwrite(img_path+str(file), img)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, help="Absolute path to the image directory that contains the images to be reshaped")
    parser.add_argument("--width", type=int, help="Target width of the image")
    parser.add_argument("--height", type=int, help="Target height of the image")
    args = parser.parse_args()
    if args.img_path and args.width and args.height is not None:
        resize(args.img_path, (args.width, args.height))
    else:
        print("Wrong usage, please refer to the below syntax")
        parser.print_help()
        exit(1)