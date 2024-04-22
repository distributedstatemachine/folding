from tqdm import tqdm
import pickle as pkl
import argparse
from typing import Dict, List
import concurrent.futures
from folding.utils.ops import download_pdb

COMPLETE_IDs_FILE = "./pdb_ids_complete.pkl"
INCOMPLETE_IDs_FILE = "./pdb_ids_incomplete.pkl"
NOT_DOWNLOADABLE_IDs_FILE = "./pdb_ids_not_downloadable.pkl"

COMPLETE_PDB_FILES = "./complete_pdbs/"


def save_pkl(file, data):
    with open(file, "wb") as f:
        pkl.dump(data, f)


def verbose_analysis(complete, incomplete, not_downloadable, number_of_pdb_ids):
    """
    Perform a verbose analysis of the given PDB data.

    Args:
        complete (dict): A dictionary containing complete PDB data.
        incomplete (dict): A dictionary containing incomplete PDB data.
        not_downloadable (dict): A dictionary containing not downloadable PDB data.
        number_of_pdb_ids (int): The total number of PDB IDs.

    Returns:
        None

    Prints the analysis summary, including the total number of PDB IDs, the number of complete,
    incomplete, and not downloadable PDBs, and their respective percentages.
    """
    total_complete = sum([len(v) for v in complete.values()])
    total_incomplete = sum([len(v) for v in incomplete.values()])
    total_not_downloadable = sum([len(v) for v in not_downloadable.values()])
    complete_percentage = total_complete / number_of_pdb_ids * 100
    incomplete_percentage = total_incomplete / number_of_pdb_ids * 100
    not_downloadable_percentage = total_not_downloadable / number_of_pdb_ids * 100

    print("=====================================")
    print("Analysis Summary:")
    print(f"Total number of PDB IDs: {number_of_pdb_ids}")
    print(f"Complete: {total_complete} ({complete_percentage:.2f}%)")
    print(f"Incomplete: {total_incomplete} ({incomplete_percentage:.2f}%)")
    print(
        f"Not Downloadable: {total_not_downloadable} ({not_downloadable_percentage:.2f}%)"
    )
    print("=====================================")


def classify_pdb_batch(data, verbose=False):
    """Downloads PDB files from a batch of PDB IDs and classifies them into complete, incomplete, and not downloadable dictionaries. Saves the results to pickle files.

    Args:
        data (defaultdict[List]): A batch of PDB IDs, as returned by scripts/gather_pdbs.py.
        verbose (bool, optional): If True, print the time required by the analysis and the percentages + frequencies of each dictionary. Defaults to False.

    Returns:
        None
    """
    number_of_pdb_ids = sum([len(v) for v in data.values()])

    complete = {k: [] for k in data.keys()}
    incomplete = {k: [] for k in data.keys()}
    not_downloadable = {k: [] for k in data.keys()}
    count = 0

    for k, v in tqdm(data.items()):

        for pdb_id in v:
            count += 1
            try:
                result = download_pdb(COMPLETE_PDB_FILES, pdb_id + ".pdb")
                if result:  # PDB was correctly downloaded and is complete
                    complete[k].append(pdb_id)
                else:  # PDB was correctly downloaded but is incomplete
                    incomplete[k].append(pdb_id)
            except Exception:  # Unable to download PDB
                not_downloadable[k].append(pdb_id)
                continue

            if count % 10 == 0:  # Saving progress for safety
                save_pkl(file=COMPLETE_IDs_FILE, data=complete)
                save_pkl(file=INCOMPLETE_IDs_FILE, data=incomplete)
                save_pkl(file=NOT_DOWNLOADABLE_IDs_FILE, data=not_downloadable)

    # Filtering out empty lists
    complete = {k: v for k, v in complete.items() if v}
    incomplete = {k: v for k, v in incomplete.items() if v}
    not_downloadable = {k: v for k, v in not_downloadable.items() if v}

    # Once the entire process is finished, we save all the data.
    save_pkl(file=COMPLETE_IDs_FILE, data=complete)
    save_pkl(file=INCOMPLETE_IDs_FILE, data=incomplete)
    save_pkl(file=NOT_DOWNLOADABLE_IDs_FILE, data=not_downloadable)

    if verbose:
        verbose_analysis(complete, incomplete, not_downloadable, number_of_pdb_ids)
    print(
        f"Analysis done!\nPDB ID files saved at {COMPLETE_IDs_FILE}, {INCOMPLETE_IDs_FILE}, and {NOT_DOWNLOADABLE_IDs_FILE}\nPDB files saved at {COMPLETE_PDB_FILES}"
    )
    print("=====================================")


def parallel_classify_pdb_batch(data, verbose=False):
    """
    Classifies PDB IDs in parallel and saves the results to pickle files.

    Args:
        data (dict): A dictionary containing PDB IDs to be classified into complete, incomplete and not_downloadable.
        verbose (bool, optional): If True, prints an analysis summary. Defaults to False.

    Returns:
        None

    Raises:
        None

    Example:
        data = {
            'group1': ['pdb1', 'pdb2', 'pdb3'],
            'group2': ['pdb4', 'pdb5']
        }
        parallel_classify_pdb_batch(data, verbose=True)

    """
    number_of_pdb_ids = sum([len(v) for v in data.values()])
    complete = {k: [] for k in data.keys()}
    incomplete = {k: [] for k in data.keys()}
    not_downloadable = {k: [] for k in data.keys()}

    def process_pdb(pdb_id, k):
        nonlocal complete, incomplete, not_downloadable
        try:
            result = download_pdb(COMPLETE_PDB_FILES, pdb_id + ".pdb")
            if result:
                complete[k].append(pdb_id)
            else:
                incomplete[k].append(pdb_id)
        except Exception:
            not_downloadable[k].append(pdb_id)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_pdb, pdb_id, k)
            for k, v in data.items()
            for pdb_id in v
        ]
        concurrent.futures.wait(futures)

    # Filtering out empty lists
    complete = {k: v for k, v in complete.items() if v}
    incomplete = {k: v for k, v in incomplete.items() if v}
    not_downloadable = {k: v for k, v in not_downloadable.items() if v}

    save_pkl(file=COMPLETE_IDs_FILE, data=complete)
    save_pkl(file=INCOMPLETE_IDs_FILE, data=incomplete)
    save_pkl(file=NOT_DOWNLOADABLE_IDs_FILE, data=not_downloadable)

    if verbose:
        verbose_analysis(complete, incomplete, not_downloadable, number_of_pdb_ids)

    print(
        f"Analysis done!\nPDB ID files saved at {COMPLETE_IDs_FILE}, {INCOMPLETE_IDs_FILE}, and {NOT_DOWNLOADABLE_IDs_FILE}\nPDB files saved at {COMPLETE_PDB_FILES}"
    )
    print("=====================================")


def main(
    classification_type: str = "parallel",
    verbose=False,
    pdb_id_path: str = "pdb_ids.pkl",
):
    # Load the PDB IDs
    with open(pdb_id_path, "rb") as f:
        PDB_IDS = pkl.load(f)

    if classification_type == "parallel":
        parallel_classify_pdb_batch(PDB_IDS, verbose=verbose)
    else:
        classify_pdb_batch(PDB_IDS, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--classification_type",
        type=str,
        default="parallel",
        help="Type of classification (parallel or sequential)",
    )
    parser.add_argument(
        "--pdb_id_path",
        type=str,
        default="pdb_ids.pkl",
        help="Path to the PDB ID file",
    )
    parser.add_argument("--verbose", action="store_true", help="Print analysis summary")
    args = parser.parse_args()

    main(
        classification_type=args.classification_type,
        verbose=args.verbose,
        pdb_id_path=args.pdb_id_path,
    )
