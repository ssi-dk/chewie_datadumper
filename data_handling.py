import pathlib
import redis


r = redis.Redis(charset="utf-8", decode_responses=True)

def line_reader(file_name):
    """Get lines from text file one by one using a generator object
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row

def line_splitter(line: str):
    return (value for value in line.split('\t'))

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
        elements = line_splitter(line)
        sample_name = next(elements)
        print("Sample name: ", sample_name)
        # We need to exchange the sample name with a hash id.

        for string in elements:
            try:
                allele_hash = int(string)
            except ValueError:
                allele_hash = None