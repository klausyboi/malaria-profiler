# malaria-profiler

## Install

```
wget  https://raw.githubusercontent.com/jodyphelan/malaria-profiler/main/env.yml
conda env create -f env.yml 
conda activate malaria-profiler
pip install git+https://github.com/jodyphelan/malaria-profiler.git
pip install git+https://github.com/jodyphelan/pathogen-profiler.git
malaria-profiler update_db
```

## Updating

```
conda activate malaria-profiler
pip install git+https://github.com/jodyphelan/malaria-profiler.git
pip install git+https://github.com/jodyphelan/pathogen-profiler.git
```

## Usage

### Input types

#### Fastq 

```bash
malaria-profiler -1 </path/to/reads_1.fq.gz> -2 </path/to/reads_2.fq.gz> -p <sample_name> -t [threads] --txt 
```

#### Bam/Cram 

```bash
malaria-profiler -a </path/to/bam/cram> -p <sample_name> -t [threads] --txt
```

#### Fasta 

```bash
malaria-profiler -f </path/to/fasta> -p <sample_name> -t [threads] --txt
```

#### VCF 

```bash
malaria-profiler -v </path/to/vcf> -p <sample_name> -t [threads] --txt
```

### Collating results across runs

```bash
malaria-profiler collate 
```