# §2023.07
This user-bot is thought to edit the user messages that contains a latex-like math ambient into text that uses greek characters, symbols, subscript and superscript text
for example if the text contains `$\phi(x^2)$` it becomes `ϕ(x²)`. There are some exceptions, eg `$y = a_{x_2}$` just becomes `y = a_{x₂}`, and there are still some problems too, eg `$x^2^3$` becomes `x²³`.

To get the special characters, instead of just creating dictionaries by myself, I made some scraping:
- many superscripted characters come from [www.loc.gov](https://www.loc.gov/marc/specifications/codetables/Superscripts.html) and [rupertshepherd.info](https://rupertshepherd.info/resource_pages/superscript-letters-in-unicode).
- many subscripted characters come from [www.loc.gov](https://www.loc.gov/marc/specifications/codetables/Subscripts.html).
- all the normal size symbols come from [www.mathworks.com](https://www.mathworks.com/help/matlab/creating_plots/greek-letters-and-special-characters-in-graph-text.html)

the first time the code is run, 3 dictionaries will be created that will be used each and everytime a latex math ambient is found