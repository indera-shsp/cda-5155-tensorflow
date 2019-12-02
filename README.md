
# Intro

This repo contains code developed for the CDA class - Fall 2019


# Setup steps

    python3 -m venv .env
    source ./.env/bin/activate
    pip install -r requirements.txt


# Image processing


    ./parse_images.py -h
    usage: parse_images.py [-h] [-i INPUTDIR] [-o OUTPUTDIR] [-w WIDTH]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUTDIR, --inputdir INPUTDIR
                            input directory name
      -o OUTPUTDIR, --outputdir OUTPUTDIR
                            output directory name
      -w WIDTH, --width WIDTH
                            output image width (default 512 px)



# References

# Anaconda

    brew cask install anaconda
    du -hcs /usr/local/Caskroom/anaconda/2019.10/Anaconda3-2019.10-MacOSX-x86_64.sh
        ==> 424M

    Update path to make accessible - add to ~/.zshrc
        export PATH="/usr/local/anaconda3/bin:$PATH"
     source ~/.zshrc

    conda init zsh
    conda create -n test-conda
    conda activate test-conda
    jupyter notebook

    conda deactivate
    conda remove -n test-conda -all

## Geohash
- https://en.wikipedia.org/wiki/Geohash#Design
- http://geohash.org/djm2wjk4u0rm
- https://github.com/vinsci/geohash/blob/master/Geohash/geohash.py


## Picking the number of clusters

- (!) https://stackoverflow.com/questions/44416764/loading-folders-of-images-in-tensorflow
- (!) https://datascience.stackexchange.com/questions/761/clustering-geo-location-coordinates-lat-long-pairs/25424#25424
- https://nbviewer.jupyter.org/github/nborwankar/LearnDataScience/blob/master/notebooks/D3.%20K-Means%20Clustering%20Analysis.ipynb

##  Deep Learning: Our Miraculous Year 1990-1991

- http://people.idsia.ch/~juergen/deep-learning-miraculous-year-1990-1991.html

