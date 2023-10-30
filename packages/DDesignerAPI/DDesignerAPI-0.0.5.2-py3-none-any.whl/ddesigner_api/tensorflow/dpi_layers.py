# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import tensorflow as tf
from tensorflow.keras import layers, initializers, regularizers, constraints
from tensorflow.python.keras import backend as K

from .xwn import keras_layers as klayers



##############
# Unit layers
##############
@tf.keras.utils.register_keras_serializable()
class SqueezeAndExcitation2D(layers.Layer):
    def __init__(
        self, 
        filters, 
        data_format=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        # Components
        convolution_0=None, 
        convolution_1=None, 
        activation=None, 
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SqueezeAndExcitation2D, self).__init__(**kwargs)

        self.filters = filters
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        if convolution_0 is None:
            self.conv_0 = klayers.Conv2D(
                se_filters, 
                (1,1),
                strides=(1,1), 
                padding='valid', 
                data_format=data_format,
                use_bias=False, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv_0 = convolution_0

        if activation is None:
            self.act = layers.ReLU()
        else:
            self.act = activation

        if convolution_1 is None:
            self.conv_1 = klayers.Conv2D(
                filters, 
                (1,1),
                strides=(1,1), 
                padding='valid', 
                data_format=data_format,
                use_bias=False, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv_1 = convolution_1

    def call(self, inputs, training=None):
        x = inputs
        x_se = tf.reduce_mean(x, axis=[1,2], keepdims=True)
        x_se = self.conv_0(x_se)
        x_se = self.act(x_se)
        x_se = self.conv_1(x_se)
        x_se = tf.nn.sigmoid(x_se)
        x *= x_se
        return x

    def get_config(self):
        config = {
            'filters' : self.filters,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution_0' : self.conv_0,
            'convolution_1' : self.conv_1,
            'activation' : self.act,
        }
        base_config = super(SqueezeAndExcitation2D, self).get_config()
        base_config.update(config)
        return base_config

@tf.keras.utils.register_keras_serializable()
class SqueezeAndExcitation1D(layers.Layer):
    def __init__(
        self, 
        filters, 
        data_format=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        # Components
        convolution_0=None, 
        convolution_1=None, 
        activation=None, 
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SqueezeAndExcitation1D, self).__init__(**kwargs)

        self.filters = filters
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        if convolution_0 is None:
            self.conv_0 = klayers.Conv1D(
                se_filters, 
                (1,1),
                strides=(1,1), 
                padding='valid', 
                data_format=data_format,
                use_bias=False, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv_0 = convolution_0

        if activation is None:
            self.act = layers.ReLU()
        else:
            self.act = activation

        if convolution_1 is None:
            self.conv_1 = klayers.Conv1D(
                filters, 
                (1,1),
                strides=(1,1), 
                padding='valid', 
                data_format=data_format,
                use_bias=False, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv_1 = convolution_1

    def call(self, inputs, training=None):
        x = inputs
        x_se = tf.reduce_mean(x, axis=1, keepdims=True)
        x_se = self.conv_0(x_se)
        x_se = self.act(x_se)
        x_se = self.conv_1(x_se)
        x_se = tf.nn.sigmoid(x_se)
        x *= x_se
        return x

    def get_config(self):
        config = {
            'filters' : self.filters,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution_0' : self.conv_0,
            'convolution_1' : self.conv_1,
            'activation' : self.act,
        }
        base_config = super(SqueezeAndExcitation1D, self).get_config()
        base_config.update(config)
        return base_config


@tf.keras.utils.register_keras_serializable()
class SubPixelConv2D(layers.Layer):
    def __init__(
        self, 
        filters:int, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Custom
        scale_ratio:int=2,
        # Components
        convolution=None, 
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SubPixelConv2D, self).__init__(**kwargs)

        # Assign
        self.sr = scale_ratio

        self.filters = filters
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        # Conv
        self.conv = klayers.Conv2D(
            filters * (scale_ratio ** 2), 
            kernel_size,
            strides=strides, 
            padding=padding, 
            data_format=data_format,
            dilation_rate=dilation_rate, 
            use_bias=use_bias, 
            kernel_initializer=kernel_initializer, 
            bias_initializer=bias_initializer, 
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,
            dtype=dtype,

            use_transform=self.use_transform, 
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
            **kwargs,
        )

    def call(self, inputs, training=None):
        x = self.conv(inputs)
        x = tf.nn.depth_to_space(x, self.sr)
        return x

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'scale_ratio' : self.sr,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
        }
        base_config = super(SubPixelConv2D, self).get_config()
        base_config.update(config)
        return base_config

@tf.keras.utils.register_keras_serializable()
class EmbeddingCosineSimilarity(layers.Layer):                                                        
    def __init__(
        self,
        classes:int,
        initializer='glorot_uniform',
        regularizer=None,
        dtype='float32',
        **kwargs
    ):
        super(EmbeddingCosineSimilarity, self).__init__(**kwargs)
        self.classes = classes
        self.initializer = initializer
        self.regularizer = regularizer
        self.op_dtype = dtype
                             
    def build(self, input_shape):
        self.channel = input_shape[-1]
        self.w = self.add_weight(
            name='weight',
            shape=(self.channel, self.classes),
            initializer=self.initializer,
            regularizer=self.regularizer,
            dtype=self.op_dtype,
        )
    
    def call(self, inputs, training=None):
        # normalize feature
        x = tf.nn.l2_normalize(x = tf.cast(inputs, self.op_dtype), axis=-1)
        x = x[..., None] * tf.ones((self.classes,), dtype=self.dtype) # (..., E, C)
        
        # normalize weights
        w = tf.nn.l2_normalize(tf.cast(self.w, self.dtype), axis=0)  # (E, C)
        w = tf.broadcast_to(w, tf.shape(x))     # (..., E, C)
        x = tf.reduce_sum(x * w, axis=-2) # (..., C)
        
        return x                                                                                      
    
    def get_config(self):
        config = {
            'classes' : self.classes,
            'initializer' : self.initializer,
            'regularizer' : self.regularizer,
            'dtype' : self.op_dtype,
        }
        base_config = super(EmbeddingCosineSimilarity, self).get_config()
        base_config.update(config)
        return base_config


# @tf.keras.utils.register_keras_serializable()
# # Reference : https://www.kaggle.com/code/danmoller/keras-training-with-float16-test-kernel-2
# class BatchNormalization(layers.Layer):
# 
#     def __init__(self,
#                  axis=-1,
#                  momentum=0.99,
#                  epsilon=1e-3,
#                  center=True,
#                  scale=True,
#                  beta_initializer='zeros',
#                  gamma_initializer='ones',
#                  moving_mean_initializer='zeros',
#                  moving_variance_initializer='ones',
#                  beta_regularizer=None,
#                  gamma_regularizer=None,
#                  beta_constraint=None,
#                  gamma_constraint=None,
#                  **kwargs):
# 
#         super(BatchNormalization, self).__init__(**kwargs)
#         self.supports_masking = True
#         self.axis = axis
#         self.momentum = momentum
#         self.epsilon = epsilon
#         self.center = center
#         self.scale = scale
#         self.beta_initializer = initializers.get(beta_initializer)
#         self.gamma_initializer = initializers.get(gamma_initializer)
#         self.moving_mean_initializer = initializers.get(moving_mean_initializer)
#         self.moving_variance_initializer = (
#             initializers.get(moving_variance_initializer))
#         self.beta_regularizer = regularizers.get(beta_regularizer)
#         self.gamma_regularizer = regularizers.get(gamma_regularizer)
#         self.beta_constraint = constraints.get(beta_constraint)
#         self.gamma_constraint = constraints.get(gamma_constraint)
# 
# 
#     def build(self, input_shape):
#         dim = input_shape[self.axis]
#         if dim is None:
#             raise ValueError('Axis ' + str(self.axis) + ' of '
#                              'input tensor should have a defined dimension '
#                              'but the layer received an input with shape ' +
#                              str(input_shape) + '.')
#         self.input_spec = layers.InputSpec(ndim=len(input_shape),
#                                     axes={self.axis: dim})
#         shape = (dim,)
# 
#         if self.scale:
#             self.gamma = self.add_weight(shape=shape,
#                                          name='gamma',
#                                          initializer=self.gamma_initializer,
#                                          regularizer=self.gamma_regularizer,
#                                          constraint=self.gamma_constraint)
#         else:
#             self.gamma = None
#         if self.center:
#             self.beta = self.add_weight(shape=shape,
#                                         name='beta',
#                                         initializer=self.beta_initializer,
#                                         regularizer=self.beta_regularizer,
#                                         constraint=self.beta_constraint)
#         else:
#             self.beta = None
#         self.moving_mean = self.add_weight(
#             shape=shape,
#             name='moving_mean',
#             initializer=self.moving_mean_initializer,
#             trainable=False)
#         self.moving_variance = self.add_weight(
#             shape=shape,
#             name='moving_variance',
#             initializer=self.moving_variance_initializer,
#             trainable=False)
#         self.built = True
# 
#     def call(self, inputs, training=None):
#         input_shape = K.int_shape(inputs)
#         # Prepare broadcasting shape.
#         ndim = len(input_shape)
#         reduction_axes = list(range(len(input_shape)))
#         del reduction_axes[self.axis]
#         broadcast_shape = [1] * len(input_shape)
#         broadcast_shape[self.axis] = input_shape[self.axis]
# 
#         # Determines whether broadcasting is needed.
#         needs_broadcasting = (sorted(reduction_axes) != list(range(ndim))[:-1])
# 
#         def normalize_inference():
#             if needs_broadcasting:
#                 # In this case we must explicitly broadcast all parameters.
#                 broadcast_moving_mean = K.reshape(self.moving_mean,
#                                                   broadcast_shape)
#                 broadcast_moving_variance = K.reshape(self.moving_variance,
#                                                       broadcast_shape)
#                 if self.center:
#                     broadcast_beta = K.reshape(self.beta, broadcast_shape)
#                 else:
#                     broadcast_beta = None
#                 if self.scale:
#                     broadcast_gamma = K.reshape(self.gamma,
#                                                 broadcast_shape)
#                 else:
#                     broadcast_gamma = None
#                 return tf.nn.batch_normalization(#K.batch_normalization(
#                     inputs,
#                     broadcast_moving_mean,
#                     broadcast_moving_variance,
#                     broadcast_beta,
#                     broadcast_gamma,
#                     #axis=self.axis,
#                     self.epsilon)#epsilon=self.epsilon)
#             else:
#                 return tf.nn.batch_normalization(#K.batch_normalization(
#                     inputs,
#                     self.moving_mean,
#                     self.moving_variance,
#                     self.beta,
#                     self.gamma,
#                     #axis=self.axis,
#                     self.epsilon)#epsilon=self.epsilon)
# 
#         # If the learning phase is *static* and set to inference:
#         if training in {0, False}:
#             return normalize_inference()
# 
#         # If the learning is either dynamic, or set to training:
#         normed_training, mean, variance = K._regular_normalize_batch_in_training(#K.normalize_batch_in_training(
#             inputs, self.gamma, self.beta, reduction_axes,
#             epsilon=self.epsilon)
# 
#         if K.backend() != 'cntk':
#             sample_size = K.prod([K.shape(inputs)[axis]
#                                   for axis in reduction_axes])
#             sample_size = K.cast(sample_size, dtype=K.dtype(inputs))
# 
#             # sample variance - unbiased estimator of population variance
#             variance *= sample_size / (sample_size - (1.0 + self.epsilon))
# 
#         self.add_update([K.moving_average_update(self.moving_mean,
#                                                  mean,
#                                                  self.momentum),
#                          K.moving_average_update(self.moving_variance,
#                                                  variance,
#                                                  self.momentum)],
#                         inputs)
# 
#         # Pick the normalized form corresponding to the training phase.
#         return K.in_train_phase(normed_training,
#                                 normalize_inference,
#                                 training=training)
# 
#     def get_config(self):
#         config = {
#             'axis': self.axis,
#             'momentum': self.momentum,
#             'epsilon': self.epsilon,
#             'center': self.center,
#             'scale': self.scale,
#             'beta_initializer': initializers.serialize(self.beta_initializer),
#             'gamma_initializer': initializers.serialize(self.gamma_initializer),
#             'moving_mean_initializer':
#                 initializers.serialize(self.moving_mean_initializer),
#             'moving_variance_initializer':
#                 initializers.serialize(self.moving_variance_initializer),
#             'beta_regularizer': regularizers.serialize(self.beta_regularizer),
#             'gamma_regularizer': regularizers.serialize(self.gamma_regularizer),
#             'beta_constraint': constraints.serialize(self.beta_constraint),
#             'gamma_constraint': constraints.serialize(self.gamma_constraint)
#         }
#         base_config = super(BatchNormalization, self).get_config()
#         return dict(list(base_config.items()) + list(config.items()))
# 
#     def compute_output_shape(self, input_shape):
#         return input_shape
