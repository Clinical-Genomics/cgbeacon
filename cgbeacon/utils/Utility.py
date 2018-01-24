#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cyvcf2 import VCF

from cgbeacon.utils.mysql_handler import bare_variants_uploader
from cgbeacon.utils.vcf_panel_filter import vcf_intersect
from cgbeacon.utils.vcfparser import get_variants, count_variants
from cgbeacon.utils.pdf_report_writer import create_report

def beacon_upload(connection, vcf_path, panel_path, dataset, outfile="", customer="", samples=None, qual=20, genome_reference="grch37"):
    """ This object is the backbone of the beacon importer.

        Args:
        1) Path to the VCF file
        2) Path to gene panel (or coordinates) to use to filter VCF file
        3) dataset name ( a string )
        4) Optional: An array of samples to be used for extracting variants from the VCF file
        5) Optional: quality threshold to filter variants (use variants >=qual)
        6) Optional: genome reference, default is grch37

        Creates a report file on the provided outpath

        Returns: number of new variants in the Beacon
    """
    samples = samples or []

    # Get number of raw variants in original VCF file:
    raw_variants = count_variants(vcf_path)

    ## Do VCF filter by panel:
    # Returns a tuple with:
    # a mini-VCF file object
    # the number of original intervals in the bed panel
    # the number of variants mapping to these intervals

    # If the vcf should be filtered by a gene panel bed file:
    panel_filtered_results = None
    if panel_path:
        panel_filtered_results = vcf_intersect(vcf_path, panel_path)
    else:
        vcf_obj = VCF(vcf_path)
        panel_filtered_results = (vcf_obj, raw_variants, raw_variants)

    ## Extracts variants from mini-VCF file object:
    # returns a this tuple-> ( n_total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
    ### beacon_vars is a disctionary with key --> sample, and value --> list of tuples containing the non-reference variants. Each tuple is defined as: (chr, start, alt_allele)
    ### discaded_vars is a dictionary with key --> sample and value --> number of discarded vars due to quality for that sample.
    vcf_results = get_variants(panel_filtered_results[0], raw_variants, samples, qual)

    # Insert variants into the beacon. It returns a tuple: (vars_before_upload, vars_after_upload)
    beacon_update_result = bare_variants_uploader(connection, dataset, vcf_results, genome_reference)

    # Print the pdf report with the variant upload results:
    if outfile:
        print("Printing a report with beacon upload results to --> ",outfile)
        title = "Clinical Genomics Beacon: variants upload report"
        create_report(title, outfile, panel_path, raw_variants, qual, vcf_results, beacon_update_result, customer)

    # Return the number of new vars uploaded in beacon
    print("new vars in beacon:", beacon_update_result[1])
    return beacon_update_result[1]
