#!/usr/bin/env python3

import fire
import datetime
import json
import os
import numpy as np
import tensorflow as tf
import random


import model, sample, encoder
temp = 1
def saveToIndex(num):
    temp = random.uniform(0.5, 2.0)
    # num = random.randint(0,1000);
    text = fire.Fire(sample_model)
    try:
        if "<end>" in text:
            text = text.split("<end>")[1]
        recipeParts = text.split("\n")
        finalIndex = '''
        <head>

            <style>
                .ing p {
                margin: 0 15px;
                }

                .dir p {
                    margin: 15px;
                }
                .dir, .ing{
                    margin-top:50px
                }

                .container {
                    margin-top: 50px;
                    margin-bottom: 50px;
                }
        .container .content{
border: 1px solid #cacaca
}
                .footer {
                    text-align: center;
                    color: #adb5bd;
                    font-size: 10px;
                }
            </style>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        </head>
        <div class="container"><div class="content shadow p-3 mb-5 bg-light rounded"><h1>''' + recipeParts[1] + "</h1>"
        for line in recipeParts[2:]:
            if line is "":
                continue
            if "Directions" in line:
                finalIndex += "</div><div class='dir'><h2>Directions</h2>"
            elif "Ingredients" in line:
                finalIndex += "<div class='ing'><h2>Ingredients</h2>"
            else:
                finalIndex += "<p>- " + line + "</p>"

        finalIndex += "</div></div></div><div class='footer'>Recipe generated with temp of " + str(round(temp,3)) + " at "+datetime.datetime.now().strftime('%B %d %Y %I:%M%p')+"</div>"

        if not os.path.exists(str(num)):
            os.makedirs(str(num))
        f = open(str(num) + "/index.html", "w")
        f.write(finalIndex)
    except:
        pass

def sample_model(
    model_name='345-recipes',
    seed=None,
    nsamples=1,
    batch_size=8,
    length=None,
    temperature=temp,
    top_k=0,
):
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
        while nsamples == 0 or generated < nsamples:
            out = sess.run(output)
            for i in range(batch_size):
                generated += batch_size
                text = enc.decode(out[i])
                return(text)

if __name__ == '__main__':
    while(True):
        saveToIndex(random.randint(0,5000))