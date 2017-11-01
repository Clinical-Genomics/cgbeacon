#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import click
import coloredlogs

from cyvcf2 import VCF

from cgbeacon.utils.vcfparser import count_variants, get_samples, get_variants
from cgbeacon.utils.mysql_handler import db_handler

LOG = logging.getLogger(__name__)


@click.command()
@click.option('--vcf', type=click.Path(exists=True), nargs=1)
@click.option('--qual', type=click.FLOAT, nargs=1, default=20)
@click.option('--ref', type=click.STRING, nargs=1, default='grch37')
@click.option('--dataset', type=click.STRING, nargs=1, required=True)
@click.argument('samples', nargs=-1, type=click.STRING, default = None)

def cli(vcf, qual, ref, dataset, samples):
    """Simple program that parses a VCF file and store the variants in a MySQL database."""

    #checking that the quality filter values is a valid float in the range 0-99
    if qual > 99 or qual <0:
        click.echo("The provided quality filter must be a number in the range 0-99", err=True)
        sys.exit()

    coloredlogs.install(level='INFO')
    LOG.info("Reading vcf file: %s", vcf)

    # Try to transform what's provided into a VCF object:
    try:
        vcf_obj = VCF(vcf)
    except:
        LOG.critical('Please provide a valid path to a VCF file!')
        print("Usage: cgbeacon --vcf path/to/vcf_file --qual [0-99] --ref grch37 --dataset dataset_name  <sample1> <sample2> .. \n\n")
        sys.exit()

    vcfsamples = get_samples(vcf_obj)

    # If samples are provided, check that they're valid, againt samples in VCF
    if samples:
        LOG.info('Comparing samples provided by user to those present on the VCF file')
        vcfsamples = _compare_samples(vcfsamples, samples)

    # returns a this tuple-> ( total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
    vcf_results = get_variants(vcf_obj, vcfsamples, qual)

    # Print overall results of VCF file parsing to terminal
    _print_results(vcf_results, qual)

    # Insert variants in database:
    LOG.info('Connecting to beacon db:')

    db_handler(ref, dataset, vcf_results)



# Prints results to the terminal. results is this tuple -> ( total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
def _print_results(results, qual):

    """Prints the results of VCF parsing to the terminal.

        Args:
            A tuple defined as this: ( total_vars, discaded_vars(type: dict), beacon_vars(type: dict) )

        What it does:
            Plots statistics of VCF parsing to terminal. It's going to plot:
                1) Total variants found
                2) Variants to be imported in database for each sample
                3) Discarded variants for each sample
    """

    print("\n\n\n")

    # print n. of variants found:
    print("#" * 80)
    print("total number of variants in this file:",results[0], ", QUAL filter >=", qual)
    print("#" * 80)
    print("\n")

    print("{0:<40}{1:^15}{2:>15}".format("samples", "include in beacon", "discarded"))
    count=0
    for keys, values in results[1].items():
        count +=1
        print("{0:<40}{1:^15}{2:>15}".format( keys, len(values), results[2][keys] ))
    print("\n\n")


def _compare_samples(vcfsamples, usersamples):

    """check if the user-provided samples are valid samples in the vcf file"""
    valid_samples =[]

    for sample in usersamples:
        if sample in vcfsamples:
            valid_samples.append(sample)

        else:
            #Reading vcf file: %s", vcf
            #LOG.error('Comparing samples provided by user to those present on the VCF file')
            LOG.critical("Sample %s is not valid.",sample)
            LOG.info("valid samples are:%s", ",".join(vcfsamples))
            #LOG.error("valid samples are:  ",", ".join(vcfsamples),"\n")
            sys.exit()


        if not valid_samples:
            print("\nPlease provide at least a valid sample to insert into beacon!")
            print("valid samples are: ",", ".join(vcfsamples),"\n")
            sys.exit()

    return valid_samples


if __name__ == '__main__':
    cli()
