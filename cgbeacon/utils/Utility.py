#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cgbeacon.utils.mysql_handler import bare_variants_uploader
from cgbeacon.utils.vcf_panel_filter import vcf_intersect
from cgbeacon.utils.vcfparser import get_variants, count_variants
from pdf_report_writer import create_report

def beacon_upload(vcf_path, panel_path, dataset, conn, outfile="", customer="", samples=[], qual=20, genome_reference="grch37"):
    """ This object is the backbone of the beacon importer.

        Args:
        1) Path to the VCF file
        2) Path to gene panel (or coordinates) to use to filter VCF file
        3) dataset name ( a string )
        4) Connection object to the beacon database
        5) Optional: An array of samples to be used for extracting variants from the VCF file
        6) Optional: quality threshold to filter variants (use variants >=qual)
        7) Optional: genome reference, default is grch37

        Creates a report file on the provided outpath

        Returns: number of new variants in the Beacon
    """
    # Get number of raw variants in original VCF file:
    raw_variants = count_variants(vcf_path)

    ## Do VCF filter by panel:
    # Returns a tuple with:
    # a mini-VCF file object
    # the number of original intervals in the bed panel
    # the number of variants mapping to these intervals
    panel_filtered_results = vcf_intersect(vcf_path, panel_path)
    print("Intervals in panel:",panel_filtered_results[1], "\nVars in intervals:", panel_filtered_results[2])

    ## Extracts variants from mini-VCF file object:
    # returns a this tuple-> ( n_total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
    ### beacon_vars is a disctionary with key --> sample, and value --> list of tuples containing the non-reference variants. Each tuple is defined as: (chr, start, alt_allele)
    ### discaded_vars is a dictionary with key --> sample and value --> number of discarded vars due to quality for that sample.
    vcf_results = get_variants(panel_filtered_results[0], samples, qual)

    # Insert variants into the beacon. It returns a tuple: (vars_before_upload, vars_after_upload)
    beacon_update_result = bare_variants_uploader(connection, dataset, vcf_results, genome_reference)

    # Print the pdf report with the variant upload results:
    print("Printing a report with beacon upload results to --> ",outfile)
    title = "Clinical Genomics Beacon: variants upload report"
    create_report(title, outfile, panel_path, raw_variants, qual, vcf_results, beacon_update_result, customer)

    # Return the number of new vars uploaded in beacon
    print("new vars in beacon:", beacon_update_result[1])
    return beacon_update_result[1]

if __name__ == '__main__':
    beacon_upload("path_to_VCF_file", "path_to_gene_panel", "dataset_name", None, "path_to_outfile" , "Chiara", ["sample1", "sample2", "sample3" ], 30, "grch38")
