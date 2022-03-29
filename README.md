# malaria-profiler

## Install

```
git clone https://github.com/jodyphelan/malaria-profiler.git
cd malaria-profiler
conda env create -f env.yml 
conda activate malaria-profiler
pip install .
pip3 install git+https://github.com/jodyphelan/pathogen-profiler.git
malaria-profiler update_db
```

## Usage

### Fastq input

```bash
malaria-profiler -1 </path/to/reads_1.fq.gz> -2 </path/to/reads_2.fq.gz> -p <sample_name> -t [threads] --txt 
```

### Bam/Cram imput

```bash
malaria-profiler -a </path/to/bam/cram> -p <sample_name> -t [threads] --txt
```
