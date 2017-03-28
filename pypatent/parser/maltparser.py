from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile as tempfile
import os


class MaltParser:
    def __init__(self, work_directory, malt_name, model_name):
        self.path = work_directory
        self.malt = malt_name
        self.model = model_name

    def parse(self, text_conll):

        with tempfile(prefix="malt_input_", dir=self.path, mode="w", delete=False) as input_file:
            with tempfile(prefix="malt_output_", dir=self.path, mode="w", delete=False) as output_file:
                input_file.write(text_conll)

        current_path = os.getcwd()

        try:
            os.chdir(self.path)
        except Exception:
            print(Exception)

        cmd = "java -Xmx1024m -jar JARFILE -c MODEL -i INFILE -o OUTFILE -m parse".split(" ")
        cmd[3] = self.malt
        cmd[5] = self.model
        cmd[7] = input_file.name
        cmd[9] = output_file.name

        with open(input_file.name, "w") as f:
            f.write(text_conll)

        ret = self.__execute(cmd)

        if ret is not 0:
            raise Exception("MaltParser parsing {} failed with exit code {}".format(" ".join(cmd), ret))

        with open(output_file.name, "r") as f:
            result = f.read()

        os.remove(input_file.name)
        os.remove(output_file.name)
        os.chdir(current_path)

        return result

    def __execute(self, cmd):
        p = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return p.wait()
