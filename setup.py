import setuptools


setuptools.setup(

	name="tbprofiler",

	version="0.0.1",
	packages=["malariaprofiler","pathogenprofiler"],
	license="MIT",
	long_description="Malaria-profiler command line tool",
	scripts= [
		'bin/malaria-profiler'
	]
)
