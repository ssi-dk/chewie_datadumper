def line_reader(file_name):
    """Get lines from text file one by one using a generator object
    """
    with open(file_name, 'r') as file_handler:
        for row in file_handler:
            yield row


def write_allele_profiles_to_mongo(file):
    allele_profile_reader = line_reader(file)
    next(allele_profile_reader)  # Skip header line
    for line in allele_profile_reader:
        allele_profile = line.split('\t')
        sample_name = allele_profile.pop(0)
        print("Sample name: ", sample_name)
        print("Length of allele profile:", len(allele_profile))
        print(type(allele_profile[0]))