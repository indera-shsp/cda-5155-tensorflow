
run:
	./parse_images.py -i input -o output/test -w 256

run_set_1:
	@ # for f in `find output/set_1 -type d`; do  echo -n $f; ls -1q $f | wc -l; done
	./parse_images.py -i input_raw_images/set_1_262_images/ -o output/set_1 -w 256

run_set_2:
	./parse_images.py -i input_raw_images/set_2_320_images/ -o output/set_2 -w 256
