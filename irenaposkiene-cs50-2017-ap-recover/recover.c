#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
// ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Please enter file to open.\n");
        return 1;
    }

//  filenames
    FILE *file = fopen(argv[1], "r");

//If the file does not exist
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }

// Create output file for picture
    FILE *pic = NULL;

// Create buffer and filename arrays
    BYTE buffer[512];

    char filename[8];
//Set counter for filename
    int counter = 0;
//Set flag
    bool flag = false;
//Read the file
    while (fread(buffer, 512, 1, file) == 1)
    {
//Check if we are at the beginning of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

          if (flag ==true)
             {
                fclose(pic);
              }

          else
             {
             flag =true;
             }
         sprintf(filename, "%03i.jpg", counter);
            pic = fopen(filename, "w");
            counter++;
      }
     if (flag == true)
           {
            fwrite(&buffer, 512, 1, pic);
        }
    }

    fclose(file);
    fclose(pic);

   return 0;
}