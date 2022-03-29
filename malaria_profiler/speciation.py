import pathogenprofiler as pp

def speciate(args):
    if args.external_species_db:
        conf = pp.get_species_db(args.software_name,args.external_species_db)
    else:
        conf = pp.get_species_db(args.software_name,args.species_db)
    
    if args.bam==None:
        fastq = pp.fastq(args.read1,args.read2)
        kmer_dump = fastq.get_kmer_counts(args.files_prefix)

    else:
        if args.mitochondria_seq_name:
            pp.run_cmd(f"samtools view -b {args.bam} {args.mitochondria_seq_name} | samtools fastq > {args.files_prefix}.tmp.fq")
            kmer_dump = pp.fastq(f"{args.files_prefix}.tmp.fq").get_kmer_counts(args.files_prefix,threads=args.threads)
        else:
            bam = pp.bam(args.bam,args.files_prefix,"illumina")
            if bam.filetype=="cram":
                pp.run_cmd(f"samtools fastq {bam.bam_file} > {args.files_prefix}.tmp.fq")
                kmer_dump = pp.fastq(f"{args.files_prefix}.tmp.fq").get_kmer_counts(args.files_prefix,threads=args.threads)
            else:
                kmer_dump = bam.get_kmer_counts(args.files_prefix,threads=args.threads)
    
    species = kmer_dump.get_taxonomic_support(conf['kmers'])
    return species