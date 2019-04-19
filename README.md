# ML Trust Model
A centralised trust model that uses either a neural network or kernel machine
to figure out the trust of the nodes.

## Installation
```
pip3 install -r requirements.txt
```

## Running
To run every using an ANN as the predictor:
```
python3 TrustModel.py
```

Running `python3 TrustModel.py -h` will give a help menu with the available options,
when the ANN is training you may run `tensorboard --logdir ./logs` to get a live graph
of the error curve and accuracy.
