# Description
Simple prototype script for integration of chewieSnake in Bifrost.

# Example
Set BIFROST_DB_KEY unless you want to use default ("mongodb://localhost/bifrost_test").

export CHEWIESNAKE_IMAGE_ID=5d783e56b485
export CHEWIESNAKE_MOUNT_POINT=/home/finn/data
python run_chewiesnake.py "1912T00314_S99_L999"
