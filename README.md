# VCF Beaconizer
A package which extracts variants from a VCF file and inserts them into a MySQL Elixir Beacon database. The database schema might be downloaded from this page: https://github.com/Clinical-Genomics/beacon.

## Installation
Clone this repository in a local directory using the following command:
<pre>
git clone https://github.com/northwestwitch/vcf_beaconizer.git
</pre>

Change directory to the newly created folder:
<pre>
cd vcf_beaconizer
</pre>

Install the package:
<pre>
pip install .
</pre>

## Database settings
Database settings are specified in the file <b>settings/mysqlconfig.txt</b>. Consider to modify this file before testing the executable.

## Usage
The program parses variants from a VCF file. Samples to be included in the Beacon database and variant quality threshold might be specified as optional parameters.

To execute the program:
<pre>
vcf_beaconizer --vcf path_to_vcf_file --dataset dataset_name
</pre>

Optional parameters:

<pre>
--qual [0-99] (variant quality threshold. default=20)
--ref chr_build (default is grch37)
[list of samples to process separated by space] (Default is all samples found in the VCF file)
</pre>
