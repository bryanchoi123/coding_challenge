def mappings(fileName):
    # check to make sure we get a .csv file to process
    if fileName[-3:] != 'csv':
        raise NameError("File must be .csv file")

    mapping = {}
    mappingFile = open(fileName, "r")
    
    # skip first line of headers
    mappingFile.readline()

    # read through rest of file
    for line in mappingFile:
        parts = line.split(",")
        # check to see if measurement is there
        if len(parts) == 5:
            filePart = parts[2]
            measure = parts[4]
            # check to see if filename not already accounted for
            if filePart not in mapping and measure != "\n":
                mapping[filePart] = measure[:-1]

    # close file
    mappingFile.close()
    return mapping
