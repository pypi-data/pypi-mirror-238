import keras_core as keras
from keras import Model
from keras.applications import MobileNetV2
from keras.layers import (
    Concatenate,
    Conv2D,
    Dense,
    GlobalAveragePooling2D,
    Input,
    MaxPooling2D,
    Multiply,
    Reshape,
    UpSampling2D,
)


def se_block(input_tensor, ratio=16):
    channel = input_tensor.shape[-1]

    se = GlobalAveragePooling2D()(input_tensor)
    se = Reshape((1, 1, channel))(se)
    se = Dense(
        channel // ratio,
        activation="relu",
        kernel_initializer="he_normal",
        use_bias=False,
    )(se)
    se = Dense(
        channel,
        activation="sigmoid",
        kernel_initializer="he_normal",
        use_bias=False,
    )(se)

    x = Multiply()([input_tensor, se])
    return x


def fusion_dense_block(x, growth_rate, num_blocks):
    for _ in range(num_blocks):
        x_se = se_block(x)
        x = Conv2D(growth_rate, (3, 3), padding="same", activation="relu")(x)
        x = Concatenate(axis=-1)([x, x_se])
    return x


class FastMDE(Model):
    """
    The FastMDE model is a network that allows for quick
    and efficient Monocular Depth Estimation using
    Squeeze-and-Excite blocks.

    Example Usage:
        ```python
        input_shape = (256, 256, 3)

        model = FastMDE()
        ```
    """

    def __init__(self, input_shape=(256, 256, 3)):
        super(FastMDE, self).__init__()
        self.encoder = MobileNetV2(
            input_shape=input_shape, include_top=False, weights="imagenet"
        )

        self.conv4 = fusion_dense_block(
            self.encoder.get_layer("block_16_project_BN").output, 512, 4
        )
        self.up5 = UpSampling2D(size=(2, 2))(self.conv4)
        self.conv5 = fusion_dense_block(self.up5, 256, 4)
        self.up6 = UpSampling2D(size=(2, 2))(self.conv5)
        self.conv6 = fusion_dense_block(self.up6, 128, 4)
        self.up7 = UpSampling2D(size=(2, 2))(self.conv6)
        self.conv8 = fusion_dense_block(self.up7, 128, 4)
        self.conv9 = fusion_dense_block(self.conv8, 64, 4)
        self.output_layer = Conv2D(
            1, (3, 3), activation="sigmoid", padding="same"
        )

    def call(self, inputs):
        x = self.encoder(inputs)
        x = self.conv4(x)
        x = self.up5(x)
        x = self.conv5(x)
        x = self.up6(x)
        x = self.conv6(x)
        x = self.up7(x)
        x = self.conv8(x)
        x = self.conv9(x)
        output = self.output_layer(x)
        return output
