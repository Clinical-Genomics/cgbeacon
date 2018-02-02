#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import coloredlogs
import os
from tempfile import NamedTemporaryFile
from cyvcf2 import VCF
from pybedtools import BedTool

LOG = logging.getLogger(__name__)

def vcf_intersect(vcf_path, bed_panel):
    """Uses Pybedtoolst a.intersect(b) to ectract from VCF variants mapping in the gene panel intervals

    Args:
        1) a path to a valid VCF file to estract variants from.
        2) bed file containing the genetic intervals of interest.

    Returns:
        A tuple, containing:
            1) a VCF object built from the intervals-filtered VCF
            2) the number of original intervals in the bed panel
            3) the number of variants mapping to these intervals
    """

    try:
        vcf_file = BedTool(vcf_path)
        gene_panel = BedTool(bed_panel) # gene panel doesn't need to be sorted by chrom and position.

        # Do the actual filtering and create a mini VCF with only the variants from the bed file's intervals:

        intersections = vcf_file.intersect(gene_panel, header=True)
        LOG.info('Computing intersections between interval filter and VCF file..')
        panel_intervals =  gene_panel.count()
        intersected_vars = intersections.count()

        LOG.info('Extracting %s intervals from the %s total entries of the VCF file.', gene_panel.count(), vcf_file.count())
        LOG.info('Number of variants found in the intervals:%s', intersected_vars)

        temp_intersections_file = NamedTemporaryFile('w+t', dir=os.getcwd())
        intersections.saveas(temp_intersections_file.name)
        mini_VCF = VCF(temp_intersections_file.name)

        #remove temporary file:
        temp_intersections_file.close()

        # Return a tuple with:
        # a mini-VCF file object
        # the number of original intervals in the bed panel
        # the number of variants mapping to these intervals
        return (mini_VCF, panel_intervals, intersected_vars)

    except Exception as e:

        LOG.critical(e)
        return False
