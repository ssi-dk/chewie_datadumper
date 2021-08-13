def tsv_reader(file_name):
    """Get lines from text file one by one using a generator object
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row


def write_allele_profiles_to_mongo(file):
    line_count = 0
    for line in tsv_reader(file):
        if line_count > 0:  # First line is header
            print(f"Saving allele profile #{line_count} to MongoDB...")
            print(line)
        line_count += 1