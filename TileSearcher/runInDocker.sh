if [ "$#" -ne 1 ]; then
    echo 'Usage:'
    echo './runInDocker.sh "./getTileVariants.py -i 1234"'
    echo './runInDocker.sh "./getRsids.py -i 1000 -v 1"'
    exit
fi

# if your Docker image is not named "kfang/tile-tools", then change it in the command below.
docker run -it -v $PWD:/tile-searcher kfang/tile-tools sh -c "cd tile-searcher && $1"
