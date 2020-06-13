import plaidml.keras
plaidml.keras.install_backend()
import keras

from keras.models import Sequential
from keras.optimizers import Adam

Sequential().compile(Adam())
