import re


class DATAttributes(object):
    # Container of attributes. Attributes are dynamically created.
    pass


class DATParser(object):
    @staticmethod
    def _tryParse(x):
        """
        Attempts to parse a value as int, float, or bool. Defaults to string if parsing fails.
        """
        try:
            return int(x)
        except ValueError:
            pass

        try:
            return float(x)
        except ValueError:
            pass

        if x in ['True', 'true', 'TRUE', 'T', 't']:
            return True
        if x in ['False', 'false', 'FALSE', 'F', 'f']:
            return False

        return x  # Return as string if all parsing fails.

    @staticmethod
    def parse(filePath):
        """
        Parses a .dat file to extract scalar, 1D, and 2D attributes.
        :param filePath: Path to the .dat file.
        :return: An object of DATAttributes containing parsed attributes.
        """
        datAttr = DATAttributes()

        with open(filePath, 'r') as file:
            fileContent = file.read()

        # Parse scalar attributes
        scalar_pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*=[\s]*([\w\/\.\-]+)[\s]*;', re.M)
        scalar_entries = scalar_pattern.findall(fileContent)
        for key, value in scalar_entries:
            setattr(datAttr, key, DATParser._tryParse(value))

        # Parse 1-dimensional vector attributes
        vector_pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*=[\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*;', re.M)
        vector_entries = vector_pattern.findall(fileContent)
        for key, value, _ in vector_entries:
            elements = re.findall(r'[\w\/\.\-]+', value)
            setattr(datAttr, key, list(map(DATParser._tryParse, elements)))

        # Parse 2-dimensional vector attributes
        matrix_pattern = re.compile(r'^[\s]*([a-zA-Z][\w]*)[\s]*=[\s]*\[(([\s]*\[[\s]*(([\w\/\.\-]+[\s]*)+)\][\s]*)+)\][\s]*;', re.M)
        matrix_entries = matrix_pattern.findall(fileContent)
        for key, value, *_ in matrix_entries:
            rows = re.findall(r'\[[\s]*(([\w\/\.\-]+[\s]*)+)\]', value)
            matrix = []
            for row, _ in rows:
                elements = re.findall(r'[\w\/\.\-]+', row)
                matrix.append(list(map(DATParser._tryParse, elements)))
            setattr(datAttr, key, matrix)

        return datAttr
