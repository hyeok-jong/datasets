import numpy as np
from PIL import Image
import os
import pickle
import wget
import tarfile

'''
source code from ...
https://mindw96.tistory.com/9
'''


wget.download('https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz', out = './cifar10.tar.gr')

file = tarfile.open('./cifar10.tar.gr')
file.extractall('./CIFAR10')
file.close()



def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

with open('./CIFAR10/cifar-10-batches-py/batches.meta', 'rb') as infile:
    data = pickle.load(infile, encoding='latin1')
    classes = data['label_names']

# 클래스 별 폴더 생성
os.mkdir('./CIFAR10/train')
os.mkdir('./CIFAR10/test')
for name in classes:
    os.mkdir('./CIFAR10/train/{}'.format(name))
    os.mkdir('./CIFAR10/test/{}'.format(name))
# Trainset Unpacking
# data_batch 파일들 순서대로 unpacking
print('')
for i in range(1, 6):
    print('Unpacking Train File {}/{}'.format(i, 5))
    train_file = unpickle('./CIFAR10/cifar-10-batches-py/data_batch_{}'.format(i))

    train_data = train_file[b'data']

    # 10000, 3072 -> 10000, 3, 32, 32 형태로 변환
    train_data_reshape = np.vstack(train_data).reshape((-1, 3, 32, 32))
    # 이미지 저장을 위해 10000, 32, 32, 3으로 변환
    train_data_reshape = train_data_reshape.swapaxes(1, 3)
    train_data_reshape = train_data_reshape.swapaxes(1, 2)
    # 레이블 리스트 생성
    train_labels = train_file[b'labels']
    # 파일 이름 리스트 생성
    train_filename = train_file[b'filenames']

    # 10000개의 파일을 순차적으로 저장
    for idx in range(10000):
        train_label = train_labels[idx]
        train_image = Image.fromarray(train_data_reshape[idx])
        # 클래스 별 폴더에 파일 저장
        train_image.save('./CIFAR10/train/{}/{}'.format(classes[train_label], train_filename[idx].decode('utf8')))
# -----------------------------------------------------------------------------------------
# Testset Unpacking
print('Unpacking Test File')
test_file = unpickle('./CIFAR10/cifar-10-batches-py/test_batch')

test_data = test_file[b'data']

# 10000, 3072 -> 10000, 3, 32, 32 형태로 변환
test_data_reshape = np.vstack(test_data).reshape((-1, 3, 32, 32))
# 이미지 저장을 위해 10000, 32, 32, 3으로 변환
test_data_reshape = test_data_reshape.swapaxes(1, 3)
test_data_reshape = test_data_reshape.swapaxes(1, 2)
# 레이블 리스트 생성
test_labels = test_file[b'labels']
# 파일 이름 리스트 생성
test_filename = test_file[b'filenames']

# 10000개의 파일을 순차적으로 저장
for idx in range(10000):
    test_label = test_labels[idx]
    test_image = Image.fromarray(test_data_reshape[idx])
    # 클래스 별 폴더에 파일 저장
    test_image.save('./CIFAR10/test/{}/{}'.format(classes[test_label], test_filename[idx].decode('utf8')))

print('Unpacking Finish')


os.remove('./cifar10.tar.gr')
import shutil

shutil.rmtree('./CIFAR10/cifar-10-batches-py')

print('remove finished')
