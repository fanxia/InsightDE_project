FROM fanxia08/numpydarknet_cpu:v1

Run \
    pip3 install mysql-connector-python pika \
    && git clone https://github.com/fanxia/InsightDE_project.git

WORKDIR InsightDE_project/AnimalTag/src
ENTRYPOINT ["python3","-u","consumer.py"]
CMD ["bash"]