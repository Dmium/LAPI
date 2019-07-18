from os import walk

files = []
for (dirpath, dirnames, filenames) in walk("../src/lazyAPI"):
    for file in filenames:
        if ".py" in file and ".pyc" not in file:
            path = dirpath.split("../src/lazyAPI")
            pathstring = ''
            for s in path:
                pathstring += s
            pathstring = "lazyAPI" + pathstring.replace("/", ".") + "." + file.split(".py")[0]
            files.append((pathstring, file.split(".py")[0]))
f = open("index.rst", "w")

f.write("Welcome to LAPI's documentation!\n")
f.write("================================\n\n")
f.write(".. toctree::\n")
f.write("   :maxdepth: 4\n")
f.write("   :caption: Contents:\n\n")
f.write("API\n")
f.write("===\n\n")

for file in files:
    f.write(file[1] + "\n")
    for i in range(len(file[1])):
        f.write("-")
    f.write("\n\n")
    f.write(".. automodule:: " + file[0] + "\n")
    f.write("   :members:\n")
    f.write("   :inherited-members:\n\n")
    