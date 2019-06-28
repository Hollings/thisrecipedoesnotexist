#!/usr/bin/env python3

import datetime
import json
import os
import numpy as np
import tensorflow as tf
import random
import pymysql
import time
import requests
import twitter 

import model, sample, encoder
temp = 1

def sendRecipe(text):
    if "<end>" in text:
        text = text.split("<end>")[1]
    recipeParts = text.split("\n")
    title = recipeParts[1]
    ingredients = []
    directions = []
    currentSection = "ingredients"
    for line in recipeParts[2:]:
        if line is "":
            continue
        if "Directions" in line:
            currentSection = "directions"
        elif "Ingredients" in line:
            continue
        else:
            if currentSection is "ingredients":
                ingredients.append(line)
            if currentSection is "directions":
                directions.append(line)  
    print(title)
    if len(title)<200 and len(ingredients)>0 and len(directions)>0:
        f = open("conf.json","r")
        config = json.loads(f.read());
        url = config['url'];
        data = [title, json.dumps(ingredients), json.dumps(directions)]
        response = requests.post(url + '/api/add/', json={'title':data[0], 
                                                      'ingredients':data[1],
                                                      'directions': data[2],
                                                      'temp': temp,
                                                      'password': config['api_pass']})
        return True
    else:
        return False


def sample_random_model(
    model_name='345-recipes-32M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=temp,
    top_k=0,
):
    # print("TEMP IS " + str(temp))
    """
    Run the sample_model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to
     reproduce results
    :nsamples=0 : Number of samples to return, if 0, continues to
     generate samples indefinately.
    :batch_size=1 : Number of batches (only affects speed/memory).
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    """



    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        np.random.seed(seed)
        tf.set_random_seed(seed)

        output = sample.sample_sequence(
            hparams=hparams, length=length,
            start_token=enc.encoder['<|endoftext|>'],
            batch_size=batch_size,
            temperature=temperature, top_k=top_k
        )[:, 1:]

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        saver.restore(sess, ckpt)

        generated = 0
        while True:
            out = sess.run(output)
            for i in range(batch_size):
                generated += batch_size
                text = enc.decode(out[i])
                # print(text)
                sendRecipe(text)

if __name__ == '__main__':
    text = sample_random_model(temperature=temp)
