#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import coloredlogs
import logging
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
from tempfile import NamedTemporaryFile
import time

def create_report(title, outfile, panel, raw_variants, qual, VCF_parsing_results, database_insert_results, customer_id=''):
    """Prints the variants upload to beacon results to a PDF report.

        Args:
            1) A title for this report
            2) Path folder to write outfile to
            3) path to panel used to filter VCF file (if any)
            4) quality filter used for filtering variants prior to upload to beacon
            5) VCF parsing results [ A tuple defined as this: ( total_vars, discaded_vars(type: dict), beacon_vars(type: dict) )]
            6) A tuple containing n. of variants in the beacon before and after the variants' upload.
            7) Customer ID or name (Optional)
            8) Customer email (Optional)

        What it does:
            Prints a PDF report with the results.
    """
    try:
        outpath = os.path.join(os.getcwd(), outfile)
        print("outpath is:",outpath)

        pdf = canvas.Canvas(outpath, pagesize=letter)

        pdf.setLineWidth(.3)
        pdf.setFont('Helvetica', 10)

        #Set pdf generation date:
        now = time.strftime("%c")
        pdf.drawString(420,740, "cgbeacon:"+time.strftime("%x") + "," + time.strftime("%X"))

        #Set logo:
        try:
            logo = ImageReader('https://raw.githubusercontent.com/Clinical-Genomics/cgbeacon/master/img/SLL_logo.png')
            pdf.drawImage(logo, 20, 700, mask='auto', width=7*cm, height=2*cm)
        except Exception as e:
            print("Couldn't fetch logo from the web. Printing PDF without it! Errror:",e)
        pdf.drawString(38,695,'Science for Life Laboratory')
        pdf.drawString(38,680,'Tomtebodavägen 23A 17165 Solna, Sweden.')
        pdf.drawString(38,665,'Clinical Genomics, Stockholm.')
        pdf.drawString(38,650,'clinical.scilifelab.se')

        pdf.setFont('Helvetica-Bold', 16)
        pdf.drawString(100, 600, title)

        pdf.setFont('Helvetica', 11)

        xcoord = 560

        if customer_id:
            pdf.drawString(38, xcoord, "Upload ordered by user: " + str(customer_id))
            xcoord -= 20

        pdf.drawString(38, xcoord, "Raw variants present on VCF file: " + str(raw_variants))
        xcoord -= 20

        if panel:
            panel = panel.split("/")
            panel = str(panel [ len(panel)-1 ] ).split(".")
            pdf.drawString(38, xcoord, "VCF file was filtered using panel: " + str(panel [ len(panel)-1 ] ))
            xcoord -= 20

            pdf.drawString(38, xcoord, "Number of variants mapping to panel: " + str(VCF_parsing_results[0]))
            xcoord -= 20

        pdf.drawString(38, xcoord, "Min. quality used to filter VCF variants: " + str(qual))
        xcoord -= 20

        pdf.line(38,xcoord,575,xcoord)
        xcoord -= 10
        pdf.drawString(38, xcoord, "Samples")
        pdf.drawString(250, xcoord, "Variants to submit")
        pdf.drawString(400, xcoord, "Variants with Qual<="+str(qual))
        xcoord -= 8
        pdf.line(38,xcoord,575,xcoord)
        xcoord -= 5
        for keys, values in VCF_parsing_results[1].items():

            if len(values)>0:
                xcoord -= 10
                pdf.drawString(38, xcoord, str(keys))
                pdf.drawString(250, xcoord, str(len(values)))
                pdf.drawString(400, xcoord, str(VCF_parsing_results[2][keys]))

        xcoord -=10
        pdf.line(38,xcoord,575,xcoord)

        #add results of beacon queries:
        xcoord -= 20
        pdf.drawString(38, xcoord, "Number of variants in Beacon BEFORE submission: " + str(database_insert_results[0]))
        xcoord -= 20
        pdf.drawString(38, xcoord, "Number of new variants submitted to Beacon: " + str(database_insert_results[1]))
        xcoord -= 20
        pdf.drawString(38, xcoord, "Number of variants in Beacon AFTER submission: " + str(database_insert_results[0]+database_insert_results[1]))

        pdf.drawString(500, 50, "page 1 of 1")
        pdf.save()


    except Exception as e:
        print('Unexpected error:',e)

if __name__ == '__main__':

    #feeding the sub fake data just to create an example report:
    create_report("Clinical Genomics Beacon: variants upload report", 'path/to/a/panel', 20, (10000, { 'sample1':{'var1':'T', 'var2':'G'}, 'sample2':{'var1':'T', 'var2':'G', 'var3':'A'}, 'sample3':{'var1':'T', 'var2':'G', 'var3':'A'}}, { 'sample1': 99450, 'sample2': 99800, 'sample3':99560 } ), (34000, 34580), 'cust000')
