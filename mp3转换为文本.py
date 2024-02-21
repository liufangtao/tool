'''
1、把mp3格式转换成wav格式
'''
# import soundfile
# data, samplerate = soundfile.read('李坤仑协商退款金额.mp3')
# soundfile.write('李坤仑协商退款金额new.wav', data, samplerate, subtype='PCM_16')

'''
2、把一个wav切成100秒每小段
'''
# from pydub import AudioSegment
# import os
# # 定义输入WAV文件路径
# input_wav_file = "/1T/liufangtao/tool/李坤仑协商退款金额new.wav"
# output_folder = '/1T/liufangtao/tool/wav'
# os.makedirs(output_folder, exist_ok = True)

# # 定义每个音频片段的时长（毫秒）
# segment_duration = 10000  # 例如，切分为10秒一段

# # 使用pydub加载音频文件
# audio = AudioSegment.from_wav(input_wav_file)

# # 获取音频的总时长（毫秒）
# total_duration = len(audio)

# # 计算需要切分的片段数量
# num_segments = total_duration // segment_duration

# # 切分音频并保存每个片段
# for i in range(num_segments):
#     start_time = i * segment_duration
#     end_time = (i + 1) * segment_duration

#     # 切分音频片段
#     segment = audio[start_time:end_time]

#     # 定义输出音频片段的文件名
#     output_wav_file = os.path.join(output_folder, f"segment_{i}.wav")

#     # 保存音频片段为WAV文件
#     segment.export(output_wav_file, format="wav")

#     print(f"保存音频片段 {i} 到 {output_wav_file}")

# print("切分完成")
#############################################
'''
3、开始语音wav转换为文字,并保存到txt中。
'''
import os
import glob
import paddlehub as hub
from tqdm import tqdm

def custom_sort(item):
    # 使用正则表达式从字符串末尾提取数字部分，并转换为整数
    import re
    match = re.search(r'\d+$', item[:-4])
    if match:
        return int(match.group())
    else:
        return 0  # 如果没有数字，则默认为0

model = hub.Module(
    name='u2_conformer_wenetspeech',
    version='1.0.0')

folder_path = '/1T/liufangtao/tool/wav'
wav_files = glob.glob(os.path.join(folder_path, "*.wav"))
wav_files = sorted(wav_files, key=custom_sort)

for wav_file in tqdm(wav_files):
    text = model.speech_recognize(wav_file)
    print(text)
    with open("speech_to_text.txt", "a", encoding="utf-8") as file:         
        file.write(text)


