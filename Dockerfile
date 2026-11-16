FROM runpod/comfyui:2.2.0-comfyuiv0.44.0-cuda13.2
COPY bootstrap.py /opt/h3-bootstrap/bootstrap.py
ENTRYPOINT ["python3.12", "/opt/h3-bootstrap/bootstrap.py"]
CMD []
