from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap

# Configuration
RESOLUTION = (1080, 1920)  # 9:16 for YouTube Shorts
FPS = 30
FONT_SIZE = 50
TIMER_FONT_SIZE = 120
OUTRO_TEXT_QUIZ = "Subscribe for more quizzes!"
OUTRO_TEXT_FACT = "Subscribe for more fun facts!"
OUTRO_TEXT_EMOJI = "Subscribe for more emoji challenges!"
OUTRO_TEXT_CHARACTER = "Subscribe for more character reveals!"
OUTRO_TEXT_MINIMALIST = "Subscribe for more minimalist challenges!"
OUTRO_TEXT_THEN_NOW = "Subscribe for more comparisons!"
OUTRO_TEXT_OPINION = "Subscribe for more hot takes!"
INTRO_DURATION = 2
OUTRO_DURATION = 3

# Utility functions (load_background, create_text_with_shadow, etc.) remain unchanged
def load_background(media_path, duration):
    """Load and prepare background video or image (GIF, MP4, or Image)."""
    if media_path.endswith(('.mp4', '.mov', '.avi')):
        clip = VideoFileClip(media_path).resize(RESOLUTION)
        if clip.duration < duration:
            num_loops = int(duration / clip.duration) + 1
            clip = concatenate_videoclips([clip] * num_loops).subclip(0, duration)
        else:
            clip = clip.subclip(0, duration)
        return clip
    elif media_path.endswith('.gif'):
        clip = VideoFileClip(media_path).resize(RESOLUTION)
        if clip.duration < duration:
            num_loops = int(duration / clip.duration) + 1
            clip = concatenate_videoclips([clip] * num_loops).subclip(0, duration)
        else:
            clip = clip.subclip(0, duration)
        return clip
    else:  # Image
        return ImageClip(media_path, duration=duration).resize(RESOLUTION)

def create_text_with_shadow(text, font_name, color, size, resolution=RESOLUTION, shadow=True, max_width=900, shake_offset=(0, 0)):
    """Create text with semi-transparent shadow overlay for better readability."""
    img = Image.new('RGBA', resolution, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font_paths = [
            f"C:\\Windows\\Fonts\\{font_name}.ttf",
            f"C:\\Windows\\Fonts\\{font_name.lower()}.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\calibrib.ttf",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]
        font_obj = None
        for path in font_paths:
            if os.path.exists(path):
                font_obj = ImageFont.truetype(path, size)
                break
        if font_obj is None:
            font_obj = ImageFont.load_default()
    except:
        font_obj = ImageFont.load_default()
    
    color_map = {
        'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
        'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
        'neon-green': (57, 255, 20), 'bright-yellow': (255, 234, 0),
        'gold': (255, 215, 0), 'orange': (255, 165, 0)
    }
    text_color = color_map.get(color.lower(), (255, 255, 255)) if isinstance(color, str) else color
    
    lines = []
    for line in text.split('\n'):
        if line.strip():
            wrapped = textwrap.fill(line, width=int(max_width / (size * 0.6)))
            lines.extend(wrapped.split('\n'))
        else:
            lines.append('')
    
    total_height = len(lines) * (size + 15)
    y_offset = (resolution[1] - total_height) // 2 + shake_offset[1]
    
    if shadow:
        padding = 30
        bg_box = Image.new('RGBA', resolution, (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg_box)
        
        max_width_actual = 0
        for line in lines:
            if line.strip():
                bbox = draw.textbbox((0, 0), line, font=font_obj)
                line_width = bbox[2] - bbox[0]
                max_width_actual = max(max_width_actual, line_width)
        
        left = max(20, (resolution[0] - max_width_actual) // 2 - padding + shake_offset[0])
        top = y_offset - padding
        right = min(resolution[0] - 20, left + max_width_actual + 2 * padding)
        bottom = top + total_height + 2 * padding
        bg_draw.rounded_rectangle([left, top, right, bottom], radius=20, fill=(0, 0, 0, 180))
        img = Image.alpha_composite(img, bg_box)
        draw = ImageDraw.Draw(img)
    
    for line in lines:
        if line.strip():
            bbox = draw.textbbox((0, 0), line, font=font_obj)
            text_width = bbox[2] - bbox[0]
            x = (resolution[0] - text_width) // 2
            
            if shadow:
                draw.text((x + 3, y_offset + 3), line, font=font_obj, fill=(0, 0, 0, 200))
            draw.text((x, y_offset), line, font=font_obj, fill=text_color)
        y_offset += size + 15
    
    return np.array(img)

def create_circular_timer(time_left, resolution=RESOLUTION):
    """Create a circular countdown timer overlay."""
    img = Image.new('RGBA', resolution, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = resolution[0] // 2
    center_y = 200
    radius = 80
    
    draw.ellipse([center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius], 
                 fill=(0, 0, 0, 180), outline=(57, 255, 20, 255), width=8)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", TIMER_FONT_SIZE)
    except:
        font = ImageFont.load_default()
    
    text = str(time_left)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2
    
    if time_left <= 3:
        color = (255, 0, 0)
    elif time_left <= 5:
        color = (255, 165, 0)
    else:
        color = (57, 255, 20)
    
    draw.text((text_x, text_y), text, font=font, fill=color)
    
    return np.array(img)

def create_highlight_animation(text, font_name, size, resolution=RESOLUTION):
    """Create highlighted correct answer reveal."""
    img = Image.new('RGBA', resolution, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", size + 20)
    except:
        font = ImageFont.load_default()
    
    wrapped_lines = textwrap.fill(text, width=25).split('\n')
    line_height = size + 30
    total_height = len(wrapped_lines) * line_height
    
    y_start = (resolution[1] - total_height) // 2
    
    max_width = 0
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        max_width = max(max_width, bbox[2] - bbox[0])
    
    x_center = resolution[0] // 2
    
    padding = 40
    for offset in range(30, 0, -5):
        alpha = int(100 * (offset / 30))
        draw.rounded_rectangle([x_center - max_width//2 - offset - padding, y_start - offset - padding,
                              x_center + max_width//2 + offset + padding, y_start + total_height + offset + padding],
                              radius=30, fill=(0, 255, 0, alpha))
    
    draw.rounded_rectangle([x_center - max_width//2 - padding, y_start - padding,
                          x_center + max_width//2 + padding, y_start + total_height + padding],
                          radius=20, fill=(0, 200, 0, 255))
    
    y_pos = y_start
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = x_center - line_width // 2
        draw.text((x, y_pos), line, font=font, fill=(255, 255, 255))
        y_pos += line_height
    
    return np.array(img)

def create_fact_text_with_header(fact_text, font_name, color, size, resolution=RESOLUTION):
    """Create fun fact with 'Did You Know?' header."""
    img = Image.new('RGBA', resolution, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        header_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", size + 15)
        body_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size - 5)
    except:
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    color_map = {
        'white': (255, 255, 255), 'yellow': (255, 255, 0), 'black': (0, 0, 0)
    }
    text_color = color_map.get(color.lower(), (255, 255, 255)) if isinstance(color, str) else color
    
    wrapped_fact = textwrap.fill(fact_text, width=35)
    fact_lines = wrapped_fact.split('\n')
    
    header = "Did You Know?"
    header_bbox = draw.textbbox((0, 0), header, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_height = header_bbox[3] - header_bbox[1]
    
    total_height = header_height + 40 + len(fact_lines) * (size + 10)
    y_start = (resolution[1] - total_height) // 2 + 150
    
    max_width = header_width
    for line in fact_lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        max_width = max(max_width, bbox[2] - bbox[0])
    
    padding = 40
    left = (resolution[0] - max_width) // 2 - padding
    top = y_start - padding
    right = left + max_width + 2 * padding
    bottom = y_start + total_height + padding
    
    bg_box = Image.new('RGBA', resolution, (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_box)
    bg_draw.rounded_rectangle([left, top, right, bottom], radius=20, fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img, bg_box)
    draw = ImageDraw.Draw(img)
    
    header_x = (resolution[0] - header_width) // 2
    draw.text((header_x + 2, y_start + 2), header, font=header_font, fill=(0, 0, 0, 200))
    draw.text((header_x, y_start), header, font=header_font, fill=(255, 215, 0))
    
    y_pos = y_start + header_height + 40
    for line in fact_lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_width = bbox[2] - bbox[0]
        x = (resolution[0] - line_width) // 2
        draw.text((x + 2, y_pos + 2), line, font=body_font, fill=(0, 0, 0, 200))
        draw.text((x, y_pos), line, font=body_font, fill=text_color)
        y_pos += size + 10
    
    return np.array(img)

def apply_blur_to_image(image_path, blur_radius=30):
    """Apply Gaussian blur to an image."""
    img = Image.open(image_path).convert('RGBA')
    img = img.resize(RESOLUTION, Image.Resampling.LANCZOS)
    blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return np.array(blurred)

# Video creation functions
def create_quiz_video(data):
    """Generate quiz video."""
    timer_duration = data.get('timer', 10)
    answer_reveal_duration = 5
    total_duration = INTRO_DURATION + timer_duration + answer_reveal_duration + OUTRO_DURATION
    
    if total_duration > 90:
        total_duration = 90
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    shake_offsets = [(5, 3), (-3, -5), (4, 2), (-2, -3), (0, 0), (3, -2), (-4, 4), (2, -1)]
    frame_duration = INTRO_DURATION / len(shake_offsets)
    
    intro_clips = []
    for offset in shake_offsets:
        intro_img = create_text_with_shadow("Movie Quiz Time!", data.get('font', 'Arial'), 
                                           data.get('font_color', 'white'), FONT_SIZE + 10, shake_offset=offset)
        intro_text = ImageClip(intro_img).set_duration(frame_duration)
        intro_bg = bg_clip.subclip(current_time, current_time + frame_duration)
        
        layers = [intro_bg, intro_text]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + frame_duration))
        
        intro_composite = CompositeVideoClip(layers, size=RESOLUTION)
        intro_clips.append(intro_composite)
        current_time += frame_duration
    
    all_clips.extend(intro_clips)
    
    question_text = f"{data['question']}\n\n" + "\n".join(data['options'])
    question_img = create_text_with_shadow(question_text, data.get('font', 'Arial'),
                                          data.get('font_color', 'white'), FONT_SIZE - 5)
    
    for t in range(timer_duration, 0, -1):
        bg_segment = bg_clip.subclip(current_time, current_time + 1)
        question_overlay = ImageClip(question_img).set_duration(1)
        timer_img = create_circular_timer(t)
        timer_overlay = ImageClip(timer_img).set_duration(1)
        
        layers = [bg_segment, question_overlay, timer_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + 1))
        
        composite = CompositeVideoClip(layers, size=RESOLUTION)
        all_clips.append(composite)
        current_time += 1
    
    answer_img = create_highlight_animation(f"Correct Answer:\n{data['correct_answer']}", 
                                           data.get('font', 'Arial'), FONT_SIZE)
    answer_overlay = ImageClip(answer_img).set_duration(answer_reveal_duration)
    answer_bg = bg_clip.subclip(current_time, current_time + answer_reveal_duration)
    
    layers = [answer_bg, answer_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + answer_reveal_duration))
    
    answer_composite = CompositeVideoClip(layers, size=RESOLUTION)
    all_clips.append(answer_composite)
    current_time += answer_reveal_duration
    
    outro_clips = []
    for offset in shake_offsets:
        outro_img = create_text_with_shadow(OUTRO_TEXT_QUIZ, data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE, shake_offset=offset)
        outro_overlay = ImageClip(outro_img).set_duration(frame_duration)
        outro_bg = bg_clip.subclip(current_time, min(current_time + frame_duration, bg_clip.duration))
        
        layers = [outro_bg, outro_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, min(current_time + frame_duration, bg_clip.duration)))
        
        outro_composite = CompositeVideoClip(layers, size=RESOLUTION)
        outro_clips.append(outro_composite)
        current_time += frame_duration
    
    all_clips.extend(outro_clips)
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Quiz video created: {data['output']}")

def create_fact_video(data):
    """Generate fun fact video."""
    fact_duration = 15
    total_duration = INTRO_DURATION + fact_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    shake_offsets = [(5, 3), (-3, -5), (4, 2), (-2, -3), (0, 0), (3, -2), (-4, 4), (2, -1)]
    frame_duration = INTRO_DURATION / len(shake_offsets)
    
    for offset in shake_offsets:
        intro_img = create_text_with_shadow("Movie Fun Fact!", data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE + 10, shake_offset=offset)
        intro_overlay = ImageClip(intro_img).set_duration(frame_duration)
        intro_bg = bg_clip.subclip(current_time, current_time + frame_duration)
        
        layers = [intro_bg, intro_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + frame_duration))
        
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += frame_duration
    
    fact_img = create_fact_text_with_header(data['fact'], data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE - 5)
    fact_overlay = ImageClip(fact_img).set_duration(fact_duration)
    fact_bg = bg_clip.subclip(current_time, current_time + fact_duration)
    
    layers = [fact_bg]
    if 'poster' in data and os.path.exists(data['poster']):
        poster = ImageClip(data['poster']).resize(height=700).set_position(('center', 150)).set_duration(fact_duration)
        layers.append(poster)
    layers.append(fact_overlay)
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + fact_duration))
    
    fact_composite = CompositeVideoClip(layers, size=RESOLUTION)
    all_clips.append(fact_composite)
    current_time += fact_duration
    
    for offset in shake_offsets:
        outro_img = create_text_with_shadow(OUTRO_TEXT_FACT, data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE, shake_offset=offset)
        outro_overlay = ImageClip(outro_img).set_duration(frame_duration)
        outro_bg = bg_clip.subclip(current_time, min(current_time + frame_duration, bg_clip.duration))
        
        layers = [outro_bg, outro_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, min(current_time + frame_duration, bg_clip.duration)))
        
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += frame_duration
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Fun fact video created: {data['output']}")

def create_emoji_guess_video(data):
    """Generate emoji guessing video."""
    countdown_duration = 3
    reveal_duration = 5
    total_duration = 5 + 7 + countdown_duration + reveal_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    intro_img = create_text_with_shadow("Can you guess the movie?", data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE + 10)
    intro_overlay = ImageClip(intro_img).set_duration(5)
    intro_bg = bg_clip.subclip(current_time, current_time + 5)
    layers = [intro_bg, intro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + 5))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += 5
    
    emoji_text = " ".join(data['emojis'])
    emoji_img = create_text_with_shadow(emoji_text, data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), 120)
    emoji_overlay = ImageClip(emoji_img).set_duration(7)
    emoji_bg = bg_clip.subclip(current_time, current_time + 7)
    layers = [emoji_bg, emoji_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + 7))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += 7
    
    for t in range(countdown_duration, 0, -1):
        timer_img = create_circular_timer(t)
        timer_overlay = ImageClip(timer_img).set_duration(1)
        countdown_bg = bg_clip.subclip(current_time, current_time + 1)
        layers = [countdown_bg, emoji_overlay, timer_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + 1))
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += 1
    
    reveal_text = f"{data['movie_title']}\n\n{data.get('fun_fact', '')}"
    reveal_img = create_text_with_shadow(reveal_text, data.get('font', 'Arial'),
                                        data.get('font_color', 'white'), FONT_SIZE)
    reveal_overlay = ImageClip(reveal_img).set_duration(reveal_duration)
    reveal_bg = bg_clip.subclip(current_time, current_time + reveal_duration)
    
    layers = [reveal_bg]
    if 'poster' in data and os.path.exists(data['poster']):
        poster = ImageClip(data['poster']).resize(height=800).set_position(('center', 100)).set_duration(reveal_duration)
        layers.append(poster)
        reveal_overlay = ImageClip(create_text_with_shadow(reveal_text, data.get('font', 'Arial'),
                                   data.get('font_color', 'white'), FONT_SIZE - 10)).set_duration(reveal_duration).set_position(('center', 1000))
    layers.append(reveal_overlay)
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + reveal_duration))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += reveal_duration
    
    outro_img = create_text_with_shadow(OUTRO_TEXT_EMOJI, data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE)
    outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
    outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
    layers = [outro_bg, outro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Emoji guess video created: {data['output']}")

def create_character_reveal_video(data):
    """Generate character guessing video with zoom/blur reveal."""
    hint_duration = 5
    countdown_duration = 3
    reveal_duration = 5
    total_duration = 5 + hint_duration + countdown_duration + reveal_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    intro_img = create_text_with_shadow("WHO IS THIS MOVIE CHARACTER?", data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE + 5)
    intro_overlay = ImageClip(intro_img).set_duration(5)
    intro_bg = bg_clip.subclip(current_time, current_time + 5)
    
    blurred_char = ImageClip(apply_blur_to_image(data['character_image'], blur_radius=40)).set_duration(5)
    layers = [intro_bg, blurred_char, intro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + 5))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += 5
    
    hint_img = create_text_with_shadow(f"Hint: {data['hint']}", data.get('font', 'Arial'),
                                      data.get('font_color', 'yellow'), FONT_SIZE)
    hint_overlay = ImageClip(hint_img).set_duration(hint_duration)
    hint_bg = bg_clip.subclip(current_time, current_time + hint_duration)
    blurred_char2 = ImageClip(apply_blur_to_image(data['character_image'], blur_radius=30)).set_duration(hint_duration)
    layers = [hint_bg, blurred_char2, hint_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + hint_duration))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += hint_duration
    
    for t in range(countdown_duration, 0, -1):
        timer_img = create_circular_timer(t)
        timer_overlay = ImageClip(timer_img).set_duration(1)
        countdown_bg = bg_clip.subclip(current_time, current_time + 1)
        blurred_char3 = ImageClip(apply_blur_to_image(data['character_image'], blur_radius=20)).set_duration(1)
        layers = [countdown_bg, blurred_char3, timer_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + 1))
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += 1
    
    reveal_img = create_text_with_shadow(f"{data['character_name']}\nfrom {data['movie_title']}", 
                                        data.get('font', 'Arial'),
                                        data.get('font_color', 'white'), FONT_SIZE)
    reveal_overlay = ImageClip(reveal_img).set_duration(reveal_duration).set_position(('center', 1400))
    reveal_bg = bg_clip.subclip(current_time, current_time + reveal_duration)
    clear_char = ImageClip(data['character_image']).resize(height=1200).set_position(('center', 100)).set_duration(reveal_duration)
    layers = [reveal_bg, clear_char, reveal_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + reveal_duration))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += reveal_duration
    
    outro_img = create_text_with_shadow(OUTRO_TEXT_CHARACTER, data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE)
    outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
    outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
    layers = [outro_bg, outro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Character reveal video created: {data['output']}")

def create_minimalist_challenge_video(data):
    """Generate minimalist poster challenge video."""
    display_duration = 6
    reveal_duration = 4
    total_duration = display_duration + reveal_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    guess_img = create_text_with_shadow("GUESS THE MOVIE", data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE + 10)
    guess_overlay = ImageClip(guess_img).set_duration(display_duration).set_position(('center', 200))
    display_bg = bg_clip.subclip(current_time, current_time + display_duration)
    minimalist = ImageClip(data['minimalist_icon']).resize(height=800).set_position(('center', 600)).set_duration(display_duration)
    layers = [display_bg, minimalist, guess_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + display_duration))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += display_duration
    
    reveal_bg = bg_clip.subclip(current_time, current_time + reveal_duration)
    poster = ImageClip(data['movie_poster']).resize(height=1500).set_position(('center', 200)).set_duration(reveal_duration)
    layers = [reveal_bg, poster]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, current_time + reveal_duration))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    current_time += reveal_duration
    
    outro_img = create_text_with_shadow(OUTRO_TEXT_MINIMALIST, data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE)
    outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
    outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
    layers = [outro_bg, outro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Minimalist challenge video created: {data['output']}")

def create_then_now_video(data):
    """Generate then & now comparison video."""
    then_duration = 5
    now_duration = 5
    total_duration = (then_duration + now_duration) * len(data['comparisons']) + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    for comparison in data['comparisons']:
        then_img = create_text_with_shadow(f"THEN ({comparison['then_year']})\n{comparison['name']}", 
                                          data.get('font', 'Arial'),
                                          data.get('font_color', 'white'), FONT_SIZE)
        then_overlay = ImageClip(then_img).set_duration(then_duration).set_position(('center', 1500))
        then_bg = bg_clip.subclip(current_time, current_time + then_duration)
        then_photo = ImageClip(comparison['then_image']).resize(height=1200).set_position(('center', 100)).set_duration(then_duration)
        layers = [then_bg, then_photo, then_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + then_duration))
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += then_duration
        
        now_img = create_text_with_shadow(f"NOW ({comparison['now_year']})\n{comparison['name']}", 
                                         data.get('font', 'Arial'),
                                         data.get('font_color', 'white'), FONT_SIZE)
        now_overlay = ImageClip(now_img).set_duration(now_duration).set_position(('center', 1500))
        now_bg = bg_clip.subclip(current_time, current_time + now_duration)
        now_photo = ImageClip(comparison['now_image']).resize(height=1200).set_position(('center', 100)).set_duration(now_duration)
        layers = [now_bg, now_photo, now_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + now_duration))
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        current_time += now_duration
    
    outro_img = create_text_with_shadow(OUTRO_TEXT_THEN_NOW, data.get('font', 'Arial'),
                                       data.get('font_color', 'white'), FONT_SIZE)
    outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
    outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
    layers = [outro_bg, outro_overlay]
    if logo_clip:
        layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
    all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    if logo_clip:
        logo_clip.close()
    print(f"Then & Now video created: {data['output']}")

# def create_opinion_video(data):
    # """Generate unpopular opinion video."""
    # opinion_duration = 5
    # total_duration = len(data['opinions']) * opinion_duration + OUTRO_DURATION
    
    # bg_clip = load_background(data['background'], total_duration)
    
    # logo_clip = None
    # if 'logo' in data and os.path.exists(data['logo']):
        # try:
            # logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        # except Exception as e:
            # print(f"Warning: Could not load logo - {e}")
    
    # all_clips = []
    # current_time = 0
    
    # for opinion in data['opinions']:
        # opinion_text = f"Unpopular Opinion:\n\n{opinion}"
        # opinion_img = create_text_with_shadow(opinion_text, data.get('font', 'Arial'),
                                             # data.get('font_color', 'white'), FONT_SIZE - 5)
        # opinion_overlay = ImageClip(opinion_img).set_duration(opinion_duration)
        # opinion_bg = bg_clip.subclip(current_time, current_time + opinion_duration)
        # layers = [opinion_bg, opinion_overlay]
        # if logo_clip:
            # layers.append(logo_clip.subclip(current_time, current_time + opinion_duration))
        # all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        # current_time += opinion_duration
    
    # outro_img = create_text_with_shadow(f"{OUTRO_TEXT_OPINION}\n\nTELL US YOUR HOT TAKES!", 
                                       # data.get('font', 'Arial'),
                                       # data.get('font_color', 'white'), FONT_SIZE)
    # outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
    # outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
    # layers = [outro_bg, outro_overlay]
    # if logo_clip:
        # layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
    # all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
    
    # final_clip = concatenate_videoclips(all_clips, method="compose")
    
    # if 'audio' in data and os.path.exists(data['audio']):
        # try:
            # audio = AudioFileClip(data['audio'])
            # if audio.duration < final_clip.duration:
                # num_loops = int(final_clip.duration / audio.duration) + 1
                # looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                # looped_audio = looped_audio.subclip(0, final_clip.duration)
                # final_clip = final_clip.set_audio(looped_audio)
            # else:
                # final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        # except Exception as e:
            # print(f"Warning: Could not add audio - {e}")
    
    # os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    # final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
    # final_clip.close()
    # bg_clip.close()
    # if logo_clip:
        # logo_clip.close()
    # print(f"Opinion video created: {data['output']}")





def create_opinion_video(data):
    """Generate unpopular opinion video."""
    opinion_duration = 5
    total_duration = len(data['opinions']) * opinion_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    logo_clip = None
    try:
        if 'logo' in data and os.path.exists(data['logo']):
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        
        all_clips = []
        current_time = 0
        
        for opinion in data['opinions']:
            opinion_text = f"Unpopular Opinion:\n\n{opinion}"
            opinion_img = create_text_with_shadow(opinion_text, data.get('font', 'Arial'),
                                                 data.get('font_color', 'white'), FONT_SIZE - 5)
            opinion_overlay = ImageClip(opinion_img).set_duration(opinion_duration)
            opinion_bg = bg_clip.subclip(current_time, current_time + opinion_duration)
            layers = [opinion_bg, opinion_overlay]
            if logo_clip:
                layers.append(logo_clip.subclip(current_time, current_time + opinion_duration))
            all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
            current_time += opinion_duration
        
        outro_img = create_text_with_shadow(f"{OUTRO_TEXT_OPINION}\n\nTELL US YOUR HOT TAKES!", 
                                           data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE)
        outro_overlay = ImageClip(outro_img).set_duration(OUTRO_DURATION)
        outro_bg = bg_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration))
        layers = [outro_bg, outro_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, min(current_time + OUTRO_DURATION, bg_clip.duration)))
        all_clips.append(CompositeVideoClip(layers, size=RESOLUTION))
        
        final_clip = concatenate_videoclips(all_clips, method="compose")
        
        if 'audio' in data and os.path.exists(data['audio']):
            try:
                audio = AudioFileClip(data['audio'])
                if audio.duration < final_clip.duration:
                    num_loops = int(final_clip.duration / audio.duration) + 1
                    looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                    looped_audio = looped_audio.subclip(0, final_clip.duration)
                    final_clip = final_clip.set_audio(looped_audio)
                else:
                    final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
                audio.close()
            except Exception as e:
                print(f"Warning: Could not add audio - {e}")
        
        os.makedirs(os.path.dirname(data['output']), exist_ok=True)
        final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, audio_codec='aac', threads=4)
        print(f"Opinion video created: {data['output']}")
    finally:
        try:
            bg_clip.close()
        except Exception as e:
            print(f"Warning: Failed to close bg_clip - {e}")
        if logo_clip:
            try:
                logo_clip.close()
            except Exception as e:
                print(f"Warning: Failed to close logo_clip - {e}")
        try:
            final_clip.close()
        except Exception as e:
            print(f"Warning: Failed to close final_clip - {e}")










# Process input and GUI functions
def process_input(input_file):
    """Process JSON input."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    for idx, data in enumerate(data_list, 1):
        print(f"\nGenerating video {idx}/{len(data_list)}...")
        video_type = data.get('type')
        
        if video_type == 'quiz':
            create_quiz_video(data)
        elif video_type == 'fact':
            create_fact_video(data)
        elif video_type == 'emoji_guess':
            create_emoji_guess_video(data)
        elif video_type == 'character_reveal':
            create_character_reveal_video(data)
        elif video_type == 'minimalist_challenge':
            create_minimalist_challenge_video(data)
        elif video_type == 'then_now':
            create_then_now_video(data)
        elif video_type == 'opinion':
            create_opinion_video(data)
        else:
            print(f"Unknown video type: {video_type}")

def run_gui():
    """Simple GUI."""
    root = tk.Tk()
    root.title("YouTube Shorts Generator")
    root.geometry("400x150")
    
    tk.Label(root, text="YouTube Shorts Video Generator", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Select Input JSON File").pack()
    
    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                process_input(file_path)
                messagebox.showinfo("Success", "Videos generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {str(e)}")
    
    tk.Button(root, text="Browse & Generate", command=browse_file, 
              bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=10).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_input(sys.argv[1])
    else:
        run_gui()