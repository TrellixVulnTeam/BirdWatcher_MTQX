import os
# import pickle
import tarfile
import argparse
from imagenetLabels import imagenet_original_labels
import argparse
import os
# import pickle
import tarfile

from imagenetLabels import imagenet_original_labels

BASE_DIR = os.environ.get('ImageNetDir')
imagenet_dir = BASE_DIR + './ILSVRC2012_img_train'
initial_dir = BASE_DIR + './ImageNetImagesUnsized'

def decodeDir(directory=imagenet_dir, target_dir=initial_dir):
    # labels = unpickle(imagenet_dir + '/batches.meta')
    
    tarballs = [x for x in os.listdir(directory)]
    x = 0
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for tarball_path in tarballs:
        file = '{}/{}'.format(directory, tarball_path)
        human_readable_label = imagenet_original_labels[tarball_path[:-4]]
        final_target = '{}/{}_{}'.format(target_dir, tarball_path[:-4], human_readable_label)
        if not os.path.exists(final_target):
            os.makedirs(final_target)
        with tarfile.open(file) as tarball:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tarball, final_target)
        print('Extract all the ' + human_readable_label + ' images to ' + final_target)
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decode pickled images.')
    parser.add_argument(   
        '-d',
        '--directory',
        help='Directory to decode',
        default=imagenet_dir
    )
    parser.add_argument(   
        '-t',
        '--target',
        help='Directory to decode',
        default=initial_dir
    )
    args = parser.parse_args()
    decodeDir(args.directory, args.target)