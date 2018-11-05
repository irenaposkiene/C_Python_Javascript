# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?
Is the 45-letter behemoth and the longest word in the English language
TODO

## According to its man page, what does `getrusage` do?
It means get information about resource utilization
TODO

## Per that same man page, how many members are in a variable of type `struct rusage`?
There are 16 members in a variable of type struct rusage
TODO

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?
Because of passing large structs by value is slow and it takes up a lot of memory.
TODO

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.
After opening and checking that the file has opened, the for loop iterates until the EOF, or end or file, marker is reached. With the first character from the file, pointed to by fp.
Each iteration of the for loop causes C to be assigned the value of the next character in the file. Each character, contained in variable C, is checked to ensure it is a letter or an apostrophe, as long as the apostrophe does not appear at the beginning of the word.
If it is a letter, the character will be inserted into the WORD array at the INDEX position. After this happens INDEX is incremented to go to the next position in the array.

TODO

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?
 Because fgetc() reads character by character of a file and fscanf is used for reading an entire file
TODO

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?
Because I worked with pointers

TODO
