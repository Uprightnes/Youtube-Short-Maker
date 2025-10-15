from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import json
import os
from PIL import Image, ImageDraw, ImageFont
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
INTRO_DURATION = 2
OUTRO_DURATION = 3

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
    
    # Load font
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
    
    # Color mapping
    color_map = {
        'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
        'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
        'neon-green': (57, 255, 20), 'bright-yellow': (255, 234, 0)
    }
    text_color = color_map.get(color.lower(), (255, 255, 255)) if isinstance(color, str) else color
    
    # Word wrap text to prevent cutoff
    lines = []
    for line in text.split('\n'):
        if line.strip():
            wrapped = textwrap.fill(line, width=int(max_width / (size * 0.6)))
            lines.extend(wrapped.split('\n'))
        else:
            lines.append('')
    
    # Calculate text positioning (apply shake offset)
    total_height = len(lines) * (size + 15)
    y_offset = (resolution[1] - total_height) // 2 + shake_offset[1]
    
    # Draw semi-transparent background
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
    
    # Draw text
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
    
    # Wrap text
    wrapped_lines = textwrap.fill(text, width=25).split('\n')
    line_height = size + 30
    total_height = len(wrapped_lines) * line_height
    
    y_start = (resolution[1] - total_height) // 2
    
    # Calculate max width
    max_width = 0
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        max_width = max(max_width, bbox[2] - bbox[0])
    
    x_center = resolution[0] // 2
    
    # Glow effect
    padding = 40
    for offset in range(30, 0, -5):
        alpha = int(100 * (offset / 30))
        draw.rounded_rectangle([x_center - max_width//2 - offset - padding, y_start - offset - padding,
                              x_center + max_width//2 + offset + padding, y_start + total_height + offset + padding],
                              radius=30, fill=(0, 255, 0, alpha))
    
    # Main background
    draw.rounded_rectangle([x_center - max_width//2 - padding, y_start - padding,
                          x_center + max_width//2 + padding, y_start + total_height + padding],
                          radius=20, fill=(0, 200, 0, 255))
    
    # Answer text (no checkmark)
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
    
    # Wrap fact text
    wrapped_fact = textwrap.fill(fact_text, width=35)
    fact_lines = wrapped_fact.split('\n')
    
    # Calculate positioning
    header = "Did You Know?"
    header_bbox = draw.textbbox((0, 0), header, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_height = header_bbox[3] - header_bbox[1]
    
    total_height = header_height + 40 + len(fact_lines) * (size + 10)
    y_start = (resolution[1] - total_height) // 2 + 150  # Centered, slightly below poster
    
    # Draw background
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
    
    # Draw header
    header_x = (resolution[0] - header_width) // 2
    draw.text((header_x + 2, y_start + 2), header, font=header_font, fill=(0, 0, 0, 200))
    draw.text((header_x, y_start), header, font=header_font, fill=(255, 215, 0))  # Gold color
    
    # Draw fact lines
    y_pos = y_start + header_height + 40
    for line in fact_lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_width = bbox[2] - bbox[0]
        x = (resolution[0] - line_width) // 2
        draw.text((x + 2, y_pos + 2), line, font=body_font, fill=(0, 0, 0, 200))
        draw.text((x, y_pos), line, font=body_font, fill=text_color)
        y_pos += size + 10
    
    return np.array(img)

def create_quiz_video(data):
    """Generate quiz video with proper clip timing."""
    timer_duration = data.get('timer', 10)
    answer_reveal_duration = 5
    total_duration = INTRO_DURATION + timer_duration + answer_reveal_duration + OUTRO_DURATION
    
    if total_duration > 90:
        total_duration = 90
    
    # Load background for entire duration
    bg_clip = load_background(data['background'], total_duration)
    
    # Load brand logo if provided
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    # Shake animation pattern
    shake_offsets = [(5, 3), (-3, -5), (4, 2), (-2, -3), (0, 0), (3, -2), (-4, 4), (2, -1)]
    frame_duration = INTRO_DURATION / len(shake_offsets)
    
    # INTRO (2 seconds) with shake animation
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
    
    # QUIZ SECTION with timer
    question_text = f"{data['question']}\n\n" + "\n".join(data['options'])
    question_img = create_text_with_shadow(question_text, data.get('font', 'Arial'),
                                          data.get('font_color', 'white'), FONT_SIZE - 5)
    
    # Create each second of timer countdown
    for t in range(timer_duration, 0, -1):
        # Background for this 1 second
        bg_segment = bg_clip.subclip(current_time, current_time + 1)
        
        # Question overlay (persistent)
        question_overlay = ImageClip(question_img).set_duration(1)
        
        # Timer overlay
        timer_img = create_circular_timer(t)
        timer_overlay = ImageClip(timer_img).set_duration(1)
        
        # Composite all layers
        layers = [bg_segment, question_overlay, timer_overlay]
        if logo_clip:
            layers.append(logo_clip.subclip(current_time, current_time + 1))
        
        composite = CompositeVideoClip(layers, size=RESOLUTION)
        all_clips.append(composite)
        current_time += 1
    
    # ANSWER REVEAL (5 seconds)
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
    
    # OUTRO (3 seconds) with shake animation
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
    
    # Concatenate all clips
    final_clip = concatenate_videoclips(all_clips, method="compose")
    
    # Add audio (FIXED for MoviePy 1.x)
    if 'audio' in data and os.path.exists(data['audio']):
        try:
            audio = AudioFileClip(data['audio'])
            if audio.duration < final_clip.duration:
                num_loops = int(final_clip.duration / audio.duration) + 1
                audio_clips = [audio] * num_loops
                looped_audio = concatenate_videoclips([AudioFileClip(data['audio']).set_duration(audio.duration) for _ in range(num_loops)])
                looped_audio = looped_audio.subclip(0, final_clip.duration)
                final_clip = final_clip.set_audio(looped_audio)
            else:
                final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
        except Exception as e:
            print(f"Warning: Could not add audio - {e}")
    
    # Export
    os.makedirs(os.path.dirname(data['output']), exist_ok=True)
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS, 
                               audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    print(f"Quiz video created: {data['output']}")

def create_fact_video(data):
    """Generate fun fact video with poster."""
    fact_duration = 15
    total_duration = INTRO_DURATION + fact_duration + OUTRO_DURATION
    
    bg_clip = load_background(data['background'], total_duration)
    
    # Load brand logo if provided
    logo_clip = None
    if 'logo' in data and os.path.exists(data['logo']):
        try:
            logo_clip = ImageClip(data['logo']).resize(height=120).set_position((50, 50)).set_duration(total_duration)
        except Exception as e:
            print(f"Warning: Could not load logo - {e}")
    
    all_clips = []
    current_time = 0
    
    # Shake animation pattern
    shake_offsets = [(5, 3), (-3, -5), (4, 2), (-2, -3), (0, 0), (3, -2), (-4, 4), (2, -1)]
    frame_duration = INTRO_DURATION / len(shake_offsets)
    
    # Intro with shake animation
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
    
    # Fun Fact with header
    fact_img = create_fact_text_with_header(data['fact'], data.get('font', 'Arial'),
                                           data.get('font_color', 'white'), FONT_SIZE - 5)
    fact_overlay = ImageClip(fact_img).set_duration(fact_duration)
    fact_bg = bg_clip.subclip(current_time, current_time + fact_duration)
    
    # Add poster if provided
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
    
    # Outro with shake animation
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
    
    # Add audio (FIXED)
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
    final_clip.write_videofile(data['output'], codec='libx264', fps=FPS,
                               audio_codec='aac', threads=4)
    final_clip.close()
    bg_clip.close()
    print(f"Fun fact video created: {data['output']}")

def process_input(input_file):
    """Process JSON input."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    for idx, data in enumerate(data_list, 1):
        print(f"\nGenerating video {idx}/{len(data_list)}...")
        if data['type'] == 'quiz':
            create_quiz_video(data)
        elif data['type'] == 'fact':
            create_fact_video(data)

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