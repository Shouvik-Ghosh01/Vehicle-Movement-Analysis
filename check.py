import tensorflow as tf

try:
    from tensorflow.lite.python.interpreter import Interpreter
    print("TensorFlow Lite imported successfully!")
except ImportError:
    print("Error importing TensorFlow Lite")