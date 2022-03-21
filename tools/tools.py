from vosk import Model, KaldiRecognizer
import json, wave, re


def init_model(path='vosk-model-small-ru-0.22'):
    model = Model(path)
    return model


def trasncribize(model, wavfile):
    wf = wave.open(wavfile, "rb")
    rcgn_fr = wf.getframerate() * wf.getnchannels()
    rec = KaldiRecognizer(model, rcgn_fr)
    result = ''
    last_n = False
    #read_block_size = 4000 
    read_block_size = wf.getnframes()
    while True:
        data = wf.readframes(read_block_size)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            
            if res['text'] != '':
                result += f" {res['text']}"
                if read_block_size < 200000:
                    print(res['text'] + " \n")
                
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True

    res = json.loads(rec.FinalResult())
    result += f" {res['text']}"
    final_result = '\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', result))
    return final_result