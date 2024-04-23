import os
import numpy as np
import scipy.io as sio
import shutil
from xml.etree import ElementTree as ET

# def parse_annotation(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
    
#     objects = []
#     for obj in root.findall('object'):
#         obj_info = {}
#         obj_info['name'] = obj.find('name').text
#         bbox = obj.find('bndbox')
#         obj_info['bbox'] = [
#             int(bbox.find('xmin').text),
#             int(bbox.find('ymin').text),
#             int(bbox.find('xmax').text),
#             int(bbox.find('ymax').text)
#         ]
#         objects.append(obj_info)
    
#     return objects

# def convert_to_mat(dataset_dir, output_mat_file):
#     annotations = []
#     if os.path.isfile(dataset_dir) and dataset_dir.endswith('.xml'):
#         annotations.extend(parse_annotation(dataset_dir))
#     else:
#         raise ValueError("Invalid dataset directory or file")

#     sio.savemat(output_mat_file, {'annotations': annotations})

# def convert_to_npy(dataset_dir, output_npy_file):
#     annotations = []
#     if os.path.isfile(dataset_dir) and dataset_dir.endswith('.xml'):
#         annotations.extend(parse_annotation(dataset_dir))
#     else:
#         raise ValueError("Invalid dataset directory or file")

#     np.save(output_npy_file, annotations)

# Ubah path dataset dan path output sesuai kebutuhan Anda
dataset_dir = 'oil-palm-trees.v14i.voc/train_data/labels'
output_mat_file = 'oil-palm-trees.v14i.voc/train_data/ground_truth'
output_npy_file = 'oil-palm-trees.v14i.voc/train_data/ground_truth'
labels_folder = 'oil-palm-trees.v14i.voc/train_data/labels'
images_dir = 'oil-palm-trees.v14i.voc/train_data/images'
xml_dir = 'oil-palm-trees.v14i.voc/train_data/labels'

# Pastikan output_folder_path ada atau buat jika belum ada
if not os.path.exists(output_mat_file):
    os.makedirs(output_mat_file)

if not os.path.exists(output_npy_file):
    os.makedirs(output_npy_file)

if not os.path.exists(labels_folder):
    os.makedirs(labels_folder)


# Daftar file dalam folder dataset
files = os.listdir(dataset_dir)
images_files = os.listdir(images_dir)
xml_files = os.listdir(xml_dir)

# rename image files using IMG_NUMBER.extension
# for i, file_name in enumerate(images_files):
#     if file_name.endswith('.jpg'):
#         new_file_name = f"IMG_{i+1}.jpg"
#         shutil.move(os.path.join(images_dir, file_name), os.path.join(images_dir, new_file_name))
#         print(f"File {file_name} berhasil direname menjadi {new_file_name}.")

# for i, file_name in enumerate(xml_files):
#     if file_name.endswith('.xml'):
#         new_file_name = f"IMG_{i+1}.xml"
#         shutil.move(os.path.join(xml_dir, file_name), os.path.join(xml_dir, new_file_name))
#         print(f"File {file_name} berhasil direname menjadi {new_file_name}.")

# Loop melalui setiap file dalam folder
# for file_name in files:
#     if file_name.endswith('.xml'):
#         # shutil.move(os.path.join(dataset_dir, file_name), os.path.join(labels_folder, file_name))
#         file_name_no_ext = file_name.split('.')[0]
#         mat_file_name = "GT_" + file_name_no_ext + '.mat'
#         npy_file_name = file_name_no_ext + "_densitymap" + '.npy'

#         convert_to_mat(os.path.join(dataset_dir, file_name), os.path.join(output_mat_file, mat_file_name))
#         convert_to_npy(os.path.join(dataset_dir, file_name), os.path.join(output_npy_file, npy_file_name))

#         # shutil.move(os.path.join(dataset_dir, file_name), os.path.join(labels_folder, file_name))


#         print(f"File {file_name} berhasil dikonversi dan disimpan sebagai {mat_file_name}.")
        
#         print(f"File {file_name} berhasil dikonversi dan disimpan sebagai {npy_file_name}.")

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    annotations = []
    for obj in root.findall('object'):
        label = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        annotations.append({'label': label, 'bbox': [xmin, ymin, xmax, ymax]})

    return annotations


def convert_to_mat(annotations, mat_file):
    sio.savemat(mat_file, {'annotations': annotations})

def convert_to_npy(annotations, npy_file):
    np.save(npy_file, annotations)


# Pastikan folder output sudah ada atau buat jika belum ada

# Loop melalui setiap file XML dalam folder
for xml_file in os.listdir(dataset_dir):
    if xml_file.endswith('.xml'):
        file_name = os.path.splitext(xml_file)[0]
        annotations = parse_xml(os.path.join(dataset_dir, xml_file))
        
        mat_file = os.path.join(output_mat_file, "GT_" + file_name + '.mat')
        npy_file = os.path.join(output_npy_file, file_name + "_densitymap" + '.npy')
        
        convert_to_mat(annotations, mat_file)
        convert_to_npy(annotations, npy_file)

        print(f"File {xml_file} berhasil dikonversi dan disimpan sebagai {file_name}.mat dan {file_name}.npy")

print("Konversi selesai untuk semua file-label dalam folder dataset.")