

YouTube Shorts Maker

Automatically generate **quiz** and **fun fact** videos for YouTube Shorts, TikTok, or Reels using MoviePy.
The script combines images, GIFs, videos, text, and audio to produce dynamic short videos — perfect for movie, trivia, or pop culture content creators.
 Features

✅ Generate **quiz** videos with timers, questions, and animated answer reveals
✅ Generate **fact** videos with “Did You Know?” headers
✅ Automatic **intro/outro animations** and text shadows
✅ Supports **GIFs, MP4 backgrounds, logos, and background music**
✅ Uses customizable fonts and colors
✅ GUI for easy use *(no coding required)* or CLI mode for automation

Project Structure

Youtube-Shorts-Maker/
│
├── video_maker.py          # Main script
├── inputs/                 # All media and configuration files
│   ├── input.json          # Defines your quizzes and facts
│   ├── moviecity-logo.jpg  # Logo overlay
│   ├── background_music.mp3
│   ├── BebasNeue-Regular.ttf
│   ├── movie_clip.gif
│   └── HIM_POSTER.jpg
│
└── outputs/                # Generated videos appear here
    ├── quiz_HIM.mp4
    └── him_fact.mp4


Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate

How to Run


python video_maker.py inputs/input.json

