# ML4B - Finetuning MusicGen

## Introduction

Our goal is to enhance the MusicGen AI model developed by Audiocraft at Facebook, specifically targeting the generation of rap beats. 

## Project Overview

MusicGen has shown its ability to create a variety of music pieces. However, its proficiency in generating rap beats that meet the expectations of potential listeners has been somewhat lacking. Our project aims to finetune this model, based on the medium version of MusicGen, to specifically understand and generate high-quality rap beats reminiscent of the dark, atmospheric, and psychedelic styles of artists like Travis Scott, Don Toliver, and Kid Cudi. The training set exclusively comprises beats from these three artists to ensure the model accurately captures the essence of their music.

## Streamlit App

We built a Streamlit app designed to enable users to generate rap beats quickly and easily. Users have the flexibility to input a textual description of their desired beat or select a predefined style from three options: Travis Scott, Kid Cudi, or Don Toliver. The model, based on the medium version of MusicGen, will generate a beat that mirrors the unique qualities of professional tracks but will maintain the typical length of beats produced by the medium model. Our model focuses on enhancing the quality of rap beats, ensuring they align closely with the atmospheric and psychedelic characteristics associated with these renowned artists. Additionally a beat cover will be generated. The cover gets generated by a diffusion model finetuned on the task of generating rap album covers conditioned on an artist and a beat description. Both the cover and the .wav-file can be downloaded from within the streamlit. Additionally the user can trigger a pipeline that converts the .wav-file into several midi files that can then be uploaded to a music editing program like Flstudio or GarageBand.

![architecture of the project](https://github.com/Benediktherlt/musicgen_finetune_rapbeats/assets/136809065/a6df472c-8b17-494e-8668-b6d8855ae7c2)

## Run the streamlit locally

As of now the model weights are stored on a RunPod instance that you can't access from outside. If you want to have access to that instance and try out the streamlit for yourself, write me an email to benedikt(dot)herlt16(at)gmail(dot)com and I will provide you with an API-key 
We will update this repo soon so that you just need to set our RunPod API-key as an environment variable and the whole ssh connection will be handled by the backend pipeline. 
Let aside all the conveniences we offer for connecting to the RunPod, there is still some things that you need to do manually: 
-create a conda env
-execute "poetry install"
-pip install basic-pitch v. 0.3.3 inside of the conda env (somehow basic-pitch and streamlit are not compatible


## Acknowledgments

This project builds on the foundational work done by Audiocraft - Facebook on the MusicGen model.
We also want to acknowledge Spotify for their great work on the basic-pitch package that we took use of in this project. 


