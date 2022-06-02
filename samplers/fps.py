'''
Python code to sample a .ply point cloud file using farthest point sampling
3 arguments can be provided 
 --src_file : path to the file 
 --src_folder: path to the folder
 --dst_folder: path to destination folder
'''
import torch
from torch_geometric.nn.pool import fps
import argparse
import os
import glob
import open3d as o3d
import numpy as np

def load_files(path,folder = False):
    if not folder:
        return [path]
    else:
        paths = [x for x in glob.glob(os.path.join(path,'*.ply'))]
        return paths

    
def fps_sampler(pc):
    sampled = fps(pc, random_start= True)
    return pc[sampled].numpy()

def sampler(args):
    if args.src_folder is None:
        file_list = load_files(args.src_file)
    else:
        file_list = load_files(args.src_folder, folder= True)
        print(file_list)
    if file_list == []:
        print('no .ply files in directory')
        exit(1)
    for path in file_list:
        print('sampling : ',path)
        folders = path.split('/')
        # print(file_n)
        file_n,_ = folders[-1].split('.')
        # print(file_n,ext)
        pc = o3d.io.read_point_cloud(path)
        # print(np.array(pc.points,np.float32))
        sampled = fps_sampler(torch.from_numpy(np.array(pc.points, np.float32)))
        try:
            with open(os.path.join(args.dst_folder,'sampled',folders[-2] if len(folders)>2 else '', file_n+'.npy'),'wb') as f:
                np.save(f,sampled)
        except:
            try:
                os.makedirs(os.path.join(args.dst_folder,'sampled',folders[-2] if len(folders)>2 else ''))
                print('creating new directory: %s',os.path.join(args.dst_folder,'sampled',folders[-2] if len(folders)>2 else ''))
                print('directory created.')
                with open(os.path.join(args.dst_folder,'sampled',folders[-2] if len(folders)>2 else '', file_n+'.npy'),'wb') as f:
                    np.save(f,sampled)
            except FileExistsError:
                print('file exitst')
                exit(1)
            except FileNotFoundError:
                print('file not found. Check the path')
                exit(1)

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_folder', type=str, default=None, help='Path to source folder')
    parser.add_argument('--src_file', type=str, default= None, help= 'Path to source file')
    parser.add_argument('--dst_folder', type=str, default= os.getcwd(), help='Path to destination folder')
    args = parser.parse_args()
    sampler(args)
