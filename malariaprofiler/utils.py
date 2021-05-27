import sys
import pathogenprofiler as pp
import json
def get_conf_dict_with_path(library_path):
    files = {"ref":".fasta","barcode":".barcode.bed","bed":".bed","json_db":".dr.json","version":".version.json","variables":".variables.json"}
    conf = {}
    for key in files:
        sys.stderr.write("Using %s file: %s\n" % (key,library_path+files[key]))
        if key=="variables":
            tmp = json.load(open(pp.filecheck(library_path+files[key])))
            for k in tmp:
                conf[k] = tmp[k]
        else:
            conf[key] = pp.filecheck(library_path+files[key])
    return conf

def get_conf_dict(library_prefix):
    library_prefix = "%s/share/malaria-profiler/%s" % (sys.base_prefix,library_prefix)
    return get_conf_dict_with_path(library_prefix)