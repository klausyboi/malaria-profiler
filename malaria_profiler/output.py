
from collections import defaultdict
import os
from typing import DefaultDict
from pathogenprofiler import filecheck, dict_list2text, get_summary
import csv
import time
from tqdm import tqdm
import json




def load_text(text_strings):
        return r"""
Malaria-Profiler report
=================

The following report has been generated by Malaria-Profiler.

Summary
-------
ID%(sep)s%(id)s
Date%(sep)s%(date)s

Species report
-----------------
%(species_report)s

Resistance report
-----------------
%(dr_report)s

Resistance variants report
-----------------
%(dr_var_report)s

Other variants report
---------------------
%(other_var_report)s

Coverage report
---------------------
%(coverage_report)s

Missing positions report
---------------------
%(missing_report)s

Analysis pipeline specifications
--------------------------------
Pipeline version%(sep)s%(version)s
Species Database version%(sep)s%(species_db_version)s
Resistance Database version%(sep)s%(resistance_db_version)s

%(pipeline)s
""" % text_strings


def load_species_text(text_strings):
        return r"""
Malaria-Profiler report
=================

The following report has been generated by Malaria-Profiler.

Summary
-------
ID%(sep)s%(id)s
Date%(sep)s%(date)s

Species report
-----------------
%(species_report)s

Analysis pipeline specifications
--------------------------------
Pipeline version%(sep)s%(version)s
Species Database version%(sep)s%(species_db_version)s

%(pipeline)s
""" % text_strings


def write_text(json_results,conf,outfile,columns = None,reporting_af = 0.0,sep="\t"):
    if "dr_variants" not in json_results:
        return write_species_text(json_results,conf,outfile)
    json_results = get_summary(json_results,conf,columns = columns,reporting_af=reporting_af)
    json_results["drug_table"] = [[y for y in json_results["drug_table"] if y["Drug"].upper()==d.upper()][0] for d in conf['drugs']]
    for var in json_results["dr_variants"]:
        var["drug"] = ", ".join([d["drug"] for d in var["drugs"]])
    text_strings = {}
    text_strings["id"] = json_results["id"]
    text_strings["date"] = time.ctime()
    text_strings["species_report"] = dict_list2text(json_results["species"],["species","mean"],{"species":"Species","mean":"Mean kmer coverage"},sep=sep)
    text_strings["dr_report"] = dict_list2text(json_results["drug_table"],["Drug","Genotypic Resistance","Mutations"]+columns if columns else [],sep=sep)
    text_strings["dr_var_report"] = dict_list2text(json_results["dr_variants"],["genome_pos","locus_tag","gene","change","type","freq","drugs.drug"],{"genome_pos":"Genome Position","locus_tag":"Locus Tag","freq":"Estimated fraction","drugs.drug":"Drug"},sep=sep)
    text_strings["other_var_report"] = dict_list2text(json_results["other_variants"],["genome_pos","locus_tag","gene","change","type","freq"],{"genome_pos":"Genome Position","locus_tag":"Locus Tag","freq":"Estimated fraction"},sep=sep)
    text_strings["coverage_report"] = dict_list2text(json_results["qc"]["gene_coverage"], ["gene","locus_tag","cutoff","fraction"],sep=sep) if "gene_coverage" in json_results["qc"] else "NA"
    text_strings["missing_report"] = dict_list2text(json_results["qc"]["missing_positions"],["gene","locus_tag","position","variants","drugs"],sep=sep) if "gene_coverage" in json_results["qc"] else "NA"
    text_strings["pipeline"] = dict_list2text(json_results["pipeline_software"],["Analysis","Program"],sep=sep)
    text_strings["version"] = json_results["software_version"]
    tmp = json_results["species_db_version"]
    text_strings["species_db_version"] = "%(name)s_%(commit)s_%(Author)s_%(Date)s" % tmp
    tmp = json_results["resistance_db_version"]
    text_strings["resistance_db_version"] = "%(name)s_%(commit)s_%(Author)s_%(Date)s" % tmp
    if sep=="\t":
        text_strings["sep"] = ": "
    else:
        text_strings["sep"] = ","

    o = open(outfile,"w")
    o.write(load_text(text_strings))
    o.close()


def write_species_text(json_results,conf,outfile,sep="\t"):
    text_strings = {}
    text_strings["id"] = json_results["id"]
    text_strings["date"] = time.ctime()
    text_strings["species_report"] = dict_list2text(json_results["species"],["species","mean"],{"species":"Species","mean":"Mean kmer coverage"},sep=sep)
    text_strings["pipeline"] = dict_list2text(json_results["pipeline_software"],["Analysis","Program"],sep=sep)
    text_strings["version"] = json_results["software_version"]
    tmp = json_results["species_db_version"]
    text_strings["species_db_version"] = "%(name)s_%(commit)s_%(Author)s_%(Date)s" % tmp
    if sep=="\t":
        text_strings["sep"] = ": "
    else:
        text_strings["sep"] = ","
    with open(outfile,"w") as O:
        O.write(load_species_text(text_strings))





def collate(args):
    # Get a dictionary with the database file: {"ref": "/path/to/fasta" ... etc. }
    
    if args.samples:
        samples = [x.rstrip() for x in open(args.samples).readlines()]
    else:
        samples = [x.replace(args.suffix,"") for x in os.listdir(args.dir) if x[-len(args.suffix):]==args.suffix]


    # Loop through the sample result files    
    species = {}
    dr = defaultdict(lambda: defaultdict(list))
    drugs = set()
    dr_samples = set()
    for s in tqdm(samples):
        # Data has the same structure as the .result.json files
        data = json.load(open(filecheck("%s/%s%s" % (args.dir,s,args.suffix))))
        species[s] = ";".join([d["species"] for d in data["species"]])
        
        if "resistance_db_version" in data:
            dr_samples.add(s)
            for gene in data["resistance_genes"]:
                for d in gene["drugs"]:
                    drugs.add(d["drug"])
                    dr[s][d["drug"]].append(f"{gene['gene']}_resistance_gene")
        
            for var in data["dr_variants"]:
                for d in var["drugs"]:
                    drugs.add(d["drug"])
                    dr[s][d["drug"]].append(f"{var['gene']}_{var['change']}")

    results = []
    for s in samples:
        result = {
            "id": s,
            "species": species[s]
        }
        for d in sorted(drugs):
            if s in dr_samples:
                if d in dr[s]:
                    result[d] = ";".join(dr[s][d])
                else:
                    result[d] = ""
            else:
                result[d] = "N/A"
        results.append(result)
    
    if args.format=="txt":
        args.sep = "\t"
    else:
        args.sep = ","

    with open(args.outfile,"w") as O:
        writer = csv.DictWriter(O,fieldnames=list(results[0]),delimiter=args.sep)
        writer.writeheader()
        writer.writerows(results)