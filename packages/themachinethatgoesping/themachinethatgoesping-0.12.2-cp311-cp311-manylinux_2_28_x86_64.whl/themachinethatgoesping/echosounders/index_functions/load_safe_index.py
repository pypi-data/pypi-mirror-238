# This file is authored by Peter Urban, Ghent University, and is subject to the MPL-2.0 license.
# SPDX-License-Identifier: MPL-2.0

import os
from pathlib import Path
import pickle
from collections import defaultdict
from typing import List, Dict, Union


def get_index_file_name(
    folder_path: Union[str, Path], 
    index_root: Union[str, Path, None] = None, 
    index_name: str = 'tmtgp.index', 
    create_dir: bool = True) -> Path:
    """Return the path to the index file for a given folder path

    Parameters
    ----------
    folder_path : str or Path
        The path to the folder containing files that are indexed
    index_root : str or Path, optional
        The path to the root folder containing all index files. If None, the index file will be in the same folder as the data files
    index_name : str, optional
        The name of the index file
    create_dir : bool, optional
        If true: create a subdirectory, by default True

    Returns
    -------
    Path
        The path to the index file
    """
    
    if index_root is None:
        return Path(folder_path) / Path(index_name)
            
    index_file = Path(os.path.abspath(index_root))
    folder_path = Path(os.path.abspath(folder_path))
    root_path = 'root_' + folder_path.parts[0]
    root_path = root_path.replace(':', '')

    index_file = index_file.joinpath(root_path, *folder_path.parts[1:], index_name)
    
    if create_dir:
        os.makedirs(index_file.parent, exist_ok=True)
    
    return index_file


def load_index_files(
    file_paths: List[str], force_new: bool = False, index_name: str = 'tmtgp.index', index_root: str = 'index', update_index: Dict[str, str] = None, verbose: bool = False, create_dir: bool = True) -> Dict[str, str]:
    """Load index files for a given list of file paths

    Parameters
    ----------
    file_paths : list of str
        The list of file paths to load index files for
    force_new : bool, optional
        If true: force the creation of new index files, by default False
    index_name : str, optional
        The name of the index file, by default 'tmtgp.index'
    index_root : str, optional
        The path to the root folder containing all index files, by default 'index'
    update_index : dict, optional
        A dictionary to update with the loaded index data, by default None
    verbose : bool, optional
        If true: print verbose output, by default False
    create_dir : bool, optional
        If true: create a subdirectory, by default True

    Returns
    -------
    dict
        A dictionary containing the loaded index data
    """
    
    if update_index is None:
        index = {}
    else:
        index = update_index
        
    loaded_index_files = set()
    
    # look for existing files in each folder
    for fp in file_paths:
        try:
            folder_path, file = os.path.split(fp)
            
            index_file = get_index_file_name(folder_path, index_root, index_name, create_dir=create_dir)            
            
            if index_file in loaded_index_files:
                continue
                
            loaded_index_files.add(index_file)
            
            if os.path.exists(index_file) and not force_new:
                if verbose:
                    print('Open:', index_file)
                load_index = pickle.load(open(index_file, 'rb'))
                index.update(load_index)
        except:
            pass
            
    return index


def update_index_files(cached_index_dict: Dict[str, str], force_new: bool = False, index_name: str = 'tmtgp.index', index_root: str = 'index', verbose: bool = False, create_dir: bool = True) -> None:
    """Update index files with a given dictionary of index data

    Parameters
    ----------
    cached_index_dict : dict
        A dictionary containing the index data to update the index files withu
    force_new : bool, optional
        If true: force the creation of new index files, by default False
    index_name : str, optional
        The name of the index file, by default 'tmtgp.index'
    index_root : str, optional
        The path to the root folder containing all index files, by default 'index'
    verbose : bool, optional
        If true: print verbose output, by default False
    create_dir : bool, optional
        If true: create a subdirectory, by default True
    """
    
    # group index dict into per folder index files
    index_per_folder = defaultdict(dict)
    for k, v in cached_index_dict.items():
        folder_path, file = os.path.split(k)        
        index_file = get_index_file_name(folder_path, index_root, index_name, create_dir=create_dir)    
        index_per_folder[index_file].update({k: v})
        
    # write an index file into each folder
    for index_file, index in index_per_folder.items():
        if verbose:
            print(index_file)
        
        if not os.path.exists(index_file) or force_new:
            write_index = {}
        else:
            try:
                write_index = pickle.load(open(index_file, 'rb'))
            except:
                write_index = {}
            
        write_index.update(index)
        pickle.dump(write_index, open(index_file, 'wb'))