# rumpsession
A script for concatenating PDF files downloaded from the HotCRP conference management software

# Explanation

I served as the rump session chair for CRYPTO 2022. We used HotCRP for slide submissions for rump session talks.
I wrote this Python script (with help from Nadia Heninger, my co-chair) to concatenate slides together into one big PDF,
with automatically-added interstitial slides that give title, speaker, and the next speaker.

The script will likely require some modification to fit your specific use case---specifically the
hard-coded file name templates---but should work for downloads from HotCRP of type "JSON with attachments".
It assumes the files are in the same directory as the script. It also uses a hard-coded LaTeX preamble,
which is included.


# Usage

Creating and viewing the combined PDF has three steps.

(1) The script prints a LaTeX document to stdout, so you need to pipe the output to a file. E.g.,

```
python3 rumpsession.py > FNAME.tex
```

Then, (2) compile FNAME.tex with pdflatex. If it compiles successfully, (3) view FNAME.pdf with your favorite PDF viewer.

I've also included a script `assemble_rumpsession.sh` that does (1-3) together.