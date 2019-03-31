dir_files="./training_splits/split_"

split="$1"

current_split_dir="$dir_files""$split/"
train_file="$current_split_dir""train.txt"
test_file="$current_split_dir""test.txt"

echo "$test_file"
echo "$train_file"

cp "$test_file" "./model_handling/training/darknet/data/"