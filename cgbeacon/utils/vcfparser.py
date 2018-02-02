#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cyvcf2 import VCF
import enlighten
import sys
import coloredlogs
import logging

LOG = logging.getLogger(__name__)

def count_variants(vcf):
    """Count the number of variants in a vcf file

    Args:
        vcf(iterable): An iterable VCF with variants

    Returns:
        nr_variants(int): Number of variants in file
    """
    if type(vcf) == str:
        try:
            vcf = VCF(vcf)
        except:
            LOG.critical('Please provide a valid path to a VCF file!')
            sys.exit()

    nr_variants = 0
    for variant in vcf:
        nr_variants += 1

    return nr_variants

def make_vcf(path_to_vcf_file):
    """ Creates a vcf file object from a vcf file path

    Args:
        A VCF file path

    Returns:
        A VCF file object
    """
    vcf = VCF(path_to_vcf_file)
    return vcf


def get_samples(vcf):
    """ Get the names of the samples contained in a VCF file

    Args:
        A VCF object

    Returns:
        A list of samples contained in the VCF
    """

    if type(vcf) == str:
        try:
            vcf = make_vcf(vcf)
        except Exception as e:
            LOG.critical('An error occurred while creating a VCF object from file path:%s', e)
            sys.exit()

    return vcf.samples


def get_variants(vcf, raw_variants, sample_list = None, qual_filter = 20.0):

    """Parses VCF file collecting all variants passing a QUAL filter for each sample of sample_list.

    Args:
        a VCF object
        a list of samples
        a QUAL value as a filter

    Returns:
        The following tuple -> ( total_vars, beacon_vars(type: dict), discaded_vars(type: dict))
        beacon_vars are the variants to be included in the beacon database
        discaded_vars are the variants with quality < QUAL

    """
    # If a string is provided (a path to a VCF?), try to transform it into a VCF object:
    if type(vcf) == str:
        try:
            vcf = VCF(vcf)
        except:
            LOG.critical('Please provide a valid path to a VCF file!')
            sys.exit()

    # cyvcf2 convention for genotypes is:
    # 0 -> Homoz. wild type
    # 1 -> Heteroz. alt allele
    # 2 -> Not covered (unknown)
    # 3 -> Homoz. for the alt. allele

    # create a dictionary with key --> sample, and value --> list of tuples containing the non-reference variants. Each tuple is defined as: (chr, start, alt_allele)
    #create keys from  sample list and empty lists as their values

    print("In vcfparser.get_variants. Passed samples are:",sample_list)
    print("List of samples in VCF file:",get_samples(vcf))

    if not any(i in sample_list for i in get_samples(vcf)):
        LOG.critical('Provided sample(s) not among the samples in VCF file. Aborting the upload.')
        sys.exit()

    try:
        # Check which samples must be inserted into the beacon
        idx = []
        vcf_samples = get_samples(vcf)

        # If no sample is pecified the use all samples in VCF file
        if len(sample_list) == 0:
            print("len(sample_list) == 0")
            sample_list = vcf_samples

        for sample in vcf_samples:
            if sample in sample_list:
                idx.append(True)
            else:
                idx.append(False)

        samplevars = {sample : [] for sample in sample_list}
        sampleDiscards = {sample : 0 for sample in sample_list}

        varCounter = 0
        discarded = 0

        print("Extracting variants from VCF file. It might take a while..")
        pbar = enlighten.Counter(total=raw_variants, desc='', unit='ticks')

        # loop over each variant (VCF line)
        for v in vcf:
            varCounter += 1
            if len(v.ALT) == 1: # there is just one alternate allele for samples in this VCF line

                # loop over the samples GT, QUALs and Depths
                sampleCounter = 0

                gt_counter = 0

                # looping over the genotype of each sample
                for gt in v.gt_types:

                    # If it'a a sample to be saved in the beacon
                    if idx[gt_counter]:

                        qual = int(v.gt_quals[sampleCounter])

                        #store it, but only if QUAL > qual and the position is covered
                        if qual >= qual_filter and not gt=="2":

                            # append a tuple with (chr, start, alt) with this variant to the list of variants (tuples) of this sample:
                            var_tuple = (v.CHROM, v.start, v.ALT[0] )
                            if not var_tuple in samplevars[ sample_list[sampleCounter] ]:
                                samplevars[ sample_list[sampleCounter] ].append(var_tuple)

                        else:
                            # It's discarded, so increment counter for dicarded vars for this sample
                            sampleDiscards[ sample_list[sampleCounter] ] += 1

                        sampleCounter +=1
                    gt_counter +=1
            else: # multiple alleles at this position, take care of it!

                # loop over the multiple alternate alleles:
                for i in range(len(v.ALT)):

                    #loop over the GTs of each sample and see if variant is there:
                    sampleCounter = 0

                    # looping over the genotype of each sample
                    for gt in v.gt_types:

                        # If it'a a sample to be saved in the beacon
                        if idx[gt_counter]:
                            #store it, but only if QUAL > qual and the position is covered
                            if qual >= qual_filter and not gt=="2":
                                # append a tuple with (chr, start, alt) with this variant to the list of variants (tuples) of this sample:
                                var_tuple = (v.CHROM, v.start, v.ALT[i])
                                if not var_tuple in samplevars[ sample_list[sampleCounter] ]:
                                    samplevars[ sample_list[sampleCounter] ].append( var_tuple )

                            sampleCounter += 1
                        gt_counter +=1
            pbar.update()

        return (varCounter, samplevars, sampleDiscards)

    except Exception as e:
        LOG.critical(e)
        return False
