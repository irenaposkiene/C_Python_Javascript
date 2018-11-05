/**
 * copy.c
 *
 * CS50 AP
 *
 *
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./copy f infile outfile\n");
        return 1;
    }

    // remember inputs
    int resize = atof(argv[1]);

    char *infile = argv[2];
    char *outfile = argv[3];

    // n can be between 0 and 100
    if (resize < 0.0 || resize > 100.0)
    {
        printf("Resize value must be between 0 and 100\n");
        return 2;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    //BITMAPFILEHEADER bfOld = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    BITMAPINFOHEADER biOld = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Calculate the new width and height and round the number
    bi.biWidth = bi.biWidth * resize;
    bi.biHeight = bi.biHeight * resize;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingOld = (4 - (biOld.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Calculate the new size
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);

    // Calculate the new size of the file
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER & BITMAPINFOHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    RGBTRIPLE triple[biOld.biWidth];


    for (int i = 0, biHeight = abs(biOld.biHeight), currHeight = 0; i < biHeight; i++)
    {

        if(resize < 1)
        {
            biHeight = abs(bi.biHeight);
        }


        for (int j = 0; j < biOld.biWidth; j++)
        {

            fread(&triple[j], sizeof(RGBTRIPLE), 1, inptr);
        }

            for(int j = (currHeight / resize); j == (currHeight / resize); currHeight++)
            {
            // Go through the width at current row
            for(int k = 0; k < bi.biWidth; k++)
            {
                fwrite(&triple[ (k/resize) ], sizeof(RGBTRIPLE), 1, outptr);
            }
            // Add the extra padding as needed
            for(int k = 0; k < padding; k ++)
            {
                fputc(0x00, outptr);
            }

            if(resize < 1 && ((currHeight+1) / resize) - j > 1)
            {
                fseek(inptr, sizeof(RGBTRIPLE)*biOld.biWidth + paddingOld, SEEK_CUR);
            }
        }


        fseek(inptr, paddingOld, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);


    return 0;
}
