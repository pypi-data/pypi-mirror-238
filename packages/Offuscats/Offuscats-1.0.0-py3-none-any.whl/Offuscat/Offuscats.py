try:
    import os, base64
except ImportError as e:
    error = str(e).split(" ")[-1][1:-1]
    os.system("pip install {}".format(error))
pass


class Offuscats:
    """
    A class for obfuscating and decoding Python code using base64 encoding and character replacement.

    ...

    Attributes
    ----------
    code : str
        The Python code to be obfuscated or decoded.

    Methods
    -------
    _obfuscate():
        Obfuscates the code using base64 encoding.
    _make_ilisible():
        Replaces each character in the obfuscated code with a string of special characters.
    _decode():
        Decodes the obfuscated code using base64 decoding and executes it.
    """
    def __init__(self, script=None, file=None):
        """
        Parameters
        ----------
        script : str, optional
            The Python code to be obfuscated or decoded.
        file : str, optional
            The file to be obfuscated.
        """
        self.code = script
        self.files = file
        pass
    def obfuscate(self):
        """
        Obfuscates the code using base64 encoding.

        Returns
        -------
        str
            The obfuscated code.
        """
        encoded = base64.b64encode(self.code.encode('utf-8')).decode('utf-8')
        
        return encoded

    def make_ilisible(self):
        """
        Replaces each character in the obfuscated code with a string of special characters.

        Returns
        -------
        str
            The ilisible code.
        """
        obfuscated = self.obfuscate()
        ilisible = ""
        for char in obfuscated:
            ilisible += char + "$^#^%$%@^&@#"
            pass
        return ilisible
    
    def decode(self):
        """
        Decodes the obfuscated code using base64 decoding and executes it.
        """
        ilisible = self.code
        decoded = ""
        for char in ilisible:
            if char not in "$^#^%$%@^&@#": decoded += char
            pass

        exec(__import__("base64").b64decode(decoded).decode("utf-8"))

    def obfuscate_file(self):
        """
        Obfuscates a Python file using base64 encoding and character replacement.

        Parameters
        ----------
        file : str
            The file to be obfuscated.
        """
        with open(self.files, "r") as f:
            self.code = f.read()
            pass
        with open(self.files, "w") as f:
            f.write("""from Offuscats import *\n\nOffuscats("{}").decode()""".format(self.make_ilisible()))
            pass
        pass 


