from subprocess import Popen, PIPE
from sys import platform
from .tokenize import simple_word_tokenize as tokenize


class TreeTagger:
    """
    Interface to the TreeTagger
    """

    def __init__(self, bin_file_path, par_file_path, other_args="-lemma -token -sgml"):
        self.bin_file_path = bin_file_path
        self.par_file_path = par_file_path
        self.other_args = other_args.split()

    def tag(self, input_string):
        args = [self.bin_file_path, self.par_file_path]
        args += self.other_args
        p = Popen(args, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        text = tokenize(input_string)
        text = '\n'.join(x for x in text)
        # text = '\n'.join((x for x in input_string.split()))

        (stdout, stderr) = p.communicate(bytes(text, 'UTF-8'))

        output = stdout.decode('UTF-8')

        # Different platforms have different codes for "new line".
        # Windows have \r\n, Unix has \n, Old macs have \r and yes there are some systems that have \n\r too.
        line_end = '\n'
        if platform == 'win32':
            line_end = '\r\n'

        sentences = []
        for word in output.strip().split(line_end):
            sentences.append(word.split('\t'))
        return sentences
