import datetime
import os

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from sys import platform

# number of epochs: how many times do you want
# to pass the same batch size to train
# total batch size = total train prediction size
CHECKPOINT_PATH = 'training/model_{accuracy}.hdf5'
CHECKPOINT_DIR = os.path.dirname(CHECKPOINT_PATH)
MODEL_WEIGHT_FILENAME = 'christopher_model.hdf5'


def visualise_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    # Retrieve a list of list results on training and validation prediction
    # sets for each training epoch
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # Get number of epochs
    epochs = range(len(acc))

    # Plot training and validation accuracy per epoch
    plt.plot(epochs, acc)
    plt.plot(epochs, val_acc)
    plt.title('Training and validation accuracy')

    plt.figure()

    # Plot training and validation loss per epoch
    plt.plot(epochs, loss)
    plt.plot(epochs, val_loss)
    plt.title('Training and validation loss')
    plt.show()


class ModelTrainer:
    def __init__(self,
                 train_data_gen,
                 steps_per_epoch,
                 epochs,
                 validation_gen,
                 validation_steps,
                 model):
        self.train_data_gen = train_data_gen
        self.steps_per_epoch = steps_per_epoch
        self.epochs = epochs
        self.validation_gen = validation_gen
        self.validation_steps = validation_steps
        self.model = model

    def load_model_weights(self):
        self.model = tf.keras.model.load_model(MODEL_WEIGHT_FILENAME)
        print('model successfully loaded!')
        self.model.summary()

    def train_model(self):
        cp_callback = tf.keras.callbacks.ModelCheckpoint(CHECKPOINT_PATH,
                                                         save_best_only=True)
        if not (os.path.isdir('./logs')):
            os.mkdir('./logs')

        # Checking OS for TensorBoard compatibility
        if platform == "darwin":
            print('os: OSX detected..')
            if not os.path.isdir('./logs/osx'):
                os.mkdir('./logs/osx')
            tb_log = 'logs/osx'
        elif platform == 'win32':
            print('os: Windows detected..')
            tb_log = "logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tb_callback = TensorBoard(log_dir=tb_log,
                                  histogram_freq=1,
                                  write_graph=True,
                                  write_images=True)
        tb_callback.set_model(self.model)

        if os.path.isfile(MODEL_WEIGHT_FILENAME):
            self.model.load_weights(MODEL_WEIGHT_FILENAME)

        history = self.model.fit_generator(
            self.train_data_gen,
            steps_per_epoch=self.steps_per_epoch,
            epochs=self.epochs,
            validation_data=self.validation_gen,
            validation_steps=self.validation_steps,
            callbacks=[tb_callback],
        )
        self.model.save(MODEL_WEIGHT_FILENAME)
        print('model weights saved!')
        return history



