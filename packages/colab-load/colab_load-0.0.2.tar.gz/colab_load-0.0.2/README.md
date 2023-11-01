# Colab Load #

## What is this? ##
Library to download .ipynb from google colab

## Quick Guide ##
One url:

    from colab_load.load import StartLoad
    
    s = StartLoad(logs=True)
    s.load_file_s("https://colab.research.google.com/drive/1QD1TM2TroOEqqtTURpk5sVOmGLQeREv", save_dir="file")

Lots of url:

	from colab_load.load import StartLoad
    
	urls=["https://colab.research.google.com/drive/1uQ3QH3khRGYcQ8kU3OMyG1xRF6MB70xA?usp=sharing", "https://colab.research.google.com/drive/1bKxzUeOalOelP7HQ3KGBsF35j7CC2ZFh?usp=sharing"]
	s = StartLoad(logs=True)
	s.load_file_a(urls, save_dir="file", count=2)