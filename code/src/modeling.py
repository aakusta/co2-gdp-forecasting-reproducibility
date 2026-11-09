"""Keras model constructors shared with the V3 GRU architecture."""

import numpy as np


def require_tensorflow():
    try:
        import tensorflow as tf  # type: ignore
    except Exception as exc:  # pragma: no cover - runtime dependency gate
        raise RuntimeError(
            "claim downgrade required: TensorFlow/Keras is not available. "
            "Install TensorFlow and rerun the GRU-locked pipeline."
        ) from exc

    try:
        tf.config.experimental.enable_op_determinism()
    except Exception:
        pass
    return tf


def _set_seed(tf, seed: int) -> None:
    import random

    random.seed(seed)
    np.random.seed(seed)
    tf.keras.utils.set_random_seed(seed)


def build_mt_gru_model(
    tf,
    lookback: int,
    n_features: int,
    units: int,
    dense_units: int,
    dropout: float,
    learning_rate: float,
):
    inp = tf.keras.Input(shape=(lookback, n_features), name="sequence_input")
    x = tf.keras.layers.GRU(units, dropout=dropout, recurrent_dropout=0.0, name="shared_gru")(inp)
    x = tf.keras.layers.Dense(dense_units, activation="relu", name="shared_dense")(x)
    out = tf.keras.layers.Dense(2, activation="linear", name="task_outputs")(x)
    model = tf.keras.Model(inputs=inp, outputs=out, name="MT-GRU")
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    return model


def build_st_gru_model(
    tf,
    lookback: int,
    n_features: int,
    units: int,
    dense_units: int,
    dropout: float,
    learning_rate: float,
):
    inp = tf.keras.Input(shape=(lookback, n_features), name="sequence_input")
    x = tf.keras.layers.GRU(units, dropout=dropout, recurrent_dropout=0.0, name="gru")(inp)
    x = tf.keras.layers.Dense(dense_units, activation="relu", name="dense")(x)
    out = tf.keras.layers.Dense(1, activation="linear", name="target_output")(x)
    model = tf.keras.Model(inputs=inp, outputs=out, name="ST-GRU")
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    return model
