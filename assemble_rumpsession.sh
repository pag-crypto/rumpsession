#!/bin/bash

python3 rumpsession.py > rumpsession.tex
pdflatex rumpsession.tex
open rumpsession.pdf
