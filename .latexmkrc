$pdf_mode = 1;
@default_files = ('logo.tex');
END { 
    system('convert -density 96 -strip -define png:color-type=6 logo.pdf logo.png');
    system('cp -v logo.png project/bin/logo.png');
    system('cp -v logo.png paper/logo.png');
    }
