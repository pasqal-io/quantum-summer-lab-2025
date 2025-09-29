import rdkit.Chem as Chem
from typing import Final
import numpy as np 
import networkx as nx 
from torch_geometric.utils import to_networkx
MAPPING_NODES_DATASET: Final[dict[str, dict[int, str]]] = {
    "PTC_FM": {
        0: "In",
        1: "P",
        2: "C",
        3: "O",
        4: "N",
        5: "Cl",
        6: "S",
        7: "Br",
        8: "Na",
        9: "F",
        10: "As",
        11: "K",
        12: "Cu",
        13: "I",
        14: "Ba",
        15: "Sn",
        16: "Pb",
        17: "Ca",
    }
}

MAPPING_EDGES_DATASET: Final[dict[str, dict[int, Chem.BondType]]] = {   
    "PTC_FM": {
        0: Chem.BondType.TRIPLE,
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.AROMATIC,

}
}

class MolecularMapping:
    """Helper class to centralise mapping informations."""

    def __init__(self):
        try:
            self.node_mapping = MAPPING_NODES_DATASET["PTC_FM"]
            self.edge_mapping = MAPPING_EDGES_DATASET["PTC_FM"]
            self.is_one_hot = True
        except KeyError as key_error:
            raise KeyError(f"Dataset name '{"PTC_FM"}' not found in mappings: {key_error}")
        
def inverse_one_hot(array: np.typing.ArrayLike, dim: int) -> np.ndarray:
    """Inverts a one-hot encoded tensor along a specified dimension and returns the
    indices where the value is 1.

    Parameters:
    - array (np.ndarray): The one-hot encoded array.
    - dim (int): The dimension along which to find the indices.

    Returns:
    - np.ndarray: The array of indices where the value is 1.
    """
    tmp_array = np.asarray(array)
    return np.nonzero(tmp_array == 1.0)[dim]


def graph_to_mol(graph: nx.Graph) -> Chem.Mol:
    """Reconstruct an rdkit mol object using a graph.

    Args:
        graph (nx.Graph): Networkx graph of a molecule.
        mapping (MolMapping): Object containing dicts for edges and nodes attributes.

    Returns:
        Chem.Mol: The generated rdkit molecule.
    """
    m = Chem.MolFromSmiles("")
    mw = Chem.RWMol(m)
    atom_index = {}
    mapping = MolecularMapping()
    for n, d in graph.nodes(data="x"):
        d = np.asarray(d)
        if mapping.is_one_hot:
            idx_d = inverse_one_hot(d, dim=0)[0]
        else:
            idx_d = d[0]
        atom_index[n] = mw.AddAtom(Chem.Atom(mapping.node_mapping[idx_d]))
    for a, b, d in graph.edges(data="edge_attr"):
        start = atom_index[a]
        end = atom_index[b]
        if not isinstance(d, int):
            d = np.asarray(d)
            if mapping.is_one_hot:
                idx_d = inverse_one_hot(d, dim=0)[0]
            else:
                idx_d = d[0]
        else:
            idx_d = d
        bond_type = mapping.edge_mapping.get(idx_d)
        if bond_type is None:
            raise ValueError("bond type not implemented")
        mw.AddBond(start, end, bond_type)
        # more options:
        # http://www.rdkit.org/Python_Docs/rdkit.Chem.rdchem.BondType-class.html
    return mw.GetMol()

def matching_regs(processed_dataset : list , compiled : list ) -> dict:
    """Generate for each index in the prossessed dataset a list of 
    matching ids (relatively to the input dataset) with the same register

    Args:
        processed_dataset (list): the processed dataset (after size filtration)
        compiled (list): the compiled dataset (after embedding filtration)

    Returns:
        dict: a dict with idx in the processed dataset as key, and idx in the input dataset as value
    """
    compiled_coord = dict()
    for i in range(len(compiled)):
        coords = np.array(compiled[i].sequence._register._coords)
        diff = coords[:, None, :] - coords[None, :, :]
        dist_mat = np.linalg.norm(diff, axis=-1)
        compiled_coord[i] = set(dist_mat.ravel().tolist())

    processed_coords = dict()
    for i,data_pt in enumerate(processed_dataset):
        coords = np.array(data_pt._sequence._register._coords)
        diff = coords[:, None, :] - coords[None, :, :]
        dist_mat = np.linalg.norm(diff, axis=-1)
        processed_coords[i] = set(dist_mat.ravel().tolist())
    correspondence = { i : [compiled[j].graph.id  for j in compiled_coord if compiled_coord[j] == processed_coords[i] ] for i in processed_coords}
    return correspondence