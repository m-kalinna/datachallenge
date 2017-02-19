Here are the sources and the build-instructions for yelp_data_loader.
Due to license restrictions, yelp_dataset_challenge_round9.tar must be downloaded from 
https://www.yelp.com/dataset_challenge/dataset separately.
```
mkalinna@JR35WZ1:/opt/git$ git clone git@github.com:m-kalinna/datachallenge.git
Cloning into 'datachallenge'...
Checking connectivity... done.
mkalinna@JR35WZ1:/opt/git$ cd datachallenge/src/
mkalinna@JR35WZ1:/opt/git/datachallenge/src$ cp ~/Downloads/yelp_dataset_challenge_round9.tar ./
mkalinna@JR35WZ1:/opt/git/datachallenge/src$ sudo docker build -t yelp_data_loader .
# run the tool with parameters automatically
mkalinna@JR35WZ1:sudo docker run yelp_data_loader
# run the tool manually
mkalinna@JR35WZ1:sudo docker run -it --entrypoint /bin/bash yelp_data_loader
mkalinna@JR35WZ1:/opt/git/datachallenge/src$ sudo docker run -it --entrypoint /bin/bash yelp_data_loader
root@a068626a9208:/yelp# python yelp_data_loader.py -f /data/yelp_dataset_challenge_round9.tar -c2
```
FTR (read: for me): This is how to clean up docker images
```
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -q)
```
Ideas for extending:
- the container keeps growing due to tar extractions, no matter if you delete 
  the extracted .json files or not.
  Solution might be to either solve this with Docker or to load from .tar
  without writing to disk
- should be split into two containers, one holding the Spark image with an exposed port
  and one with the python script
- implement the automated build service with dynamic downloading of the .tar file
  (add automatically accepting license from YELP)
