import pathlib

import redis


r = redis.Redis(charset="utf-8", decode_responses=True)

def line_reader(file_name):
    """Get lines from text file one by one using a generator object
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row

def line_splitter(line: str, splitter: str):
    return (value for value in line.rstrip().split(splitter))

def get_allele_profiles(folder: pathlib.Path):
    # Open relevant data files
    allele_profiles_file = pathlib.Path(folder, 'cgmlst', 'allele_profiles.tsv')
    assert allele_profiles_file.exists()
    hashids_file = pathlib.Path(folder, 'cgmlst', 'hashids.tsv')
    assert hashids_file.exists()


    # Get the list of new hash ids
    # (todo: merge with the list of already known hash ids.)


    allele_profile_reader = line_reader(allele_profiles_file)
    next(allele_profile_reader)  # Skip header line
    for line in allele_profile_reader:
        elements = line_splitter(line, '\t')
        sample_name = next(elements)
        print("Sample name: ", sample_name)
        # We need to exchange the sample name with a hash id.

        for string in elements:
            try:
                allele_hash = int(string)
            except ValueError:
                allele_hash = None

def update_distance_matrix(folder: pathlib.Path, species: str):
    distance_matrix_file = pathlib.Path(folder, 'cgmlst', 'distance_matrix.tsv')
    # Note: the distance_matrix.tsv file from chewieSnake uses space as separator.
    distance_matrix_reader = line_reader(distance_matrix_file)
    for line in distance_matrix_reader:
        elements_gen = line_splitter(line, ' ')
        print("Elements in line:")
        print(list(elements_gen))