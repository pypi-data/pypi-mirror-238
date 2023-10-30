# Copyright 2022 Dechin Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from collections import namedtuple
from .constants import resdict, atom_types


atom_order = {atom_type: i for i, atom_type in enumerate(atom_types)}
atom_type_num = len(atom_types)  # := 37.


def read_pdb(pdb_name, ignoreh=False, prefix=None):
    """Read a pdb file and return atom information with numpy array format.
    Args:
        pdb_name(str): The pdb file name, absolute path is suggested.
        ignoreh(bool): Decide to load hydrogen atoms from pdb or not.
        prefix(str): If multi results exists in a residue, we need to choose one via given prefix.
    Returns:
        atom_names(list): 1-dimension list contain all atom names in each residue.
        res_names(list): 1-dimension list of all residue names.
        res_ids(numpy.int32): Unique id for each residue names.
        crds(list): The list format of coordinates.
        res_pointer(numpy.int32): The pointer where the residue starts.
        flatten_atoms(numpy.str_): The flatten atom names.
        flatten_crds(numpy.float32): The numpy array format of coordinates.
        init_res_names(list): The residue name information of each atom.
        init_res_ids(list): The residue id of each atom.
    """
    pdb_obj = namedtuple('PDBObject', ['atom_names', 'res_names', 'res_ids', 'crds', 'res_pointer',
                         'flatten_atoms', 'flatten_crds', 'init_res_names', 'init_res_ids', 'residue_index', 'aatype',
                                       'chain_id'])

    with open(pdb_name, 'r') as pdb:
        lines = pdb.readlines()
    atom_names = []
    atom_group = []
    res_names = []
    res_ids = []
    init_res_names = []
    init_res_ids = []
    crds = []
    crd_group = []
    res_pointer = []
    flatten_atoms = []
    flatten_crds = []
    chain_id = []
    c_id = 0
    for index, line in enumerate(lines):
        if line.startswith('END'):
            atom_names.append(atom_group)
            crds.append(crd_group)
            atom_group = None
            crd_group = None
            break
        if line.startswith('TER'):
            c_id += 1
            continue
        if not (line.startswith('ATOM') or line.startswith('HETATM')):
            continue

        atom_name = line[12:16].strip()
        if ignoreh and atom_name.startswith('H'):
            continue
        res_name = line[16:20].strip()
        res_id = int(line[22:26].strip())
        crd = [float(line[30:38]),
               float(line[38:46]),
               float(line[46:54])]
        pointer = int(line[6:11].strip()) - 1

        if prefix is not None:
            if len(res_name) == 4 and not res_name.startswith(prefix):
                continue
            elif len(res_name) == 4:
                res_name = res_name[1:]

        flatten_atoms.append(atom_name)
        flatten_crds.append(crd)
        init_res_names.append(res_name)
        init_res_ids.append(res_id)
        if not res_ids:
            res_ids.append(res_id)
            res_names.append(res_name)
            atom_group.append(atom_name)
            crd_group.append(crd)
            res_pointer.append(0)
            chain_id.append(c_id)
        elif res_id != res_ids[-1]:
            atom_names.append(atom_group)
            crds.append(crd_group)
            atom_group = []
            crd_group = []
            res_ids.append(res_id)
            res_names.append(res_name)
            atom_group.append(atom_name)
            crd_group.append(crd)
            res_pointer.append(pointer)
            chain_id.append(c_id)
        else:
            atom_group.append(atom_name)
            crd_group.append(crd)

    if atom_group is not None:
        atom_names.append(atom_group)
    if crd_group is not None:
        crds.append(crd_group)

    res_ids = np.array(res_ids, np.int32)
    crds = crds
    flatten_atoms = np.array(flatten_atoms, np.str_)
    flatten_crds = np.array(flatten_crds, np.float32)
    init_res_names = np.array(init_res_names)
    init_res_ids = np.array(init_res_ids, np.int32)
    res_pointer = np.array(res_pointer, np.int32)
    # Violation loss parameters
    residue_index = np.arange(res_pointer.shape[0])
    aatype = np.zeros_like(residue_index)
    for i in range(res_pointer.shape[0]):
        if res_names[i] == 'HIP':
            aatype[i] = resdict['HIS']
        elif res_names[i] == 'GLH':
            aatype[i] = resdict['GLY']
        elif res_names[i] == 'ASH':
            aatype[i] = resdict['ASP']
        else:
            aatype[i] = resdict[res_names[i]]

    return pdb_obj(atom_names, res_names, res_ids, crds, res_pointer, flatten_atoms, flatten_crds, init_res_names,
                   init_res_ids, residue_index, aatype, chain_id)


def gen_pdb(crd, atom_names, res_names, res_ids, chain_id=None, pdb_name='temp.pdb', sequence_info=True):
    """Write protein crd information into pdb format files.
    Args:
        crd(numpy.float32): The coordinates of protein atoms.
        atom_names(numpy.str_): The atom names differ from aminos.
        res_names(numpy.str_): The residue names of amino names.
        res_ids(numpy.int32): A unique mask each same residue.
        pdb_name(str): The path to save the pdb file, absolute path is suggested.
        chain_id(numpy.int32): The chain index of each residue.
    """
    success = 1
    res_ids = np.array(res_ids, np.int32)
    chain_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    record_resids = res_ids.copy()
    with open(pdb_name, 'w') as pdb:
        pdb.write('MODEL     1\n')

        # Write sequence information
        if sequence_info and chain_id is not None:
            chain_id = np.array(chain_id, np.int32)
            seq_label = 0
            start_label = 0
            for i, res in enumerate(res_names):
                if i > 0 and res_ids[i] == res_ids[i - 1]:
                    continue
                cri = res_ids[i] - 1
                if i == 0:
                    seq_label += 1
                    pdb.write('SEQRES'.ljust(6))
                    pdb.write('{}'.format(seq_label).rjust(4))
                    pdb.write('{}'.format(chain_labels[chain_id[cri]]).rjust(2))
                    pdb.write('{}'.format((chain_id == chain_id[cri]).sum()).rjust(5))
                    pdb.write(res[-3:].rjust(5))
                elif (cri - start_label) % 13 == 0 and chain_id[cri] == chain_id[cri - 1]:
                    seq_label += 1
                    pdb.write('\n')
                    pdb.write('SEQRES'.ljust(6))
                    pdb.write('{}'.format(seq_label).rjust(4))
                    pdb.write('{}'.format(chain_labels[chain_id[cri]]).rjust(2))
                    pdb.write('{}'.format((chain_id == chain_id[cri]).sum()).rjust(5))
                    pdb.write(res[-3:].rjust(5))
                elif chain_id[cri] != chain_id[cri - 1]:
                    pdb.write('\n')
                    seq_label = 1
                    start_label = cri
                    pdb.write('SEQRES'.ljust(6))
                    pdb.write('{}'.format(seq_label).rjust(4))
                    pdb.write('{}'.format(chain_labels[chain_id[cri]]).rjust(2))
                    pdb.write('{}'.format((chain_id == chain_id[cri]).sum()).rjust(5))
                    pdb.write(res[-3:].rjust(5))
                elif (cri - start_label) % 13 != 0 and chain_id[cri] == chain_id[cri - 1]:
                    pdb.write(res[-3:].rjust(4))
            pdb.write('\n')

        # Write atom information
        for i, c in enumerate(crd):
            if chain_id is not None and i > 0:
                if chain_id[res_ids[i] - 1] > chain_id[res_ids[i - 1] - 1]:
                    pdb.write('TER\n')
                    record_resids -= record_resids[i] - 1
            pdb.write('ATOM'.ljust(6))
            pdb.write('{}'.format((i + 1) % 100000).rjust(5))
            if len(atom_names[i]) < 4:
                pdb.write('  ')
                pdb.write(atom_names[i].ljust(3))
            else:
                pdb.write(' ')
                pdb.write(atom_names[i].ljust(4))
            pdb.write(res_names[i][-3:].rjust(4))
            if chain_id is None:
                pdb.write('A'.rjust(2))
            else:
                pdb.write('{}'.format(chain_labels[chain_id[res_ids[i] - 1]]).rjust(2))
            pdb.write('{}'.format(record_resids[i] % 10000).rjust(4))
            pdb.write('    ')
            pdb.write('{:.3f}'.format(c[0]).rjust(8))
            pdb.write('{:.3f}'.format(c[1]).rjust(8))
            pdb.write('{:.3f}'.format(c[2]).rjust(8))
            pdb.write('1.0'.rjust(6))
            pdb.write('0.0'.rjust(6))
            pdb.write('{}'.format(atom_names[i][0]).rjust(12))
            pdb.write('\n')
        pdb.write('TER\n')
        pdb.write('ENDMDL\n')
        pdb.write('END\n')
    return success
