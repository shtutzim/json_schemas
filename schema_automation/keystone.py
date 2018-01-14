import os
from shutil import copyfile

main_func = "def main():\n    "
call_main_func = "if __name__ == '__main__':\n    main()"
python_files = []

def main():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "schema.py":
                schema_names = []
                with open(root+'/'+'schema.py', 'r') as f:
                    data = f.read()
                    splitted = data.split("\n")

                    for t in splitted:
                        if len(t) != 0:
                            if t[0].isalpha():
                                if t.count('=') == 1:
                                    schema_names.append(t.split(' ')[0])

                schema_name = root.replace('/', '_')+".py"
                print "trying to copy: " + root[2:] + '/' + 'schema.py'
                copyfile(root[2:]+'/'+'schema.py', "schemas/"+schema_name[2:])
                print "creating file " + schema_name
                python_files.append(schema_name[2:])

                with open("schemas/"+schema_name[2:], 'a') as f:
                    f.write("\n" + main_func)
                    for schema in schema_names:
                        f.write("with open('json/schema_" + schema + ".json', 'w') as f:" + "\n" + ' ' * 8)
                        f.write("f.write(str(" + schema + "))" + "\n\n" + ' ' * 4)
                    f.write("\n" + call_main_func)

    with open("schemas/run.sh", "w") as f:
        f.write("#!/bin/bash\n")
        for py in python_files:
            f.write("python " +py+"\n")

if __name__ == "__main__":
    main()
