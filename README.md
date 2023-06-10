# polar-ed

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Usage](#Usage)


## Introduction
Simple implementation of polar encoder and successive cancelation polar decoder. 
Encoder and decoder were created based on [this](https://archive.nptel.ac.in/courses/117/106/108106137/) course.

## Technologies
* matplotlib 3.7.1
* numpy 1.24.3

## Usage

Firstly, install requirements:
```
pip install -r requirements.txt
```
Then, simply run main function. Program will create random massages, encode them, 
send them through AWGN BPSK channel and finally decode. Graph of 
BER and FER vs E<sub>b</sub>/ N<sub>0</sub> will be shown.