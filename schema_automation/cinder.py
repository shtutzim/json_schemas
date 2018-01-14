import os
from shutil import copyfile

main_func = "def main():\n    "
call_main_func = "if __name__ == '__main__':\n    main()"
python_files = []

def main():
    for root, dirs, files in os.walk("cinder/api/schemas"):
        for json in files:
            if json != "__init__.py" and json != "nova.py":
                schema_names = []
                with open(root+'/'+json, 'r') as f:
                    data = f.read()
                    splitted = data.split("\n")
                    valid = True

                    for t in splitted:
                        if len(t) != 0:
                            if t[0].isalpha():
                                if t.count('=') == 1:
                                    var_name = t.split(' ')[0]
				    
				    schema_names.append(var_name)

                if valid is True:
                    schema_name = root.replace('/', '_')+".py"
                    print "trying to copy: " + root + '/' + 'schema.py'
                    copyfile(root+'/'+json, "schemas/"+json)
                    print "creating file " + schema_name
                    python_files.append(json)

                    with open("schemas/"+json, 'a') as f:
                        f.write("\n" + main_func)
                        for schema in schema_names:
			    if schema.find("[") != -1:
				continue
                            f.write("with open('json/" + json[:-3] + "_" + schema + ".json', 'w') as f:" + "\n" + ' ' * 8)
                            f.write("f.write(str(" + schema + "))" + "\n\n" + ' ' * 4)
                        f.write("\n" + call_main_func)

    with open("schemas/run.sh", "w") as f:
        f.write("#!/bin/bash\n")
        for py in python_files:
            f.write("python " +py+"\n")

if __name__ == "__main__":
    main()
