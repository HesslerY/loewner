#!/bin/bash

latex_file="plots.tex"
output_folder=

# Delete the previous file
rm -r "$latex_file"

# Write something to the latex file
function write_latex_file()
{
    echo "$1" >> "$latex_file"
}

# Write the preamble to the latex file
write_latex_file "\documentclass[a4paper, 12pt]{article}"
write_latex_file "\usepackage[letterpaper, portrait, margin=0.8in]{geometry}"
write_latex_file "\usepackage{graphicx}"
write_latex_file "\usepackage[space]{grffile}"
write_latex_file "\graphicspath{ {output/} }"
write_latex_file "\begin{document}"

counter=0

for f in *".png"; do

    if [[ $((counter % 2)) -eq "1" ]]; then

        write_latex_file "\includegraphics[width=0.9\textwidth]{${f}}"
        write_latex_file "\end{figure}"

    else

        write_latex_file "\begin{figure}[t]"
        write_latex_file "\centering"
        write_latex_file "\includegraphics[width=0.9\textwidth]{${f}}"

    fi
    
    counter=$((counter + 1))

done

if [[ $((counter % 2)) -eq "0" ]]; then

    write_latex_file "\includegraphics[width=0.9\textwidth]{${f}}"
    write_latex_file "\end{figure}"

done

# Write the final part of the latex file
write_latex_file "\end{document}"

# Compile the latex file
pdflatex plots.tex

