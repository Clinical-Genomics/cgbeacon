#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import click
import coloredlogs
import os.path

from cyvcf2 import VCF

from cgbeacon.utils.vcfparser import count_variants, get_samples, get_variants
from cgbeacon.utils.mysql_handler import db_handler
from cgbeacon.utils.vcf_panel_filter import vcf_intersect
from cgbeacon.utils.pdf_report_writer import create_report

LOG = logging.getLogger(__name__)


@click.command()
@click.option('--vcf', type=click.Path(exists=True), nargs=1)
@click.option('--qual', type=click.FLOAT, nargs=1, default=20)
@click.option('--ref', type=click.STRING, nargs=1, default='grch37')
@click.option('--dataset', type=click.STRING, nargs=1, required=True)
@click.option('--use_panel', type=click.Path(exists=True), nargs=1, required=False)
@click.argument('samples', nargs=-1, type=click.STRING, default = None)
@click.option('--pdf_report', is_flag=True, required=False)
@click.option('--customer', type=click.STRING, nargs=1, required=False)

def cli(vcf, qual, ref, dataset, use_panel, samples, pdf_report, customer):
    """Simple program that parses a VCF file and store the variants in a MySQL database."""

    #checking that the quality filter values is a valid float in the range 0-99
    if qual > 99 or qual <0:
        click.echo("The provided quality filter must be a number in the range 0-99", err=True)
        sys.exit()

    coloredlogs.install(level='INFO')
    LOG.info("Reading vcf file: %s", vcf)

    ## Try to transform what's provided into a VCF object:
    try:
        vcf_obj = VCF(vcf)
    except:
        LOG.critical('Please provide a valid path to a VCF file!')
        print("Usage: cgbeacon --vcf path/to/vcf_file --qual [0-99] --ref grch37 --dataset dataset_name  < --use_panel gene_panel.bed > <sample1> <sample2> <samplen> < --pdf_report > < --customer customer_id > \n\n")
        sys.exit()

    #get the raw number of variants from the original VCF file (used to produce report later)
    raw_variants = count_variants(vcf_obj)

    # If gene panel is provided, then extract from VCF file only variants contained in its intervals.
    if use_panel:
        LOG.info('Using pybedtools to extract regions from gene panel')

        if not os.path.isfile(use_panel):
            LOG.critical("Couldn't find gene panel. Please provide a path to a valid gene panel file")
            sys.exit()

        panel_filtered_results = vcf_intersect(vcf, use_panel)

        if panel_filtered_results:
            vcf_obj = panel_filtered_results[0]

        else:
            LOG.critical("Couldn't filter VCF file gene panel intervals. Please check that gene panel is a valid bed file.")
            sys.exit()


    vcfsamples = get_samples(vcf_obj)

    ## If samples are provided, check that they're valid, againt samples in VCF
    if samples:
        LOG.info('Comparing samples provided by user to those present on the VCF file')
        vcfsamples = _compare_samples(vcfsamples, samples)

    ## returns a this tuple-> ( total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
    vcf_results = get_variants(vcf_obj, vcfsamples, qual)

    ## Print overall results of VCF file parsing to terminal
    _print_results(vcf_results, qual)

    ## Insert variants in database:
    LOG.info('Connecting to beacon db:')

    beacon_update_result = db_handler(ref, dataset, vcf_results)

    if not customer:
        customer = ''

    if pdf_report:
        # print pdf report:
        create_report('Clinical Genomics Beacon: variants upload report', use_panel, raw_variants, qual, vcf_results, beacon_update_result, customer)
    else:
        LOG.info('NOT printing a pdf report for this data upload')

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
