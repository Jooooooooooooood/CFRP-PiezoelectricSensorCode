import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, losses, Sequential

# LOAD TRAINING DATA (needs to be coded)
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 250.0  # normalize data

# Separate normal data from anomalies using your labels (1 = normal, 0 = anomaly)
x_train_normal = x_train[y_train == 1]
x_test_normal = x_test[y_test == 1]
x_test_anomalies = x_test[y_test == 0]

# LENGTH OF DATASET (needs to be adjusted when data is collected)
input_dim = 140

# Encoder and Decoder Logic
autoencoder = Sequential([
    # Encoder
    layers.Dense(64, activation="relu", input_shape=(input_dim,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(16, activation="relu"),  # Bottleneck layer

    # Decoder
    layers.Dense(32, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(input_dim, activation="sigmoid")  # Matches input dimension
])
autoencoder.compile(optimizer='adam', loss='mae')

model = autoencoder.fit(
    x_train_normal, x_train_normal,
    epochs=20,
    batch_size=512,
    validation_data=(x_test_normal, x_test_normal),
    shuffle=True
)

# Get reconstruction loss for normal training data
reconstructions = autoencoder.predict(x_train_normal)
train_loss = tf.keras.losses.mae(reconstructions, x_train_normal)

# Set threshold
threshold = np.mean(train_loss) + np.std(train_loss)
print("Anomaly Threshold: ", threshold)

# Saving built model
model.save("PiezoelectricSensor-Error-Detection")
print("Model saved as: " + model.name)
