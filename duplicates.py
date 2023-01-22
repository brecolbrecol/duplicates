import sys
import os
import glob
import hashlib
import subprocess


def md5_dir(directory):
    md5s = dict()
    filenames = glob.glob(directory + '*')
    num_files = len(filenames)

    count = 0
    for filename in filenames:
        with open(filename, 'rb') as inputfile:
            count += 1
            data = inputfile.read()
            md5 = hashlib.md5(data).hexdigest()
            md5s[md5] = filename
            print(directory + "\t", str(count) + "/" + str(num_files), end="\r")
    print(directory + "\t", str(count) + "/" + str(num_files))

    return md5s


def md5_dirs(directories):
    md5s = dict()
    for directory in directories:
        md5s[directory] = md5_dir(directory)
    return md5s


def more_than_one_link(filename):
    links = os.stat(filename).st_nlink
    return links > 1


def rm_and_create_hardlink(file_src, file_dst):
    os.remove(file_dst) # ToDo: check if os.link has chances to work before removing (maybe hard linking to tmp file and only if success then rm and mv)
    os.link(file_src, file_dst)


def hard_link_duplicates(duplicates):
    count = 0
    for md5 in duplicates:
        file_src = duplicates[md5][0]
        file_dst = duplicates[md5][1]
        if more_than_one_link(file_dst):
            pass
        else:
            rm_and_create_hardlink(file_src, file_dst)
            count += 1
            print("Hard links created:\t", str(count), end="\r")
    print("Hard links created:\t", str(count))


def find_duplicates(directory1, directory2, md5s):
    duplicates = dict()

    count = 0
    for md5 in md5s[directory1]:
        if md5 in md5s[directory2]:
            duplicates[md5] = (md5s[directory1][md5], md5s[directory2][md5])
            count += 1
            print("Duplicates found:\t", str(count), end="\r")
    print("Duplicates found:\t", str(count))

    return duplicates


def print_directories_used_space(directories):
    print('Directories:')
    for directory in directories:
        du = subprocess.Popen(["du", "-sh", directory], stdout=subprocess.PIPE)
        used_space = subprocess.check_output(['du', '-sh', directory]).split()[0].decode('utf-8')
        print("\t - " + str(used_space) + "\t- " + directory)


def main(directories):
    print_directories_used_space(directories)
    print("")

    md5s = md5_dirs(directories)
    duplicates = find_duplicates(directories[0], directories[1], md5s)
    hard_link_duplicates(duplicates)

    print("")
    print_directories_used_space(directories)


if __name__ == '__main__':
    program_name = sys.argv.pop(0)  # Removes program name
    num_arguments_required = 2
    if (len(sys.argv) == num_arguments_required):
        main(sys.argv)
    else:
        err_msg = "Wrong number of arguments"
        err_msg += "\nUsage:\n\t" + program_name + " [source directory] [destination directory]"
        sys.exit(err_msg)
