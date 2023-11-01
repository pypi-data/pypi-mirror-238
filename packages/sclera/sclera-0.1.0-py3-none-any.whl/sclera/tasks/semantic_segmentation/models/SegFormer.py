import keras_core as keras


class PatchEmbedding(keras.layers.Layer):
    """
    image division to sequences (14x14)
    """

    def __init__(self, img_size=224, patch_size=16, embed_dim=768):
        super(PatchEmbedding, self).__init__()
        self.img_size = 224
        self.patch_size = patch_size
        self.n_patches = img_size // patch_size
        self.embed_dim = embed_dim

        self.projection = keras.layers.Conv2D(
            embed_dim,
            kernel_size=patch_size,
            strides=self.patch_size,
            padding="same",
            kernel_initializer=keras.initializers.HeNormal(seed=None),
            bias_initializer=keras.initializers.Zeros(),
        )  # scale=1.0,

    def call(self, inputs, *args, **kwargs):
        batches, height, width, channels = inputs.shape

        # x.shape -> [batches, n_patches, n_patches, embed_dim]
        x = self.projection(inputs)
        x = keras.ops.reshape(x, [batches, -1, self.embed_dim])

        return x


class OverlapPatchEmbedding(keras.layers.Layer):
    def __init__(self, img_size=224, patch_size=7, strides=4, embed_dim=768):
        super(OverlapPatchEmbedding, self).__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.side_length = img_size // patch_size
        self.n_patches = self.side_length**2
        self.embed_dim = embed_dim

        self.projection = keras.layers.Conv2D(
            embed_dim,
            kernel_size=patch_size,
            strides=strides,
            padding="same",
            kernel_initializer=keras.initializers.HeNormal(seed=None),
            bias_initializer=keras.initializers.Zeros(),
        )
        # self.layer_norm = LayerNormalization(epsilon=1e-5)

    def call(self, inputs, *args, **kwargs):
        x = self.projection(inputs)

        batches, height, width, embed_dim = x.shape

        x = keras.ops.reshape(x, [batches, -1, embed_dim])
        # x = self.layer_norm(x)
        return x, height, width


class PositionalEmbedding(keras.layers.Layer):
    """
    positional embedding without class token
    """

    def __init__(self, n_patches=14, embed_dim=768):
        super(PositionalEmbedding, self).__init__()
        self.positional_embedding = None
        self.n_patches = n_patches
        self.embed_dim = embed_dim

    def build(self, input_shape):
        self.positional_embedding = self.add_weight(
            shape=[1, self.n_patches**2, self.embed_dim],
            initializer=keras.initializers.Zeros(),
            trainable=True,
            dtype="float32",
        )

    def call(self, inputs, *args, **kwargs):
        batches, n_patches, embed_dim = inputs.shape
        # assert n_patches == self.n_patches ** 2
        assert embed_dim == self.embed_dim
        return inputs + self.positional_embedding


class MultiHeadSelfAttention(keras.layers.Layer):
    def __init__(
        self,
        embed_dim,
        n_heads=8,
        scaler=None,
        use_bias=True,
        attention_drop_rate=0.0,
        transition_drop_rate=0.0,
    ):
        super(MultiHeadSelfAttention, self).__init__()
        self.n_heads = n_heads
        self.embed_dim = embed_dim
        self.head_dim = embed_dim // n_heads
        self.scaler = self.head_dim**-0.5 if scaler is None else scaler

        self.query_key_value = keras.layers.Dense(
            embed_dim * 3,
            kernel_initializer=keras.initializers.GlorotUniform(),
            use_bias=use_bias,
            bias_initializer=keras.initializers.Zeros(),
        )
        self.transition = keras.layers.Dense(
            embed_dim,
            kernel_initializer=keras.initializers.GlorotUniform(),
            use_bias=use_bias,
            bias_initializer=keras.initializers.Zeros(),
        )

        self.attention_drop = keras.layers.Dropout(attention_drop_rate)
        self.transition_drop = keras.layers.Dropout(transition_drop_rate)

    def call(self, inputs, *args, **kwargs):
        batches, patches, embed_dim = inputs.shape

        qkv = self.query_key_value(inputs)
        qkv = keras.ops.reshape(
            qkv, [batches, patches, 3, self.n_heads, self.head_dim]
        )
        qkv = keras.ops.transpose(qkv, axes=[2, 0, 3, 1, 4])
        query, key, value = qkv[0], qkv[1], qkv[2]

        alpha = keras.ops.matmul(a=query, b=key, transpose_b=True) * self.scaler
        alpha_prime = keras.layers.Softmax(alpha, axis=-1)
        alpha_prime = self.attention_drop(alpha_prime)

        x = keras.ops.matmul(alpha_prime, value)
        x = keras.ops.transpose(x, axes=[0, 2, 1, 3])
        x = keras.ops.reshape(x, [batches, patches, embed_dim])

        x = self.transition(x)
        x = self.transition_drop(x)
        return x


class EfficientMultiHeadAttention(keras.layers.Layer):
    def __init__(
        self,
        embed_dim,
        n_heads=8,
        scaler=None,
        use_bias=True,
        sr_ratio: int = 1,
        attention_drop_rate=0.0,
        projection_drop_rate=0.0,
    ):
        super(EfficientMultiHeadAttention, self).__init__()
        self.embed_dim = embed_dim
        self.n_heads = n_heads
        self.sr_ratio = sr_ratio
        self.head_dim = embed_dim // n_heads
        self.scaler = self.head_dim**-0.5 if scaler is None else scaler

        self.query = keras.layers.Dense(
            embed_dim,
            kernel_initializer=keras.initializers.GlorotUniform(),
            use_bias=use_bias,
            bias_initializer=keras.initializers.Zeros(),
        )
        self.key_value = keras.layers.Dense(
            embed_dim * 2,
            kernel_initializer=keras.initializers.GlorotUniform(),
            use_bias=use_bias,
            bias_initializer=keras.initializers.Zeros(),
        )
        self.projection = keras.layers.Dense(
            embed_dim,
            kernel_initializer=keras.initializers.GlorotUniform(),
            use_bias=use_bias,
            bias_initializer=keras.initializers.Zeros(),
        )

        if sr_ratio > 1:
            self.sample_reduction = keras.layers.Conv2D(
                embed_dim,
                kernel_size=sr_ratio,
                strides=sr_ratio,
                padding="same",
            )
            self.layer_norm = keras.layers.LayerNormalization(epsilon=1e-5)

        self.attention_drop = keras.layers.Dropout(rate=attention_drop_rate)
        self.projection_drop = keras.layers.Dropout(rate=projection_drop_rate)

    def call(self, inputs, height=None, width=None, *args, **kwargs):
        batches, n_patches, embed_dim = inputs.shape
        assert embed_dim == self.embed_dim
        assert height and width and height * width == n_patches

        query = self.query(inputs)
        query = keras.ops.reshape(
            query, [batches, n_patches, self.n_heads, self.head_dim]
        )
        # shape -> [batches, self.n_heads, n_patches, self.head_dim]
        query = keras.ops.transpose(query, axes=[0, 2, 1, 3])

        if self.sr_ratio > 1:
            inputs = keras.ops.reshape(
                inputs, [batches, height, width, embed_dim]
            )
            # shape -> [batches, height/sr, width/sr, embed_dim]
            inputs = self.sample_reduction(inputs)
            inputs = self.layer_norm(inputs)
            # shape -> [batches, height * width/sr ** 2, embed_dim]
            inputs = keras.ops.reshape(inputs, [batches, -1, embed_dim])

        kv = self.key_value(inputs)
        # shape -> [batches, height * width/sr ** 2,
        #  2, self.n_heads, self.head_dim]
        kv = keras.ops.reshape(
            kv, [batches, -1, 2, self.n_heads, self.head_dim]
        )
        # shape -> [2, batches, self.n_heads,
        # height * width/sr ** 2, self.head_dim]
        kv = keras.ops.transpose(kv, axes=[2, 0, 3, 1, 4])
        key, value = kv[0], kv[1]

        # shape -> [batches, self.n_heads,
        # n_patches, height * width/sr ** 2]
        alpha = keras.ops.matmul(a=query, b=key, transpose_b=True) * self.scaler
        alpha_prime = keras.layers.Softmax(alpha, axis=-1)
        alpha_prime = self.attention_drop(alpha_prime)

        # x.shape -> [batches, n_heads, n_patches, head_dim]
        x = keras.ops.matmul(alpha_prime, value)
        x = keras.ops.transpose(x, axes=[0, 2, 1, 3])
        x = keras.ops.reshape(x, [batches, n_patches, embed_dim])

        x = self.projection(x)
        x = self.projection_drop(x)
        return x


class FeedForwardNetwork(keras.layers.Layer):
    def __init__(self, in_features, expansion_rate=4, drop_rate=0.0):
        super(FeedForwardNetwork, self).__init__()
        self.in_units = int(in_features * expansion_rate)
        self.fully_connected0 = keras.layers.Dense(
            self.in_units,
            kernel_initializer=keras.initializers.GlorotUniform(),
            bias_initializer=keras.initializers.Zeros(),
        )
        self.non_linearity = keras.layers.Activation("gelu")
        self.fully_connected1 = keras.layers.Dense(
            in_features,
            kernel_initializer=keras.initializers.GlorotUniform(),
            bias_initializer=keras.initializers.Zeros(),
        )
        self.drop_out = keras.layers.Dropout(rate=drop_rate)

    def call(self, inputs, *args, **kwargs):
        x = self.fully_connected0(inputs)
        x = self.non_linearity(x)
        x = self.drop_out(x)
        x = self.fully_connected1(x)
        x = self.drop_out(x)

        return x


class MixedFeedforwardNetwork(keras.layers.Layer):
    def __init__(
        self, embed_dim, expansion_rate=4.0, out_channels=None, drop_rate=0.0
    ):
        super(MixedFeedforwardNetwork, self).__init__()
        self.out_channels = embed_dim if not out_channels else out_channels
        self.fully_connected0 = keras.layers.Dense(
            int(embed_dim * expansion_rate),
            kernel_initializer=keras.initializers.GlorotUniform(),
            bias_initializer=keras.initializers.Zeros(),
        )
        self.depth_wise = keras.layers.DepthwiseConv2D(
            kernel_size=3, strides=1, padding="same"
        )
        self.non_linearity = keras.layers.Activation("gelu")
        self.fully_connected1 = keras.layers.Dense(
            self.out_channels,
            kernel_initializer=keras.initializers.GlorotUniform(),
            bias_initializer=keras.initializers.Zeros(),
        )
        self.dropout = keras.layers.Dropout(drop_rate)

    def call(self, inputs, height=None, width=None, *args, **kwargs):
        batches, n_patches, embed_dim = inputs.shape
        assert height and width and height * width == n_patches
        x = self.fully_connected0(inputs)
        x = keras.ops.reshape(x, [batches, height, width, -1])
        x = self.depth_wise(x)
        x = keras.ops.reshape(x, [batches, n_patches, -1])
        x = self.non_linearity(x)
        x = self.dropout(x)
        x = self.fully_connected1(x)
        x = self.dropout(x)
        return x


class TransformerBlock(keras.layers.Layer):
    def __init__(
        self,
        embed_dim,
        expansion_rate=4,
        n_heads=8,
        scaler=None,
        use_bias=True,
        attention_drop_rate=0.0,
        transition_drop_rate=0.0,
        drop_rate=0.0,
    ):
        super(TransformerBlock, self).__init__()

        self.layer_norm0 = keras.layers.LayerNormalization(epsilon=1e-5)
        self.multi_head_attention = MultiHeadSelfAttention(
            embed_dim=embed_dim,
            n_heads=n_heads,
            scaler=scaler,
            use_bias=use_bias,
            attention_drop_rate=attention_drop_rate,
            transition_drop_rate=transition_drop_rate,
        )

        self.layer_norm1 = keras.layers.LayerNormalization(epsilon=1e-5)
        self.feedforward = FeedForwardNetwork(
            embed_dim, expansion_rate=expansion_rate, drop_rate=drop_rate
        )
        self.feature_add = keras.layers.Add()

    def call(self, inputs, *args, **kwargs):
        x = self.layer_norm0(inputs)
        x = self.multi_head_attention(x)
        x1 = self.feature_add([inputs, x])

        x = self.layer_norm1(x1)
        x = self.feedforward(x)
        x = self.feature_add([x1, x])
        return x


class SegFormerBlock(keras.layers.Layer):
    def __init__(
        self,
        embed_dim,
        expansion_rate=4,
        n_heads=8,
        scaler=None,
        use_bias=True,
        sr_ratio=1,
        attention_drop_rate=0.0,
        projection_drop_rate=0.0,
        drop_rate=0.0,
    ):
        super(SegFormerBlock, self).__init__()

        self.layer_norm0 = keras.layers.LayerNormalization(epsilon=1e-5)
        self.multi_head_attention = EfficientMultiHeadAttention(
            embed_dim=embed_dim,
            n_heads=n_heads,
            scaler=scaler,
            use_bias=use_bias,
            sr_ratio=sr_ratio,
            attention_drop_rate=attention_drop_rate,
            projection_drop_rate=projection_drop_rate,
        )

        self.layer_norm1 = keras.layers.LayerNormalization(epsilon=1e-5)
        self.feedforward = MixedFeedforwardNetwork(
            embed_dim, expansion_rate=expansion_rate, drop_rate=drop_rate
        )
        self.feature_add = keras.layers.Add()

    def call(self, inputs, height=None, width=None, *args, **kwargs):
        x = self.feature_add(
            [
                inputs,
                self.multi_head_attention(
                    self.layer_norm0(inputs), height=height, width=width
                ),
            ]
        )
        x = self.feature_add(
            [
                x,
                self.feedforward(
                    self.layer_norm1(x), height=height, width=width
                ),
            ]
        )

        return x


# TODO
class MixVisionTransformer(keras.layers.Layer):
    """
    The backbone will return a list of features in each stage sequentially
    """

    def __init__(
        self,
        img_size=224,
        version="B0",
        attention_drop_rate=0.0,
        drop_rate=0.0,
    ):
        super(MixVisionTransformer, self).__init__()
        self.patch_size = [7, 3, 3, 3]
        self.strides = [4, 2, 2, 2]
        self.scaler_factors = [1, 4, 8, 16]
        self.reduction_ratio = [8, 4, 2, 1]
        self.n_heads = [1, 2, 5, 8]
        self.expansion_rates = [8, 8, 4, 4]
        self.version_dict = {
            "B0": {"channels": [32, 64, 160, 256], "n_encoder": [2, 2, 2, 2]},
            "B1": {"channels": [64, 128, 320, 512], "n_encoder": [2, 2, 2, 2]},
            "B2": {"channels": [64, 128, 320, 512], "n_encoder": [3, 3, 6, 3]},
            "B3": {"channels": [64, 128, 320, 512], "n_encoder": [3, 3, 18, 3]},
            "B4": {"channels": [64, 128, 320, 512], "n_encoder": [3, 8, 27, 3]},
            "B5": {"channels": [64, 128, 320, 512], "n_encoder": [3, 6, 40, 3]},
        }

        self.config = self.version_dict[version]

        self.overlap_embedding_list = [
            OverlapPatchEmbedding(
                img_size=img_size // self.scaler_factors[index],
                patch_size=self.patch_size[index],
                strides=self.strides[index],
                embed_dim=self.config["channels"][index],
            )
            for index in range(4)
        ]

        drop_scheduler = keras.ops.linspace(
            0, drop_rate, num=sum(self.config["n_encoder"]), dtype="float64"
        )
        attention_drop_scheduler = keras.ops.linspace(
            0,
            attention_drop_rate,
            num=sum(self.config["n_encoder"]),
            dtype="float64",
        )

        self.stage_module_list = list()
        for index, value in enumerate(self.config["n_encoder"]):
            self.stage_module_list.append(
                [
                    SegFormerBlock(
                        embed_dim=self.config["channels"][index],
                        expansion_rate=self.expansion_rates[index]
                        if version != "B5"
                        else 4,
                        sr_ratio=self.reduction_ratio[index],
                        # FIXME <scheduler not entirely used>
                        attention_drop_rate=attention_drop_scheduler[index],
                        projection_drop_rate=drop_scheduler[index],
                    )
                    for _ in range(value)
                ]
            )

        self.layer_norm_list = [
            keras.layers.LayerNormalization(epsilon=1e-5) for _ in range(4)
        ]

    def call(self, inputs, *args, **kwargs):
        batches = inputs.shape[0]
        features = list()
        x = inputs

        for patch_embedding, segformer_blocks, layer_norm in zip(
            self.overlap_embedding_list,
            self.stage_module_list,
            self.layer_norm_list,
        ):
            x, height, width = patch_embedding(x)
            for segformer_block in segformer_blocks:
                x = segformer_block(x, height=height, width=width)
            x = layer_norm(x)
            x = keras.ops.reshape(x, [batches, height, width, -1])
            features.append(x)

        return features


class ConvolutionalBlock(keras.layers.Layer):
    def __init__(
        self,
        n_filters,
        kernel_size=1,
        strides=1,
        padding="valid",
        batch_norm=True,
        activation="relu",
        drop_rate=0.0,
    ):
        super(ConvolutionalBlock, self).__init__()
        self.down_sample = keras.layers.Conv2D(
            n_filters, kernel_size=kernel_size, strides=strides, padding=padding
        )
        self.batch_norm = (
            keras.layers.BatchNormalization(momentum=0.99, epsilon=1e-6)
            if batch_norm is True
            else keras.layers.Activation("linear")
        )
        self.activation = (
            keras.layers.Activation(activation)
            if activation
            else keras.layers.Activation("linear")
        )
        self.dropout = keras.layers.Dropout(rate=drop_rate)

    def call(self, inputs, *args, **kwargs):
        x = self.activation(self.batch_norm(self.down_sample(inputs)))
        return self.dropout(x)


class MLP(keras.layers.Layer):
    """
    inputs.shape -> [batches, height, width, embed_dim]
    outputs.shape -> [batches, height * width, embed_dim]
    """

    def __init__(self, embed_dim=768):
        super(MLP, self).__init__()
        self.mlp = keras.layers.Dense(
            embed_dim,
            use_bias=True,
            kernel_initializer=keras.initializers.GlorotUniform(),
            bias_initializer=keras.initializers.Zeros(),
        )

    def call(self, inputs, *args, **kwargs):
        batches, height, width, embed_dim = inputs.shape
        x = keras.ops.reshape(inputs, [batches, -1, embed_dim])
        x = self.mlp(x)
        return x


class SegFormerDecoder(keras.layers.Layer):
    """
    inputs from SegFormer backbones, length == 4, shape -> [batches, height_patch, width_patch, embed_dim]
    :return
    """

    def __init__(
        self,
        num_classes,
        version="B0",
        interpolation="bilinear",
        drop_rate=0.0,
    ):
        super(SegFormerDecoder, self).__init__()
        self.up_sampling_scalers = [(4, 4), (8, 8), (16, 16), (32, 32)]

        embed_dim = 256 if version in ["B0", "B1"] else 768

        self.feature_linear_list = [MLP(embed_dim=embed_dim) for _ in range(4)]
        self.feature_up_list = [
            keras.layers.UpSampling2D(
                size=self.up_sampling_scalers[index],
                interpolation=interpolation,
            )
            for index in range(len(self.up_sampling_scalers))
        ]

        self.feature_concat = keras.layers.Concatenate(axis=-1)
        self.dropout = keras.layers.Dropout(rate=drop_rate)
        self.linear_fusion = ConvolutionalBlock(
            embed_dim, kernel_size=1, activation="relu"
        )
        self.outputs = keras.layers.Conv2D(
            num_classes, kernel_size=1, activation="softmax"
        )

    def call(self, inputs, *args, **kwargs):
        assert isinstance(inputs, tuple) or isinstance(inputs, list)
        assert len(inputs) == 4
        batches, height, width, embed_dim = inputs[0].shape

        features_decode = list()
        for index in range(len(inputs)):
            x = self.feature_linear_list[index](inputs[index])
            x = keras.ops.reshape(
                x, [batches, inputs[index].shape[1], inputs[index].shape[2], -1]
            )
            x = self.feature_up_list[index](x)
            features_decode.append(x)

        x = self.feature_concat(features_decode)
        x = self.linear_fusion(x)
        x = self.dropout(x)
        x = self.outputs(x)

        return x


class SegFormer(keras.models.Model):
    def __init__(
        self,
        num_classes,
        img_size=224,
        version="B0",
        attention_drop_rate=0.0,
        drop_rate=0.0,
    ):
        super(SegFormer, self).__init__()
        self.num_classes = num_classes
        self.img_size = img_size
        self.scalers = [4, 8, 16, 32]
        self.encoder = MixVisionTransformer(
            img_size=img_size,
            version=version,
            attention_drop_rate=attention_drop_rate,
            drop_rate=drop_rate,
        )

        self.decoder = SegFormerDecoder(
            num_classes, version=version, drop_rate=drop_rate
        )

    def call(self, inputs, training=None, mask=None):
        features = self.encoder(inputs)
        x = self.decoder(features)

        assert len(features) == 4
        for index in range(len(features)):
            assert (
                features[index].shape[1] == self.img_size // self.scalers[index]
            )
            assert (
                features[index].shape[2] == self.img_size // self.scalers[index]
            )

        return x
