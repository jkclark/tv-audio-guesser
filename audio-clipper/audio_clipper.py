import os
import re
import subprocess
from datetime import timedelta

import pysrt
from pymkv import MKVFile


def list_subtitle_tracks(mkv_file_path):
    mkv = MKVFile(mkv_file_path)
    subtitle_tracks = [track for track in mkv.tracks if track.track_type == "subtitles"]
    if not subtitle_tracks:
        raise ValueError("No subtitle tracks found in the MKV file")
    return subtitle_tracks

def extract_subtitles(mkv_file_path, output_srt_path, track_id):
    # Use mkvextract to extract the subtitles
    subprocess.run(["mkvextract", "tracks", mkv_file_path, f"{track_id}:{output_srt_path}"], check=True)

def print_subtitles(srt_file_path):
    subs = pysrt.open(srt_file_path)
    for sub in subs:
        print(f"Start: {sub.start}, End: {sub.end}, Text: {sub.text}")

def merge_subtitles(subs, threshold_ms):
    merged_subs = []
    current_sub = subs[0]
    
    for next_sub in subs[1:]:
        time_diff = next_sub.start.ordinal - current_sub.end.ordinal
        if time_diff <= threshold_ms:
            current_sub.text += " " + next_sub.text
            current_sub.end = next_sub.end
        else:
            merged_subs.append(current_sub)
            current_sub = next_sub
    
    merged_subs.append(current_sub)
    return merged_subs

def extract_audio_clips(mkv_file_path, srt_file_path, output_dir, threshold_ms, ignore_pattern):
    subs = pysrt.open(srt_file_path)
    merged_subs = merge_subtitles(subs, threshold_ms)

    for i, sub in enumerate(merged_subs[:100]):
        # if the subtitle's text entirely matches the ignore_regex, skip it
        if bool(ignore_pattern.fullmatch(sub.text)):
            print(f"Skipping: {sub.text}")
            continue

        start_time = sub.start.to_time()
        end_time = sub.end.to_time()
        text_snippet = sub.text[:25].replace(" ", "_")
        output_audio_path = os.path.join(output_dir, f"{i}_{text_snippet}.mp3")
        
        # Use ffmpeg to extract the audio clip
        subprocess.run([
            "ffmpeg", "-i", mkv_file_path, "-ss", str(start_time), "-to", str(end_time),
            "-q:a", "0", "-map", "a", output_audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def main():
    mkv_file_path = "videos/s3e01.mkv"
    output_srt_path = "subtitles/subtitles.srt"
    output_audio_dir = "audio_clips"
    threshold_ms = 300  # Set the threshold in milliseconds
    
    os.makedirs(output_audio_dir, exist_ok=True)
    
    subtitle_tracks = list_subtitle_tracks(mkv_file_path)
    print("Available subtitle tracks:")
    for i, track in enumerate(subtitle_tracks):
        print(f"{i}: Track ID {track.track_id}, Language: {track.language}")

    # track_index = int(input("Select the subtitle track index: "))
    track_index = 1
    selected_track = subtitle_tracks[track_index]
    
    extract_subtitles(mkv_file_path, output_srt_path, selected_track.track_id)
    # print_subtitles(output_srt_path)

    ignore_pattern = re.compile(r'^\([A-Z\s]*\)$')
    extract_audio_clips(mkv_file_path, output_srt_path, output_audio_dir, threshold_ms, ignore_pattern)

if __name__ == "__main__":
    main()
