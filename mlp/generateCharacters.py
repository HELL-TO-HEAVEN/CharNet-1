import tensorflow as tf
import numpy as np
import itertools

class generateChars():
  def __init__(self, classes, inputs, inputString, outCharCount, outputs, chars, charDictList, model):
    self.classes = classes
    self.inputs = inputs
    self.outputs = outputs
    self.chars = chars
    self.model = model
    self.charDictList = charDictList
    self.inputString = inputString
    self.outCharCount = outCharCount

  def genKey(self, inp):
    topred = np.zeros((1,self.classes*self.inputs))
    topred[0][:] = inp[:]
    if self.outputs == 1:
      pred = np.argmax(self.model.predict(topred)[0])
      pred = [self.chars[pred]]
    else:
      pred = self.model.predict(topred)[0]
      pred = [np.argmax(p) for p in pred]
      pred = [self.chars[p] for p in pred]
    return pred
    #return CHARS[np.argmax(pred)]

  def genRecurse(self, instr):
    # initial input
    inp = list(itertools.chain.from_iterable(
        [self.charDictList[self.inputString[i]] for i in range(self.inputs)]
    ))
    for i in range(self.outCharCount):
      res = self.genKey(inp[i*30*self.outputs:])
      inp = inp+list(itertools.chain.from_iterable([self.charDictList[r] for r in res]))
    return inp

  def genStr(self, instr):
    recOut = self.genRecurse(instr)
    out = ''.join(self.chars[np.argmax(recOut[i*self.classes:(i+1)*self.classes])] for i in range(self.outCharCount))
    return out

class GenerateCharsCallback(tf.keras.callbacks.Callback):
  def __init__(self, generateCharsInstance, inputString, inputs):
    self.generateCharsInstance = generateCharsInstance
    self.inputString = inputString
    self.inputs = inputs
  def on_epoch_end(self, batch, logs = {}):
    print(self.generateCharsInstance.genStr(self.inputString)[self.inputs])
    return None