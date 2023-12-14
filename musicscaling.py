from flask import Flask, request, render_template, send_from_directory
from scipy.io import wavfile
import numpy as np
import scipy.fft as sp
from tempfile import mkdtemp
import os
from pydub import AudioSegment


import IPython

app = Flask(__name__)
TEMP_FOLDER = mkdtemp()
app.config['TEMP_FOLDER'] = TEMP_FOLDER


def sample(filename, name, selected_animal):
    '''
    returns inputted song with only the frequencies within the hearing
    range of the specified animal
    
    filename be a string. must refer to a .wav file
    '''
    
    # not sure why I need this, but I do!                                                                        
    dst = "test.wav"

    # convert mp3 to wav                                                           
    sound = AudioSegment.from_mp3(filename)
    mp = sound.export(dst, format="wav")
    
    
    # pick threshold based on selected animal
    if selected_animal == 'owl':
        threshold = 12000
    elif selected_animal == 'cockatiel':
        threshold = 8000
    elif selected_animal == 'frog':
        threshold = 4000
    elif selected_animal == 'goldfish':
        threshold = 3000
    elif selected_animal == 'chicken':
        threshold = 2000
    elif selected_animal == 'tuna':
        threshold = 1000
    elif selected_animal == 'bee':
        threshold = 500
    else:
        return render_template('index.html', message='No valid animal selected.')
        
    sample_rate, song = wavfile.read(mp)
    amps = song[:,1]
    n = len(amps)
    
    length = amps.shape[0] / sample_rate
    dt = length / n
    
    freq = np.fft.fftfreq(n,d=dt)
    
    # get coefficients of fft
    co = sp.fft(amps)
    
    # set coefficients outside of upper and lower limit to 0
    for i in range(n):
        if (np.abs(freq[i])>threshold):
            co[i]=0  
        elif (np.abs(freq[i])<250):
            co[i]=0  
        else:
            pass
           
        
    # take inverse fourier transform
    ift = sp.ifft(co).real
    
    # getting name of song
    root = name[0:len(name) -4]
    filename2 = root + selected_animal + '.wav'
    
    # saving to user directory and program's temporary directory
    inverse_wav_path = os.path.join(app.config['TEMP_FOLDER'], filename2)
    audio_data = IPython.display.Audio(ift, rate=sample_rate)
    wavfile.write(inverse_wav_path, rate = sample_rate, data = ift.astype(np.int16))
    
    base = os.getcwd()
    new_directory_path = os.path.join(base, 'output')
    
    try:
        # make uploads file
        os.mkdir(new_directory_path)
    except FileExistsError:
        # need this for when the user has already run the program
        # outputs file will already exits
        pass
    
    filename2path = 'output/' + filename2
    
    # save output to uploads file
    with open(filename2path, 'wb') as f:
        f.write(audio_data.data)
    
    return filename2, audio_data.data, sample_rate



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    render_template('index.html', wavmsg='Enter a .wav file')
    
    #retrieve file
    if request.method == 'POST':
        # error: no file
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        # error: if the user doesn't select a file
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        
        # retrieve selected animal from user
        selected_animal = request.form.get('animal')
                
        # perform fourier analysis        
        inverse_path, transformed_audio_data, sample_rate = sample(file,file.filename, selected_animal)
                
        return render_template('index.html', original_wav=file.filename, inverse_wav=inverse_path, transformed_audio_data=transformed_audio_data, sample_rate=sample_rate, selected_animal = selected_animal)

    return render_template('index.html')

@app.route('/<filename>')
def temp_file(filename):
    '''
    Retrieves file from program directory to play on page
    '''
    return send_from_directory(app.config['TEMP_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)




