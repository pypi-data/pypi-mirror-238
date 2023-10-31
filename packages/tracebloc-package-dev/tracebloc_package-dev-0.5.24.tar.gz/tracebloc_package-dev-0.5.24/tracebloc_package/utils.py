import tensorflow_datasets as tfds
import tensorflow as tf
import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
from tensorflow_datasets.testing import mock_data
from importlib.machinery import SourceFileLoader
import base64
import os
import ast
import pickle
import pickletools

MODEL_PARAMS_LIMIT = 170000000
TENSORFLOW_FRAMEWORK = "tensorflow"
PYTORCH_FRAMEWORK = "pytorch"
CONSTANT = "constant"
STANDARD = "standard"
ADAPTIVE = "adaptive"
CUSTOM = "custom"
TYPE = "type"
FUNCTION = "function"
VALUE = "value"
PRETRAINED_WEIGHTS_FILENAME = "pretrained_weights"
TRAINED_WEIGHTS_FILENAME = "trained_weights"
AVERAGED_WEIGHTS_PATH = "averaged"
SUCCESS = "success"
TORCH_HUB_PATTERN = "torch.hub"


def check_MyModel(filename, path):
    try:
        # check if file contains the MyModel function
        model = SourceFileLoader(filename, f"{path}").load_module()
        model.MyModel(input_shape=(500, 500, 3), classes=10)
        return True, model

    except AttributeError:
        return (
            False,
            "Model file not provided as per docs: No function with name MyModel",
        )
    except TypeError:
        return (
            False,
            "Model file not provided as per docs: MyModel function receives no arguments",
        )
    except ValueError:
        return False, "Layers shape is not compatible with model input shape"


def is_model_supported(model_obj):
    tensorflow_supported_apis = (tf.keras.models.Sequential, tf.keras.Model)
    supported = isinstance(model_obj, tensorflow_supported_apis)
    if supported:
        # check if it of subclassing
        try:
            # Note that the `input_shape` property is only available for Functional and Sequential models.
            input_shape = model_obj.input_shape
            return True
        except AttributeError:
            return False


# function to check if layers used in tensorflow are supported
def layer_instance_check(model):
    model_layers = model.layers
    for layer in model_layers:
        if not isinstance(layer, tf.keras.layers.Layer):
            return False, []
    return True, model_layers


def is_valid_method(text):
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        return False
    return True


def get_base64_encoded_code(code):
    if not is_valid_method(code):
        raise ValueError("Input is not a valid Python method")
    code_bytes = code.encode("utf-8")
    return base64.b64encode(code_bytes).decode("utf-8")


def getImagesCount(images_count):
    count = 0
    for key in images_count.keys():
        count += images_count[key]
    return count


def get_model_info(model):
    # For Sequential model
    if isinstance(model, tf.keras.Sequential):
        # Get the input shape
        try:
            model_input_shape = model.input_shape[1:]
        except:
            raise ValueError(
                "Unable to determine input shape for the Sequential model."
            )

        # Get the number of output classes
        try:
            model_output_classes = model.layers[-1].units
        except:
            raise ValueError(
                "Unable to determine number of output classes for the Sequential model."
            )

    # For Functional model
    elif isinstance(model, tf.keras.Model):
        # Get the input shape
        try:
            model_input_shape = model.layers[0].input_shape[0][1:]
        except:
            raise ValueError(
                "Unable to determine input shape for the Functional model."
            )

        # Get the number of output classes
        try:
            output_shape = model.output_shape
            if len(output_shape) == 2:
                model_output_classes = output_shape[1]
            else:
                raise ValueError
        except:
            raise ValueError(
                "Unable to determine number of output classes for the Functional model."
            )

    else:
        raise ValueError("Model is neither Sequential nor Functional.")

    return model_input_shape, model_output_classes


def dummy_dataset(input_shape, num_classes, batch_size=8, num_examples=1000):
    # Create random images
    images = np.random.randint(0, 256, size=(num_examples,) + input_shape).astype(
        np.uint8
    )
    # Create random labels
    labels = np.random.randint(0, num_classes, size=(num_examples,))
    # One-hot encode the labels
    labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)

    # Convert to TensorFlow datasets
    ds = tf.data.Dataset.from_tensor_slices((images, labels))

    return ds.batch(batch_size)


def test_code():
    main_method = "MyModel"
    input_shape = "input_shape"
    output_classes = "output_classes"

    def MyModel(input_shape=(224, 224, 3), output_classes=3):
        base_mobilenet_model = MobileNet(
            input_shape=input_shape, include_top=False, weights=None
        )
        multi_disease_model = Sequential()
        multi_disease_model.add(base_mobilenet_model)
        multi_disease_model.add(GlobalAveragePooling2D())
        multi_disease_model.add(Dropout(0.5))
        multi_disease_model.add(Dense(output_classes, activation="sigmoid"))
        return multi_disease_model


def get_model_parameters(**kwargs) -> None:
    if kwargs["framework"] == PYTORCH_FRAMEWORK:
        parameters = [
            val.cpu().numpy() for _, val in kwargs["model"].state_dict().items()
        ]
    else:
        parameters = kwargs["model"].get_weights()
    with open(
        os.path.join(kwargs["weight_file_path"], f"{kwargs['weights_file_name']}.pkl"),
        "wb",
    ) as f:
        pickled = pickle.dumps(parameters)
        optimized_pickle = pickletools.optimize(pickled)
        f.write(optimized_pickle)
    del parameters


def get_model_output(model) -> int:
    dummy_data = np.random.rand(1, 224, 224, 3)
    # Get prediction
    predictions = model.predict(dummy_data)

    # return the class output
    return np.argmax(predictions[0])


def validate_kwargs(
    kwargs, allowed_kwargs, error_message="Keyword argument not understood:"
):
    """Checks that all keyword arguments are in the set of allowed keys."""
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise TypeError(error_message, kwarg)


def get_model_params_count(framework="tensorflow", model=None) -> int:
    """
    calculate total trainable parameters of a given model
    """
    if framework == TENSORFLOW_FRAMEWORK:
        return model.count_params()
    else:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
