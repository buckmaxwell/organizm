import sys
from time import sleep
from uuid import uuid4
from random import randrange
import os
import stat
import subprocess

MUTATIONS_RATE = 100_000
RANDOM_NUMBER = 3787


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder="big")


def mutate(genome_bitstring):
    genome_bitstring_list = list(genome_bitstring)

    val = randrange(0, 3)
    pos = randrange(0, len(genome_bitstring))

    result = None

    if val == 0:
        # deletion, do noting
        result = "".join(
            genome_bitstring_list[0:pos] + genome_bitstring_list[pos + 1 :]
        )
    elif val == 1:
        # substitution
        genome_bitstring_list[pos] = str(abs(int(genome_bitstring_list[pos]) - 1))
        result = "".join(genome_bitstring_list)
    else:
        randbit = str(randrange(0, 2))
        result = "".join(
            genome_bitstring_list[0:pos] + [randbit] + genome_bitstring_list[pos + 1 :]
        )

    # pad the string with randomness to fill out the byte
    chop = len(result) % 8
    if chop != 0:
        return result[:-chop]
    return result


def reproduce(program_filename, number_of_children):
    for _ in range(number_of_children):
        with open(program_filename, "rb") as parent_rna:
            child_filename = f"organizm_{str(uuid4())}"

            with open(child_filename, "wb") as child_rna:
                genome_bitstring = ""
                while (byte := parent_rna.read(1)) :
                    genome_bitstring += "{:08b}".format(ord(byte))

                child_genome_bitstring = mutate(genome_bitstring)
                child_rna.write(bitstring_to_bytes(child_genome_bitstring))

        # Make child binary executable
        st = os.stat(child_filename)
        os.chmod(child_filename, st.st_mode | stat.S_IEXEC)

        print(f"./{child_filename} {child_filename}")
        subprocess.Popen(
            f"./{child_filename} {child_filename}".split()
        )  # Call subprocess


if len(sys.argv) == 2:
    program_filename = sys.argv[1]
    number_of_children = 100
    # Reproduction phase
    reproduce(program_filename, number_of_children)
