# gff3toembl
Submitting annoated genomes to EMBL is a very difficult and time consuming process. This software converts GFF3 files from the most commonly use prokaryote annotation tool Prokka into a format that is suitable for submission to EMBL. It has been used to prepare more than 30% of all annotated genomes in EMBL/GenBank.

[![Build Status](https://travis-ci.org/sanger-pathogens/gff3toembl.svg?branch=master)](https://travis-ci.org/sanger-pathogens/gff3toembl)


NB this implements some EMBL specific conventions and is not a generic conversion tool. Its also not a validator, so you need to pass in parameters which are acceptable to EMBL.

## Citation
[![status](http://joss.theoj.org/papers/9253390f38f4ce6b71674f433fa72afe/status.svg)](http://joss.theoj.org/papers/9253390f38f4ce6b71674f433fa72afe)

This software has been published in The Journal of Open Source Software. Please cite it if you use it:

"GFF3toEMBL: Preparing annotated assemblies for submission to EMBL", Andrew J. Page, Sascha Steinbiss, Ben Taylor, Torsten Seemann, Jacqueline A. Keane, The Journal of Open Source Software, 1 (6) 2016. http://dx.doi.org/10.21105/joss.00080

## Installation

### Docker
A docker container is provided with all of the dependancies setup and installed. To install the container:

`docker pull sangerpathogens/gff3toembl`

To run the script from within the container on test data (substituting /home/ubuntu/data for your own directory):

`docker run --rm -it  -v /home/ubuntu/data:/data sangerpathogens/gff3toembl  gff3_to_embl --output_filename /data/output_file.embl ABC 123 PRJ1234 ABC  /opt/gff3toembl-1.1.0/gff3toembl/tests/data/single_feature.gff`

### From source
This is for advanced users. The [homebrew recipe](https://raw.githubusercontent.com/andrewjpage/homebrew-science/gff3toembl/gff3toembl.rb), [Dockerfile](Dockerfile) and the [TravisCI install dependancies script](install_dependencies.sh) all contain steps to setup depenancies and install the software so might be worth looking at for hints.

- Install genometools including python bindings
- git clone git@github.com:sanger-pathogens/gff3toembl.git
- python setup.py install

## Example usage
Run the following to get usage:
`gff3_to_embl -h`

An example:
```
gff3_to_embl --authors 'John' --title 'Some title' --publication 'Some journal' \
             --genome_type 'circular' --classification 'PROK' \
             --output_filename /tmp/single_feature.embl --translation_table 11 \
             Organism 1234 'My project' 'My description' gff3toembl/tests/data/single_feature.gff
```

### Example data
The directory 'example_data' contains an input GFF file and the output file along with the command.

## Tests
Run `python setup.py test`

## Known Issues
This doesn't work with some versions of Genometools on Mac OS X; it appears to work with Genometools 1.5.4

## Reporting Issues and contributing
Please file a Github Issue if you find any problems. All pull requests are greatly apprechiated. Please ensure the test suite passes.  If you would prefer not to file a Github issue, please email path-help@sanger.ac.uk and we will do our best to assist.


