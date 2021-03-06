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

def get_allele_profiles(folder: pathlib.Path, species_name: str):
    # Open relevant data files
    hashids_file = pathlib.Path(folder, 'cgmlst', 'hashids.tsv')
    assert hashids_file.exists()
    allele_profiles_file = pathlib.Path(folder, 'cgmlst', 'allele_profiles.tsv')
    assert allele_profiles_file.exists()

    # We need to be able to exchange a sample name into a hash id.
    hashids_reader = line_reader(hashids_file)
    next(hashids_reader)  # Skip header line
    hashids_lookup_dict = dict()
    for line in hashids_reader:
        elements = line_splitter(line, '\t')
        sample_name = next(elements)
        hash_id = next(elements)
        hashids_lookup_dict[sample_name] = hash_id
        # Todo: we should also save hash_id on the sample in MongoDB.

    # Get the list of new hash ids
    # (todo: merge with the list of already known hash ids.)
    allele_profile_reader = line_reader(allele_profiles_file)
    next(allele_profile_reader)  # Skip header line
    for line in allele_profile_reader:
        elements = line_splitter(line, '\t')
        sample_name = next(elements)
        print("Sample name: ", sample_name)
        hash_id = hashids_lookup_dict[sample_name]
        key = f"allele_profile_{species_name}:{hash_id}"
        print("Key:", key)
        if r.exists(key):
            print(f"Duplicate allele profile found: sample {sample_name} has "
                f"allele profile {hash_id} which is already known.")
        else:
            for allele_hash in elements:
                r.rpush(key, allele_hash)

def update_distance_matrix(folder: pathlib.Path, species_name: str, sample_names: list):
    print("We already know that the distance matrix should contain these sample names:")
    print(sample_names)
    distance_matrix_file = pathlib.Path(folder, 'cgmlst', 'distance_matrix.tsv')
    # Note: the distance_matrix.tsv file from chewieSnake uses space as separator.
    distance_matrix_reader = line_reader(distance_matrix_file)
    for line in distance_matrix_reader:
        elements_gen = line_splitter(line, ' ')
        sample_name = next(elements_gen)
        print("Sample name:", sample_name)
        key = species_name + ':' + sample_name
        print("Key:", key)
        # Make a Redis 'sorted set' entry with distances as scores and sample names as values
        # Todo: check for existing key.
        r.zadd(key, {sample_name: next(elements_gen) for sample_name in sample_names})