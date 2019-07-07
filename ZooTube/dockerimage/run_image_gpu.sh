# run consumer image
sudo docker run --rm -it --device=/dev/nvidiactl --device=/dev/nvidia-uvm --device=/dev/nvidia0 --name animaltag_gpu fanxia08/animaltag_gpu:v3