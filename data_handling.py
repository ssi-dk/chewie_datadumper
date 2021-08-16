def line_reader(file_name):
    """Get lines from text file one by one using a generator object
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row

def line_splitter(line: str):
    return (value for value in line.split('\t'))

def get_allele_profiles(file):
    allele_profile_reader = line_reader(file)
    next(allele_profile_reader)  # Skip header line
    for line in allele_profile_reader:
        elements = line_splitter(line)
        sample_name = next(elements)
        print("Sample name: ", sample_name)
        allele_profile = list()
        for string in elements:
            try:
                allele_hash = int(string)
            except ValueError:
                allele_hash = None
            allele_profile.append(allele_hash)
        print(allele_profile)