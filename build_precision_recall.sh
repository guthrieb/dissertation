
comma = ","
output_file = "precision_recall_data.csv"
echo "recall,precision" > output_file

for THRESHOLD in $(seq 0.0 0.1 1.0); do

  precision_key_pair = `./darknet detector map -thresh "$THRESHOLD" cfg/obj.data cfg/yolo-obj.cfg backup/yolo-obj_5000.weights | grep -Eoh "precision = [-+]?[0-9]*\.?[0-9]+"`
  precision_val = $(echo "$precision_key_pair" | grep "[-+]?[0-9]*\.?[0-9]+")

  recall_key_pair = `./darknet detector map -thresh "$THRESHOLD" cfg/obj.data cfg/yolo-obj.cfg backup/yolo-obj_5000.weights | grep -Eoh "recall = [-+]?[0-9]*\.?[0-9]+"`
  recall_val = `echo "$precision_key_pair" | grep "[-+]?[0-9]*\.?[0-9]+"``

  file_write = "$recall_val$comma$precision_val\n"

  echo file_write >> output_file

done
