import multiprocessing as mp
import tensorflow as tf
from pprint import pprint
import numpy as np

def convert (keras_model, saveto):
    converter = tf.lite.TFLiteConverter.from_keras_model (keras_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert ()
    with open (saveto, 'wb') as f:
        f.write (tflite_model)


class Model:
    def __init__ (self, path, batch_size = 1, outputs_order = None, num_threads = None):
        self.path = path
        self.batch_size = batch_size
        self.outputs_order = outputs_order
        self.lock = mp.Lock ()
        self.interp = tf.lite.Interpreter (model_path = path, num_threads = num_threads)

        self.input_details = self.interp.get_input_details ()
        self.output_details = self.interp.get_output_details ()
        if self.outputs_order:
            self.output_details = [self.output_details [idx] for idx in self.outputs_order]

        self.allocate (self.batch_size)

    def allocate (self, batch_size):
        for input_detail in self.input_details:
            shape = input_detail ['shape']
            shape [0] = batch_size
            self.interp.resize_tensor_input (input_detail ['index'], shape)
        self.interp.allocate_tensors ()

    def predict (self, inputs):
        if not isinstance (inputs, tuple):
            inputs = (inputs,)
        valid_batch_size = len (inputs [0])
        with self.lock:
            for input_detail, input in zip (self.input_details, inputs):
                if valid_batch_size < self.batch_size:
                    pad = np.repeat (np.expand_dims (np.zeros_like (input [0]), 0), self.batch_size - valid_batch_size, 0)
                    input = np.append (input, pad, 0)
                self.interp.set_tensor (input_detail ['index'], input.astype (np.float32))
            self.interp.invoke ()
            outputs = []
            for idx, output_detail in enumerate (self.output_details):
                outputs.append (self.interp.get_tensor (output_detail ['index']) [:valid_batch_size])
            return outputs [0] if len (self.output_details) == 1 else tuple (outputs)
