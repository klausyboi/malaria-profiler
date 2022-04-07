from pathogenprofiler import bam_profiler, get_barcoding_mutations, bam, debug
from copy import deepcopy
import os

def assign_region(snps_report, conf):
    condition = set([(r[3],int(r[5])) for r in [l.strip().split() for l in open(conf['geo_barcode'])]])
    region_result = []
    for item in condition:
        sum_snps = sum([it[5] for it in snps_report if it[0] == item[0]])
        region_result.append([item[0], item[1], sum_snps])
    res = [x[0] for x in region_result if x[2] >= x[1]]

    if "geoclassification_order" in conf:
        order = conf["geoclassification_order"]
        if len(res)>1:
            region = [(sorted(res,key=lambda x:order.index(x)))[0]]
        elif len(res) == 1:
            region = res
        else:
            region = ["Unassigned"]
    else:
        region = res

    return(region)


def malaria_bam_profiler(args):
    
    results = bam_profiler(
        conf=args.conf, bam_file=args.bam_file, prefix=args.files_prefix, platform=args.platform,
        caller=args.caller, threads=args.threads, no_flagstat=args.no_flagstat,
        run_delly = args.run_delly, calling_params=args.calling_params,
        coverage_fraction_threshold=args.coverage_fraction_threshold,
        missing_cov_threshold=args.missing_cov_threshold, samclip=args.no_clip,
        min_depth=args.min_depth,delly_vcf_file=args.delly_vcf,call_wg=args.call_whole_genome,
        variant_annotations=args.add_variant_annotations, coverage_tool=args.coverage_tool
    )

    if "geo_barcode" in args.conf:
        bam_class = bam(args.bam_file,prefix=args.files_prefix,platform=args.platform)
        barcode_mutations = bam_class.get_bed_gt(bed_file=args.conf['geo_barcode'],ref_file=args.conf['ref'],caller=args.caller,platform=args.platform)
        barcode_support,snps_report = get_barcoding_mutations(barcode_mutations,args.conf["geo_barcode"])
        region_result = assign_region(snps_report, args.conf)
        results['geoclassification'] = region_result

    return results