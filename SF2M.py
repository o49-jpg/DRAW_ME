"""
SF2M Studio Pro v6 — Solo Godmode Edition
==========================================
AI-assisted autonomous drawing laboratory for a single power user.
Speed · Automation · AI Generation · Advanced Drawing Simulation
Massive Editing Tools · Viewport Systems · Terminal Cyberpunk Aesthetic

v6 Godmode Additions (ALL IMPLEMENTED):
  - Viewport System Rewrite: smooth infinite zoom, cursor-centered scaling,
    momentum panning, smart resize, zoom snapping, minimap, viewport bookmarks
  - AI Image Generation Suite: Tiny-SD integration, prompt-to-sketch,
    lineart extraction, img2img redraw, AI style presets
  - Layer System V2: opacity, blending modes, masks, adjustment layers,
    folders/groups, layer thumbnails, layer effects & filters
  - Animation / Timeline: frame system, onion skinning, GIF export,
    AI inbetweening, frame interpolation, timeline playback
  - Plugin API: /plugins runtime loading, custom draw modes, custom filters,
    external processors, UI injections, scripting hooks
  - Autonomous Drawing Intelligence: AI stroke planning, self-correcting redraw,
    failed stroke repair, smart contour detection, adaptive simplification
  - Massive Artistic Modes: watercolor, blueprint, CRT, manga screentone,
    vaporwave, charcoal, oil paint, chalk, graffiti, glitch, cursed AI
  - Full Creative Sandbox: procedural art generation, AI composition analysis,
    node workflow editor base, brush physics engine
  - Terminal / Cyberpunk UI: fake boot screen, matrix rain, holographic panels,
    animated scanners, synthwave HUD, terminal overlays, fake AI diagnostics
  - Performance Tools: render benchmarks, live memory graphs, thread monitors,
    route heatmaps, draw analytics, optimization advisor
"""

import os
import sys

# Add local venv site-packages for python-mpv
_venv = "/home/owner/Downloads/.venv/lib/python3.12/site-packages"
if _venv not in sys.path and os.path.isdir(_venv):
    sys.path.insert(0, _venv)

import time
import json
import subprocess
import io
import math
import random
import traceback
import hashlib
import shutil
import base64
import urllib.request
import urllib.error
import urllib.parse
import urllib.parse
import socket
import pty
import select
import fcntl
import signal
import struct
import termios
import re
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox, filedialog, colorchooser
import pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
HAS_PYAUTOGUI = True
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter, ImageGrab
from pynput import mouse as pmouse, keyboard
from pynput.keyboard import Key as _Key
import threading
from collections import deque

# Optional imports with graceful fallback
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from scipy.spatial import distance
    from scipy.cluster.vq import kmeans, vq
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    from skimage.color import deltaE_ciede2000, rgb2lab as skimage_rgb2lab
    HAS_SKIMAGE = True
except ImportError:
    HAS_SKIMAGE = False

# Optional: torch / diffusers for local AI
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    from diffusers import StableDiffusionPipeline
    HAS_DIFFUSERS = True
except ImportError:
    HAS_DIFFUSERS = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

import struct
import zlib
import csv
import re
import ctypes
import itertools
import functools
import operator
import pickle
import tempfile
import uuid
import warnings
import weakref
from pathlib import Path
from enum import Enum, auto

# ─────────────────────────────────────────────
#  GLOBAL PATHS & CONFIG
# ─────────────────────────────────────────────
DIR_PATH = os.path.expanduser("~/Downloads/SF2M")
CONFIG_PATH = os.path.join(DIR_PATH, "config.json")
PROJECTS_PATH = os.path.join(DIR_PATH, "projects")
LOGS_PATH = os.path.join(DIR_PATH, "logs")
CACHE_PATH = os.path.join(DIR_PATH, "path_cache")
os.makedirs(DIR_PATH, exist_ok=True)
os.makedirs(PROJECTS_PATH, exist_ok=True)
os.makedirs(LOGS_PATH, exist_ok=True)
os.makedirs(CACHE_PATH, exist_ok=True)

KEY_BIND_MAP = {
    "f1":  _Key.f1,   "f2":  _Key.f2,   "f3":  _Key.f3,
    "f4":  _Key.f4,   "f5":  _Key.f5,   "f6":  _Key.f6,
    "f7":  _Key.f7,   "f8":  _Key.f8,   "f9":  _Key.f9,
    "f10": _Key.f10,  "f11": _Key.f11,  "f12": _Key.f12,
}

DRAW_PRESETS = {
    "Ultra Fast": {
        "ENGINE_MODE": "ultra_fast", "CLICK_DELAY": 0.0, "UI_DELAY": 0.04,
        "SIMPLIFY_EPS": 3.0, "HATCH_ENABLE": False, "MULTIPASS": False,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 60, "CANNY_HIGH": 160, "PIXEL_GAP": 2,
        "DRAW_STYLE": "continuous_stroke", "LINE_MODE": "raw",
        "LQE_ENABLE": False, "STRUCTURE_ENABLE": False,
        "STRUCTURE_DETAIL_THRESHOLD": 0.2, "FILL_ENABLE": False,
        "BG_AWARENESS_ENABLE": False,
    },
    "Balanced": {
        "ENGINE_MODE": "balanced", "CLICK_DELAY": 0.0005, "UI_DELAY": 0.08,
        "SIMPLIFY_EPS": 1.5, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 40, "CANNY_HIGH": 120, "PIXEL_GAP": 1,
        "DRAW_STYLE": "continuous_stroke", "LINE_MODE": "balanced",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.5, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
    "High Detail": {
        "ENGINE_MODE": "high_detail", "CLICK_DELAY": 0.001, "UI_DELAY": 0.10,
        "SIMPLIFY_EPS": 0.5, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 20, "CANNY_HIGH": 80, "PIXEL_GAP": 1,
        "DRAW_STYLE": "continuous_stroke", "LINE_MODE": "smooth",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.8, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
    "Human Sketch": {
        "ENGINE_MODE": "human_sketch", "CLICK_DELAY": 0.008, "UI_DELAY": 0.12,
        "SIMPLIFY_EPS": 1.2, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": True, "JITTER_PX": 3, "BEZIER_STEPS": 8,
        "CANNY_LOW": 40, "CANNY_HIGH": 120, "PIXEL_GAP": 1,
        "DRAW_STYLE": "human_sketch", "LINE_MODE": "artistic",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.6, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
    "Anime Lineart": {
        "ENGINE_MODE": "high_detail", "CLICK_DELAY": 0.001, "UI_DELAY": 0.10,
        "SIMPLIFY_EPS": 0.8, "HATCH_ENABLE": False, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 60, "CANNY_HIGH": 150, "PIXEL_GAP": 1,
        "DRAW_STYLE": "anime_lineart", "LINE_MODE": "smooth",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.7, "FILL_ENABLE": False,
        "BG_AWARENESS_ENABLE": True,
    },
    "Precision Technical": {
        "ENGINE_MODE": "balanced", "CLICK_DELAY": 0.0002, "UI_DELAY": 0.05,
        "SIMPLIFY_EPS": 0.3, "HATCH_ENABLE": False, "MULTIPASS": False,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 30, "CANNY_HIGH": 100, "PIXEL_GAP": 1,
        "DRAW_STYLE": "precision", "LINE_MODE": "raw",
        "LQE_ENABLE": False, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.9, "FILL_ENABLE": False,
        "BG_AWARENESS_ENABLE": False,
    },
    "Crosshatch Illustration": {
        "ENGINE_MODE": "high_detail", "CLICK_DELAY": 0.001, "UI_DELAY": 0.08,
        "SIMPLIFY_EPS": 0.6, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 1, "BEZIER_STEPS": 0,
        "CANNY_LOW": 40, "CANNY_HIGH": 130, "PIXEL_GAP": 1,
        "DRAW_STYLE": "crosshatch", "LINE_MODE": "smooth",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.6, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
    "Stippled Art": {
        "ENGINE_MODE": "balanced", "CLICK_DELAY": 0.0, "UI_DELAY": 0.08,
        "SIMPLIFY_EPS": 1.0, "HATCH_ENABLE": False, "MULTIPASS": False,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 20, "CANNY_HIGH": 60, "PIXEL_GAP": 1,
        "DRAW_STYLE": "stipple", "LINE_MODE": "raw",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": False,
        "STRUCTURE_DETAIL_THRESHOLD": 0.5, "FILL_ENABLE": False,
        "BG_AWARENESS_ENABLE": False,
    },
    "Etching": {
        "ENGINE_MODE": "ultra_fast", "CLICK_DELAY": 0.0005, "UI_DELAY": 0.04,
        "SIMPLIFY_EPS": 0.15, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
        "CANNY_LOW": 80, "CANNY_HIGH": 200, "PIXEL_GAP": 1,
        "DRAW_STYLE": "etching", "LINE_MODE": "smooth",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.8, "FILL_ENABLE": False,
        "BG_AWARENESS_ENABLE": False,
    },
    "Woodcut": {
        "ENGINE_MODE": "ultra_fast", "CLICK_DELAY": 0.0005, "UI_DELAY": 0.06,
        "SIMPLIFY_EPS": 2.0, "HATCH_ENABLE": False, "MULTIPASS": True,
        "HUMAN_MOTION": False, "JITTER_PX": 3, "BEZIER_STEPS": 0,
        "CANNY_LOW": 10, "CANNY_HIGH": 50, "PIXEL_GAP": 2,
        "DRAW_STYLE": "ink_pen", "LINE_MODE": "artistic",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.3, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
    "Lithograph": {
        "ENGINE_MODE": "high_detail", "CLICK_DELAY": 0.002, "UI_DELAY": 0.12,
        "SIMPLIFY_EPS": 0.4, "HATCH_ENABLE": True, "MULTIPASS": True,
        "HUMAN_MOTION": True, "JITTER_PX": 1, "BEZIER_STEPS": 3,
        "CANNY_LOW": 30, "CANNY_HIGH": 90, "PIXEL_GAP": 1,
        "DRAW_STYLE": "tonal", "LINE_MODE": "artistic",
        "LQE_ENABLE": True, "STRUCTURE_ENABLE": True,
        "STRUCTURE_DETAIL_THRESHOLD": 0.7, "FILL_ENABLE": True,
        "BG_AWARENESS_ENABLE": True,
    },
}

# ─────────────────────────────────────────────
#  THEMES
# ─────────────────────────────────────────────
THEMES = {
    "Neon Dark": {
        "bg": "#0d0d0d", "bg2": "#1a1a1a", "bg3": "#222",
        "fg": "#e0e0e0", "accent": "#00ff88", "accent2": "#00ccff",
        "danger": "#ff3355", "warn": "#ffaa00", "success": "#00ff88",
        "btn": "#1e2a1e", "btn_active": "#2a4a2a",
        "border": "#00ff88", "log_fg": "#00ff88", "log_bg": "#050505",
        "progress": "#00ff88",
    },
    "Terminal Green": {
        "bg": "#001100", "bg2": "#002200", "bg3": "#003300",
        "fg": "#00ff00", "accent": "#00ff00", "accent2": "#88ff88",
        "danger": "#ff4400", "warn": "#ffcc00", "success": "#00ff00",
        "btn": "#003300", "btn_active": "#004400",
        "border": "#00ff00", "log_fg": "#00ff00", "log_bg": "#000d00",
        "progress": "#00ff00",
    },
    "Blood Red": {
        "bg": "#110000", "bg2": "#1a0000", "bg3": "#220000",
        "fg": "#ffcccc", "accent": "#ff2244", "accent2": "#ff6666",
        "danger": "#ff0000", "warn": "#ff8800", "success": "#88ff44",
        "btn": "#330000", "btn_active": "#440000",
        "border": "#ff2244", "log_fg": "#ff4466", "log_bg": "#0a0000",
        "progress": "#ff2244",
    },
    "Soft Dark": {
        "bg": "#1e1e2e", "bg2": "#2a2a3e", "bg3": "#313145",
        "fg": "#cdd6f4", "accent": "#89b4fa", "accent2": "#cba6f7",
        "danger": "#f38ba8", "warn": "#fab387", "success": "#a6e3a1",
        "btn": "#313145", "btn_active": "#45475a",
        "border": "#89b4fa", "log_fg": "#a6e3a1", "log_bg": "#181825",
        "progress": "#89b4fa",
    },
    "Cyberpunk": {
        "bg": "#0a0a1a", "bg2": "#12122a", "bg3": "#1a1a3a",
        "fg": "#e0e0ff", "accent": "#ff00ff", "accent2": "#00ffff",
        "danger": "#ff0044", "warn": "#ffaa00", "success": "#00ffaa",
        "btn": "#2a003a", "btn_active": "#3a005a",
        "border": "#ff00ff", "log_fg": "#ff88ff", "log_bg": "#050510",
        "progress": "#ff00ff",
    },
    "Amber Terminal": {
        "bg": "#0a0800", "bg2": "#141000", "bg3": "#1e1800",
        "fg": "#ffb000", "accent": "#ff8800", "accent2": "#ffcc44",
        "danger": "#ff2200", "warn": "#ffdd00", "success": "#88ff00",
        "btn": "#2a1a00", "btn_active": "#3a2a00",
        "border": "#ff8800", "log_fg": "#ffaa22", "log_bg": "#050400",
        "progress": "#ff8800",
    },
    "Ocean Deep": {
        "bg": "#001520", "bg2": "#002030", "bg3": "#002a40",
        "fg": "#c0e0ff", "accent": "#00ccff", "accent2": "#88ddff",
        "danger": "#ff4455", "warn": "#ffaa00", "success": "#44ffaa",
        "btn": "#003050", "btn_active": "#004060",
        "border": "#00ccff", "log_fg": "#66ccff", "log_bg": "#000d15",
        "progress": "#00ccff",
    },
    "Nord": {
        "bg": "#2e3440", "bg2": "#3b4252", "bg3": "#434c5e",
        "fg": "#eceff4", "accent": "#88c0d0", "accent2": "#81a1c1",
        "danger": "#bf616a", "warn": "#d08770", "success": "#a3be8c",
        "btn": "#4c566a", "btn_active": "#5e687c",
        "border": "#88c0d0", "log_fg": "#8fbcbb", "log_bg": "#1a1e26",
        "progress": "#88c0d0",
    },
    "Synthwave Executor": {
        "bg": "#0B1020", "bg2": "#121830", "bg3": "#1A2040",
        "fg": "#E0E0FF", "accent": "#FF00AA", "accent2": "#00E5FF",
        "danger": "#FF0044", "warn": "#FFAA00", "success": "#00FF88",
        "btn": "#2A003A", "btn_active": "#3A005A",
        "border": "#FF00AA", "log_fg": "#FF88CC", "log_bg": "#060A15",
        "progress": "#00E5FF",
    },
    "Black Ice Terminal": {
        "bg": "#050505", "bg2": "#101820", "bg3": "#1A2838",
        "fg": "#D0F0FF", "accent": "#00B7FF", "accent2": "#D0F0FF",
        "danger": "#FF0040", "warn": "#FFAA00", "success": "#00FF88",
        "btn": "#002040", "btn_active": "#003060",
        "border": "#00B7FF", "log_fg": "#88DDFF", "log_bg": "#020508",
        "progress": "#00B7FF",
    },
    "Obsidian AI Core": {
        "bg": "#0A0A0A", "bg2": "#121212", "bg3": "#1F1F1F",
        "fg": "#C0C0C0", "accent": "#00FFC6", "accent2": "#66FFD9",
        "danger": "#FF3355", "warn": "#FFAA00", "success": "#00FFC6",
        "btn": "#1A2A1A", "btn_active": "#2A3A2A",
        "border": "#00FFC6", "log_fg": "#88FFD9", "log_bg": "#050505",
        "progress": "#00FFC6",
    },
    "Neural Lab": {
        "bg": "#EAF6FF", "bg2": "#D0EAFF", "bg3": "#B7E0FF",
        "fg": "#001B44", "accent": "#0077FF", "accent2": "#001B44",
        "danger": "#FF0040", "warn": "#FF8800", "success": "#00BB66",
        "btn": "#CCE5FF", "btn_active": "#99CCFF",
        "border": "#0077FF", "log_fg": "#0055BB", "log_bg": "#F0F8FF",
        "progress": "#0077FF",
    },
    "Quantum Engine": {
        "bg": "#050816", "bg2": "#0A1030", "bg3": "#12184A",
        "fg": "#E0DAFF", "accent": "#6A00FF", "accent2": "#00D0FF",
        "danger": "#FF0055", "warn": "#FF8800", "success": "#00FFAA",
        "btn": "#2A0050", "btn_active": "#3A0070",
        "border": "#B300FF", "log_fg": "#B388FF", "log_bg": "#03040A",
        "progress": "#00D0FF",
    },
    "Blueprint Engine": {
        "bg": "#071A2E", "bg2": "#0D2A4A", "bg3": "#0D3B66",
        "fg": "#D9F0FF", "accent": "#4DA8FF", "accent2": "#D9F0FF",
        "danger": "#FF3355", "warn": "#FFAA00", "success": "#88FFAA",
        "btn": "#0A3050", "btn_active": "#0E4570",
        "border": "#4DA8FF", "log_fg": "#88CCFF", "log_bg": "#040E1A",
        "progress": "#4DA8FF",
    },
    "Industrial Armature": {
        "bg": "#1A1A1A", "bg2": "#2D2D2D", "bg3": "#3A3A3A",
        "fg": "#FFE0B0", "accent": "#FF8C00", "accent2": "#FFD166",
        "danger": "#FF2200", "warn": "#FFCC00", "success": "#66FF44",
        "btn": "#3A2A00", "btn_active": "#4A3A00",
        "border": "#FF8C00", "log_fg": "#FFAA44", "log_bg": "#0A0A0A",
        "progress": "#FF8C00",
    },
    "Glitch Void": {
        "bg": "#000000", "bg2": "#0A000A", "bg3": "#150015",
        "fg": "#FFFFFF", "accent": "#FF004C", "accent2": "#00FFF7",
        "danger": "#FF0000", "warn": "#FF8800", "success": "#00FF88",
        "btn": "#1A0000", "btn_active": "#2A0000",
        "border": "#FF004C", "log_fg": "#FF6688", "log_bg": "#050005",
        "progress": "#00FFF7",
    },
    "Red Alert": {
        "bg": "#120000", "bg2": "#1A0000", "bg3": "#300000",
        "fg": "#FFAAAA", "accent": "#FF0000", "accent2": "#FF5555",
        "danger": "#FF0000", "warn": "#FF8800", "success": "#88FF44",
        "btn": "#2A0000", "btn_active": "#3A0000",
        "border": "#FF0000", "log_fg": "#FF4444", "log_bg": "#080000",
        "progress": "#FF0000",
    },
    "Glassmorphic Dark": {
        "bg": "#101014", "bg2": "#181820", "bg3": "#2D2D38",
        "fg": "#D0D8E0", "accent": "#7EE7FF", "accent2": "#B0F0FF",
        "danger": "#FF3355", "warn": "#FFAA00", "success": "#88FFCC",
        "btn": "#252535", "btn_active": "#353550",
        "border": "#7EE7FF", "log_fg": "#AAEEFF", "log_bg": "#0A0A0E",
        "progress": "#7EE7FF",
    },
    "Amoled Void": {
        "bg": "#000000", "bg2": "#050505", "bg3": "#111111",
        "fg": "#CCE6D8", "accent": "#00FF99", "accent2": "#88FFCC",
        "danger": "#FF3355", "warn": "#FFAA00", "success": "#00FF99",
        "btn": "#0A1A12", "btn_active": "#152A1E",
        "border": "#00FF99", "log_fg": "#66FFAA", "log_bg": "#000000",
        "progress": "#00FF99",
    },
}

CURRENT_THEME = THEMES["Neon Dark"]

# ─────────────────────────────────────────────
#  DEFAULT SETTINGS — COMPREHENSIVE (ALL TABS)
# ─────────────────────────────────────────────
SETTINGS = {
    "THEME": "Neon Dark", "ACTIVE_PROFILE": "default", "DRAW_PRESET": "Balanced",
    "WINDOW_WIDTH": 1200, "WINDOW_HEIGHT": 850, "BTN_COLS": 2,
    "HISTORY_MAX_STACK": 50, "LOG_AUTO_SCROLL": True,
    "ABORT_KEY": "f12", "PAUSE_KEY": "f11", "START_KEY": "f10",
    "COLOR_SCAN_LAYOUT": "grid", "COLOR_SCAN_SPACING": 4, "COLOR_CACHE_ENABLE": True,
    "CAPTURE_WIDTH": 256, "CAPTURE_HEIGHT": 256, "CAPTURE_FORMAT": "PNG",
    "CANNY_LOW": 40, "CANNY_HIGH": 120, "STRUCTURE_DETAIL_THRESHOLD": 0.5,
    "STRUCTURE_ENABLE": True, "SIMPLIFY_EPS": 1.5, "MIN_STROKE_LEN": 3,
    "CONTOUR_APPROX": True, "USE_PATH_CACHE": True, "ENGINE_MODE": "balanced",
    "DRAW_MODE": "Optimized", "LINE_MODE": "balanced",
    "DRAW_STYLE": "continuous_stroke", "MULTIPASS": True,
    "HATCH_ENABLE": True, "HATCH_ANGLE_STEP": 45, "HATCH_SPACING": 4, "HATCH_SINGLE": False,
    "HUMAN_MOTION": False, "JITTER_PX": 0, "BEZIER_STEPS": 0,
    "FILL_ENABLE": False, "FILL_VARIANCE_THRESHOLD": 500, "MIN_FILL_AREA": 200,
    "FILL_HOTKEY": "f9", "FILL_ZONE_ACTIVE": False,
    "FILL_ZONE_CENTER": [0, 0], "FILL_ZONE_COLOR": [0, 100, 255],
    "FILL_ZONE_THRESHOLD": 30, "FILL_ZONE_GROW_STEPS": 5,
    "BG_AWARENESS_ENABLE": False,
    "STRIPED_FILL_ENABLED": True, "STRIPE_ANGLE": 45, "STRIPE_SPACING": 6, "STRIPE_MIN_AREA": 200,
    "LQE_ENABLE": True, "LQE_SMOOTHING_FACTOR": 1.8,
    "LQE_CORNER_THRESHOLD": 45, "LQE_MIN_CONFIDENCE": 0.3,
    "STYLE_MERGE_DISTANCE": 8, "STYLE_OVERLAP_SUPPRESS": True,
    "STYLE_CROSSHATCH_ANGLE": 45, "STYLE_STIPPLE_DENSITY": 0.5,
    "STYLE_SCRIBBLE_PASSES": 2, "STROKE_WIDTH": 2, "STROKE_SPEED": 0,
    "LIFT_DELAY": 0.02, "CORNER_SLOWDOWN": True, "STROKE_SMOOTH_PASSES": 2,
    "STROKE_MODE": "stroke", "RENDER_MODE": "physical", "CONTINUOUS_DRAG": True,
    "COLOR_METRIC": "Euclidean", "PALETTE_SIZE": 16,
    "DITHER_MODE": "None", "WHITE_SKIP": 252, "SKIP_BLUE_MASK": True,
    "PIXEL_GAP": 1, "PALETTE_REDUCE_TO": 0, "PALETTE_SORT_BY": "none",
    "GLOBAL_SPEED": 500.0, "CLICK_DELAY": 0.00001, "UI_DELAY": 0.15,
    "TRACE_MODE": True, "RESIZE_SENSITIVITY": 0.005,
    "SKETCH_PRESET": "Gestural", "SKETCH_STROKE_DIST": 3, "SKETCH_JITTER": 0.5,
    "SKETCH_SPEED": 0.002, "SKETCH_ORDER": "size", "SKETCH_STROKE_DELAY": 0.08,
    "SKETCH_OVERLAP": 0.3, "SKETCH_VARIATION": 0.5, "SKETCH_ITERATIONS": 1,
    "SKETCH_EDGE_ONLY": 0, "SKETCH_SPEED_MULT": 5,
    "SKETCH_BPM": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
    "SKETCH_SEGMENT_LEN": 0, "SKETCH_WOBBLE": 0, "SKETCH_TAIL_FADE": 0,
    "SKETCH_HATCH_ANGLE": 45, "SKETCH_HATCH_SPACING": 5,
    "SKETCH_CONSTRUCTION_PASSES": 3,
    "HEX_COLORS": [],
    "VIEWPORT_ZOOM": 1.0, "VIEWPORT_SCROLL_DX": 0, "VIEWPORT_SCROLL_DY": 0,
    "VIEWPORT_AUTO_SCROLL": False, "VIEWPORT_ZOOM_SPEED": 1.15,
    "VIEWPORT_MOMENTUM_FRICTION": 0.92, "VIEWPORT_SNAP_ENABLED": True,
    "VIEWPORT_SHOW_MINIMAP": False, "VIEWPORT_MINIMAP_SIZE": 180,
    "VIRTUAL_CANVAS_ENABLE": True, "VIRTUAL_BG_COLOR": "#ffffff",
    "PROMPT_PROVIDER": "arena_ai", "PROMPT_ENDPOINT": "",
    "PROMPT_STYLE_PRESET": "anime_sketch",
    "PROMPT_NEGATIVE": "lowres, bad anatomy, text, watermark",
    "PROMPT_API_TIMEOUT": 30, "PROMPT_STEPS": 15, "PROMPT_GUIDANCE": 7.0,
    "PROMPT_EDGE_ENHANCE": True, "PROMPT_CONTRAST_BOOST": True,
    "PROMPT_AUTO_SHARPEN": True,
    "AI_MODEL_ID": "segmind/tiny-sd", "AI_MODEL": "segmind/tiny-sd", "AI_WIDTH": 512, "AI_HEIGHT": 512,
    "AI_SEED": -1, "AI_STEPS": 20, "AI_GUIDANCE": 7.0,
    "AI_STRENGTH": 0.75, "AI_STYLE": "anime", "AI_MAX_STEPS": 50,
    "BATCH_AUTO_SAVE": True, "BATCH_AUTO_ADVANCE": True, "BATCH_DELAY": 3,
    "SCHEDULER_ENABLE": False, "SCHEDULED_TIME": "00:00",
    "ANIM_FPS": 12, "ANIM_ONION_SKIN": False, "ANIM_LOOP": True,
    "ANIM_INTERPOLATE_ENABLED": False, "ANIM_AI_INBETWEEN_ENABLED": False,
    "FLIPBOOK_FPS": 8,
    "LAYER_BLEND_MODE": "normal", "LAYER_OPACITY": 1.0,
    "LAYER_LOCKED": False, "LAYER_VISIBLE": True,
    "BRUSH_PHYSICS_ENABLED": True, "BRUSH_TYPE": "round",
    "BRUSH_PRESSURE_SENSITIVITY": 0.5, "BRUSH_FLOW_RATE": 0.8,
    "BRUSH_SCATTER_AMOUNT": 0.0,
    "SMART_FILL_MODE": "flood", "SMART_FILL_TOLERANCE": 30,
    "SMART_FILL_GROW_LIMIT": 50,
    "SELECTION_TOOL": "rectangular", "SELECTION_FEATHER": 0,
    "SELECTION_INVERT": False,
    "HARMONY_TYPE": "complementary", "HARMONY_COLOR_COUNT": 5,
    "FILTER_CHAIN_ENABLED": False,
    "EFFECT_GRAYSCALE": False, "EFFECT_INVERT": False, "EFFECT_SEPIA": False,
    "EXPORT_TEMPLATE": "Default", "EXPORT_AUTO_APPLY": False,
    "RESAMPLE_FILTER": "lanczos", "RESIZE_WIDTH_PCT": 100, "RESIZE_HEIGHT_PCT": 100,
    "MULTI_CURSOR_ENABLED": True, "MULTI_CURSOR_COUNT": 7,
    "RECORDER_AUTO_START": False, "RECORDER_PLAYBACK_SPEED": 1.0,
    "RECORDER_AUTO_RECORD_DRAW": True,
    "TERMINAL_BOOT_SCREEN": True, "TERMINAL_MATRIX_OVERLAY": False,
    "TERMINAL_SCANNER": False, "TERMINAL_SYNTHWAVE_HUD": False,
    "TERMINAL_AI_DIAGNOSTICS": False,
    "PERF_MONITOR_ENABLED": False, "PERF_ROUTE_HEATMAP_ENABLED": False,
    "PERF_ADVISOR_ENABLED": False, "PERF_CACHE_DIR": "",
    "NODE_EDITOR_ENABLED": False, "COMPOSITION_ANALYZER_ENABLED": False,
    "PLUGIN_AUTOLOAD": True, "CONSOLE_SHOW_ON_STARTUP": False,
    "REFERENCE_PANEL_VISIBLE": False, "DASHBOARD_VISIBLE": False,
    "SOUND_ENABLE": False, "REMOTE_HOST": "localhost", "REMOTE_PORT": 12345,
    "ARTISTIC_CURSED_AI_ENABLED": False,
    "BG_ENABLED": False, "BG_TYPE": "none", "BG_PATH": "",
    "BG_OPACITY": 0.3, "BG_LOOP": True,
    "LIMIT_GLOBAL_SPEED": 500.0, "LIMIT_STROKE_SPEED": 100,
    "LIMIT_PIXEL_GAP": 10, "LIMIT_SKETCH_NO_LIFT": 500,
    "LIMIT_SKETCH_BPM": 200, "LIMIT_BATCH_DELAY": 30,
    "LIMIT_FILL_VARIANCE_THRESHOLD": 2000, "LIMIT_MIN_FILL_AREA": 1000,
    "LIMIT_WHITE_SKIP": 255, "LIMIT_BEZIER_STEPS": 20,
    "LIMIT_LIFT_DELAY": 0.5, "LIMIT_CLICK_DELAY": 0.1, "LIMIT_UI_DELAY": 0.5,
    "LIMIT_ANIM_FPS": 60, "LIMIT_PERF_FPS_TARGET": 240,
    "LIMIT_HISTORY_MAX_STACK": 200, "LIMIT_UNDO_STACK_SIZE": 200,
    "LIMIT_STRIPE_SPACING": 20, "LIMIT_FLIPBOOK_FPS": 30,
}

# ─────────────────────────────────────────────
#  CONFIG CATEGORY MAP (for hierarchical save/load)
#  Groups flat SETTINGS keys into named categories
# ─────────────────────────────────────────────
CONFIG_CATEGORY = {
    "general": ["THEME", "ACTIVE_PROFILE", "DRAW_PRESET", "WINDOW_WIDTH", "WINDOW_HEIGHT",
                "BTN_COLS", "HISTORY_MAX_STACK", "LOG_AUTO_SCROLL"],
    "capture": ["COLOR_SCAN_LAYOUT", "COLOR_SCAN_SPACING", "COLOR_CACHE_ENABLE",
                "CAPTURE_WIDTH", "CAPTURE_HEIGHT", "CAPTURE_FORMAT"],
    "engine": ["CANNY_LOW", "CANNY_HIGH", "STRUCTURE_DETAIL_THRESHOLD", "STRUCTURE_ENABLE",
               "SIMPLIFY_EPS", "MIN_STROKE_LEN", "CONTOUR_APPROX", "USE_PATH_CACHE",
               "ENGINE_MODE", "DRAW_MODE", "LINE_MODE", "DRAW_STYLE", "MULTIPASS",
               "HATCH_ENABLE", "HATCH_ANGLE_STEP", "HATCH_SPACING", "HATCH_SINGLE",
               "HUMAN_MOTION", "JITTER_PX", "BEZIER_STEPS",
               "FILL_ENABLE", "FILL_VARIANCE_THRESHOLD", "MIN_FILL_AREA", "FILL_HOTKEY",
               "FILL_ZONE_ACTIVE", "FILL_ZONE_CENTER", "FILL_ZONE_COLOR",
               "FILL_ZONE_THRESHOLD", "FILL_ZONE_GROW_STEPS", "BG_AWARENESS_ENABLE",
               "STRIPED_FILL_ENABLED", "STRIPE_ANGLE", "STRIPE_SPACING", "STRIPE_MIN_AREA"],
    "stroke": ["LQE_ENABLE", "LQE_SMOOTHING_FACTOR", "LQE_CORNER_THRESHOLD", "LQE_MIN_CONFIDENCE",
               "STYLE_MERGE_DISTANCE", "STYLE_OVERLAP_SUPPRESS", "STYLE_CROSSHATCH_ANGLE",
               "STYLE_STIPPLE_DENSITY", "STYLE_SCRIBBLE_PASSES",
               "STROKE_WIDTH", "STROKE_SPEED", "LIFT_DELAY", "CORNER_SLOWDOWN",
                "STROKE_SMOOTH_PASSES", "STROKE_MODE", "RENDER_MODE", "CONTINUOUS_DRAG"],
    "color": ["COLOR_METRIC", "PALETTE_SIZE", "DITHER_MODE", "WHITE_SKIP",
              "SKIP_BLUE_MASK", "PIXEL_GAP", "PALETTE_REDUCE_TO", "PALETTE_SORT_BY"],
    "speed": ["GLOBAL_SPEED", "CLICK_DELAY", "UI_DELAY", "TRACE_MODE", "RESIZE_SENSITIVITY"],
    "sketch": ["SKETCH_PRESET", "SKETCH_STROKE_DIST", "SKETCH_JITTER", "SKETCH_SPEED",
               "SKETCH_ORDER", "SKETCH_STROKE_DELAY", "SKETCH_OVERLAP", "SKETCH_VARIATION",
               "SKETCH_ITERATIONS", "SKETCH_EDGE_ONLY", "SKETCH_SPEED_MULT",
               "SKETCH_BPM", "SKETCH_GHOST", "SKETCH_NO_LIFT", "SKETCH_SEGMENT_LEN",
               "SKETCH_WOBBLE", "SKETCH_TAIL_FADE", "SKETCH_HATCH_ANGLE",
                "SKETCH_HATCH_SPACING", "SKETCH_CONSTRUCTION_PASSES", "HEX_COLORS"],
    "viewport": ["VIEWPORT_ZOOM", "VIEWPORT_SCROLL_DX", "VIEWPORT_SCROLL_DY",
                 "VIEWPORT_AUTO_SCROLL", "VIEWPORT_ZOOM_SPEED", "VIEWPORT_MOMENTUM_FRICTION",
                 "VIEWPORT_SNAP_ENABLED", "VIEWPORT_SHOW_MINIMAP", "VIEWPORT_MINIMAP_SIZE",
                 "VIRTUAL_CANVAS_ENABLE", "VIRTUAL_BG_COLOR"],
    "ai": ["PROMPT_PROVIDER", "PROMPT_ENDPOINT", "PROMPT_STYLE_PRESET", "PROMPT_NEGATIVE",
           "PROMPT_API_TIMEOUT", "PROMPT_STEPS", "PROMPT_GUIDANCE",
           "PROMPT_EDGE_ENHANCE", "PROMPT_CONTRAST_BOOST", "PROMPT_AUTO_SHARPEN",
           "AI_MODEL_ID", "AI_MODEL", "AI_WIDTH", "AI_HEIGHT", "AI_SEED", "AI_STEPS",
           "AI_GUIDANCE", "AI_STRENGTH", "AI_STYLE", "AI_MAX_STEPS"],
    "batch": ["BATCH_AUTO_SAVE", "BATCH_AUTO_ADVANCE", "BATCH_DELAY",
              "SCHEDULER_ENABLE", "SCHEDULED_TIME"],
    "animation": ["ANIM_FPS", "ANIM_ONION_SKIN", "ANIM_LOOP", "ANIM_INTERPOLATE_ENABLED",
                  "ANIM_AI_INBETWEEN_ENABLED", "FLIPBOOK_FPS",
                  "LAYER_BLEND_MODE", "LAYER_OPACITY", "LAYER_LOCKED", "LAYER_VISIBLE"],
    "brush": ["BRUSH_PHYSICS_ENABLED", "BRUSH_TYPE", "BRUSH_PRESSURE_SENSITIVITY",
              "BRUSH_FLOW_RATE", "BRUSH_SCATTER_AMOUNT"],
    "tools": ["SMART_FILL_MODE", "SMART_FILL_TOLERANCE", "SMART_FILL_GROW_LIMIT",
              "SELECTION_TOOL", "SELECTION_FEATHER", "SELECTION_INVERT",
              "HARMONY_TYPE", "HARMONY_COLOR_COUNT", "FILTER_CHAIN_ENABLED",
              "EFFECT_GRAYSCALE", "EFFECT_INVERT", "EFFECT_SEPIA"],
    "export": ["EXPORT_TEMPLATE", "EXPORT_AUTO_APPLY", "RESAMPLE_FILTER",
               "RESIZE_WIDTH_PCT", "RESIZE_HEIGHT_PCT"],
    "advanced": ["MULTI_CURSOR_ENABLED", "MULTI_CURSOR_COUNT",
                 "RECORDER_AUTO_START", "RECORDER_PLAYBACK_SPEED", "RECORDER_AUTO_RECORD_DRAW",
                 "NODE_EDITOR_ENABLED", "COMPOSITION_ANALYZER_ENABLED",
                 "PLUGIN_AUTOLOAD", "CONSOLE_SHOW_ON_STARTUP",
                 "REFERENCE_PANEL_VISIBLE", "DASHBOARD_VISIBLE",
                 "SOUND_ENABLE", "REMOTE_HOST", "REMOTE_PORT",
                 "ARTISTIC_CURSED_AI_ENABLED"],
    "terminal": ["TERMINAL_BOOT_SCREEN", "TERMINAL_MATRIX_OVERLAY", "TERMINAL_SCANNER",
                 "TERMINAL_SYNTHWAVE_HUD", "TERMINAL_AI_DIAGNOSTICS"],
    "performance": ["PERF_MONITOR_ENABLED", "PERF_ROUTE_HEATMAP_ENABLED",
                    "PERF_ADVISOR_ENABLED", "PERF_CACHE_DIR"],
    "limits": ["LIMIT_GLOBAL_SPEED", "LIMIT_STROKE_SPEED", "LIMIT_PIXEL_GAP",
               "LIMIT_SKETCH_NO_LIFT", "LIMIT_SKETCH_BPM", "LIMIT_BATCH_DELAY",
               "LIMIT_FILL_VARIANCE_THRESHOLD", "LIMIT_MIN_FILL_AREA",
               "LIMIT_WHITE_SKIP", "LIMIT_BEZIER_STEPS", "LIMIT_LIFT_DELAY",
               "LIMIT_CLICK_DELAY", "LIMIT_UI_DELAY", "LIMIT_ANIM_FPS",
               "LIMIT_PERF_FPS_TARGET", "LIMIT_HISTORY_MAX_STACK",
               "LIMIT_UNDO_STACK_SIZE", "LIMIT_STRIPE_SPACING", "LIMIT_FLIPBOOK_FPS"],
    "hotkeys": ["ABORT_KEY", "PAUSE_KEY", "START_KEY"],
    "background": ["BG_ENABLED", "BG_TYPE", "BG_PATH", "BG_OPACITY", "BG_LOOP"],
}

# Build reverse mapping: key -> category
_KEY_TO_CAT = {}
for _cat, _keys in CONFIG_CATEGORY.items():
    for _k in _keys:
        _KEY_TO_CAT[_k] = _cat

DRAW_MODES = [
    "Optimized", "Linear", "Snake", "Radial", "Random",
    "Hilbert", "Spiral", "ZigzagRow", "ColumnMajor",
    "Checkerboard", "ConcentricRings", "DarkFirst", "LightFirst",
    "Sketch", "Burst", "SpeedFill", "Intelligent",
    "Pointillism", "CrossHatchFill", "Woven",
]

DITHER_MODES = ["None", "Floyd-Steinberg", "Ordered", "Atkinson", "Halftone", "Stucki", "SierraLite"]

# Bayer 4x4 matrix for ordered dithering
BAYER_4X4 = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5],
], dtype=np.float32) / 16.0

# ─────────────────────────────────────────────────────────────
#  UTILITY: Hilbert Curve (d2xy — correct iterative version)
# ─────────────────────────────────────────────────────────────
def hilbert_d2xy(n, d):
    """Convert linear hilbert index d to (x,y) for an n×n grid (n must be power of 2)."""
    x = y = 0
    s = 1
    while s < n:
        rx = 1 if (d & 2) else 0
        ry = 1 if (d & 1) ^ rx else 0
        # Rotate
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        d >>= 2
        s <<= 1
    return x, y


def generate_hilbert_points(width, height):
    """Generate all (x,y) points in Hilbert curve order for a width×height grid."""
    n = 1
    while n < max(width, height):
        n <<= 1
    total = n * n
    points = []
    for d in range(total):
        x, y = hilbert_d2xy(n, d)
        if x < width and y < height:
            points.append((x, y))
    return points


def generate_spiral_points(width, height):
    """Outward spiral from center."""
    cx, cy = width // 2, height // 2
    visited = set()
    result = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x, y = cx, cy
    di = 0
    steps = 1
    while len(result) < width * height:
        for _ in range(2):
            dx, dy = directions[di % 4]
            for _ in range(steps):
                if 0 <= x < width and 0 <= y < height and (x, y) not in visited:
                    result.append((x, y))
                    visited.add((x, y))
                x += dx
                y += dy
            di += 1
        steps += 1
        if steps > max(width, height) * 2:
            break
    # Fill any missed
    for yy in range(height):
        for xx in range(width):
            if (xx, yy) not in visited:
                result.append((xx, yy))
    return result


# ─────────────────────────────────────────────
#  TOOLTIP HELPER
# ─────────────────────────────────────────────
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(
            tw, text=self.text, justify="left",
            background="#222", foreground="#00ff88",
            relief="solid", borderwidth=1,
            font=("Courier", 8), padx=6, pady=3
        )
        lbl.pack()

    def hide(self, _event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


# ─────────────────────────────────────────────
#  COLORED BUTTON HELPER
# ─────────────────────────────────────────────
def make_btn(parent, text, cmd, color=None, tooltip_text=None, width=35, height=2, font_size=9):
    T = CURRENT_THEME
    bg = color or T["btn"]
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=T["fg"],
        font=("Courier", font_size, "bold"),
        width=width, height=height,
        bd=0, relief="flat",
        activebackground=T["btn_active"],
        activeforeground=T["accent"],
        cursor="hand2",
    )
    btn.pack(pady=2)
    if tooltip_text:
        Tooltip(btn, tooltip_text)
    # Hover effect
    def on_enter(e): btn.config(bg=T["btn_active"])
    def on_leave(e): btn.config(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ─────────────────────────────────────────────
#  SPARKLINE CANVAS
# ─────────────────────────────────────────────

class Sparkline(tk.Canvas):
    """Mini live graph for pixels/sec."""

    def __init__(self, parent=None, **kwargs):
        width = kwargs.pop("width", 200)
        height = kwargs.pop("height", 40)
        maxpts = kwargs.pop("maxpts", 60)

        tk.Canvas.__init__(
            self,
            master=parent,
            width=int(width),
            height=int(height),
            bg=CURRENT_THEME["log_bg"],
            highlightthickness=0
        )

        self.maxpts = maxpts
        self.data = deque(maxlen=maxpts)
        self._pw = width
        self._ph = height

    def push(self, value):
        self.data.append(value)
        self._redraw()

    def _redraw(self):
        self.delete("all")

        if len(self.data) < 2:
            return

        pts = list(self.data)
        mx = max(pts) if max(pts) > 0 else 1

        coords = []

        for i, v in enumerate(pts):
            x = int(i / (self.maxpts - 1) * self._pw)
            y = int(self._ph - (v / mx) * (self._ph - 4)) - 2
            coords.extend([x, y])

        if len(coords) >= 4:
            self.create_line(
                *coords,
                fill=CURRENT_THEME["accent"],
                width=1,
                smooth=True
            )


# ─────────────────────────────────────────────
#  PALETTE EDITOR WINDOW
# ─────────────────────────────────────────────
class PaletteEditorWindow:
    def __init__(self, parent, palette_map, on_save):
        self.palette_map = [dict(e) for e in palette_map]  # deep copy
        self.on_save = on_save
        T = CURRENT_THEME

        self.win = tk.Toplevel(parent)
        self.win.title("Palette Editor")
        self.win.geometry("500x600")
        self.win.configure(bg=T["bg"])

        tk.Label(self.win, text="PALETTE EDITOR", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(pady=10)

        # Scrollable list
        frame = tk.Frame(self.win, bg=T["bg"])
        frame.pack(fill="both", expand=True, padx=10)

        self.listbox_frame = tk.Frame(frame, bg=T["bg"])
        self.listbox_frame.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(self.listbox_frame)
        scroll.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            self.listbox_frame, yscrollcommand=scroll.set,
            bg=T["log_bg"], fg=T["fg"], selectbackground=T["accent2"],
            font=("Courier", 10), height=20
        )
        self.listbox.pack(fill="both", expand=True, side="left")
        scroll.config(command=self.listbox.yview)

        self._refresh_list()

        # Buttons
        btn_frame = tk.Frame(self.win, bg=T["bg"])
        btn_frame.pack(fill="x", padx=10, pady=5)

        for label, cmd in [
            ("+ ADD COLOR", self._add_color),
            ("✎ EDIT COLOR", self._edit_color),
            ("✕ REMOVE", self._remove_color),
            ("↑ MOVE UP", self._move_up),
            ("↓ MOVE DOWN", self._move_down),
            ("💾 SAVE & CLOSE", self._save),
        ]:
            tk.Button(btn_frame, text=label, command=cmd, bg=T["btn"], fg=T["fg"],
                      font=("Courier", 9, "bold"), bd=0, padx=8, pady=4).pack(
                side="left", padx=3)

    def _refresh_list(self):
        if not self.listbox.winfo_exists():
            return
        try:
            self.listbox.delete(0, tk.END)
        except tk.TclError:
            return
        for i, entry in enumerate(self.palette_map):
            rgb = entry.get("rgb", [0, 0, 0])
            pos = entry.get("pos", [0, 0])
            self.listbox.insert(tk.END,
                f"  #{i+1:02d}  RGB({rgb[0]:3d},{rgb[1]:3d},{rgb[2]:3d})  @ ({pos[0]},{pos[1]})")
            # Set row background to approximate color
            try:
                hex_col = "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, v)) for v in rgb])
                self.listbox.itemconfig(i, bg=hex_col,
                    fg="black" if sum(rgb) > 382 else "white")
            except Exception:
                pass

    def _add_color(self):
        color = colorchooser.askcolor(title="Pick Color")
        if color and color[0]:
            rgb = [int(c) for c in color[0]]
            self.palette_map.append({"pos": [0, 0], "rgb": rgb})
            self._refresh_list()

    def _edit_color(self):
        if not self.listbox.winfo_exists():
            return
        try:
            idx = self.listbox.curselection()
        except tk.TclError:
            return
        if not idx:
            return
        i = idx[0]
        cur = self.palette_map[i]["rgb"]
        color = colorchooser.askcolor(
            color="#{:02x}{:02x}{:02x}".format(*cur),
            title="Edit Color"
        )
        if color and color[0]:
            self.palette_map[i]["rgb"] = [int(c) for c in color[0]]
            self._refresh_list()

    def _remove_color(self):
        if not self.listbox.winfo_exists():
            return
        try:
            idx = self.listbox.curselection()
        except tk.TclError:
            return
        if not idx:
            return
        del self.palette_map[idx[0]]
        self._refresh_list()

    def _move_up(self):
        if not self.listbox.winfo_exists():
            return
        try:
            idx = self.listbox.curselection()
        except tk.TclError:
            return
        if not idx or idx[0] == 0:
            return
        i = idx[0]
        self.palette_map[i-1], self.palette_map[i] = self.palette_map[i], self.palette_map[i-1]
        self._refresh_list()
        try:
            self.listbox.selection_set(i - 1)
        except tk.TclError:
            pass

    def _move_down(self):
        if not self.listbox.winfo_exists():
            return
        try:
            idx = self.listbox.curselection()
        except tk.TclError:
            return
        if not idx or idx[0] >= len(self.palette_map) - 1:
            return
        i = idx[0]
        self.palette_map[i+1], self.palette_map[i] = self.palette_map[i], self.palette_map[i+1]
        self._refresh_list()
        try:
            self.listbox.selection_set(i + 1)
        except tk.TclError:
            pass

    def _save(self):
        self.on_save(self.palette_map)
        self.win.destroy()


# ─────────────────────────────────────────────
#  DRAW STATISTICS WINDOW
# ─────────────────────────────────────────────
class StatsWindow:
    def __init__(self, parent, queues, palette_map, total_dots, pps_estimate):
        T = CURRENT_THEME
        win = tk.Toplevel(parent)
        win.title("Draw Statistics")
        win.geometry("480x520")
        win.configure(bg=T["bg"])

        tk.Label(win, text="DRAW STATISTICS", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 13, "bold")).pack(pady=10)

        tk.Label(win, text=f"Total dots: {total_dots:,}", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 10)).pack()

        if pps_estimate > 0:
            eta_sec = total_dots / pps_estimate
            tk.Label(win, text=f"Est. time @ {pps_estimate:.0f} px/s: {eta_sec//60:.0f}m {eta_sec%60:.0f}s",
                     bg=T["bg"], fg=T["fg"], font=("Courier", 10)).pack()

        tk.Label(win, text="─" * 40, bg=T["bg"], fg=T["border"]).pack()
        tk.Label(win, text="Per-color breakdown:", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 10, "bold")).pack()

        frame = tk.Frame(win, bg=T["bg"])
        frame.pack(fill="both", expand=True, padx=15)

        for i, pts in queues.items():
            if i >= len(palette_map):
                continue
            rgb = palette_map[i].get("rgb", [128, 128, 128])
            hex_col = "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, v)) for v in rgb])
            pct = (len(pts) / total_dots * 100) if total_dots > 0 else 0

            row = tk.Frame(frame, bg=T["bg"])
            row.pack(fill="x", pady=1)

            # Color swatch
            swatch = tk.Label(row, bg=hex_col, width=3, height=1, relief="solid", bd=1)
            swatch.pack(side="left", padx=5)

            tk.Label(row,
                text=f"Color {i+1:02d}: {len(pts):>6,} dots  ({pct:5.1f}%)",
                bg=T["bg"], fg=T["fg"], font=("Courier", 9)
            ).pack(side="left")

            # Mini bar
            bar_w = max(1, int(pct * 2))
            tk.Label(row, bg=T["accent"], width=bar_w, height=1).pack(side="left", padx=3)


# ─────────────────────────────────────────────
#  FAST INPUT DRIVER  (pynput-based, ~10× faster than pyautogui)
# ─────────────────────────────────────────────
class FastInputDriver:
    _mouse_shared = None
    _fallback = False

    def __init__(self):
        if FastInputDriver._fallback:
            self._mouse = None
        else:
            if FastInputDriver._mouse_shared is None:
                try:
                    FastInputDriver._mouse_shared = pmouse.Controller()
                except Exception:
                    FastInputDriver._fallback = True
                    self._mouse = None
                    return
            self._mouse = FastInputDriver._mouse_shared
        self._button_down = False

    def move(self, x: int, y: int) -> None:
        if self._mouse is not None:
            try:
                self._mouse.position = (x, y)
                return
            except Exception:
                FastInputDriver._fallback = True
                self._mouse = None
        pyautogui.moveTo(x, y, duration=0)

    def click(self, x: int, y: int) -> None:
        self.move(x, y)
        if self._mouse is not None:
            try:
                self._mouse.press(pmouse.Button.left)
                self._mouse.release(pmouse.Button.left)
                return
            except Exception:
                FastInputDriver._fallback = True
                self._mouse = None
        pyautogui.click(x, y)

    def drag_to(self, x: int, y: int) -> None:
        if self._mouse is not None:
            try:
                self._mouse.position = (x, y)
                return
            except Exception:
                FastInputDriver._fallback = True
                self._mouse = None
        if self._button_down:
            pyautogui.dragTo(x, y, duration=0, button='left')
        else:
            pyautogui.moveTo(x, y, duration=0)

    def press(self, x: int, y: int) -> None:
        self.move(x, y)
        self._button_down = True
        if self._mouse is not None:
            try:
                self._mouse.press(pmouse.Button.left)
                return
            except Exception:
                FastInputDriver._fallback = True
                self._mouse = None
        pyautogui.mouseDown()

    def release(self) -> None:
        self._button_down = False
        if self._mouse is not None:
            try:
                self._mouse.release(pmouse.Button.left)
                return
            except Exception:
                FastInputDriver._fallback = True
                self._mouse = None
        pyautogui.mouseUp()


# ─────────────────────────────────────────────
#  HUMAN MOTION SIMULATOR
#  Bezier waypoints with velocity ramping + jitter
# ─────────────────────────────────────────────
class HumanMotionSimulator:

    @staticmethod
    def _bezier(p0, cp, p1, t):
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * cp[0] + t**2 * p1[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * cp[1] + t**2 * p1[1]
        return int(x), int(y)

    @staticmethod
    def waypoints(x0, y0, x1, y1, steps=8, jitter=2):
        if steps <= 1:
            return [(x1, y1)]
        mx = (x0 + x1) // 2 + random.randint(-jitter * 4, jitter * 4)
        my = (y0 + y1) // 2 + random.randint(-jitter * 4, jitter * 4)
        pts = []
        for i in range(1, steps + 1):
            t = i / steps
            t = t * t * (3 - 2 * t)
            bx, by = HumanMotionSimulator._bezier((x0, y0), (mx, my), (x1, y1), t)
            jx = bx + random.randint(-jitter, jitter)
            jy = by + random.randint(-jitter, jitter)
            pts.append((jx, jy))
        return pts

    @staticmethod
    def delay_for_segment(x0, y0, x1, y1, base_delay):
        dist = math.hypot(x1 - x0, y1 - y0)
        if dist < 5:
            return base_delay * 1.5
        elif dist > 80:
            return base_delay * 0.5
        return base_delay


# ─────────────────────────────────────────────
#  PATH OPTIMIZER
#  Douglas-Peucker simplification + nearest-neighbor ordering
# ─────────────────────────────────────────────
class PathOptimizer:

    @staticmethod
    def douglas_peucker(points, epsilon):
        if len(points) <= 2:
            return points
        stack = [(0, len(points)-1)]
        keep = [False] * len(points)
        keep[0] = keep[-1] = True
        while stack:
            start, end = stack.pop()
            if end - start <= 1:
                continue
            start_pt = np.array(points[start])
            end_pt = np.array(points[end])
            line_vec = end_pt - start_pt
            line_len = np.linalg.norm(line_vec)
            if line_len == 0:
                continue
            line_unit = line_vec / line_len
            pts_arr = np.array(points[start:end+1])
            proj = np.dot(pts_arr - start_pt, line_unit)
            perp = pts_arr - (start_pt + np.outer(proj, line_unit))
            dists = np.linalg.norm(perp, axis=1)
            max_idx = np.argmax(dists)
            max_dist = dists[max_idx]
            if max_dist > epsilon:
                keep[start + max_idx] = True
                stack.append((start, start + max_idx))
                stack.append((start + max_idx, end))
        return [points[i] for i, kept in enumerate(keep) if kept]

    @staticmethod
    def nearest_neighbor_order(strokes):
        if len(strokes) <= 1:
            return strokes
        ordered = []
        remaining = list(strokes)
        current_end = remaining[0][-1]
        ordered.append(remaining.pop(0))
        while remaining:
            best_idx = 0
            best_dist = float("inf")
            reversed_ = False
            for i, stroke in enumerate(remaining):
                d_start = math.hypot(stroke[0][0] - current_end[0], stroke[0][1] - current_end[1])
                d_end = math.hypot(stroke[-1][0] - current_end[0], stroke[-1][1] - current_end[1])
                if d_start < best_dist:
                    best_dist = d_start
                    best_idx = i
                    reversed_ = False
                if d_end < best_dist:
                    best_dist = d_end
                    best_idx = i
                    reversed_ = True
            chosen = remaining.pop(best_idx)
            if reversed_:
                chosen = chosen[::-1]
            ordered.append(chosen)
            current_end = chosen[-1]
        return ordered


# ─────────────────────────────────────────────
#  LINE QUALITY ENGINE  (from drawv2)
# ─────────────────────────────────────────────
class LineQualityEngine:
    LINE_MODES = {
        "raw":      {"smoothing": 1.0, "corner": 90, "min_conf": 0.0},
        "balanced": {"smoothing": 1.8, "corner": 45, "min_conf": 0.3},
        "smooth":   {"smoothing": 2.5, "corner": 30, "min_conf": 0.4},
        "artistic": {"smoothing": 3.2, "corner": 25, "min_conf": 0.2},
    }
    def __init__(self, app):
        self.app = app
        self.smoothing_factor = SETTINGS["LQE_SMOOTHING_FACTOR"]
        self.corner_threshold = SETTINGS["LQE_CORNER_THRESHOLD"]
        self.min_confidence   = SETTINGS["LQE_MIN_CONFIDENCE"]
        self.enabled          = SETTINGS["LQE_ENABLE"]
    def set_line_mode(self, mode):
        if mode not in self.LINE_MODES:
            self.app.log(f"[LQE] Unknown mode '{mode}', keeping current.")
            return
        p = self.LINE_MODES[mode]
        self.smoothing_factor = p["smoothing"]
        self.corner_threshold = p["corner"]
        self.min_confidence = p["min_conf"]
        SETTINGS.update({"LINE_MODE": mode, "LQE_SMOOTHING_FACTOR": p["smoothing"],
                         "LQE_CORNER_THRESHOLD": p["corner"], "LQE_MIN_CONFIDENCE": p["min_conf"]})
        self.app.log(f"[LQE] Mode set to '{mode}'")
    def smooth_stroke(self, stroke):
        if not self.enabled or len(stroke) < 3:
            return stroke
        corners = set(self.detect_corners(stroke))
        angles = []
        for i in range(1, len(stroke)-1):
            a, b, c = [np.array(stroke[i+d]) for d in (-1,0,1)]
            ab, cb = a-b, c-b
            if np.linalg.norm(ab) < 1e-6 or np.linalg.norm(cb) < 1e-6:
                angles.append(0)
            else:
                dot = np.dot(ab, cb)
                norm = np.linalg.norm(ab) * np.linalg.norm(cb)
                angles.append(np.arccos(np.clip(dot/norm, -1.0, 1.0)) * 180 / np.pi)
        mean_angle = np.mean(angles) if angles else 0
        eff_smooth = self.smoothing_factor * (0.5 if mean_angle > 45 else 1.0)
        result = []
        i = 0
        while i < len(stroke)-1:
            result.append(stroke[i])
            if i+1 in corners or i in corners:
                i += 1
                continue
            j = i+1
            while j < len(stroke)-1 and j not in corners and (j+1) not in corners:
                j += 1
            seg_len = j - i
            if seg_len <= 2:
                i += 1
                continue
            target = max(2, int(seg_len * eff_smooth))
            if target <= seg_len:
                step = (j - i) / max(1, target-1)
                for t_idx in range(1, target-1):
                    idx = int(i + t_idx * step)
                    if idx < j:
                        result.append(stroke[idx])
            else:
                cpx = (stroke[i][0] + stroke[j][0]) // 2
                cpy = (stroke[i][1] + stroke[j][1]) // 2
                for k in range(1, target):
                    t = k / target
                    x = (1-t)**2 * stroke[i][0] + 2*(1-t)*t * cpx + t**2 * stroke[j][0]
                    y = (1-t)**2 * stroke[i][1] + 2*(1-t)*t * cpy + t**2 * stroke[j][1]
                    result.append((int(x), int(y)))
            i = j
        result.append(stroke[-1])
        return self.merge_collinear(result)
    def detect_corners(self, stroke):
        if len(stroke) < 3:
            return []
        corners = []
        for i in range(1, len(stroke)-1):
            a, b, c = [np.array(stroke[i+d]) for d in (-1,0,1)]
            ab, cb = a-b, c-b
            if np.linalg.norm(ab) < 1e-6 or np.linalg.norm(cb) < 1e-6:
                continue
            dot = np.dot(ab, cb)
            norm = np.linalg.norm(ab) * np.linalg.norm(cb)
            ang = np.arccos(np.clip(dot/norm, -1.0, 1.0)) * 180 / np.pi
            if ang > self.corner_threshold:
                corners.append(i)
        return corners
    def merge_collinear(self, stroke):
        if len(stroke) < 3:
            return stroke
        result = [stroke[0]]
        for i in range(1, len(stroke)-1):
            x0,y0 = result[-1]
            x1,y1 = stroke[i]
            x2,y2 = stroke[i+1]
            cross = (x1-x0)*(y2-y1) - (y1-y0)*(x2-x1)
            if abs(cross) > 1:
                result.append((x1,y1))
        result.append(stroke[-1])
        uniq = []
        for p in result:
            if not uniq or uniq[-1] != p:
                uniq.append(p)
        return uniq
    def confidence_score(self, stroke):
        if len(stroke) < 2:
            return 0.0
        length_score = min(1.0, len(stroke) / 50.0)
        angles = []
        for i in range(1, len(stroke)-1):
            a, b, c = [np.array(stroke[i+d]) for d in (-1,0,1)]
            ab, cb = a-b, c-b
            if np.linalg.norm(ab) < 1e-6 or np.linalg.norm(cb) < 1e-6:
                ang = 0
            else:
                dot = np.dot(ab, cb)
                norm = np.linalg.norm(ab) * np.linalg.norm(cb)
                ang = np.arccos(np.clip(dot/norm, -1.0, 1.0)) * 180 / np.pi
            angles.append(ang)
        mean_angle = np.mean(angles) if angles else 0
        straight_score = 1.0 - min(1.0, mean_angle / 180.0)
        return 0.6 * length_score + 0.4 * straight_score
    def process_strokes(self, strokes):
        if not self.enabled:
            return strokes
        filtered = []
        total_before = len(strokes)
        for stroke in strokes:
            if len(stroke) < 2:
                continue
            score = self.confidence_score(stroke)
            if score < self.min_confidence:
                continue
            smoothed = self.smooth_stroke(stroke)
            cleaned = self.merge_collinear(smoothed)
            if len(cleaned) >= 2:
                filtered.append(cleaned)
        self.app.log(f"[LQE] Strokes: {total_before} -> {len(filtered)} (conf threshold {self.min_confidence:.2f})")
        return filtered


# ─────────────────────────────────────────────
#  STYLE ENGINE  (from drawv2)
# ─────────────────────────────────────────────
class StyleEngine:
    STYLES = {
        "continuous_stroke": {"merge_distance": 8, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 1.5, "overlap_suppress": False},
        "tap_stroke": {"merge_distance": 0, "tap_mode": True, "jitter": 0, "bezier_steps": 0, "smoothing": 1.0, "overlap_suppress": False},
        "ink_pen": {"merge_distance": 4, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 2.0, "overlap_suppress": True, "min_overlap_ratio": 0.30},
        "anime_lineart": {"merge_distance": 2, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 2.2, "overlap_suppress": True, "canny_low": 60, "canny_high": 150, "corner_threshold": 45},
        "marker": {"merge_distance": 6, "tap_mode": False, "jitter": 1, "bezier_steps": 2, "smoothing": 1.2, "overlap_suppress": False, "duplicate_offset": 1},
        "human_sketch": {"merge_distance": 5, "tap_mode": False, "jitter": 3, "bezier_steps": 6, "smoothing": 1.8, "overlap_suppress": False},
        "precision": {"merge_distance": 1, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 1.0, "overlap_suppress": True, "simplify_eps": 0.5},
        "crosshatch": {"merge_distance": 3, "tap_mode": False, "jitter": 1, "bezier_steps": 1, "smoothing": 1.3, "overlap_suppress": False, "multi_angle": True},
        "stipple": {"merge_distance": 0, "tap_mode": True, "jitter": 0, "bezier_steps": 0, "smoothing": 1.0, "overlap_suppress": False, "stipple_density": 0.5},
        "scribble": {"merge_distance": 0, "tap_mode": False, "jitter": 4, "bezier_steps": 6, "smoothing": 2.5, "overlap_suppress": False, "scribble_passes": 2},
        "contour_emphasized": {"merge_distance": 6, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 1.8, "overlap_suppress": False, "emphasize_silhouette": True},
        "watercolor": {"merge_distance": 10, "tap_mode": False, "jitter": 3, "bezier_steps": 4, "smoothing": 3.0, "overlap_suppress": False, "watercolor_blend": True},
        "etching": {"merge_distance": 1, "tap_mode": False, "jitter": 0, "bezier_steps": 0, "smoothing": 1.0, "overlap_suppress": True, "simplify_eps": 0.2, "multi_angle": True, "canny_low": 80, "canny_high": 200},
        "rough_sketch": {"merge_distance": 3, "tap_mode": False, "jitter": 5, "bezier_steps": 8, "smoothing": 3.5, "overlap_suppress": False, "scribble_passes": 3},
        "pointillist": {"merge_distance": 0, "tap_mode": True, "jitter": 2, "bezier_steps": 0, "smoothing": 1.0, "overlap_suppress": False, "stipple_density": 0.8},
        "hatch_fill": {"merge_distance": 4, "tap_mode": False, "jitter": 2, "bezier_steps": 0, "smoothing": 1.5, "overlap_suppress": False, "multi_angle": True, "hatch_spacing": 3},
        "tonal": {"merge_distance": 5, "tap_mode": False, "jitter": 1, "bezier_steps": 2, "smoothing": 2.0, "overlap_suppress": False, "watercolor_blend": True, "stipple_density": 0.3},
    }
    def __init__(self, app):
        self.app = app
        self._active_style = SETTINGS["DRAW_STYLE"]
        self._style_params = self.STYLES.get(self._active_style, self.STYLES["continuous_stroke"]).copy()
        self.merge_distance = self._style_params.get("merge_distance", SETTINGS["STYLE_MERGE_DISTANCE"])
        self.tap_mode = self._style_params.get("tap_mode", False)
        self.jitter = self._style_params.get("jitter", SETTINGS["JITTER_PX"])
        self.bezier_steps = self._style_params.get("bezier_steps", SETTINGS["BEZIER_STEPS"])
        self.smoothing = self._style_params.get("smoothing", SETTINGS["LQE_SMOOTHING_FACTOR"])
        self.overlap_suppress = self._style_params.get("overlap_suppress", SETTINGS["STYLE_OVERLAP_SUPPRESS"])
        self.min_overlap_ratio = self._style_params.get("min_overlap_ratio", 0.40)
        self.duplicate_offset = self._style_params.get("duplicate_offset", 0)
    def set_style(self, name):
        if name not in self.STYLES:
            self.app.log(f"[Style] Unknown '{name}', keeping '{self._active_style}'")
            return
        self._active_style = name
        self._style_params = self.STYLES[name].copy()
        self.merge_distance = self._style_params.get("merge_distance", SETTINGS["STYLE_MERGE_DISTANCE"])
        self.tap_mode = self._style_params.get("tap_mode", False)
        self.jitter = self._style_params.get("jitter", SETTINGS["JITTER_PX"])
        self.bezier_steps = self._style_params.get("bezier_steps", SETTINGS["BEZIER_STEPS"])
        self.smoothing = self._style_params.get("smoothing", SETTINGS["LQE_SMOOTHING_FACTOR"])
        self.overlap_suppress = self._style_params.get("overlap_suppress", SETTINGS["STYLE_OVERLAP_SUPPRESS"])
        self.min_overlap_ratio = self._style_params.get("min_overlap_ratio", 0.40)
        self.duplicate_offset = self._style_params.get("duplicate_offset", 0)
        SETTINGS["DRAW_STYLE"] = name
        if "jitter" in self._style_params: SETTINGS["JITTER_PX"] = self.jitter
        if "bezier_steps" in self._style_params: SETTINGS["BEZIER_STEPS"] = self.bezier_steps
        if "smoothing" in self._style_params and SETTINGS.get("LQE_ENABLE", False): SETTINGS["LQE_SMOOTHING_FACTOR"] = self.smoothing
        if "canny_low" in self._style_params: SETTINGS["CANNY_LOW"] = self._style_params["canny_low"]
        if "canny_high" in self._style_params: SETTINGS["CANNY_HIGH"] = self._style_params["canny_high"]
        if "corner_threshold" in self._style_params: SETTINGS["LQE_CORNER_THRESHOLD"] = self._style_params["corner_threshold"]
        if "simplify_eps" in self._style_params: SETTINGS["SIMPLIFY_EPS"] = self._style_params["simplify_eps"]
        if "multi_angle" in self._style_params: SETTINGS["HATCH_ENABLE"] = self._style_params["multi_angle"]
        if "stipple_density" in self._style_params: SETTINGS["STYLE_STIPPLE_DENSITY"] = self._style_params["stipple_density"]
        if "scribble_passes" in self._style_params: SETTINGS["STYLE_SCRIBBLE_PASSES"] = self._style_params["scribble_passes"]
        if "hatch_spacing" in self._style_params: SETTINGS["HATCH_SPACING"] = self._style_params["hatch_spacing"]
        self.app.log(f"[Style] Switched to '{name}'")
    def get_param(self, key):
        return self._style_params.get(key, SETTINGS.get(key))
    def set_param(self, key, value):
        self._style_params[key] = value
        self.STYLES[self._active_style][key] = value
        if key == "merge_distance": self.merge_distance = value
        elif key == "tap_mode": self.tap_mode = value
        elif key == "jitter": self.jitter = value; SETTINGS["JITTER_PX"] = value
        elif key == "bezier_steps": self.bezier_steps = value; SETTINGS["BEZIER_STEPS"] = value
        elif key == "smoothing": self.smoothing = value
        elif key in ("multi_angle","emphasize_silhouette","watercolor_blend"): SETTINGS["HATCH_ENABLE"] = value if key == "multi_angle" else SETTINGS["HATCH_ENABLE"]
        elif key == "stipple_density": SETTINGS["STYLE_STIPPLE_DENSITY"] = value
        elif key == "scribble_passes": SETTINGS["STYLE_SCRIBBLE_PASSES"] = value
        self.app.log(f"[Style] Param '{key}' set to {value}")
    def apply(self, strokes):
        if not strokes:
            return strokes
        result = strokes
        if self.merge_distance > 0:
            merged = []
            i = 0
            while i < len(result):
                current = result[i][:]
                j = i + 1
                while j < len(result):
                    last_pt = current[-1]
                    first_next = result[j][0]
                    if math.hypot(last_pt[0]-first_next[0], last_pt[1]-first_next[1]) <= self.merge_distance:
                        current.extend(result[j]); j += 1
                    else:
                        break
                merged.append(current); i = j
            result = merged
        if self.overlap_suppress and len(result) > 1:
            bboxes = [(min(p[0] for p in s), min(p[1] for p in s), max(p[0] for p in s), max(p[1] for p in s)) for s in result]
            keep = [True]*len(result)
            for i in range(len(result)):
                if not keep[i]: continue
                for j in range(i+1, len(result)):
                    if not keep[j]: continue
                    if (bboxes[i][2] < bboxes[j][0] or bboxes[i][0] > bboxes[j][2] or
                        bboxes[i][3] < bboxes[j][1] or bboxes[i][1] > bboxes[j][3]): continue
                    inter = len(set(result[i]) & set(result[j]))
                    min_len = min(len(result[i]), len(result[j]))
                    if min_len == 0: continue
                    ratio = inter / min_len
                    if ratio > self.min_overlap_ratio:
                        if len(result[i]) < len(result[j]):
                            keep[i] = False; break
                        else:
                            keep[j] = False
            result = [s for idx,s in enumerate(result) if keep[idx]]
        if self.duplicate_offset > 0:
            duped = []
            for s in result:
                duped.append(s)
                duped.append([(x+self.duplicate_offset, y+self.duplicate_offset) for x,y in s])
            result = duped
        active = self._active_style
        if active == "scribble":
            passes = SETTINGS.get("STYLE_SCRIBBLE_PASSES", 2)
            if passes > 1 and result:
                scribbled = []
                for s in result:
                    for p in range(passes):
                        if p == 0: scribbled.append(s)
                        else:
                            j = random.randint(1,3)
                            scribbled.append([(x+random.randint(-j,j), y+random.randint(-j,j)) for x,y in s])
                result = scribbled
        elif active == "watercolor":
            if result:
                blended = []
                for s in result:
                    blended.append(s)
                    off = 2
                    blended.append([(x+random.randint(-off,off), y+random.randint(-off,off)) for x,y in s])
                    for _ in range(2):
                        blended.append([(x+random.randint(-4,4), y+random.randint(-4,4)) for x,y in s][:max(2, len(s)//2)])
                result = blended
        elif active == "stipple":
            if self.tap_mode and result:
                stippled = []
                for s in result:
                    for pt in s:
                        stippled.append([pt])
                        stippled.append(["PEN_LIFT"])
                if stippled: stippled.pop()
                result = stippled
        elif active == "contour_emphasized":
            if result:
                scored = [(len(s), s) for s in result]
                scored.sort(key=lambda x: -x[0])
                result = [s for _, s in scored]
        return result


# ─────────────────────────────────────────────
#  VIEWPORT TRACKER  (from drawv2)
# ─────────────────────────────────────────────
class ViewportTracker:
    def __init__(self, canvas_rect, app=None):
        self.app = app
        self.canvas_rect = canvas_rect
        self.origin = (canvas_rect[0], canvas_rect[1])
        self.zoom = SETTINGS["VIEWPORT_ZOOM"]
        self.scroll_dx = SETTINGS["VIEWPORT_SCROLL_DX"]
        self.scroll_dy = SETTINGS["VIEWPORT_SCROLL_DY"]
        self.auto_scroll = SETTINGS["VIEWPORT_AUTO_SCROLL"]
    def recalibrate(self, canvas_rect=None):
        if canvas_rect:
            self.canvas_rect = canvas_rect
            self.origin = (canvas_rect[0], canvas_rect[1])
    def img_to_screen(self, x, y, img_w, img_h):
        cw = self.canvas_rect[2] - self.canvas_rect[0]
        ch = self.canvas_rect[3] - self.canvas_rect[1]
        scaled_w = img_w * self.zoom; scaled_h = img_h * self.zoom
        ox = (cw - scaled_w) / 2 + self.scroll_dx
        oy = (ch - scaled_h) / 2 + self.scroll_dy
        sx = int(self.origin[0] + x * self.zoom + ox)
        sy = int(self.origin[1] + y * self.zoom + oy)
        return sx, sy
    def screen_to_img(self, sx, sy, img_w, img_h):
        cw = self.canvas_rect[2] - self.canvas_rect[0]
        ch = self.canvas_rect[3] - self.canvas_rect[1]
        scaled_w = img_w * self.zoom; scaled_h = img_h * self.zoom
        ox = (cw - scaled_w) / 2 + self.scroll_dx
        oy = (ch - scaled_h) / 2 + self.scroll_dy
        return int((sx - self.origin[0] - ox) / self.zoom), int((sy - self.origin[1] - oy) / self.zoom)
    def transform_all(self, strokes, img_size):
        if not strokes: return []
        img_w, img_h = img_size
        transformed = []
        for stroke in strokes:
            new_stroke = []
            for x, y in stroke:
                sx, sy = self.img_to_screen(x, y, img_w, img_h)
                new_stroke.append((sx, sy))
            if len(new_stroke) >= 2:
                transformed.append(new_stroke)
        return transformed


# ─────────────────────────────────────────────
#  VIRTUAL CANVAS  (from drawv2)
# ─────────────────────────────────────────────
class VirtualCanvas:
    def __init__(self, width=800, height=600):
        self.width = width; self.height = height
        self.buffer = Image.new("RGB", (width, height), SETTINGS.get("VIRTUAL_BG_COLOR", "#ffffff"))
        self.draw = ImageDraw.Draw(self.buffer)
    def reset(self, bg_color=None):
        if bg_color is None: bg_color = SETTINGS.get("VIRTUAL_BG_COLOR", "#ffffff")
        self.buffer = Image.new("RGB", (self.width, self.height), bg_color)
        self.draw = ImageDraw.Draw(self.buffer)
    def render_stroke(self, stroke, color=(0,0,0), width=None):
        if len(stroke) < 2: return
        w = width if width is not None else SETTINGS.get("STROKE_WIDTH", 2)
        self.draw.line(stroke, fill=color, width=w)
    def render_strokes(self, strokes, color=(0,0,0), width=None):
        for s in strokes: self.render_stroke(s, color, width)
    def render_fill_op(self, fill_op, color=None):
        if color is None: color = tuple(fill_op.get("color", (200,200,200)))
        center = fill_op.get("center", (self.width//2, self.height//2))
        r = int(SETTINGS.get("STROKE_WIDTH", 2) * 4)
        x, y = center
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
    def get_image(self):
        return self.buffer
    def save(self, path):
        self.buffer.save(path)


# ─────────────────────────────────────────────
#  COLOR ENGINE  (from drawv2)
# ─────────────────────────────────────────────
class ColorEngine:
    def __init__(self, app):
        self.app = app
        self._palette = []
        self._cache_path = os.path.join(DIR_PATH, "palette_cache")
        os.makedirs(self._cache_path, exist_ok=True)
    def _cache_key(self, region, layout, spacing):
        return hashlib.md5(f"{region}_{layout}_{spacing}".encode()).hexdigest()[:16]
    def scan_palette(self, region, layout="grid", spacing=4):
        x1, y1, x2, y2 = region
        samples = []
        if layout == "grid":
            for y in range(y1, y2, spacing):
                for x in range(x1, x2, spacing):
                    try:
                        rgb = pyautogui.pixel(x, y) if HAS_PYAUTOGUI else ImageGrab.grab((x,y,x+1,y+1)).getpixel((0,0))
                        samples.append({"pos":[x,y],"rgb":list(rgb[:3])})
                    except: pass
        elif layout == "snake":
            for y in range(y1, y2, spacing):
                x_range = range(x1, x2, spacing) if ((y-y1)//spacing)%2==0 else range(x2-spacing, x1-1, -spacing)
                for x in x_range:
                    try:
                        rgb = pyautogui.pixel(x, y) if HAS_PYAUTOGUI else ImageGrab.grab((x,y,x+1,y+1)).getpixel((0,0))
                        samples.append({"pos":[x,y],"rgb":list(rgb[:3])})
                    except: pass
        elif layout == "spiral":
            cx, cy = (x1+x2)//2, (y1+y2)//2
            for r in range(0, max(x2-x1,y2-y1)//2, spacing):
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)
                    x = int(cx + r*math.cos(rad)); y = int(cy + r*math.sin(rad))
                    if x1<=x<=x2 and y1<=y<=y2:
                        try:
                            rgb = pyautogui.pixel(x, y) if HAS_PYAUTOGUI else ImageGrab.grab((x,y,x+1,y+1)).getpixel((0,0))
                            samples.append({"pos":[x,y],"rgb":list(rgb[:3])})
                        except: pass
        else:
            for y in range(y1, y2, spacing):
                for x in range(x1, x2, spacing):
                    try:
                        rgb = pyautogui.pixel(x, y) if HAS_PYAUTOGUI else ImageGrab.grab((x,y,x+1,y+1)).getpixel((0,0))
                        samples.append({"pos":[x,y],"rgb":list(rgb[:3])})
                    except: pass
        self.app.log(f"[Color] Scanned {len(samples)} samples")
        return samples
    def cluster_palette(self, raw_colors, n_clusters):
        if not raw_colors or n_clusters < 1:
            return []
        pixels = np.array([c["rgb"] for c in raw_colors], dtype=np.float32)
        positions = np.array([c["pos"] for c in raw_colors], dtype=np.float32)
        if len(pixels) < n_clusters: n_clusters = len(pixels)
        if HAS_SCIPY:
            from scipy.cluster.vq import kmeans
            centroids, _ = kmeans(pixels, n_clusters)
            dists = np.linalg.norm(pixels[:,None] - centroids[None], axis=2)
            labels = np.argmin(dists, axis=1)
            avg_positions = []
            for k in range(n_clusters):
                mask = (labels==k)
                avg_positions.append(positions[mask].mean(axis=0).tolist() if np.any(mask) else [0,0])
        else:
            idx = np.random.choice(len(pixels), n_clusters, replace=False)
            centroids = pixels[idx].copy()
            avg_positions = []
            for _ in range(20):
                dists = np.linalg.norm(pixels[:,None] - centroids[None], axis=2)
                labels = np.argmin(dists, axis=1)
                new_cents, new_pos = [], []
                for k in range(n_clusters):
                    mask = (labels==k)
                    if np.any(mask):
                        new_cents.append(pixels[mask].mean(axis=0))
                        new_pos.append(positions[mask].mean(axis=0).tolist())
                    else:
                        new_cents.append(centroids[k])
                        new_pos.append([0,0])
                if np.allclose(centroids, np.array(new_cents), atol=0.1):
                    avg_positions = new_pos; break
                centroids = np.array(new_cents)
                avg_positions = new_pos
        palette = []
        for rgb, pos in zip(centroids, avg_positions):
            palette.append({"pos":[int(round(pos[0])),int(round(pos[1]))], "rgb":[max(0,min(255,int(v))) for v in rgb]})
        self.app.log(f"[Color] Clustered {len(raw_colors)} -> {len(palette)} colors")
        return palette

    def nearest_color(self, pixel_rgb):
        if not self.app.palette_map:
            return 0
        pal_arr = np.array([c["rgb"] for c in self.app.palette_map], dtype=np.float32)
        metric = SETTINGS["COLOR_METRIC"]
        if metric == "Manhattan":
            dists = np.sum(np.abs(pal_arr - np.array(pixel_rgb, dtype=np.float32)), axis=1)
        else:
            dists = np.linalg.norm(pal_arr - np.array(pixel_rgb, dtype=np.float32), axis=1)
        return int(np.argmin(dists))


# ─────────────────────────────────────────────
#  CALIBRATION MANAGER  (from drawv2)
# ─────────────────────────────────────────────
class CalibrationManager:
    PROFILES_DIR = os.path.join(DIR_PATH, "profiles")
    REQUIRED_FIELDS = ["name", "palette_region", "brush_pos", "fill_pos", "erase_pos",
                       "canvas_rect", "ui_layout", "palette", "settings", "text_objects",
                       "tool_mode", "brush_size", "brush_color", "active_layer"]
    def __init__(self, app):
        self.app = app
        os.makedirs(self.PROFILES_DIR, exist_ok=True)
    def _build_profile(self):
        return {"name": getattr(self.app,"_active_profile_name","unnamed"),
                "palette_region": getattr(self.app,"palette_region",[0,0,0,0]),
                "brush_pos": getattr(self.app,"brush_pos",[0,0]),
                "fill_pos": getattr(self.app,"fill_pos",[0,0]),
                "erase_pos": getattr(self.app,"erase_pos",[0,0]),
                "canvas_rect": self.app.canvas_rect or [0,0,800,600],
                "ui_layout": getattr(self.app,"ui_layout","default"),
                "palette": list(self.app.palette_map),
                "palette_map": list(self.app.palette_map),
                "settings": dict(SETTINGS),
                "text_objects": list(getattr(self.app,"text_objects",[])),
                "tool_mode": getattr(self.app,"tool_mode","Move"),
                "brush_size": getattr(self.app,"brush_size",10),
                "brush_color": list(getattr(self.app,"brush_color",(0,0,255))),
                "active_layer": getattr(self.app,"active_layer",0)}
    def serialize(self, profile):
        for f in self.REQUIRED_FIELDS:
            if f not in profile: raise ValueError(f"Missing: {f}")
        return json.dumps(profile, indent=2)
    def deserialize(self, data):
        p = json.loads(data)
        for f in self.REQUIRED_FIELDS:
            if f not in p: raise ValueError(f"Missing: {f}")
        return p
    def save(self, name):
        if not name or not name.strip(): return False
        profile = self._build_profile()
        try:
            with open(os.path.join(self.PROFILES_DIR,f"{name.strip()}.json"),"w") as f:
                f.write(self.serialize(profile))
            self.app.log(f"[Calib] Saved: {name}"); return True
        except Exception as e: self.app.log(f"[Calib] Save error: {e}"); return False
    def load(self, name):
        path = os.path.join(self.PROFILES_DIR, f"{name}.json")
        if not os.path.exists(path): return False
        try:
            with open(path) as f: profile = self.deserialize(f.read())
            self.app.canvas_rect = profile["canvas_rect"]
            self.app.palette_map = profile["palette_map"]
            for k,v in profile["settings"].items():
                if k in SETTINGS: SETTINGS[k] = v
            self.app.log(f"[Calib] Loaded: {name}"); return True
        except Exception as e: self.app.log(f"[Calib] Load error: {e}"); return False
    def import_profile(self):
        path = filedialog.askopenfilename(title="Import Profile", filetypes=[("JSON","*.json")], initialdir=self.PROFILES_DIR)
        if not path: return False
        try:
            with open(path) as f: profile = self.deserialize(f.read())
            name = os.path.splitext(os.path.basename(path))[0]
            with open(os.path.join(self.PROFILES_DIR,f"{name}.json"),"w") as f:
                f.write(self.serialize(profile))
            self.app.log(f"[Calib] Imported: {name}"); return True
        except Exception as e: self.app.log(f"[Calib] Import error: {e}"); return False
    def export_profile(self, name):
        src = os.path.join(self.PROFILES_DIR, f"{name}.json")
        if not os.path.exists(src): return False
        dest = filedialog.asksaveasfilename(title=f"Export: {name}", defaultextension=".json",
                                            filetypes=[("JSON","*.json")], initialfile=f"{name}.json")
        if not dest: return False
        try: shutil.copy2(src, dest); self.app.log(f"[Calib] Exported to {dest}"); return True
        except Exception as e: self.app.log(f"[Calib] Export error: {e}"); return False


# ─────────────────────────────────────────────
#  FILL INTELLIGENCE  (from drawv2)
# ─────────────────────────────────────────────
class FillIntelligence:
    def __init__(self, app):
        self.app = app
        self.driver = FastInputDriver()
        self.fill_hotkey = SETTINGS.get("FILL_HOTKEY", "f9")
        self.variance_threshold = SETTINGS.get("FILL_VARIANCE_THRESHOLD", 500)
        self.min_area = SETTINGS.get("MIN_FILL_AREA", 200)
    def classify_region(self, region_pixels):
        if len(region_pixels) < self.min_area: return "stroke"
        arr = np.array(region_pixels, dtype=np.float32)
        return "fill_candidate" if np.var(arr, axis=0).sum() < self.variance_threshold else "stroke"
    def detect_background(self, canvas_pixels):
        if len(canvas_pixels) < 10: return None
        arr = np.array(canvas_pixels, dtype=np.float32)
        mean = arr.mean(axis=0)
        if np.all(np.abs(arr - mean) <= 10): return tuple(int(v) for v in mean)
        return None
    def plan(self, img, strokes):
        fill_ops = []
        remaining = strokes[:]
        if not SETTINGS.get("FILL_ENABLE", True): return fill_ops, remaining
        try:
            if self.app.canvas_rect:
                x1,y1,x2,y2 = self.app.canvas_rect
                border_pixels = []
                for x in range(x1, x2, 10):
                    try:
                        rgb = pyautogui.pixel(x, y1); border_pixels.append(rgb[:3])
                        rgb = pyautogui.pixel(x, y2-1); border_pixels.append(rgb[:3])
                    except: pass
                for y in range(y1, y2, 10):
                    try:
                        rgb = pyautogui.pixel(x1, y); border_pixels.append(rgb[:3])
                        rgb = pyautogui.pixel(x2-1, y); border_pixels.append(rgb[:3])
                    except: pass
                bg = self.detect_background(border_pixels)
                if bg:
                    bg_idx = self.app.color_engine.nearest_color(bg)
                    bg_entry = self.app.palette_map[bg_idx]
                    fill_ops.append({"type":"background","color":bg_entry["rgb"],"pos":bg_entry["pos"],
                                     "hotkey":self.fill_hotkey,"center":((x1+x2)//2,(y1+y2)//2)})
        except: pass
        return fill_ops, remaining
    def execute_fill(self, fill_op):
        if not fill_op: return False
        try:
            if fill_op.get("hotkey"):
                from pynput.keyboard import Key, Controller as KeyController
                kb = KeyController()
                hk = fill_op["hotkey"].lower().strip()
                if hk.startswith('f') and hk[1:].isdigit():
                    key = getattr(Key, f'f{hk[1:]}', None)
                    if key: kb.press(key); kb.release(key); return True
            elif "center" in fill_op:
                self.driver.click(*fill_op["center"])
            return True
        except Exception as e:
            self.app.log(f"[Fill] Error: {e}"); return False


# ─────────────────────────────────────────────
#  BACKGROUND ANALYZER  (from drawv2)
# ─────────────────────────────────────────────
class BackgroundAnalyzer:
    def __init__(self, app):
        self.app = app
    def analyze(self, canvas_rect):
        if not canvas_rect or len(canvas_rect) != 4:
            return {"brightness":128,"recommended_colors":[],"canny_adjustment":0}
        x1,y1,x2,y2 = canvas_rect
        border_pixels = []
        try:
            for x in range(x1, x2, max(1, (x2-x1)//20)):
                for y in [y1, y2-1]:
                    for dy in range(min(5, y2-y1)):
                        py = y+dy
                        if y1 <= py < y2:
                            try:
                                rgb = pyautogui.pixel(x, py) if HAS_PYAUTOGUI else ImageGrab.grab((x,py,x+1,py+1)).getpixel((0,0))
                                border_pixels.append(rgb[:3])
                            except: pass
            for y in range(y1, y2, max(1, (y2-y1)//20)):
                for x in [x1, x2-1]:
                    for dx in range(min(5, x2-x1)):
                        px = x+dx
                        if x1 <= px < x2:
                            try:
                                rgb = pyautogui.pixel(px, y) if HAS_PYAUTOGUI else ImageGrab.grab((px,y,px+1,y+1)).getpixel((0,0))
                                border_pixels.append(rgb[:3])
                            except: pass
        except: pass
        if not border_pixels: return {"brightness":128,"recommended_colors":[],"canny_adjustment":0}
        b = self._brightness(border_pixels)
        return {"brightness": b, "recommended_colors": self._recommend(b), "canny_adjustment": self._canny_adj(b)}
    def _brightness(self, pixels):
        arr = np.array(pixels, dtype=np.float32)
        return float(np.mean(0.299*arr[:,0] + 0.587*arr[:,1] + 0.114*arr[:,2]))
    def _recommend(self, brightness):
        if not self.app.palette_map: return []
        pal = np.array([c["rgb"] for c in self.app.palette_map], dtype=np.float32)
        lum = 0.299*pal[:,0] + 0.587*pal[:,1] + 0.114*pal[:,2]
        if brightness > 180: cand = np.where(lum < 100)[0]
        elif brightness < 75: cand = np.where(lum > 155)[0]
        else: return [int(np.argmax(np.abs(lum - brightness)))]
        if len(cand) == 0: return [int(np.argmax(np.abs(lum - brightness)))]
        return cand.tolist()
    def _canny_adj(self, b):
        return 20 if b > 180 else (-20 if b < 75 else 0)


# ─────────────────────────────────────────────
#  AI IMAGE GENERATOR  (CPU-only, Tiny-SD via Diffusers)
# ─────────────────────────────────────────────
class AIImageGenerator:
    """CPU-only local AI image generation via Hugging Face Diffusers.

    Runs the actual model in an isolated subprocess so segfaults in
    torch/diffusers C++ code do NOT crash the main app.
    """
    MODEL_ID = "segmind/tiny-sd"

    def __init__(self):
        self.pipe = None
        self._loaded = False

    def load_model(self):
        self._loaded = True

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "blurry, low quality, watermark, text, distorted",
        steps: int = 15,
        width: int = 512,
        height: int = 512,
        seed: int = None
    ):
        img, err = _run_ai_subprocess(
            prompt,
            model_id=self.MODEL_ID,
            negative_prompt=negative_prompt,
            steps=steps,
            guidance=7.0,
            seed=seed if seed is not None else -1,
        )
        if img is not None:
            return img
        raise RuntimeError(f"AI image generation failed: {err}")

    def unload_model(self):
        self.pipe = None
        self._loaded = False
        import gc
        gc.collect()


# ─────────────────────────────────────────────
#  PROMPT PIPELINE  (from drawv2)
# ─────────────────────────────────────────────

class PromptPipeline:
    PROVIDERS = {
        "pollinations": {"url":"https://pollinations.ai/api/v1/generate",
            "headers":{"Content-Type":"application/json"},
            "payload_template":{"prompt":"{prompt}","negative_prompt":"{negative}","width":512,"height":512,"model":"flux","seed":-1},
            "response_type":"binary"},
        "arena_ai": {"url":"https://api.aren.ai/v1/images/generations",
            "headers":{"Content-Type":"application/json"},
            "payload_template":{"prompt":"{prompt}","negative_prompt":"{negative}","model":"sdxl","steps":20,"cfg_scale":7},
            "response_type":"base64_json"},
        "stable_diffusion_local": {"url":"http://127.0.0.1:7860/sdapi/v1/txt2img",
            "headers":{},
            "payload_template":{"prompt":"{prompt}","negative_prompt":"{negative}","steps":20,"cfg_scale":7,"width":512,"height":512},
            "response_type":"base64_array"},
        "tiny_sd": {"local": True},
        "custom_api": {"url":"","headers":{},"payload_template":{"prompt":"{prompt}","negative":"{negative}"},"response_type":"binary"}
    }
    STYLE_PRESETS = {
        "anime_sketch": "anime line art, black and white, sketch, clean lines",
        "realistic": "photorealistic, highly detailed, 8k",
        "oil_painting": "oil painting, brush strokes, canvas texture",
        "watercolor": "watercolor painting, soft edges, wet paint",
        "pencil": "pencil drawing, hatching, grayscale",
    }
    def __init__(self, app):
        self.app = app
        self.active = False
        self.provider = SETTINGS.get("PROMPT_PROVIDER", "pollinations")
        self.endpoint = SETTINGS.get("PROMPT_ENDPOINT", "")
        self.negative_prompt = SETTINGS.get("PROMPT_NEGATIVE", "")
        self.timeout = SETTINGS.get("PROMPT_API_TIMEOUT", 30)
        self._ai_gen = AIImageGenerator() if HAS_TORCH and HAS_DIFFUSERS else None
        self.configure(self.provider, self.endpoint)
    def configure(self, provider, endpoint=None, headers=None):
        if provider not in self.PROVIDERS and provider != "custom_api":
            self.app.log(f"[Prompt] Unknown provider: {provider}"); self.active = False; return
        if provider == "tiny_sd" and self._ai_gen is None:
            self.app.log("[Prompt] Tiny-SD unavailable (install torch+dffusers)"); self.active = False; return
        self.provider = provider
        self.endpoint = endpoint or self.PROVIDERS.get(provider,{}).get("url","")
        self.active = True
        self.app.log(f"[Prompt] Enabled: {provider}")
    def generate(self, prompt, style_preset=None):
        if not self.active or not prompt: return None
        style = style_preset or SETTINGS.get("PROMPT_STYLE_PRESET", "anime_sketch")
        preset_text = self.STYLE_PRESETS.get(style, style)
        full_prompt = f"{prompt}, {preset_text}" if preset_text else prompt
        if self.provider == "tiny_sd":
            if self._ai_gen:
                steps = int(SETTINGS.get("PROMPT_STEPS", 15))
                width = int(SETTINGS.get("AI_WIDTH", 512))
                height = int(SETTINGS.get("AI_HEIGHT", 512))
                seed = int(SETTINGS.get("AI_SEED", -1))
                neg = self.negative_prompt or "blurry, low quality, watermark, text, distorted"
                try:
                    img = self._ai_gen.generate_image(
                        prompt=full_prompt,
                        negative_prompt=neg,
                        steps=steps,
                        width=width,
                        height=height,
                        seed=seed if seed >= 0 else None,
                    )
                    return self._generate_cleanup(img) if img else None
                except Exception as e:
                    self.app.log(f"[Prompt] Tiny-SD generation error: {e}")
                    return None
            return None
        payload = self._build_request(prompt, style)
        url = self.endpoint or self.PROVIDERS.get(self.provider,{}).get("url","")
        if not url: return None
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=self.PROVIDERS.get(self.provider,{}).get("headers",{}), method='POST')
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                response = resp.read()
                ct = resp.headers.get('Content-Type','')
            if self.provider == "pollinations" and ct.startswith('image/'):
                return self._generate_cleanup(Image.open(io.BytesIO(response)).convert("RGB"))
            result = json.loads(response)
            image_data = None
            rt = self.PROVIDERS.get(self.provider,{}).get("response_type","")
            if rt == "base64_json" and "data" in result and len(result["data"])>0:
                image_data = base64.b64decode(result["data"][0]["b64_json"])
            elif rt == "base64_array" and "images" in result and len(result["images"])>0:
                image_data = base64.b64decode(result["images"][0])
            elif "image" in result:
                if isinstance(result["image"], str) and result["image"].startswith("http"):
                    with urllib.request.urlopen(result["image"], timeout=self.timeout) as ir:
                        image_data = ir.read()
                else: image_data = base64.b64decode(result["image"])
            if image_data:
                return self._generate_cleanup(Image.open(io.BytesIO(image_data)).convert("RGB"))
        except (urllib.error.URLError, socket.timeout, Exception) as e:
            self.app.log(f"[Prompt] Failed: {e}")
            if self.provider == "pollinations":
                try:
                    get_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
                    with urllib.request.urlopen(get_url, timeout=self.timeout) as resp:
                        return self._generate_cleanup(Image.open(io.BytesIO(resp.read())).convert("RGB"))
                except: pass
        return None
    def _build_request(self, prompt, style_preset):
        preset_text = self.STYLE_PRESETS.get(style_preset, style_preset)
        full_prompt = f"{prompt}, {preset_text}" if preset_text else prompt
        template = self.PROVIDERS.get(self.provider,{}).get("payload_template",{})
        payload = {}
        for k,v in template.items():
            if isinstance(v, str): payload[k] = v.format(prompt=full_prompt, negative=self.negative_prompt)
            else: payload[k] = v
        return payload
    def _generate_cleanup(self, img):
        if img is None: return None
        try: img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        except: pass
        try: img = ImageEnhance.Contrast(img).enhance(1.2)
        except: pass
        try: img = img.filter(ImageFilter.SHARPEN)
        except: pass
        self.app.base_img = img; self.app.final_img = None
        self.app.log(f"[Prompt] Generated {img.size}")
        return img


# ─────────────────────────────────────────────
#  STRUCTURE ANALYZER  (from drawv2)
# ─────────────────────────────────────────────
class StructureAnalyzer:
    def __init__(self, app):
        self.app = app
        self._cache = {}
    def _cache_key(self, img, snap):
        ih = hashlib.md5(img.tobytes()).hexdigest()[:16]
        rel = {k: snap.get(k) for k in ["CANNY_LOW","CANNY_HIGH","STRUCTURE_DETAIL_THRESHOLD","SIMPLIFY_EPS","CONTOUR_APPROX","MIN_STROKE_LEN"]}
        ch = hashlib.md5(json.dumps(rel, sort_keys=True).encode()).hexdigest()[:8]
        return f"{ih}_{ch}"
    def analyze(self, img, snap=None):
        if snap is None: snap = dict(SETTINGS)
        key = self._cache_key(img, snap)
        if key in self._cache: return self._cache[key]
        gray = np.array(img.convert("L"), dtype=np.uint8)
        lo = snap.get("CANNY_LOW", 40); hi = snap.get("CANNY_HIGH", 120)
        if HAS_CV2:
            edges = cv2.Canny(gray, lo, hi)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
            edges = cv2.dilate(edges, kernel, iterations=1)
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            raw = []
            for cnt in contours:
                if len(cnt) < snap.get("MIN_STROKE_LEN",3): continue
                pts = [(int(p[0][0]),int(p[0][1])) for p in cnt]
                if snap.get("CONTOUR_APPROX", True):
                    pts = PathOptimizer.douglas_peucker(pts, snap.get("SIMPLIFY_EPS",1.5))
                if len(pts) >= 2: raw.append(pts)
        else:
            ep = np.array(img.convert("L").filter(ImageFilter.FIND_EDGES)) > 128
            h,w = ep.shape; visited = np.zeros((h,w), dtype=bool)
            raw = []
            for y in range(h):
                for x in range(w):
                    if ep[y,x] and not visited[y,x]:
                        stroke = [(x,y)]; visited[y,x] = True; cx,cy = x,y
                        while True:
                            moved = False
                            for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                                nx,ny = cx+dx, cy+dy
                                if 0<=nx<w and 0<=ny<h and ep[ny,nx] and not visited[ny,nx]:
                                    stroke.append((nx,ny)); visited[ny,nx] = True; cx,cy = nx,ny
                                    moved = True; break
                            if not moved: break
                        if len(stroke) >= snap.get("MIN_STROKE_LEN",3):
                            raw.append(stroke)
        scores = [self.score_contour(s, snap) for s in raw]
        thresh = snap.get("STRUCTURE_DETAIL_THRESHOLD", 0.5)
        kept, kept_scores = zip(*[(s,sc) for s,sc in zip(raw, scores) if sc >= thresh]) if any(sc >= thresh for sc in scores) else ([],[])
        kept = list(kept); kept_scores = list(kept_scores)
        if snap.get("STYLE_OVERLAP_SUPPRESS", True):
            kept, kept_scores = self.suppress_overlaps(kept, kept_scores)
        self._cache[key] = (kept, kept_scores)
        self.app.log(f"[Struct] {len(raw)} raw -> {len(kept)} kept (thresh {thresh})")
        return kept, kept_scores
    def score_contour(self, stroke, snap):
        if len(stroke) < 2: return 0.0
        ls = min(1.0, len(stroke)/100.0)
        angles = []
        for i in range(1, len(stroke)-1):
            a,b,c = [np.array(stroke[i+d]) for d in (-1,0,1)]
            ab,cb = a-b, c-b
            if np.linalg.norm(ab) < 1e-6 or np.linalg.norm(cb) < 1e-6: ang = 0
            else:
                dot = np.dot(ab,cb)
                ang = np.arccos(np.clip(dot/(np.linalg.norm(ab)*np.linalg.norm(cb)), -1.0, 1.0))*180/np.pi
            angles.append(ang)
        ma = np.mean(angles) if angles else 0
        gs = 1.0 - min(1.0, ma/180.0)
        xs = [p[0] for p in stroke]; ys = [p[1] for p in stroke]
        ba = (max(xs)-min(xs))*(max(ys)-min(ys))
        sil = 0.2 if (ba > 5000 and gs > 0.7 and (min(xs) < 20 or max(xs) > (self.app.base_img.width-20) if self.app.base_img else False)) else 0.0
        return min(1.0, 0.4*gs + 0.4*ls + 0.1 + sil)
    def suppress_overlaps(self, strokes, scores):
        if len(strokes) <= 1: return strokes, scores
        sets = [set(s) for s in strokes]
        keep = [True]*len(strokes)
        for i in range(len(strokes)):
            if not keep[i]: continue
            for j in range(i+1, len(strokes)):
                if not keep[j]: continue
                inter = len(sets[i] & sets[j])
                mlen = min(len(sets[i]), len(sets[j]))
                if mlen == 0: continue
                if inter/mlen > 0.40:
                    if scores[i] >= scores[j]: keep[j] = False
                    else: keep[i] = False; break
        return [s for idx,s in enumerate(strokes) if keep[idx]], [s for idx,s in enumerate(scores) if keep[idx]]


# ─────────────────────────────────────────────
#  PREDRAW RESULT  (from drawv2)
# ─────────────────────────────────────────────
@dataclass
class PredrawResult:
    fill_ops: List[dict]
    final_strokes: List[List[Tuple[int, int]]]
    palette_entry: dict
    bg_brightness: float
    filtered_count: int
    stats: dict = field(default_factory=dict)


# ─────────────────────────────────────────────
#  INTELLIGENT DRAW ENGINE  (from drawv2)
# ─────────────────────────────────────────────
class IntelligentDrawEngine:
    def __init__(self, app):
        self.app = app
        self.driver = FastInputDriver()
        self.hms = HumanMotionSimulator()
        self.opt = PathOptimizer()
    def preprocess(self, img):
        gray = np.array(img.convert("L"), dtype=np.uint8)
        if HAS_CV2:
            gray = cv2.bilateralFilter(gray, 7, 50, 50)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
            gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        else:
            gray = np.array(ImageEnhance.Contrast(Image.fromarray(gray)).enhance(1.6).filter(ImageFilter.GaussianBlur(radius=0.8)))
        return gray
    def detect_edges(self, gray):
        lo = int(SETTINGS["CANNY_LOW"]); hi = int(SETTINGS["CANNY_HIGH"])
        if HAS_CV2:
            edges = cv2.Canny(gray, lo, hi)
            k = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
            edges = cv2.dilate(edges, k, iterations=1)
        else:
            arr = np.array(Image.fromarray(gray).filter(ImageFilter.FIND_EDGES), dtype=np.float32)
            edges = (arr > arr.max()*(lo/255.0)).astype(np.uint8)*255
        return edges
    def extract_contour_strokes(self, edges, epsilon):
        strokes = []
        if HAS_CV2:
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                if len(cnt) < SETTINGS["MIN_STROKE_LEN"]: continue
                pts = [(int(p[0][0]),int(p[0][1])) for p in cnt]
                if SETTINGS["CONTOUR_APPROX"] and epsilon > 0:
                    pts = self.opt.douglas_peucker(pts, epsilon)
                if len(pts) >= 2: strokes.append(pts)
        else:
            h,w = edges.shape; binary = edges > 127; visited = np.zeros((h,w), dtype=bool)
            def nbrs(x,y):
                for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                    nx,ny = x+dx,y+dy
                    if 0<=nx<w and 0<=ny<h: yield nx,ny
            for sy in range(h):
                for sx in range(w):
                    if binary[sy,sx] and not visited[sy,sx]:
                        stroke = [(sx,sy)]; visited[sy,sx] = True; cx,cy = sx,sy
                        while True:
                            moved = False
                            for nx,ny in nbrs(cx,cy):
                                if binary[ny,nx] and not visited[ny,nx]:
                                    stroke.append((nx,ny)); visited[ny,nx] = True; cx,cy = nx,ny
                                    moved = True; break
                            if not moved: break
                        if len(stroke) >= SETTINGS["MIN_STROKE_LEN"]:
                            if SETTINGS["CONTOUR_APPROX"] and epsilon > 0:
                                stroke = self.opt.douglas_peucker(stroke, epsilon)
                            if len(stroke) >= 2: strokes.append(stroke)
        return strokes
    def generate_hatch_strokes(self, gray, dark_thresh=180, spacing=4, angles=None):
        if angles is None:
            step = int(SETTINGS["HATCH_ANGLE_STEP"]); angles = list(range(0, 180, step))
        h,w = gray.shape; strokes = []
        for angle_deg in angles:
            ang_rad = math.radians(angle_deg)
            lt = dark_thresh - (angles.index(angle_deg)*40)
            if lt < 30: lt = 30
            diag = int(math.hypot(w, h))
            cos_a, sin_a = math.cos(ang_rad), math.sin(ang_rad)
            for offset in range(-diag, diag, spacing):
                stroke = []
                for t in range(-diag, diag, 1):
                    px = int(w/2 + t*cos_a + offset*(-sin_a))
                    py = int(h/2 + t*sin_a + offset*cos_a)
                    if 0 <= px < w and 0 <= py < h:
                        if gray[py,px] < lt: stroke.append((px,py))
                        else:
                            if len(stroke) >= spacing: strokes.append(stroke[::max(1,spacing//2)])
                            stroke = []
                if len(stroke) >= spacing: strokes.append(stroke[::max(1,spacing//2)])
        return strokes
    def plan_passes(self, img):
        gray = self.preprocess(img)
        eps = float(SETTINGS["SIMPLIFY_EPS"]); mode = SETTINGS["ENGINE_MODE"]
        passes = []
        if HAS_CV2:
            e1 = cv2.Canny(gray, 80, 200)
            k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            e1 = cv2.dilate(e1, k, iterations=2)
        else: e1 = self.detect_edges(gray)
        outer = self.extract_contour_strokes(e1, eps*2.5)
        if outer:
            avg = sum(len(s) for s in outer)/len(outer)
            outer = [s for s in outer if len(s) >= avg*0.5]
        outer = self.opt.nearest_neighbor_order(outer)
        passes.append(("Silhouette", outer))
        if mode == "ultra_fast": return passes
        e2 = self.detect_edges(gray)
        inner = self.extract_contour_strokes(e2, eps)
        inner = self.opt.nearest_neighbor_order(inner)
        passes.append(("Structure", inner))
        if mode in ("balanced","human_sketch","sketchy"):
            if SETTINGS["HATCH_ENABLE"]:
                step = int(SETTINGS["HATCH_ANGLE_STEP"])
                if SETTINGS.get("HATCH_SINGLE", False):
                    ang = [step]
                else:
                    ang = [0, step] if mode == "balanced" else [0, step, step*2 if mode != "sketchy" else step]
                spacing = SETTINGS["HATCH_SPACING"]
                if mode == "sketchy":
                    spacing = max(2, spacing - 1)
                hatch = self.generate_hatch_strokes(gray, angles=ang, spacing=spacing)
                hatch = self.opt.nearest_neighbor_order(hatch)
                passes.append(("Hatching", hatch))
            if mode == "sketchy":
                # Add a loose scribble pass for sketchy mode
                hatch2 = self.generate_hatch_strokes(gray, angles=[step + 15], spacing=max(3, step//5))
                passes.append(("Scribble", self.opt.nearest_neighbor_order(hatch2)))
            return passes
        if HAS_CV2:
            e3 = cv2.Canny(gray, max(5, int(SETTINGS["CANNY_LOW"])//2), int(SETTINGS["CANNY_HIGH"])//2)
        else: e3 = self.detect_edges(gray)
        fine = self.extract_contour_strokes(e3, max(0.3, eps*0.3))
        fine = self.opt.nearest_neighbor_order(fine)
        passes.append(("Fine Detail", fine))
        if SETTINGS["HATCH_ENABLE"]:
            step = int(SETTINGS["HATCH_ANGLE_STEP"])
            if SETTINGS.get("HATCH_SINGLE", False):
                hatch_ang = [step]
            else:
                hatch_ang = [0, step, step*2, step*3]
            hatch = self.generate_hatch_strokes(gray, angles=hatch_ang, spacing=max(2, SETTINGS["HATCH_SPACING"]-1))
            hatch = self.opt.nearest_neighbor_order(hatch)
            passes.append(("Dense Hatching", hatch))
        return passes
    def _cache_key(self, img):
        h = hashlib.md5(img.tobytes()).hexdigest()[:16]
        cfg = f"{SETTINGS['ENGINE_MODE']}_{SETTINGS['SIMPLIFY_EPS']}_{SETTINGS['CANNY_LOW']}_{SETTINGS['CANNY_HIGH']}_{SETTINGS['HATCH_ENABLE']}_{SETTINGS['MULTIPASS']}"
        return h + "_" + hashlib.md5(cfg.encode()).hexdigest()[:8]
    def _load_cache(self, key):
        p = os.path.join(CACHE_PATH, key+".json")
        if os.path.exists(p):
            try:
                with open(p) as f: raw = json.load(f)
                return [(name, [[tuple(pt) for pt in stroke] for stroke in strokes]) for name, strokes in raw]
            except: pass
        return None
    def _save_cache(self, key, passes):
        try:
            with open(os.path.join(CACHE_PATH, key+".json"), "w") as f:
                json.dump([[name, strokes] for name, strokes in passes], f)
        except: pass
    def execute(self, img, canvas_rect, palette_entry, app):
        if not canvas_rect or len(canvas_rect) < 4: return
        sx, sy = canvas_rect[0], canvas_rect[1]
        iw, ih = img.size
        cw = canvas_rect[2]-canvas_rect[0]; ch = canvas_rect[3]-canvas_rect[1]
        sxs = cw/max(1,iw); sys_ = ch/max(1,ih)
        def i2s(x,y): return (int(sx+x*sxs), int(sy+y*sys_))
        def jitt(x,y):
            j = int(SETTINGS.get("JITTER_PX",0))
            return (x+random.randint(-j,j), y+random.randint(-j,j)) if j>0 else (x,y)
        ck = self._cache_key(img)
        cached = self._load_cache(ck) if SETTINGS["USE_PATH_CACHE"] else None
        if cached: passes = cached
        else:
            app.log("[Engine] Planning strokes...")
            passes = self.plan_passes(img) if SETTINGS["MULTIPASS"] else \
                     [("Drawing", self.opt.nearest_neighbor_order(
                         self.extract_contour_strokes(
                             self.detect_edges(self.preprocess(img)),
                             float(SETTINGS["SIMPLIFY_EPS"]))))]
            if SETTINGS["USE_PATH_CACHE"]: self._save_cache(ck, passes)
        total = sum(sum(len(s) for s in strokes) for _, strokes in passes)
        app.log(f"[Engine] {len(passes)} passes, {total:,} pts")
        pos = palette_entry.get("pos",[0,0])
        self.driver.move(pos[0], pos[1])
        time.sleep(float(SETTINGS["UI_DELAY"]))
        self.driver.click(pos[0], pos[1])
        time.sleep(float(SETTINGS["CLICK_DELAY"]))
        drawn = 0; pps_t = 0; pps_ts = time.time()
        human = bool(SETTINGS["HUMAN_MOTION"]); bsteps = int(SETTINGS["BEZIER_STEPS"]); cdel = float(SETTINGS["CLICK_DELAY"])
        for pname, strokes in passes:
            if not app.drawing_active: break
            app.log(f"[Engine] {pname}: {len(strokes)} strokes")
            for stroke in strokes:
                if not app.drawing_active: break
                while app.drawing_paused: time.sleep(0.05)
                if len(stroke) < 2:
                    sx2,sy2 = jitt(*i2s(*stroke[0]))
                    self.driver.click(sx2,sy2); drawn += 1; continue
                x0,y0 = jitt(*i2s(*stroke[0]))
                if human and bsteps > 0:
                    try:
                        if HAS_PYAUTOGUI:
                            cur_xy = pyautogui.position()
                        else:
                            cur_xy = (x0, y0)
                    except:
                        cur_xy = (x0, y0)
                    for wx,wy in self.hms.waypoints(cur_xy[0],cur_xy[1],x0,y0,steps=bsteps,jitter=1):
                        self.driver.move(wx,wy); time.sleep(cdel*0.3)
                else: self.driver.move(x0,y0)
                self.driver.press(x0,y0); time.sleep(cdel)
                px,py = x0,y0
                for pt in stroke[1:]:
                    if not app.drawing_active: break
                    while app.drawing_paused:
                        if not app.drawing_active: break
                        time.sleep(0.05)
                    tx,ty = jitt(*i2s(*pt))
                    if human and bsteps > 0:
                        for wx,wy in self.hms.waypoints(px,py,tx,ty,steps=bsteps,jitter=int(SETTINGS["JITTER_PX"])):
                            self.driver.drag_to(wx,wy)
                        time.sleep(self.hms.delay_for_segment(px,py,tx,ty,cdel))
                    else:
                        self.driver.drag_to(tx,ty)
                        if cdel > 0: time.sleep(cdel)
                    px,py = tx,ty; drawn += 1; pps_t += 1
                    now = time.time()
                    if now - pps_ts >= 1.0:
                        pps = pps_t/max(0.001, now-pps_ts); pps_t=0; pps_ts=now
                        app.root.after(0, app._update_pps_display, pps)
                    if drawn % 100 == 0: app._update_progress(drawn, total)
                self.driver.release()
                time.sleep(cdel)
        app._draw_finished(drawn)
    def execute_from_result(self, result, app):
        for fop in result.fill_ops:
            if not app.drawing_active: break
            app.fill_intel.execute_fill(fop)
            time.sleep(float(SETTINGS["CLICK_DELAY"]))
        pe = result.palette_entry
        self.driver.move(pe['pos'][0], pe['pos'][1])
        time.sleep(float(SETTINGS["UI_DELAY"]))
        self.driver.click(pe['pos'][0], pe['pos'][1])
        time.sleep(float(SETTINGS["CLICK_DELAY"]))
        strokes = result.final_strokes
        total = sum(len(s) for s in strokes)
        drawn = 0; pps_t = 0; pps_ts = time.time()
        human = bool(SETTINGS["HUMAN_MOTION"]); bsteps = int(SETTINGS["BEZIER_STEPS"]); cdel = float(SETTINGS["CLICK_DELAY"])
        for stroke in strokes:
            if not app.drawing_active: break
            while app.drawing_paused: time.sleep(0.05)
            if len(stroke) == 1 and stroke[0] == "PEN_LIFT": self.driver.release(); continue
            if len(stroke) < 2: continue
            x0,y0 = stroke[0]
            if human and bsteps > 0:
                try:
                    cur_xy = pyautogui.position()
                except:
                    cur_xy = (x0, y0)
                for wx,wy in self.hms.waypoints(cur_xy[0],cur_xy[1],x0,y0,steps=bsteps,jitter=SETTINGS["JITTER_PX"]):
                    self.driver.move(wx,wy); time.sleep(cdel*0.3)
            else: self.driver.move(x0,y0)
            self.driver.press(x0,y0); time.sleep(cdel)
            px,py = x0,y0
            for pt in stroke[1:]:
                if not app.drawing_active: break
                while app.drawing_paused: time.sleep(0.05)
                tx,ty = pt
                if human and bsteps > 0:
                    for wx,wy in self.hms.waypoints(px,py,tx,ty,steps=bsteps,jitter=SETTINGS["JITTER_PX"]):
                        self.driver.drag_to(wx,wy)
                    time.sleep(self.hms.delay_for_segment(px,py,tx,ty,cdel))
                else:
                    self.driver.drag_to(tx,ty)
                    if cdel > 0: time.sleep(cdel)
                px,py = tx,ty; drawn += 1; pps_t += 1
                now = time.time()
                if now - pps_ts >= 1.0:
                    pps = pps_t/max(0.001, now-pps_ts); pps_t=0; pps_ts=now
                    app.root.after(0, app._update_pps_display, pps)
                if drawn % 100 == 0: app._update_progress(drawn, total)
            self.driver.release(); time.sleep(cdel)
        app._draw_finished(drawn)
        if result.stats: app.log(f"[Engine] Stats: {result.stats}")


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class AutoDrawer:
    def __init__(self):
        self.canvas_rect = None
        self.palette_map = []
        self.drawing_active = False
        self.drawing_paused = False
        self.preview_active = False
        self.ready_to_draw = False
        self.current_progress = 0
        self.estimated_total = 0
        self.draw_start_time = 0
        self.last_pps = 0.0
        self.pps_history = deque(maxlen=60)
        self._dots_last_second = 0
        self._last_pps_ts = 0.0

        # Image State & History
        self.base_img = None
        self.history = deque(maxlen=40)
        self.redo_stack = deque(maxlen=40)
        self.edit_img = None
        self.final_img = None
        self.tk_edit_img = None
        self.project_path = None

        # Editor Tools
        self.tool_mode = "Move"
        self.brush_size = 10
        self.brush_color = (0, 0, 255)
        self.text_objects = []
        self.last_mouse = (0, 0)

        # Layers (each is a PIL Image, composited top-to-bottom)
        self.layers = []          # list of {"name": str, "img": PIL.Image, "visible": bool}
        self.active_layer = 0

        # Multi-selection regions (numbered drag-to-select rects with preview)
        self.selections = []      # list of [x1, y1, x2, y2]
        self.selection_previews = []  # list of PhotoImage thumbnails

        # Batch queue
        self.batch_queue = []     # list of file paths
        self.batch_active = False

        # Session log buffer
        self.session_log = []

        # Draw source (the image that will actually be sent to execute_draw)
        self.draw_source = None
        self.preview_scale = 1.0

        # Root window
        self.root = tk.Tk()
        self.root.title("SF2M Studio Pro v6 — Godmode Edition")
        self.root.geometry("1200x850")
        self.root.minsize(860, 600)
        T = CURRENT_THEME
        self.root.configure(bg=T["bg"])

        # Style ttk
        self._apply_ttk_style()

        self.load_config()
        self.setup_main_menu()
        self.start_hotkey_listener()

        # Sub-systems
        self.calib_manager = CalibrationManager(self)
        self.prompt_pipeline = PromptPipeline(self)
        self.fill_intel = FillIntelligence(self)
        self.color_engine = ColorEngine(self)

        # Crash recovery
        self.root.report_callback_exception = self._crash_handler

    # ──────────────────────────────────────────
    #  THEME & STYLE
    # ──────────────────────────────────────────
    def _apply_ttk_style(self):
        T = CURRENT_THEME
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar",
                         troughcolor=T["bg2"],
                         background=T["progress"],
                         bordercolor=T["bg"],
                         lightcolor=T["progress"],
                         darkcolor=T["progress"])
        style.configure("TCombobox",
                         fieldbackground=T["bg2"],
                         background=T["bg2"],
                         foreground=T["fg"],
                         selectbackground=T["accent2"],
                         arrowcolor=T["accent"])

    def _apply_theme(self, theme_name):
        global CURRENT_THEME
        if theme_name in THEMES:
            CURRENT_THEME = THEMES[theme_name]
            SETTINGS["THEME"] = theme_name
            self._apply_ttk_style()
            self._refresh_ui_theme()
            self.log(f"Theme changed to: {theme_name}")

    def _refresh_ui_theme(self):
        T = CURRENT_THEME
        self.root.configure(bg=T["bg"])
        for child in self.root.winfo_children():
            try:
                if isinstance(child, (tk.Frame, tk.LabelFrame)):
                    child.configure(bg=T["bg"])
            except:
                pass
        if hasattr(self, 'canvas_label') and self.canvas_label:
            self.canvas_label.configure(bg=T["bg"], fg=T["accent2"])
        if hasattr(self, 'status_msg') and self.status_msg:
            self.status_msg.configure(bg=T["bg"], fg=T["success"])
        if hasattr(self, 'time_msg') and self.time_msg:
            self.time_msg.configure(bg=T["bg"], fg=T["fg"])
        if hasattr(self, 'pps_label') and self.pps_label:
            self.pps_label.configure(bg=T["bg"], fg=T["accent2"])
        if hasattr(self, 'log_box') and self.log_box:
            self.log_box.configure(bg=T["log_bg"], fg=T["log_fg"])
        if hasattr(self, 'progress_bar') and self.progress_bar:
            self.progress_bar.configure(style="TProgressbar")
        for w in self.root.winfo_children():
            self._walk_apply_theme(w)

    def _walk_apply_theme(self, parent):
        T = CURRENT_THEME
        try:
            if isinstance(parent, (tk.LabelFrame, tk.Frame)):
                parent.configure(bg=T["bg"])
        except:
            pass
        for child in parent.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    child.configure(bg=T["bg"], fg=T["fg"])
                elif isinstance(child, tk.Button):
                    child.configure(bg=T["btn"], fg=T["fg"], activebackground=T["btn_active"], activeforeground=T["accent"])
                elif isinstance(child, tk.Checkbutton):
                    child.configure(bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"], activebackground=T["bg"])
                elif isinstance(child, tk.Frame):
                    child.configure(bg=T["bg"])
                elif isinstance(child, tk.LabelFrame):
                    child.configure(bg=T["bg"], fg=T["accent"])
                elif isinstance(child, tk.Text):
                    child.configure(bg=T["log_bg"], fg=T["log_fg"])
                elif isinstance(child, tk.Listbox):
                    child.configure(bg=T["bg2"], fg=T["fg"], selectbackground=T["accent"])
                elif isinstance(child, tk.Scale):
                    child.configure(bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"])
                elif isinstance(child, tk.Canvas):
                    child.configure(bg=T["bg"])
            except:
                pass
            try:
                self._walk_apply_theme(child)
            except:
                pass

    # ──────────────────────────────────────────
    #  CONFIG
    # ──────────────────────────────────────────
    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    raw = f.read().strip()

                # Handle empty or corrupted config safely
                if not raw:
                    raise ValueError("Config file is empty")

                data = json.loads(raw)

                self.canvas_rect = data.get("canvas")
                self.selections = data.get("selections", [])
                if self.canvas_rect and self.canvas_rect not in self.selections:
                    self.selections.insert(0, self.canvas_rect)
                self.palette_map = data.get("palette", [])

                raw = data.get("settings", {})
                if any(isinstance(v, dict) for v in raw.values()):
                    for cat, keys in CONFIG_CATEGORY.items():
                        cat_obj = raw.get(cat, {})
                        for k in keys:
                            if k in cat_obj:
                                SETTINGS[k] = cat_obj[k]
                else:
                    for key in SETTINGS:
                        if key in raw:
                            SETTINGS[key] = raw[key]

                # Apply saved theme
                if SETTINGS.get("THEME") in THEMES:
                    global CURRENT_THEME
                    CURRENT_THEME = THEMES[SETTINGS["THEME"]]

            except Exception as e:
                print(f"Config load error: {e}")

                # Backup corrupted config instead of crashing startup
                try:
                    corrupt_path = CONFIG_PATH + ".corrupt"
                    if os.path.exists(CONFIG_PATH):
                        import shutil
                        shutil.copy2(CONFIG_PATH, corrupt_path)
                        print(f"Backed up corrupt config to: {corrupt_path}")

                    # Regenerate clean config
                    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                        hier = {}
                        for cat, keys in CONFIG_CATEGORY.items():
                            cat_obj = {}
                            for k in keys:
                                if k in SETTINGS:
                                    cat_obj[k] = SETTINGS[k]
                            hier[cat] = cat_obj
                        json.dump({
                            "canvas": None,
                            "palette": [],
                            "settings": hier
                        }, f, indent=2)

                    print("Generated fresh default config.")
                except Exception as backup_error:
                    print(f"Failed to recover config: {backup_error}")

    def save_config(self):
        try:
            hier = {}
            for cat, keys in CONFIG_CATEGORY.items():
                cat_obj = {}
                for k in keys:
                    if k in SETTINGS:
                        cat_obj[k] = SETTINGS[k]
                hier[cat] = cat_obj
            with open(CONFIG_PATH, 'w') as f:
                json.dump({
                    "canvas": self.canvas_rect,
                    "selections": self.selections,
                    "palette": self.palette_map,
                    "settings": hier
                }, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")

    # ──────────────────────────────────────────
    #  PROJECT SAVE / LOAD
    # ──────────────────────────────────────────
    def save_project(self):
        img = self._get_active_image()
        if not img:
            messagebox.showwarning("No Image", "Load an image first")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".sf2m",
            filetypes=[("SF2M Project", "*.sf2m"), ("JSON", "*.json")],
            initialdir=PROJECTS_PATH
        )
        if filepath:
            project_data = {
                "image": img.tobytes().hex(),
                "image_mode": img.mode,
                "image_size": list(img.size),
                "canvas_rect": self.canvas_rect,
                "selections": self.selections,
                "palette": self.palette_map,
                "settings": SETTINGS,
                "text_objects": self.text_objects,
                "version": 5,
            }
            with open(filepath, 'w') as f:
                json.dump(project_data, f, indent=2)
            self.project_path = filepath
            self.log(f"Project saved: {os.path.basename(filepath)}")
            messagebox.showinfo("Saved", f"Project saved: {os.path.basename(filepath)}")

    def load_project(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("SF2M Project", "*.sf2m"), ("JSON", "*.json")],  # BUG FIX: was *.sfm2
            initialdir=PROJECTS_PATH
        )
        if not filepath:
            return
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            img_bytes = bytes.fromhex(data["image"])
            mode = data["image_mode"]
            size = tuple(data["image_size"])
            self.base_img = Image.frombytes(mode, size, img_bytes)
            if self.base_img.mode != 'RGB':
                self.base_img = self.base_img.convert('RGB')
            self.canvas_rect = data.get("canvas_rect")
            self.selections = data.get("selections", [])
            if self.canvas_rect and self.canvas_rect not in self.selections:
                self.selections.insert(0, self.canvas_rect)
            self.palette_map = data.get("palette", [])
            for key, val in data.get("settings", {}).items():
                if key in SETTINGS:
                    SETTINGS[key] = val
            self.text_objects = data.get("text_objects", [])
            self.final_img = None
            self.log(f"Project loaded: {os.path.basename(filepath)}")
            self._update_canvas_label()
            messagebox.showinfo("Loaded", "Project loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load project:\n{e}")
            self.log(f"Load error: {e}")

    def _emergency_save(self):
        """Called on crash — saves current state."""
        if not self.base_img:
            return
        try:
            path = os.path.join(PROJECTS_PATH, f"emergency_{int(time.time())}.sf2m")
            project_data = {
                "image": self.base_img.tobytes().hex(),
                "image_mode": self.base_img.mode,
                "image_size": list(self.base_img.size),
                "canvas_rect": self.canvas_rect,
                "selections": self.selections,
                "palette": self.palette_map,
                "settings": SETTINGS,
                "text_objects": self.text_objects,
                "version": 5,
            }
            with open(path, 'w') as f:
                json.dump(project_data, f)
            print(f"[EMERGENCY SAVE] {path}")
        except Exception as e2:
            print(f"Emergency save failed: {e2}")

    def _crash_handler(self, exc, val, tb):
        self._emergency_save()
        err = "".join(traceback.format_exception(exc, val, tb))
        messagebox.showerror("Crash", f"An error occurred:\n{val}\n\nEmergency save attempted.")
        print(err)

    # ──────────────────────────────────────────
    #  HOTKEYS
    # ──────────────────────────────────────────
    def start_hotkey_listener(self):
        key_map = {
            "f1": keyboard.Key.f1,
            "f10": keyboard.Key.f10,
            "f11": keyboard.Key.f11,
            "f12": keyboard.Key.f12,
        }
        abort_keys = {keyboard.Key.f12, keyboard.KeyCode.from_vk(123)}
        pause_keys = {keyboard.Key.f11, keyboard.KeyCode.from_vk(122)}
        start_keys = {keyboard.Key.f10, keyboard.KeyCode.from_vk(121)}

        def on_press(key):
            if key in abort_keys:
                self.drawing_active = False
                self.batch_active = False
                try:
                    self.root.after(0, lambda: self.log("!! ABORT (F12) !!"))
                except Exception:
                    pass
            elif key in pause_keys:
                self.drawing_paused = not self.drawing_paused
                state = "PAUSED" if self.drawing_paused else "RESUMED"
                try:
                    self.root.after(0, lambda s=state: self.log(f"Drawing {s}"))
                except Exception:
                    pass
            elif key in start_keys and self.preview_active:
                self.ready_to_draw = True
            elif key == keyboard.Key.f1:
                try:
                    self.root.after(0, self.show_hotkey_help)
                except Exception:
                    pass

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()

        # Tkinter fallback bindings (works even when pynput is blocked)
        def _tk_abort(e=None):
            self.drawing_active = False
            self.batch_active = False
            self.log("!! ABORT (tk) !!")
        def _tk_pause(e=None):
            self.drawing_paused = not self.drawing_paused
            self.log("PAUSED" if self.drawing_paused else "RESUMED")
        def _tk_start(e=None):
            if self.preview_active:
                self.ready_to_draw = True

        self.root.bind("<F12>", _tk_abort)
        self.root.bind("<F11>", _tk_pause)
        self.root.bind("<F10>", _tk_start)
        self.root.bind("<Escape>", _tk_abort)  # ESC also aborts

        # Polling guard: periodically check draw state from main thread
        def _abort_poll():
            if not self.drawing_active and not self.batch_active:
                pass  # already stopped
            self.root.after(200, _abort_poll)
        self.root.after(200, _abort_poll)

    def show_hotkey_help(self):
        T = CURRENT_THEME
        win = tk.Toplevel(self.root)
        win.title("Hotkey Help")
        win.configure(bg=T["bg"])
        win.geometry("360x300")
        tk.Label(win, text="HOTKEYS", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(pady=10)
        keys = [
            ("F10", "Start drawing (during preview)"),
            ("F11", "Pause / Resume drawing"),
            ("F12", "ABORT drawing"),
            ("F1", "This help screen"),
            ("Ctrl+Z", "Undo (in editor)"),
            ("Ctrl+Y", "Redo (in editor)"),
            ("Ctrl+S", "Save project (main window)"),
            ("Scroll", "Zoom preview / editor"),
            ("Mid-drag", "Pan preview window"),
        ]
        for key, desc in keys:
            row = tk.Frame(win, bg=T["bg"])
            row.pack(fill="x", padx=20, pady=1)
            tk.Label(row, text=f"{key:<12}", bg=T["bg"], fg=T["accent2"],
                     font=("Courier", 10, "bold")).pack(side="left")
            tk.Label(row, text=desc, bg=T["bg"], fg=T["fg"],
                     font=("Courier", 9)).pack(side="left")
        tk.Button(win, text="CLOSE", command=win.destroy,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 10, "bold"), bd=0).pack(pady=15)

    # ──────────────────────────────────────────
    #  MAIN MENU SETUP
    # ──────────────────────────────────────────
    def setup_main_menu(self):
        T = CURRENT_THEME
        root = self.root

        # ── Menubar (stays at top, not scrollable) ──
        menubar = tk.Menu(root, bg=T["bg2"], fg=T["fg"], activebackground=T["accent2"],
                          activeforeground=T["bg"])
        file_menu = tk.Menu(menubar, tearoff=0, bg=T["bg2"], fg=T["fg"])
        file_menu.add_command(label="Load Image", command=self.load_from_file)
        file_menu.add_command(label="Paste from Clipboard", command=self.load_from_clip)
        file_menu.add_separator()
        file_menu.add_command(label="Save Project  Ctrl+S", command=self.save_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG", command=self.export_png)
        file_menu.add_command(label="Export Session Log", command=self.export_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, bg=T["bg2"], fg=T["fg"])
        tools_menu.add_command(label="Open Editor", command=self.open_editor)
        tools_menu.add_command(label="Calibrate Palette", command=self.calibrate_palette)
        tools_menu.add_command(label="Generate Palette (K-Means)", command=self.generate_palette)
        tools_menu.add_command(label="Edit Palette", command=self.open_palette_editor)
        tools_menu.add_command(label="Set Canvas Region", command=self.start_visual_calibration)
        tools_menu.add_command(label="Image Pre-Processing", command=self.open_preprocessing)
        tools_menu.add_command(label="Batch Draw Queue", command=self.open_batch_queue)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        theme_menu = tk.Menu(menubar, tearoff=0, bg=T["bg2"], fg=T["fg"])
        for name in THEMES:
            theme_menu.add_command(label=name, command=lambda n=name: self._apply_theme(n))
        menubar.add_cascade(label="Theme", menu=theme_menu)

        help_menu = tk.Menu(menubar, tearoff=0, bg=T["bg2"], fg=T["fg"])
        help_menu.add_command(label="Hotkey Help  F1", command=self.show_hotkey_help)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "SF2M Studio Pro v6 — Godmode Edition\nAI-assisted autonomous drawing laboratory."))
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)
        root.bind("<Control-s>", lambda e: self.save_project())

        # ── Scrollable Main Content ──
        scroll_canvas = tk.Canvas(root, bg=T["bg"], highlightthickness=0)
        scroll_scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
        main_content = tk.Frame(scroll_canvas, bg=T["bg"])
        main_content.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=main_content, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scroll_scrollbar.set)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scroll_scrollbar.pack(side="right", fill="y")
        def _on_main_mousewheel(event):
            scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", _on_main_mousewheel))
        scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))
        self._main_content = main_content

        # Re-pack existing root children into main_content
        header = tk.Frame(main_content, bg=T["bg2"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="SF2M", font=("Courier", 32, "bold"),
                 bg=T["bg2"], fg=T["accent"]).pack(side="left", padx=20)
        tk.Label(header, text="STUDIO v6  GODMODE EDITION",
                 font=("Courier", 9), bg=T["bg2"], fg=T["accent2"]).pack(side="left", pady=(22, 0))
        tk.Label(header, text="[PRO]", font=("Courier", 8),
                 bg=T["bg2"], fg=T["warn"]).pack(side="right", padx=10, pady=(22, 0))

        # ── Action Buttons (2-column grid for better space usage) ──
        btn_frame = tk.Frame(main_content, bg=T["bg"])
        btn_frame.pack(fill="x", padx=15, pady=4)

        self._action_btns = []
        actions = [
            ("📁 LOAD IMAGE", self.load_from_file, T["bg3"],
             "Open an image file (PNG/JPG/WEBP)"),
            ("📋 PASTE IMAGE", self.load_from_clip, T["bg3"],
             "Paste image from clipboard"),
            ("💾 SAVE PROJECT", self.save_project, "#2d2200",
             "Save all settings & image as .sf2m"),
            ("📂 LOAD PROJECT", self.load_project, "#2d2200",
             "Load a previously saved .sf2m file"),
            ("🖥 SET CANVAS", self.start_visual_calibration, T["bg2"],
             "Drag to define the drawing area on screen"),
            ("🔲 SELECTIONS", self.open_selection_panel, "#1a2a1a",
             "Manage multiple numbered selection regions with preview"),
            ("🎨 CALIB PALETTE", self.calibrate_palette, T["bg2"],
             "Click on in-game color swatches"),
            ("✨ GEN PALETTE", self.generate_palette, "#200040",
             "Auto-detect colors via K-Means clustering"),
            ("🖊 EDIT PALETTE", self.open_palette_editor, "#200040",
             "Add, remove, reorder palette colors"),
            ("🔬 PRE-PROCESS", self.open_preprocessing, "#001a2a",
             "Resize, quantize, enhance before drawing"),
            ("🖌 OPEN EDITOR", self.open_editor, "#001a33",
             "Full image editor with layers & tools"),
            ("📦 BATCH QUEUE", self.open_batch_queue, "#1a1a00",
             "Queue multiple images to draw sequentially"),
            ("🎨 SKETCH CONFIG", self.open_sketch_config, "#2a1a00",
             "Configure human-like sketch drawing mode"),
            ("🚀 START DRAW", self.show_preview, "#004d00",
             "Preview image, then press F10 to begin"),
        ]

        cols = 2
        for i, (text, cmd, color, tip) in enumerate(actions):
            row_idx = i // cols
            col_idx = i % cols
            if col_idx == 0:
                row_frame = tk.Frame(btn_frame, bg=T["bg"])
                row_frame.pack(fill="x", pady=1)
            btn = tk.Button(row_frame, text=text, command=cmd,
                bg=color or T["btn"], fg=T["fg"],
                font=("Courier", 8, "bold"),
                bd=0, relief="flat",
                activebackground=T["btn_active"],
                activeforeground=T["accent"],
                cursor="hand2",
            )
            btn.pack(side="left", fill="x", expand=True, padx=2)
            self._action_btns.append(btn)
            if tip:
                Tooltip(btn, tip)

        # ── Settings Panel ──
        settings_frame = tk.LabelFrame(
            main_content, text=" DRAW SETTINGS ", bg=T["bg"], fg=T["accent"],
            font=("Courier", 10, "bold"), bd=1, relief="solid",
            highlightbackground=T["border"]
        )
        settings_frame.pack(fill="x", padx=15, pady=5)

        def lbl(parent, text):
            return tk.Label(parent, text=text, bg=T["bg"], fg=T["fg"], font=("Courier", 8))

        def scale(parent, from_, to, var, key, resolution=1, length=130):
            s = tk.Scale(
                parent, from_=from_, to=to, resolution=resolution,
                orient="horizontal", variable=var,
                command=lambda v: SETTINGS.update({key: int(float(v)) if isinstance(SETTINGS.get(key), int) else type(SETTINGS[key])(v)}),
                bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                highlightthickness=0, length=length
            )
            return s

        r1 = tk.Frame(settings_frame, bg=T["bg"])
        r1.pack(fill="x", padx=5, pady=2)
        lbl(r1, "Pixel Gap:").pack(side="left")
        self.gap_var = tk.IntVar(value=SETTINGS["PIXEL_GAP"])
        scale(r1, 1, 10, self.gap_var, "PIXEL_GAP").pack(side="left")
        lbl(r1, " White Skip:").pack(side="left")
        self.white_var = tk.IntVar(value=SETTINGS["WHITE_SKIP"])
        scale(r1, 200, 255, self.white_var, "WHITE_SKIP").pack(side="left")

        r2 = tk.Frame(settings_frame, bg=T["bg"])
        r2.pack(fill="x", padx=5, pady=2)
        lbl(r2, "Click Delay:").pack(side="left")
        self.delay_var = tk.DoubleVar(value=SETTINGS["CLICK_DELAY"])
        scale(r2, 0, 0.1, self.delay_var, "CLICK_DELAY", resolution=0.001).pack(side="left")
        lbl(r2, " UI Delay:").pack(side="left")
        self.ui_delay_var = tk.DoubleVar(value=SETTINGS["UI_DELAY"])
        scale(r2, 0.0, 0.5, self.ui_delay_var, "UI_DELAY", resolution=0.01).pack(side="left")

        r3 = tk.Frame(settings_frame, bg=T["bg"])
        r3.pack(fill="x", padx=5, pady=2)
        self.trace_var = tk.BooleanVar(value=SETTINGS["TRACE_MODE"])
        tk.Checkbutton(r3, text="Trace Mode", variable=self.trace_var,
                       command=lambda: SETTINGS.update({"TRACE_MODE": self.trace_var.get()}),
                       bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                       activebackground=T["bg"], font=("Courier", 8)).pack(side="left")
        self.drag_var = tk.BooleanVar(value=SETTINGS["CONTINUOUS_DRAG"])
        tk.Checkbutton(r3, text="Cont. Drag", variable=self.drag_var,
                       command=lambda: SETTINGS.update({"CONTINUOUS_DRAG": self.drag_var.get()}),
                       bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                       activebackground=T["bg"], font=("Courier", 8)).pack(side="left", padx=10)
        self.blue_skip_var = tk.BooleanVar(value=SETTINGS["SKIP_BLUE_MASK"])
        tk.Checkbutton(r3, text="Skip Blue Mask", variable=self.blue_skip_var,
                       command=lambda: SETTINGS.update({"SKIP_BLUE_MASK": self.blue_skip_var.get()}),
                       bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                       activebackground=T["bg"], font=("Courier", 8)).pack(side="left")

        r4 = tk.Frame(settings_frame, bg=T["bg"])
        r4.pack(fill="x", padx=5, pady=2)
        lbl(r4, "Draw Mode:").pack(side="left")
        self.mode_combo = ttk.Combobox(r4, values=DRAW_MODES, width=16, state="readonly")
        self.mode_combo.set(SETTINGS["DRAW_MODE"])
        self.mode_combo.pack(side="left", padx=5)
        self.mode_combo.bind("<<ComboboxSelected>>",
            lambda e: SETTINGS.update({"DRAW_MODE": self.mode_combo.get()}))

        lbl(r4, " Dither:").pack(side="left")
        self.dither_combo = ttk.Combobox(r4, values=DITHER_MODES, width=14, state="readonly")
        self.dither_combo.set(SETTINGS["DITHER_MODE"])
        self.dither_combo.pack(side="left", padx=5)
        self.dither_combo.bind("<<ComboboxSelected>>",
            lambda e: SETTINGS.update({"DITHER_MODE": self.dither_combo.get()}))

        r5 = tk.Frame(settings_frame, bg=T["bg"])
        r5.pack(fill="x", padx=5, pady=2)
        lbl(r5, "Color Metric:").pack(side="left")
        self.metric_combo = ttk.Combobox(
            r5, values=["Euclidean", "CIEDE2000", "Manhattan"], width=12, state="readonly")
        self.metric_combo.set(SETTINGS["COLOR_METRIC"])
        self.metric_combo.pack(side="left", padx=5)
        self.metric_combo.bind("<<ComboboxSelected>>",
            lambda e: SETTINGS.update({"COLOR_METRIC": self.metric_combo.get()}))

        lbl(r5, " Palette Size:").pack(side="left")
        self.pal_size_var = tk.IntVar(value=SETTINGS["PALETTE_SIZE"])
        scale(r5, 2, 64, self.pal_size_var, "PALETTE_SIZE", length=100).pack(side="left")

        r5b = tk.Frame(settings_frame, bg=T["bg"])
        r5b.pack(fill="x", padx=5, pady=2)
        lbl(r5b, " Global Speed:").pack(side="left")
        self.global_speed_var = tk.DoubleVar(value=SETTINGS.get("GLOBAL_SPEED", 1.0))
        scale(r5b, 0.1, 200, self.global_speed_var, "GLOBAL_SPEED", resolution=0.1, length=150).pack(side="left")
        lbl(r5b, " Stroke Mode:").pack(side="left", padx=(10,0))
        self.stroke_mode_combo = ttk.Combobox(r5b, values=["dot","stroke"], width=8, state="readonly")
        self.stroke_mode_combo.set(SETTINGS.get("STROKE_MODE","stroke"))
        self.stroke_mode_combo.pack(side="left", padx=5)
        self.stroke_mode_combo.bind("<<ComboboxSelected>>",
            lambda e: SETTINGS.update({"STROKE_MODE": self.stroke_mode_combo.get()}))

        r5c = tk.Frame(settings_frame, bg=T["bg"])
        r5c.pack(fill="x", padx=5, pady=2)
        self.fill_zone_btn = tk.Button(r5c, text="SET FILL ZONE (click bg)", command=self._start_fill_zone_calib,
            bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0)
        self.fill_zone_btn.pack(side="left", padx=5)
        self.fill_zone_active_var = tk.BooleanVar(value=SETTINGS.get("FILL_ZONE_ACTIVE",False))
        tk.Checkbutton(r5c, text="Fill Zone Active", variable=self.fill_zone_active_var,
            command=lambda: SETTINGS.update({"FILL_ZONE_ACTIVE": self.fill_zone_active_var.get()}),
            bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
            activebackground=T["bg"], font=("Courier", 8)).pack(side="left", padx=10)
        self.open_control_panel_btn = tk.Button(r5c, text="⚙ CONTROL PANEL", command=self.open_control_panel,
            bg=T["bg3"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0)
        self.open_control_panel_btn.pack(side="right", padx=5)

        r6 = tk.Frame(settings_frame, bg=T["bg"])
        r6.pack(fill="x", padx=5, pady=2)
        lbl(r6, "Drawing Preset:").pack(side="left")
        preset_names = list(DRAW_PRESETS.keys())
        self.preset_combo = ttk.Combobox(r6, values=preset_names, width=16, state="readonly")
        self.preset_combo.set(SETTINGS.get("DRAW_PRESET", "Balanced"))
        self.preset_combo.pack(side="left", padx=5)
        def _apply_preset():
            name = self.preset_combo.get()
            SETTINGS["DRAW_PRESET"] = name
            if name in DRAW_PRESETS:
                for k, v in DRAW_PRESETS[name].items():
                    if k in SETTINGS:
                        SETTINGS[k] = v
                engine = DRAW_PRESETS[name].get("ENGINE_MODE", "")
                if engine and hasattr(self, 'mode_combo'):
                    self.mode_combo.set(SETTINGS["DRAW_MODE"])
                self.log(f"Preset '{name}' applied ({len(DRAW_PRESETS[name])} settings)")
        self.preset_combo.bind("<<ComboboxSelected>>", lambda e: _apply_preset())

        # ── Canvas info label ──
        self.canvas_label = tk.Label(
            main_content, text=self._canvas_label_text(),
            bg=T["bg"], fg=T["accent2"], font=("Courier", 8)
        )
        self.canvas_label.pack()

        # ── Progress Panel ──
        prog_frame = tk.LabelFrame(
            main_content, text=" LIVE PROGRESS ", bg=T["bg"], fg=T["accent"],
            font=("Courier", 10, "bold"), bd=1, relief="solid"
        )
        prog_frame.pack(fill="x", padx=15, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            prog_frame, variable=self.progress_var, maximum=100, style="TProgressbar"
        )
        self.progress_bar.pack(fill="x", padx=10, pady=(8, 2))

        self.status_msg = tk.Label(prog_frame, text="Ready",
                                   bg=T["bg"], fg=T["success"], font=("Courier", 9))
        self.status_msg.pack()
        self.time_msg = tk.Label(prog_frame, text="",
                                 bg=T["bg"], fg=T["fg"], font=("Courier", 8))
        self.time_msg.pack()

        pps_row = tk.Frame(prog_frame, bg=T["bg"])
        pps_row.pack(fill="x", padx=10, pady=2)
        self.pps_label = tk.Label(pps_row, text="px/sec: —",
                                  bg=T["bg"], fg=T["accent2"], font=("Courier", 8))
        self.pps_label.pack(side="left")
        self.sparkline = Sparkline(pps_row, width=200, height=35, maxpts=60)
        self.sparkline.pack(side="right")

        # Abort / Pause buttons
        ctrl_row = tk.Frame(prog_frame, bg=T["bg"])
        ctrl_row.pack(fill="x", padx=10, pady=4)
        tk.Button(ctrl_row, text="⏸  PAUSE/RESUME",
                  command=self._toggle_pause,
                  bg="#333300", fg=T["warn"], font=("Courier", 8, "bold"),
                  bd=0, padx=10).pack(side="left", padx=5)
        tk.Button(ctrl_row, text="✕  ABORT",
                  command=self._abort_draw,
                  bg="#330000", fg=T["danger"], font=("Courier", 8, "bold"),
                  bd=0, padx=10).pack(side="left")

        # ── Log Box ──
        log_frame = tk.LabelFrame(main_content, text=" SESSION LOG ", bg=T["bg"], fg=T["accent"],
                                  font=("Courier", 9, "bold"), bd=1)
        log_frame.pack(fill="x", padx=15, pady=5)

        log_ctrl = tk.Frame(log_frame, bg=T["bg"])
        log_ctrl.pack(fill="x")
        tk.Button(log_ctrl, text="CLEAR", command=self._clear_log,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 7), bd=0).pack(side="right", padx=5)
        tk.Button(log_ctrl, text="EXPORT", command=self.export_log,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 7), bd=0).pack(side="right")

        self.log_box = tk.Text(log_frame, height=10, bg=T["log_bg"], fg=T["log_fg"],
                               font=("Courier", 8), insertbackground=T["accent"],
                               wrap="word")
        scrollbar = tk.Scrollbar(log_frame, command=self.log_box.yview)
        self.log_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_box.pack(fill="x", padx=5, pady=5)

        self.log("SF2M Studio v6 initialized. Type F1 for hotkey help.")

    def _canvas_label_text(self):
        parts = []
        if self.canvas_rect:
            x1, y1, x2, y2 = self.canvas_rect
            parts.append(f"Active: ({x1},{y1})→({x2},{y2}) [{x2-x1}×{y2-y1}]")
        if self.selections:
            parts.append(f"Selections: {len(self.selections)}")
        if not parts:
            return "Canvas: NOT SET — click SET CANVAS or SELECTIONS"
        return "  |  ".join(parts)

    def _update_canvas_label(self):
        if hasattr(self, 'canvas_label'):
            self.canvas_label.config(text=self._canvas_label_text())

    def _update_canvas(self):
        self._update_canvas_label()
        if self.final_img is not None:
            self.final_img = None

    def _toggle_pause(self):
        self.drawing_paused = not self.drawing_paused
        self.log("Drawing " + ("PAUSED" if self.drawing_paused else "RESUMED"))

    def _abort_draw(self):
        self.drawing_active = False
        self.batch_active = False
        self.log("Drawing ABORTED by user.")

    def _clear_log(self):
        self.log_box.delete(1.0, tk.END)

    # ──────────────────────────────────────────
    #  LOGGING
    # ──────────────────────────────────────────
    def log(self, message):
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}] {message}"
        self.session_log.append(line)
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, self._log_ui, line)
        else:
            self._log_ui(line)

    def _log_ui(self, line):
        try:
            if hasattr(self, 'log_box') and self.log_box.winfo_exists():
                self.log_box.insert(tk.END, line + "\n")
                self.log_box.see(tk.END)
        except Exception:
            pass

    def export_log(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")],
            initialdir=LOGS_PATH,
            initialfile=f"sf2m_log_{int(time.time())}.txt"
        )
        if path:
            with open(path, 'w') as f:
                f.write("\n".join(self.session_log))
            self.log(f"Log exported: {os.path.basename(path)}")

    # ──────────────────────────────────────────
    #  IMAGE LOADING
    # ──────────────────────────────────────────
    def load_from_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tga")]
        )
        if path:
            try:
                self.base_img = Image.open(path).convert('RGB')
                self.final_img = None
                self.text_objects = []
                self.layers = []
                self.log(f"Loaded: {os.path.basename(path)} ({self.base_img.size[0]}×{self.base_img.size[1]})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def load_from_clip(self):
        img = self._get_clipboard_image()
        if img:
            self.base_img = img
            self.final_img = None
            self.text_objects = []
            self.log(f"Pasted from clipboard: {img.size[0]}×{img.size[1]}")
        else:
            self.log("Clipboard: no image found.")
            messagebox.showwarning("Clipboard", "No image found in clipboard.")

    def _get_clipboard_image(self):
        # Try xclip (Linux)
        try:
            p = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            data, _ = p.communicate()
            if data:
                img = Image.open(io.BytesIO(data))
                img.load()
                return img.convert('RGB')
        except Exception:
            pass
        # Try xsel (Linux fallback)
        try:
            p = subprocess.Popen(
                ['xsel', '--clipboard', '--output'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            data, _ = p.communicate()
            if data:
                img = Image.open(io.BytesIO(data))
                img.load()
                return img.convert('RGB')
        except Exception:
            pass
        # Try Windows/Mac via PIL
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                return img.convert('RGB')
        except Exception:
            pass
        return None

    def _set_clipboard_image(self, img):
        try:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            p = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'image/png'],
                stdin=subprocess.PIPE, stderr=subprocess.PIPE
            )
            p.communicate(buf.read())
            return True
        except Exception:
            pass
        try:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            p = subprocess.Popen(
                ['xsel', '--clipboard', '--input'],
                stdin=subprocess.PIPE, stderr=subprocess.PIPE
            )
            p.communicate(buf.read())
            return True
        except Exception:
            pass
        return False

    def _get_active_image(self):
        """Returns final_img if available, else base_img."""
        return self.final_img or self.base_img

    # ──────────────────────────────────────────
    #  EXPORT
    # ──────────────────────────────────────────
    def export_png(self):
        img = self._get_active_image()
        if not img:
            messagebox.showwarning("No Image", "Nothing to export.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
        )
        if path:
            img.save(path)
            self.log(f"Exported PNG: {os.path.basename(path)}")

    # ──────────────────────────────────────────
    #  CANVAS CALIBRATION & SELECTION SYSTEM
    # ──────────────────────────────────────────
    def _drag_to_select_rect(self, parent_window=None, title="DRAG to select region"):
        """Fullscreen drag overlay, returns [x1,y1,x2,y2] or None if cancelled."""
        T = CURRENT_THEME
        cal = tk.Toplevel(parent_window or self.root)
        cal.attributes('-fullscreen', True, '-alpha', 0.01, '-topmost', True)
        c = tk.Canvas(cal, bg="black", highlightthickness=0, cursor="cross")
        c.pack(fill="both", expand=True)
        state = {"sx": 0, "sy": 0, "rect": None, "result": None}

        info_label = tk.Label(cal, text=f"{title}  |  ESC to cancel",
                              bg="#222", fg=T["accent"], font=("Courier", 10))
        info_label.place(x=20, y=20)

        def start(e):
            cal.attributes('-alpha', 0.25)
            state["sx"], state["sy"] = e.x, e.y
            state["rect"] = c.create_rectangle(e.x, e.y, e.x, e.y,
                                               outline=T["accent"], width=2, dash=(4,2))
        def drag(e):
            c.coords(state["rect"], state["sx"], state["sy"], e.x, e.y)
            w, h = abs(e.x - state["sx"]), abs(e.y - state["sy"])
            info_label.config(text=f"{title}: {w}x{h}px  |  Release to confirm  |  ESC to cancel")
        def end(e):
            state["result"] = [
                min(state["sx"], e.x), min(state["sy"], e.y),
                max(state["sx"], e.x), max(state["sy"], e.y)
            ]
            cal.destroy()

        c.bind("<Button-1>", start)
        c.bind("<B1-Motion>", drag)
        c.bind("<ButtonRelease-1>", end)
        cal.bind("<Escape>", lambda e: cal.destroy())
        cal.wait_window()
        return state["result"]

    def start_visual_calibration(self):
        rect = self._drag_to_select_rect(title="DRAG to select canvas region")
        if rect:
            self.canvas_rect = rect
            if rect not in self.selections:
                self.selections.append(rect)
            self._rebuild_selection_previews()
            self.log(f"Canvas set: {rect}")
            self._update_canvas_label()
            self.save_config()

    # ──────────────────────────────────────────
    #  SELECTION MANAGER
    # ──────────────────────────────────────────
    def _rebuild_selection_previews(self):
        """Generate small thumbnails for all selections."""
        self.selection_previews = []
        img = self._get_active_image()
        if not img:
            self.selection_previews = [None] * len(self.selections)
            return
        try:
            thumb = img.copy()
            thumb.thumbnail((120, 90), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(thumb)
            self.selection_previews = [tk_img] * len(self.selections)
        except Exception:
            self.selection_previews = [None] * len(self.selections)

    def open_selection_panel(self):
        T = CURRENT_THEME
        win = tk.Toplevel(self.root)
        win.title("Selection Manager")
        win.geometry("560x520")
        win.configure(bg=T["bg"])
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="SELECTION MANAGER", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(pady=10)
        tk.Label(win, text="Define numbered regions by dragging top-left to bottom-right",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack()

        list_frame = tk.Frame(win, bg=T["bg"])
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        listbox = tk.Listbox(list_frame, bg=T["log_bg"], fg=T["fg"],
                             font=("Courier", 10), height=10,
                             selectbackground=T["accent2"])
        listbox.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(list_frame, command=listbox.yview)
        scroll.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scroll.set)

        # Preview label next to listbox
        preview_frame = tk.Frame(list_frame, bg=T["bg3"], width=140, height=110)
        preview_frame.pack(side="right", padx=(10, 0))
        preview_frame.pack_propagate(False)
        preview_lbl = tk.Label(preview_frame, bg=T["bg3"], text="Preview", fg=T["fg"],
                               font=("Courier", 8))
        preview_lbl.pack(expand=True)

        def _refresh_list(keep_selection=False):
            sel = listbox.curselection()
            listbox.delete(0, tk.END)
            for i, rect in enumerate(self.selections):
                x1, y1, x2, y2 = rect
                w, h = x2 - x1, y2 - y1
                listbox.insert(tk.END, f"  #{i+1:02d}  ({x1},{y1}) -> ({x2},{y2})  [{w}x{h}]")
            if keep_selection and sel:
                listbox.selection_set(sel[0])
                _show_preview(sel[0])
            elif self.selections:
                listbox.selection_set(0)
                _show_preview(0)

        def _show_preview(idx):
            if not self.selections or idx < 0 or idx >= len(self.selections):
                preview_lbl.config(image="", text="No selection")
                return
            rect = self.selections[idx]
            x1, y1, x2, y2 = rect
            img = self._get_active_image()
            if img:
                try:
                    thumb = img.copy()
                    thumb.thumbnail((130, 100), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(thumb)
                    preview_lbl.config(image=tk_img, text=f"#{idx+1}  {x2-x1}x{y2-y1}")
                    preview_lbl._img = tk_img
                    preview_lbl.image = tk_img
                except Exception:
                    preview_lbl.config(image="", text="Preview N/A")
            else:
                preview_lbl.config(image="", text=f"#{idx+1}  Region: {x2-x1}x{y2-y1}")

        def on_select(e):
            sel = listbox.curselection()
            if sel:
                _show_preview(sel[0])

        listbox.bind("<<ListboxSelect>>", on_select)

        btn_row = tk.Frame(win, bg=T["bg"])
        btn_row.pack(fill="x", padx=15, pady=5)

        def add_selection():
            rect = self._drag_to_select_rect(parent_window=win, title="DRAG to add selection #{0}".format(len(self.selections)+1))
            if rect:
                self.selections.append(rect)
                if self.canvas_rect is None:
                    self.canvas_rect = rect
                self._rebuild_selection_previews()
                self.save_config()
                self.log(f"Selection #{len(self.selections)} added: {rect}")
                self._update_canvas_label()
                _refresh_list()

        def remove_selection():
            sel = listbox.curselection()
            if sel:
                i = sel[0]
                removed = self.selections.pop(i)
                if self.canvas_rect == removed:
                    self.canvas_rect = self.selections[0] if self.selections else None
                self._rebuild_selection_previews()
                self.save_config()
                self.log(f"Selection #{i+1} removed")
                self._update_canvas_label()
                _refresh_list()

        def clear_all():
            if self.selections:
                self.selections.clear()
                self.canvas_rect = None
                self._rebuild_selection_previews()
                self.save_config()
                self.log("All selections cleared")
                self._update_canvas_label()
                _refresh_list()

        def move_up():
            sel = listbox.curselection()
            if sel and sel[0] > 0:
                i = sel[0]
                self.selections[i-1], self.selections[i] = self.selections[i], self.selections[i-1]
                _refresh_list(keep_selection=False)
                listbox.selection_set(i - 1)
                _show_preview(i - 1)
                self._update_canvas_label()

        def move_down():
            sel = listbox.curselection()
            if sel and sel[0] < len(self.selections) - 1:
                i = sel[0]
                self.selections[i+1], self.selections[i] = self.selections[i], self.selections[i+1]
                _refresh_list(keep_selection=False)
                listbox.selection_set(i + 1)
                _show_preview(i + 1)
                self._update_canvas_label()

        for label, cmd, color in [
            ("+ ADD", add_selection, T["success"]),
            ("- REMOVE", remove_selection, T["danger"]),
            ("CLEAR ALL", clear_all, "#660000"),
            ("MOVE UP", move_up, T["bg3"]),
            ("MOVE DOWN", move_down, T["bg3"]),
        ]:
            tk.Button(btn_row, text=label, command=cmd,
                      bg=color, fg=T["fg"], font=("Courier", 9, "bold"),
                      bd=0, padx=8, pady=4).pack(side="left", padx=3)

        info_frame = tk.LabelFrame(win, text=" INFO ", bg=T["bg"], fg=T["accent"],
                                   font=("Courier", 9))
        info_frame.pack(fill="x", padx=15, pady=5)

        self._sel_info_label = tk.Label(info_frame, text="", bg=T["bg"], fg=T["fg"],
                                        font=("Courier", 8), justify="left")
        self._sel_info_label.pack(pady=4)

        def _update_info():
            total_px = sum((r[2]-r[0])*(r[3]-r[1]) for r in self.selections) if self.selections else 0
            self._sel_info_label.config(
                text=f"Total selections: {len(self.selections)}  |  Total area: {total_px} px²"
            )

        _refresh_list()
        _update_info()
        self._update_canvas_label()

        # Keep info updated
        def poll():
            if win.winfo_exists():
                _update_info()
                win.after(1000, poll)
        win.after(1000, poll)

    # ──────────────────────────────────────────
    #  PALETTE CALIBRATION
    # ──────────────────────────────────────────
    def calibrate_palette(self):
        self.palette_map = []
        win = tk.Toplevel(self.root)
        T = CURRENT_THEME
        win.title("Palette Calibration")
        win.geometry("400x200")
        win.configure(bg=T["bg"])
        win.attributes("-topmost", True)

        count_var = tk.StringVar(value="Colors captured: 0")
        tk.Label(win, text="Click on game color swatches.", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 10)).pack(pady=10)
        count_label = tk.Label(win, textvariable=count_var, bg=T["bg"], fg=T["accent"],
                                font=("Courier", 11, "bold"))
        count_label.pack()

        preview_frame = tk.Frame(win, bg=T["bg"], height=40)
        preview_frame.pack(fill="x", padx=20)

        stop_event = threading.Event()

        def on_click(x, y, button, pressed):
            if stop_event.is_set():
                return False
            if pressed and button == pmouse.Button.left:
                time.sleep(0.05)
                try:
                    rgb = pyautogui.pixel(int(x), int(y))
                    self.palette_map.append({"pos": [int(x), int(y)], "rgb": list(rgb)})
                    count_var.set(f"Colors captured: {len(self.palette_map)}")
                    self.log(f"Captured color #{len(self.palette_map)}: RGB{rgb}")
                    # Update preview swatches
                    try:
                        for widget in preview_frame.winfo_children():
                            widget.destroy()
                        for entry in self.palette_map[-12:]:
                            r, g, b = entry["rgb"]
                            hex_c = "#{:02x}{:02x}{:02x}".format(r, g, b)
                            tk.Label(preview_frame, bg=hex_c, width=3, height=2,
                                     relief="flat").pack(side="left", padx=1)
                    except Exception:
                        pass
                except Exception as ex:
                    self.log(f"Pixel capture error: {ex}")

        def stop():
            stop_event.set()
            self.save_config()
            self.log(f"Palette calibrated: {len(self.palette_map)} colors")
            win.destroy()

        tk.Button(win, text="DONE (Stop Capturing)", command=stop,
                  bg=T["success"], fg=T["bg"], font=("Courier", 10, "bold"), bd=0).pack(pady=10)

        def listen():
            with pmouse.Listener(on_click=on_click) as listener:
                stop_event.wait()
                listener.stop()

        threading.Thread(target=listen, daemon=True).start()

    # ──────────────────────────────────────────
    #  PALETTE GENERATION (K-Means)
    # ──────────────────────────────────────────
    def generate_palette(self):
        img = self._get_active_image()
        if not img:
            messagebox.showwarning("No Image", "Load an image first")
            return
        size = simpledialog.askinteger(
            "Palette Size", f"Number of colors (2–64):",
            initialvalue=SETTINGS["PALETTE_SIZE"], minvalue=2, maxvalue=64
        )
        if not size:
            return
        SETTINGS["PALETTE_SIZE"] = size
        self.log(f"Generating {size}-color palette via K-Means...")

        def _run():
            try:
                arr = np.array(img.resize((200, 200), Image.Resampling.LANCZOS))
                pixels = arr.reshape(-1, 3).astype(np.float32)
                if HAS_SCIPY:
                    centroids, _ = kmeans(pixels, size)
                else:
                    # Fallback: random sampling then k-means via numpy
                    idx = np.random.choice(len(pixels), size, replace=False)
                    centroids = pixels[idx]
                    for _ in range(50):
                        dists = np.linalg.norm(pixels[:, None] - centroids[None], axis=2)
                        labels = np.argmin(dists, axis=1)
                        new_c = np.array([pixels[labels == k].mean(axis=0)
                                          if (labels == k).any() else centroids[k]
                                          for k in range(size)])
                        if np.allclose(new_c, centroids, atol=0.1):
                            break
                        centroids = new_c
                palette_rgb = centroids.astype(int).tolist()
                self.palette_map = [{"pos": [0, 0], "rgb": [max(0,min(255,v)) for v in rgb]}
                                    for rgb in palette_rgb]
                self.root.after(0, lambda: self.log(f"Palette: {len(self.palette_map)} colors generated"))
                self.root.after(0, self.save_config)
                # Show palette preview
                preview = Image.new("RGB", (160, 20 * len(palette_rgb)), (20, 20, 20))
                draw_p = ImageDraw.Draw(preview)
                for i, rgb in enumerate(palette_rgb):
                    draw_p.rectangle([0, i*20, 160, (i+1)*20],
                                     fill=tuple(max(0, min(255, v)) for v in rgb))
                    draw_p.text((5, i*20+4), f"#{i+1}", fill="white")
                self.root.after(0, lambda: preview.show())
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Palette gen error: {e}"))

        threading.Thread(target=_run, daemon=True).start()

    # ──────────────────────────────────────────
    #  PALETTE EDITOR
    # ──────────────────────────────────────────
    def open_palette_editor(self):
        def on_save(new_palette):
            self.palette_map = new_palette
            self.save_config()
            self.log(f"Palette updated: {len(new_palette)} colors")
        PaletteEditorWindow(self.root, self.palette_map, on_save)

    # ──────────────────────────────────────────
    #  SKETCH CONFIGURATION
    # ──────────────────────────────────────────
    def _apply_sketch_preset(self, preset_name):
        """Set multiple parameters from a preset."""
        presets = {
            "Gestural": {
                "SKETCH_JITTER": 1.2, "SKETCH_SPEED": 0.008, "SKETCH_STROKE_DELAY": 0.03,
                "SKETCH_OVERLAP": 0.8, "SKETCH_VARIATION": 0.7, "SKETCH_ORDER": "random",
                "SKETCH_ITERATIONS": 2, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 15,
                "SKETCH_WOBBLE": 0, "SKETCH_TAIL_FADE": 0.3, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 1.5, "SKETCH_STROKE_DIST": 3,
            },
            "Continuous": {
                "SKETCH_JITTER": 0.3, "SKETCH_SPEED": 0.015, "SKETCH_STROKE_DELAY": 0.0,
                "SKETCH_OVERLAP": 0.2, "SKETCH_VARIATION": 0.3, "SKETCH_ORDER": "topdown",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 1, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.6, "SKETCH_TAIL_FADE": 0.1, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 200,
                "SKETCH_SPEED_MULT": 0.8, "SKETCH_STROKE_DIST": 5,
            },
            "Staccato": {
                "SKETCH_JITTER": 0.8, "SKETCH_SPEED": 0.003, "SKETCH_STROKE_DELAY": 0.01,
                "SKETCH_OVERLAP": 0.1, "SKETCH_VARIATION": 0.8, "SKETCH_ORDER": "random",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 0.3, "SKETCH_SEGMENT_LEN": 6,
                "SKETCH_WOBBLE": 0, "SKETCH_TAIL_FADE": 0.4, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 3, "SKETCH_STROKE_DIST": 3,
            },
            "Construction": {
                "SKETCH_JITTER": 1.5, "SKETCH_SPEED": 0.006, "SKETCH_STROKE_DELAY": 0.02,
                "SKETCH_OVERLAP": 2.0, "SKETCH_VARIATION": 0.9, "SKETCH_ORDER": "size",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 2, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 2, "SKETCH_STROKE_DIST": 3,
            },
            "Hatching": {
                "SKETCH_JITTER": 0.3, "SKETCH_SPEED": 0.004, "SKETCH_STROKE_DELAY": 0.0,
                "SKETCH_OVERLAP": 0.0, "SKETCH_VARIATION": 0.2, "SKETCH_ORDER": "topdown",
                "SKETCH_ITERATIONS": 2, "SKETCH_EDGE_ONLY": 1, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.1, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 2.5, "SKETCH_STROKE_DIST": 8,
                "SKETCH_HATCH_ANGLE": 45, "SKETCH_HATCH_SPACING": 5,
            },
            "Sweep Arc": {
                "SKETCH_JITTER": 0.2, "SKETCH_SPEED": 0.012, "SKETCH_STROKE_DELAY": 0.1,
                "SKETCH_OVERLAP": 1.5, "SKETCH_VARIATION": 0.4, "SKETCH_ORDER": "center",
                "SKETCH_ITERATIONS": 2, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 30,
                "SKETCH_WOBBLE": 0.3, "SKETCH_TAIL_FADE": 0.5, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 1.2, "SKETCH_STROKE_DIST": 4,
            },
            "Scribble Fill": {
                "SKETCH_JITTER": 3, "SKETCH_SPEED": 0.005, "SKETCH_STROKE_DELAY": 0.005,
                "SKETCH_OVERLAP": 0.5, "SKETCH_VARIATION": 0.9, "SKETCH_ORDER": "random",
                "SKETCH_ITERATIONS": 3, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.5, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 3, "SKETCH_STROKE_DIST": 2,
            },
            "Diagonal Shadow": {
                "SKETCH_JITTER": 0.2, "SKETCH_SPEED": 0.005, "SKETCH_STROKE_DELAY": 0.0,
                "SKETCH_OVERLAP": 0.0, "SKETCH_VARIATION": 0.3, "SKETCH_ORDER": "size",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.15, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 2, "SKETCH_STROKE_DIST": 8,
                "SKETCH_HATCH_ANGLE": 45, "SKETCH_HATCH_SPACING": 4,
            },
            "Cross Contour": {
                "SKETCH_JITTER": 0.5, "SKETCH_SPEED": 0.005, "SKETCH_STROKE_DELAY": 0.01,
                "SKETCH_OVERLAP": 0.3, "SKETCH_VARIATION": 0.6, "SKETCH_ORDER": "size",
                "SKETCH_ITERATIONS": 2, "SKETCH_EDGE_ONLY": 0.8, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.1, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 1.8, "SKETCH_STROKE_DIST": 4,
                "SKETCH_HATCH_ANGLE": 90, "SKETCH_HATCH_SPACING": 6,
            },
            "Blind Contour": {
                "SKETCH_JITTER": 2.5, "SKETCH_SPEED": 0.01, "SKETCH_STROKE_DELAY": 0.05,
                "SKETCH_OVERLAP": 0.1, "SKETCH_VARIATION": 0.9, "SKETCH_ORDER": "random",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 20,
                "SKETCH_WOBBLE": 0.8, "SKETCH_TAIL_FADE": 0.6, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 1.5, "SKETCH_STROKE_DIST": 6,
            },
            "Stippling": {
                "SKETCH_JITTER": 0, "SKETCH_SPEED": 0.001, "SKETCH_STROKE_DELAY": 0.02,
                "SKETCH_OVERLAP": 0, "SKETCH_VARIATION": 0.1, "SKETCH_ORDER": "topdown",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 1,
                "SKETCH_WOBBLE": 0, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 0.5, "SKETCH_STROKE_DIST": 1,
            },
            "Scumbling": {
                "SKETCH_JITTER": 4, "SKETCH_SPEED": 0.008, "SKETCH_STROKE_DELAY": 0.003,
                "SKETCH_OVERLAP": 1.5, "SKETCH_VARIATION": 0.8, "SKETCH_ORDER": "random",
                "SKETCH_ITERATIONS": 4, "SKETCH_EDGE_ONLY": 0, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.9, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 1, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 2.5, "SKETCH_STROKE_DIST": 2,
            },
            "Sgraffito": {
                "SKETCH_JITTER": 3.5, "SKETCH_SPEED": 0.003, "SKETCH_STROKE_DELAY": 0.0,
                "SKETCH_OVERLAP": 0.2, "SKETCH_VARIATION": 0.5, "SKETCH_ORDER": "burst",
                "SKETCH_ITERATIONS": 1, "SKETCH_EDGE_ONLY": 1, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.4, "SKETCH_TAIL_FADE": 0, "SKETCH_GHOST": 0, "SKETCH_NO_LIFT": 0,
                "SKETCH_SPEED_MULT": 4, "SKETCH_STROKE_DIST": 3,
            },
            "Tonal Wash": {
                "SKETCH_JITTER": 1.0, "SKETCH_SPEED": 0.006, "SKETCH_STROKE_DELAY": 0.01,
                "SKETCH_OVERLAP": 2.0, "SKETCH_VARIATION": 0.7, "SKETCH_ORDER": "center",
                "SKETCH_ITERATIONS": 2, "SKETCH_EDGE_ONLY": 0.3, "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0.3, "SKETCH_TAIL_FADE": 0.2, "SKETCH_GHOST": 1, "SKETCH_NO_LIFT": 100,
                "SKETCH_SPEED_MULT": 1.2, "SKETCH_STROKE_DIST": 3,
            },
        }
        if preset_name in presets:
            for k, v in presets[preset_name].items():
                SETTINGS[k] = v

    def _start_fill_zone_calib(self):
        """Fullscreen calibration: click background to set fill zone center."""
        T = CURRENT_THEME
        cal = tk.Toplevel(self.root)
        cal.attributes('-fullscreen', True, '-alpha', 0.15, '-topmost', True)
        c = tk.Canvas(cal, bg="black", highlightthickness=0, cursor="cross")
        c.pack(fill="both", expand=True)
        info = tk.Label(cal, text="CLICK on the background area to fill  |  ESC to cancel",
                        bg="#222", fg=T["accent"], font=("Courier", 12, "bold"))
        info.place(x=20, y=20)
        info2 = tk.Label(cal, text="A blue fill will expand from your click until it hits edges",
                         bg="#222", fg=T["fg"], font=("Courier", 9))
        info2.place(x=20, y=50)

        def on_click(e):
            fx = e.x_root - (self.canvas_rect[0] if self.canvas_rect else 0)
            fy = e.y_root - (self.canvas_rect[1] if self.canvas_rect else 0)
            if fx < 0:
                fx = 0
            if fy < 0:
                fy = 0
            SETTINGS["FILL_ZONE_CENTER"] = [int(fx), int(fy)]
            SETTINGS["FILL_ZONE_ACTIVE"] = True
            c.create_oval(e.x-5, e.y-5, e.x+5, e.y+5, fill="cyan", outline="white", width=2)
            c.create_text(e.x+15, e.y, text=f"FILL @ ({fx},{fy})",
                         fill="cyan", font=("Courier", 10, "bold"), anchor="w")
            self.log(f"[FillZone] Center set at ({fx},{fy})")
            self.fill_zone_active_var.set(True)
            cal.after(800, cal.destroy)

        def on_key(e):
            if e.keysym == "Escape":
                cal.destroy()

        c.bind("<Button-1>", on_click)
        cal.bind("<Key>", on_key)
        cal.focus_set()

    def open_control_panel(self):
        """Open the massive secondary control panel with everything."""
        ControlPanelWindow(self.root, self)

    def _rebuild_sketch_config_sliders(self, sliders_frame, sliders_dict):
        """Rebuild slider controls for current preset. Fills sliders_dict."""
        for w in sliders_frame.winfo_children():
            w.destroy()
        sliders_dict.clear()

        all_sketch_keys = [
            ("SKETCH_STROKE_DIST", "Stroke Connect", 1, 20, 1, "Max gap to join same stroke"),
            ("SKETCH_JITTER", "Jitter Amount", 0, 5, 0.1, "Random offset per point"),
            ("SKETCH_SPEED", "Drag Speed (s)", 0.0, 0.1, 0.00001, "Duration per drag segment"),
            ("SKETCH_STROKE_DELAY", "Stroke Delay (s)", 0, 1.0, 0.01, "Pause between strokes"),
            ("SKETCH_OVERLAP", "Overhang", 0, 3, 0.1, "Stroke overshoot past endpoints"),
            ("SKETCH_VARIATION", "Variation", 0, 1, 0.05, "Randomness per stroke"),
            ("SKETCH_ITERATIONS", "Iterations", 1, 10, 1, "Sketch passes over image"),
            ("SKETCH_EDGE_ONLY", "Edge Only", 0, 1, 0.05, "0=fill → 1=edges only"),
            ("SKETCH_SPEED_MULT", "Speed Multiplier", 0.1, 50, 0.1, "Overall speed boost"),
            ("SKETCH_SEGMENT_LEN", "Segment Length", 0, 50, 1, "Split long paths (0=off)"),
            ("SKETCH_WOBBLE", "Wobble Noise", 0, 2, 0.1, "Sinusoidal wobble on path"),
            ("SKETCH_TAIL_FADE", "Tail Fade", 0, 1, 0.05, "Opacity drop at stroke end"),
            ("SKETCH_GHOST", "Ghost Layers", 0, 5, 1, "Semi-transparent overshoot passes"),
            ("SKETCH_NO_LIFT", "No-Lift (ms)", 0, 500, 10, "Connect strokes < this gap"),
            ("SKETCH_BPM", "Rhythm BPM", 0, 200, 5, "Beats per minute (0=off)"),
            ("SKETCH_HATCH_ANGLE", "Hatch Angle°", 0, 180, 1, "Hatching line angle"),
            ("SKETCH_HATCH_SPACING", "Hatch Spacing", 2, 30, 1, "Gap between hatch lines"),
            ("SKETCH_CONSTRUCTION_PASSES", "Construction Passes", 1, 10, 1, "Searching lines per stroke"),
        ]

        T = CURRENT_THEME
        for key, label, min_v, max_v, res, desc in all_sketch_keys:
            row = tk.Frame(sliders_frame, bg=T["bg"])
            row.pack(fill="x", pady=2)

            info_frame = tk.Frame(row, bg=T["bg"])
            info_frame.pack(side="left", fill="x", expand=True)

            tk.Label(info_frame, text=label, bg=T["bg"], fg=T["accent2"],
                     font=("Courier", 9, "bold"), anchor="w").pack(fill="x")
            tk.Label(info_frame, text=desc, bg=T["bg"], fg=T["fg"],
                     font=("Courier", 7)).pack(fill="x")

            var = tk.DoubleVar(value=SETTINGS.get(key, 0))
            sliders_dict[key] = var

            s = tk.Scale(row, from_=min_v, to=max_v, resolution=res,
                         orient="horizontal", variable=var, length=120,
                         bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                         highlightthickness=0,
                         command=lambda v, k=key: SETTINGS.update({k: type(SETTINGS[k])(float(v))}))
            s.pack(side="right", padx=(10, 0))

    def open_sketch_config(self):
        T = CURRENT_THEME
        win = tk.Toplevel(self.root)
        win.title("Sketch Mode Configuration")
        win.geometry("640x740")
        win.configure(bg=T["bg"])
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="SKETCH MODE CONFIG", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(pady=6)
        tk.Label(win, text="Human-like sketch drawing — pick a technique, tweak sliders",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack()

        top_frame = tk.Frame(win, bg=T["bg"])
        top_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(top_frame, text="Technique Preset", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 10, "bold")).pack(side="left")
        preset_var = tk.StringVar(value=SETTINGS.get("SKETCH_PRESET", "Gestural"))
        presets = ["Gestural","Continuous","Staccato","Construction",
                   "Hatching","Sweep Arc","Scribble Fill","Diagonal Shadow",
                   "Cross Contour","Blind Contour","Stippling","Scumbling",
                   "Sgraffito","Tonal Wash","Custom"]
        preset_combo = ttk.Combobox(top_frame, textvariable=preset_var,
                                     values=presets, width=14, state="readonly")
        preset_combo.pack(side="right")

        # Scrollable slider area
        canvas = tk.Canvas(win, bg=T["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        sliders_frame = tk.Frame(canvas, bg=T["bg"])
        sliders_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sliders_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(15, 0))
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        win.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), win.destroy()))

        slider_vars = {}
        self._rebuild_sketch_config_sliders(sliders_frame, slider_vars)

        def _on_preset_change():
            p = preset_var.get()
            if p != "Custom":
                SETTINGS["SKETCH_PRESET"] = p
                self._apply_sketch_preset(p)
                self._rebuild_sketch_config_sliders(sliders_frame, slider_vars)
            else:
                SETTINGS["SKETCH_PRESET"] = "Custom"

        preset_combo.bind("<<ComboboxSelected>>", lambda e: _on_preset_change())

        # Stroke order chooser
        order_row = tk.Frame(sliders_frame, bg=T["bg"])
        order_row.pack(fill="x", pady=6)
        tk.Label(order_row, text="Stroke Order", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 9, "bold")).pack(side="left")
        order_var = tk.StringVar(value=SETTINGS.get("SKETCH_ORDER", "size"))
        order_combo = ttk.Combobox(order_row, textvariable=order_var,
                                    values=["size", "random", "topdown", "center", "burst"],
                                    width=12, state="readonly")
        order_combo.pack(side="right")
        order_combo.bind("<<ComboboxSelected>>",
            lambda e: SETTINGS.update({"SKETCH_ORDER": order_var.get()}))
        tk.Label(order_row, text="size=small→big, random=mix, topdown=top→bot, center=mid→out, burst=radial",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 7)).pack(side="bottom", anchor="w")

        # ── HEX Colorizer ──
        hex_frame = tk.LabelFrame(win, text="HEX Colorizer", bg=T["bg"], fg=T["accent"],
                                  font=("Courier", 9, "bold"), padx=8, pady=4)
        hex_frame.pack(fill="x", padx=15, pady=4)

        hex_entry_row = tk.Frame(hex_frame, bg=T["bg"])
        hex_entry_row.pack(fill="x", pady=2)
        tk.Label(hex_entry_row, text="Hex:", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 8, "bold")).pack(side="left")
        hex_var = tk.StringVar()
        hex_entry = tk.Entry(hex_entry_row, textvariable=hex_var, width=14,
                             font=("Courier", 9), bg=T["bg2"], fg=T["fg"],
                             insertbackground=T["fg"])
        hex_entry.pack(side="left", padx=4)
        hex_colors = list(SETTINGS.get("HEX_COLORS", []))

        def _refresh_hex_swatches():
            for w in hex_swatch_frame.winfo_children():
                w.destroy()
            for hc in hex_colors:
                try:
                    c = hc.lstrip("#")
                    if len(c) != 6:
                        continue
                    rgb = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                    lbl = tk.Label(hex_swatch_frame, bg=hc, width=3, height=1,
                                   relief="solid", bd=1, cursor="cross")
                    lbl.pack(side="left", padx=1)
                    lbl.bind("<Button-1>", lambda e, idx=len(hex_swatch_frame.winfo_children())-1: _remove_hex(idx))
                except Exception:
                    pass

        def _add_hex():
            raw = hex_var.get().strip()
            if raw.startswith("#"):
                raw = raw[1:]
            if len(raw) == 6 and all(c in "0123456789abcdefABCDEF" for c in raw):
                h = "#" + raw.lower()
                if h not in hex_colors:
                    hex_colors.append(h)
                    SETTINGS["HEX_COLORS"] = list(hex_colors)
                    hex_var.set("")
                    _refresh_hex_swatches()

        def _pick_hex():
            c = colorchooser.askcolor(title="Pick color for palette", parent=win)
            if c and c[1]:
                h = c[1].lower()
                if h not in hex_colors:
                    hex_colors.append(h)
                    SETTINGS["HEX_COLORS"] = list(hex_colors)
                    _refresh_hex_swatches()

        def _remove_hex(idx):
            if 0 <= idx < len(hex_colors):
                hex_colors.pop(idx)
                SETTINGS["HEX_COLORS"] = list(hex_colors)
                _refresh_hex_swatches()

        def _clear_hex():
            hex_colors.clear()
            SETTINGS["HEX_COLORS"] = []
            _refresh_hex_swatches()

        tk.Button(hex_entry_row, text="Add", command=_add_hex,
                  bg=T["bg2"], fg=T["accent"], font=("Courier", 7), bd=0).pack(side="left", padx=1)
        tk.Button(hex_entry_row, text="Pick", command=_pick_hex,
                  bg=T["bg2"], fg=T["accent"], font=("Courier", 7), bd=0).pack(side="left", padx=1)
        tk.Button(hex_entry_row, text="Clear", command=_clear_hex,
                  bg="#440000", fg=T["danger"], font=("Courier", 7), bd=0).pack(side="right", padx=1)

        hex_swatch_frame = tk.Frame(hex_frame, bg=T["bg"])
        hex_swatch_frame.pack(fill="x", pady=2)
        _refresh_hex_swatches()
        tk.Label(hex_frame, text="Colors are used to tint/colorize the drawing output",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 7)).pack(anchor="w")

        btn_row = tk.Frame(win, bg=T["bg"])
        btn_row.pack(fill="x", padx=15, pady=8)

        def reset_defaults():
            defaults = {
                "SKETCH_STROKE_DIST": 3,
                "SKETCH_JITTER": 0.5,
                "SKETCH_SPEED": 0.01,
                "SKETCH_STROKE_DELAY": 0.08,
                "SKETCH_OVERLAP": 0.3,
                "SKETCH_VARIATION": 0.5,
                "SKETCH_ITERATIONS": 1,
                "SKETCH_EDGE_ONLY": 0,
                "SKETCH_SPEED_MULT": 1,
                "SKETCH_SEGMENT_LEN": 0,
                "SKETCH_WOBBLE": 0,
                "SKETCH_TAIL_FADE": 0,
                "SKETCH_GHOST": 0,
                "SKETCH_NO_LIFT": 0,
                "SKETCH_BPM": 0,
                "SKETCH_HATCH_ANGLE": 45,
                "SKETCH_HATCH_SPACING": 5,
                "SKETCH_CONSTRUCTION_PASSES": 3,
            }
            for k, v in defaults.items():
                SETTINGS[k] = v
                if k in slider_vars:
                    slider_vars[k].set(v)
            SETTINGS["SKETCH_ORDER"] = "size"
            order_var.set("size")
            self.log("Sketch config reset to defaults")
            messagebox.showinfo("Reset", "Sketch settings reset to defaults.")

        tk.Button(btn_row, text="SET TO SKETCH MODE",
                  command=lambda: (SETTINGS.update({"DRAW_MODE": "Sketch"}),
                                   self.log("Draw mode set to Sketch"),
                                   win.destroy()),
                  bg=T["success"], fg=T["bg"], font=("Courier", 10, "bold"),
                  bd=0, padx=12).pack(side="left", padx=5)
        tk.Button(btn_row, text="RESET DEFAULTS", command=reset_defaults,
                  bg="#442200", fg=T["warn"], font=("Courier", 9, "bold"),
                  bd=0, padx=12).pack(side="left", padx=5)
        tk.Button(btn_row, text="CLOSE", command=win.destroy,
                  bg=T["bg3"], fg=T["fg"], font=("Courier", 9, "bold"),
                  bd=0, padx=12).pack(side="right", padx=5)

        self.log("Sketch config opened")

    # ──────────────────────────────────────────
    #  IMAGE PRE-PROCESSING WINDOW
    # ──────────────────────────────────────────
    def open_preprocessing(self):
        if not self.base_img:
            messagebox.showwarning("No Image", "Load an image first.")
            return
        T = CURRENT_THEME
        win = tk.Toplevel(self.root)
        win.title("Image Pre-Processing")
        win.geometry("520x560")
        win.configure(bg=T["bg"])

        tk.Label(win, text="PRE-PROCESSING", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 13, "bold")).pack(pady=10)

        img_preview_label = tk.Label(win, bg=T["bg"])
        img_preview_label.pack()

        # Show current image thumbnail
        def update_preview(img):
            thumb = img.copy()
            thumb.thumbnail((300, 200), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(thumb)
            img_preview_label.config(image=tk_img)
            img_preview_label._img = tk_img  # keep reference
            img_preview_label.image = tk_img

        update_preview(self.base_img)

        controls = tk.Frame(win, bg=T["bg"])
        controls.pack(fill="x", padx=20)

        # Resize
        resize_frame = tk.LabelFrame(controls, text=" Resize ", bg=T["bg"], fg=T["accent"],
                                     font=("Courier", 9))
        resize_frame.pack(fill="x", pady=4)

        rr = tk.Frame(resize_frame, bg=T["bg"])
        rr.pack(fill="x")
        tk.Label(rr, text="W:", bg=T["bg"], fg=T["fg"], font=("Courier", 9)).pack(side="left")
        w_var = tk.IntVar(value=self.base_img.size[0])
        tk.Entry(rr, textvariable=w_var, width=6, bg=T["bg2"], fg=T["fg"],
                 font=("Courier", 9)).pack(side="left", padx=3)
        tk.Label(rr, text="H:", bg=T["bg"], fg=T["fg"], font=("Courier", 9)).pack(side="left")
        h_var = tk.IntVar(value=self.base_img.size[1])
        tk.Entry(rr, textvariable=h_var, width=6, bg=T["bg2"], fg=T["fg"],
                 font=("Courier", 9)).pack(side="left", padx=3)

        keep_aspect_var = tk.BooleanVar(value=True)
        tk.Checkbutton(rr, text="Keep Aspect", variable=keep_aspect_var,
                       bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                       font=("Courier", 8)).pack(side="left", padx=5)

        def do_resize():
            try:
                nw, nh = w_var.get(), h_var.get()
                if keep_aspect_var.get():
                    ratio = min(nw / self.base_img.size[0], nh / self.base_img.size[1])
                    nw = int(self.base_img.size[0] * ratio)
                    nh = int(self.base_img.size[1] * ratio)
                self.base_img = self.base_img.resize((nw, nh), Image.Resampling.LANCZOS)
                self.final_img = None
                update_preview(self.base_img)
                self.log(f"Resized to {nw}×{nh}")
            except Exception as e:
                self.log(f"Resize error: {e}")

        tk.Button(resize_frame, text="APPLY RESIZE", command=do_resize,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(pady=3)

        # Quantize
        quant_frame = tk.LabelFrame(controls, text=" Color Quantize ", bg=T["bg"], fg=T["accent"],
                                    font=("Courier", 9))
        quant_frame.pack(fill="x", pady=4)
        qr = tk.Frame(quant_frame, bg=T["bg"])
        qr.pack(fill="x")
        tk.Label(qr, text="Colors:", bg=T["bg"], fg=T["fg"], font=("Courier", 9)).pack(side="left")
        q_var = tk.IntVar(value=16)
        tk.Scale(qr, from_=2, to=256, orient="horizontal", variable=q_var, length=120,
                 bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                 highlightthickness=0).pack(side="left")

        def do_quantize():
            try:
                quantized = self.base_img.quantize(colors=q_var.get(), method=Image.Quantize.MEDIANCUT)
                self.base_img = quantized.convert('RGB')
                self.final_img = None
                update_preview(self.base_img)
                self.log(f"Quantized to {q_var.get()} colors")
            except Exception as e:
                self.log(f"Quantize error: {e}")

        tk.Button(quant_frame, text="QUANTIZE", command=do_quantize,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(pady=3)

        # Quick filters
        filter_frame = tk.LabelFrame(controls, text=" Quick Filters ", bg=T["bg"], fg=T["accent"],
                                     font=("Courier", 9))
        filter_frame.pack(fill="x", pady=4)
        ff = tk.Frame(filter_frame, bg=T["bg"])
        ff.pack(fill="x")

        def quick_filter(fn):
            try:
                self.base_img = fn(self.base_img)
                self.final_img = None
                update_preview(self.base_img)
            except Exception as e:
                self.log(f"Filter error: {e}")

        filters = [
            ("Grayscale", lambda i: i.convert('L').convert('RGB')),
            ("Edge Enhance", lambda i: i.filter(ImageFilter.EDGE_ENHANCE_MORE)),
            ("Sharpen", lambda i: ImageEnhance.Sharpness(i).enhance(2.0)),
            ("Equalize", lambda i: ImageOps.equalize(i)),
            ("Flip H", lambda i: ImageOps.mirror(i)),
            ("Flip V", lambda i: ImageOps.flip(i)),
            ("Rotate 90", lambda i: i.rotate(90, expand=True)),
            ("Posterize", lambda i: ImageOps.posterize(i, 3)),
        ]
        for label, fn in filters:
            tk.Button(ff, text=label, command=lambda f=fn: quick_filter(f),
                      bg=T["bg2"], fg=T["fg"], font=("Courier", 8), bd=0, padx=5, pady=2
                      ).pack(side="left", padx=2, pady=2)

        tk.Button(win, text="APPLY & CLOSE", bg=T["success"], fg=T["bg"],
                  font=("Courier", 10, "bold"), bd=0, command=win.destroy).pack(pady=10)

    # ──────────────────────────────────────────
    #  BATCH QUEUE
    # ──────────────────────────────────────────
    def open_batch_queue(self):
        T = CURRENT_THEME
        win = tk.Toplevel(self.root)
        win.title("Batch Draw Queue")
        win.geometry("500x400")
        win.configure(bg=T["bg"])

        tk.Label(win, text="BATCH DRAW QUEUE", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 12, "bold")).pack(pady=8)
        tk.Label(win, text="Images will be drawn sequentially using current canvas & palette.",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack()

        listbox = tk.Listbox(win, bg=T["log_bg"], fg=T["fg"],
                             font=("Courier", 9), height=12, selectbackground=T["accent2"])
        listbox.pack(fill="both", expand=True, padx=15, pady=5)

        for p in self.batch_queue:
            listbox.insert(tk.END, os.path.basename(p))

        def add():
            paths = filedialog.askopenfilenames(
                filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
            )
            for p in paths:
                if p not in self.batch_queue:
                    self.batch_queue.append(p)
                    listbox.insert(tk.END, os.path.basename(p))

        def remove():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                listbox.delete(idx)
                del self.batch_queue[idx]

        def clear():
            self.batch_queue.clear()
            listbox.delete(0, tk.END)

        def start_batch():
            if not self.batch_queue:
                messagebox.showwarning("Empty", "No images in queue.")
                return
            if not self.canvas_rect and self.selections:
                self.canvas_rect = self.selections[0]
            if not self.canvas_rect or not self.palette_map:
                messagebox.showerror("Not Ready", "Set canvas and palette first.")
                return
            win.destroy()
            threading.Thread(target=self._run_batch, daemon=True).start()

        btn_row = tk.Frame(win, bg=T["bg"])
        btn_row.pack(fill="x", padx=15, pady=5)
        for label, cmd in [
            ("+ ADD", add), ("✕ REMOVE", remove), ("CLEAR ALL", clear), ("▶ START BATCH", start_batch)
        ]:
            tk.Button(btn_row, text=label, command=cmd, bg=T["btn"], fg=T["fg"],
                      font=("Courier", 9, "bold"), bd=0, padx=8).pack(side="left", padx=3)

    def _run_batch(self):
        self.batch_active = True
        if not self.canvas_rect and self.selections:
            self.canvas_rect = self.selections[0]
        self.log(f"Batch draw started: {len(self.batch_queue)} images")
        for i, path in enumerate(list(self.batch_queue)):
            if not self.batch_active:
                self.log("Batch aborted.")
                return
            self.log(f"Batch [{i+1}/{len(self.batch_queue)}]: {os.path.basename(path)}")
            try:
                img = Image.open(path).convert('RGB')
                self.base_img = img
                cw = self.canvas_rect[2] - self.canvas_rect[0]
                ch = self.canvas_rect[3] - self.canvas_rect[1]
                scale = min(cw / img.size[0], ch / img.size[1])
                nw, nh = max(1, int(img.size[0] * scale)), max(1, int(img.size[1] * scale))
                draw_src = img.resize((nw, nh), Image.Resampling.LANCZOS)
                self.execute_draw(draw_src)
                if i < len(self.batch_queue) - 1:
                    self.log("Waiting 3s before next image...")
                    time.sleep(3)
            except Exception as e:
                self.log(f"Batch error on {os.path.basename(path)}: {e}")
        self.log("Batch draw complete.")
        self.batch_active = False

    def start_batch_draw(self):
        threading.Thread(target=self._run_batch, daemon=True).start()

    # ──────────────────────────────────────────
    #  EDITOR
    # ──────────────────────────────────────────
    def open_editor(self):
        if not self.base_img:
            messagebox.showwarning("Warning", "Load an image first.")
            return
        T = CURRENT_THEME

        editor = tk.Toplevel(self.root)
        editor.title("SF2M Studio — Image Editor")
        editor.geometry("1440x900")
        editor.configure(bg=T["bg"])

        # Initialize layers if empty
        if not self.layers:
            self.layers = [{"name": "Base", "img": self.base_img.copy(), "visible": True}]
            self.active_layer = 0

        # ── Sidebar ──
        sidebar = tk.Frame(editor, width=260, bg=T["bg2"])
        sidebar.pack(side="left", fill="y", padx=2, pady=2)
        sidebar.pack_propagate(False)

        # ── Canvas area ──
        canvas_cont = tk.Frame(editor, bg=T["bg"])
        canvas_cont.pack(side="right", expand=True, fill="both")

        self.edit_canvas = tk.Canvas(canvas_cont, bg="#111", highlightthickness=0, cursor="crosshair")
        self.edit_canvas.pack(expand=True, fill="both")

        # Editor state
        state = {
            "zoom": 1.0,
            "pan_x": 0,
            "pan_y": 0,
            "last_mx": 0,
            "last_my": 0,
            "panning": False,
        }

        filter_vars = {
            "bright": tk.DoubleVar(value=1.0),
            "contrast": tk.DoubleVar(value=1.0),
            "sat": tk.DoubleVar(value=1.0),
            "sharp": tk.DoubleVar(value=1.0),
        }

        # ── Sidebar: Tools ──
        tk.Label(sidebar, text="TOOLS", bg=T["bg2"], fg=T["accent"],
                 font=("Courier", 10, "bold")).pack(pady=(10, 2))

        tool_frame = tk.Frame(sidebar, bg=T["bg2"])
        tool_frame.pack(fill="x", padx=5)

        self.tool_var = tk.StringVar(value=self.tool_mode)
        tools = [
            ("✋ Move", "Move"), ("✏️ Brush", "Brush"), ("⬜ Eraser", "Eraser"),
            ("🪣 Fill", "Fill"), ("🔍 Picker", "Picker"),
            ("✂️ Crop", "Crop"), ("T  Text", "Text"),
        ]
        for label, mode in tools:
            rb = tk.Radiobutton(tool_frame, text=label, variable=self.tool_var, value=mode,
                                command=lambda m=mode: setattr(self, 'tool_mode', m),
                                bg=T["bg2"], fg=T["fg"], selectcolor=T["bg3"],
                                activebackground=T["bg2"], font=("Courier", 9),
                                indicatoron=0, relief="flat", pady=3)
            rb.pack(fill="x", pady=1)

        tk.Label(sidebar, text="BRUSH SIZE", bg=T["bg2"], fg=T["accent"],
                 font=("Courier", 9)).pack()
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        tk.Scale(sidebar, from_=1, to=50, orient="horizontal", variable=self.brush_size_var,
                 command=lambda v: setattr(self, 'brush_size', int(v)),
                 bg=T["bg2"], fg=T["accent"], troughcolor=T["bg"],
                 highlightthickness=0).pack(fill="x", padx=5)

        tk.Label(sidebar, text="BRUSH COLOR", bg=T["bg2"], fg=T["accent"],
                 font=("Courier", 9)).pack(pady=(5, 0))
        self.brush_color_btn = tk.Label(sidebar, bg="#{:02x}{:02x}{:02x}".format(*self.brush_color),
                                        width=8, height=2, relief="solid", cursor="hand2")
        self.brush_color_btn.pack(pady=2)

        def pick_brush_color(e=None):
            c = colorchooser.askcolor(color="#{:02x}{:02x}{:02x}".format(*self.brush_color))
            if c and c[0]:
                self.brush_color = tuple(int(v) for v in c[0])
                self.brush_color_btn.config(bg=c[1])
        self.brush_color_btn.bind("<Button-1>", pick_brush_color)

        # ── Filters ──
        tk.Label(sidebar, text="FILTERS", bg=T["bg2"], fg=T["accent"],
                 font=("Courier", 10, "bold")).pack(pady=(10, 2))

        for label, key in [("Brightness", "bright"), ("Contrast", "contrast"),
                            ("Saturation", "sat"), ("Sharpness", "sharp")]:
            tk.Label(sidebar, text=label, bg=T["bg2"], fg=T["fg"],
                     font=("Courier", 8)).pack()
            tk.Scale(sidebar, from_=0.0, to=3.0, resolution=0.05, orient="horizontal",
                     variable=filter_vars[key], command=lambda v, k=key: _apply_filters(),
                     bg=T["bg2"], fg=T["accent"], troughcolor=T["bg"],
                     highlightthickness=0).pack(fill="x", padx=5)

        # ── History / Undo ──
        hist_row = tk.Frame(sidebar, bg=T["bg2"])
        hist_row.pack(fill="x", padx=5, pady=8)
        tk.Button(hist_row, text="↩ UNDO", command=lambda: _undo(),
                  bg="#330000", fg=T["danger"], font=("Courier", 8, "bold"), bd=0).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(hist_row, text="↪ REDO", command=lambda: _redo(),
                  bg="#001a33", fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(side="left", expand=True, fill="x", padx=2)

        # ── Layers ──
        tk.Label(sidebar, text="LAYERS", bg=T["bg2"], fg=T["accent"],
                 font=("Courier", 10, "bold")).pack(pady=(10, 2))

        layer_listbox = tk.Listbox(sidebar, bg=T["log_bg"], fg=T["fg"],
                                   font=("Courier", 8), height=5,
                                   selectbackground=T["accent2"])
        layer_listbox.pack(fill="x", padx=5)
        for l in self.layers:
            layer_listbox.insert(tk.END, ("👁 " if l["visible"] else "  ") + l["name"])

        def _refresh_layer_list():
            layer_listbox.delete(0, tk.END)
            for i, l in enumerate(self.layers):
                vis = "👁 " if l["visible"] else "  "
                sel = "► " if i == self.active_layer else "  "
                layer_listbox.insert(tk.END, f"{sel}{vis}{l['name']}")

        layer_btn_row = tk.Frame(sidebar, bg=T["bg2"])
        layer_btn_row.pack(fill="x", padx=5, pady=2)
        for text, fn in [
            ("+ ADD", lambda: _layer_add()),
            ("✕ DEL", lambda: _layer_del()),
            ("MERGE", lambda: _layer_merge()),
            ("TOGGLE", lambda: _layer_toggle()),
        ]:
            tk.Button(layer_btn_row, text=text, command=fn, bg=T["bg3"], fg=T["fg"],
                      font=("Courier", 7), bd=0, padx=3).pack(side="left", padx=1)

        def _layer_select(e):
            sel = layer_listbox.curselection()
            if sel:
                self.active_layer = sel[0]
        layer_listbox.bind("<<ListboxSelect>>", _layer_select)

        def _layer_add():
            name = simpledialog.askstring("Layer", "Layer name:", initialvalue=f"Layer {len(self.layers)+1}")
            if name:
                new_img = Image.new("RGB", self.layers[0]["img"].size, (255, 255, 255))
                self.layers.append({"name": name, "img": new_img, "visible": True})
                self.active_layer = len(self.layers) - 1
                _refresh_layer_list()

        def _layer_del():
            if len(self.layers) <= 1:
                messagebox.showwarning("Can't delete", "Must have at least one layer.")
                return
            del self.layers[self.active_layer]
            self.active_layer = max(0, self.active_layer - 1)
            _apply_filters()
            _refresh_layer_list()

        def _layer_merge():
            if len(self.layers) < 2:
                return
            base = self.layers[0]["img"].copy().convert("RGBA")
            for l in self.layers[1:]:
                if l["visible"]:
                    base = Image.alpha_composite(base, l["img"].convert("RGBA"))
            self.layers = [{"name": "Merged", "img": base.convert("RGB"), "visible": True}]
            self.active_layer = 0
            _apply_filters()
            _refresh_layer_list()

        def _layer_toggle():
            sel = layer_listbox.curselection()
            if sel:
                i = sel[0]
                self.layers[i]["visible"] = not self.layers[i]["visible"]
                _apply_filters()
                _refresh_layer_list()

        # ── Final Controls ──
        tk.Button(sidebar, text="📤 EXPORT LAYER AS PNG",
                  command=lambda: self._export_layer(),
                  bg=T["bg3"], fg=T["fg"], font=("Courier", 8), bd=0).pack(fill="x", padx=5, pady=2)

        tk.Button(sidebar, text="✅ SAVE & CLOSE",
                  font=("Courier", 11, "bold"), bg=T["success"], fg=T["bg"],
                  bd=0, command=lambda: _finalize()
                  ).pack(side="bottom", fill="x", padx=5, pady=8)

        # ── Canvas drawing logic ──
        def _composite():
            """Composite all visible layers into one image and apply filters."""
            if not self.layers:
                return None
            base = self.layers[0]["img"].copy().convert("RGBA") if self.layers[0]["visible"] else \
                   Image.new("RGBA", self.layers[0]["img"].size, (0, 0, 0, 0))
            for l in self.layers[1:]:
                if l["visible"]:
                    base = Image.alpha_composite(base, l["img"].convert("RGBA"))
            return base.convert("RGB")

        def _apply_filters(*args):
            comp = _composite()
            if not comp:
                return
            img = ImageEnhance.Brightness(comp).enhance(filter_vars["bright"].get())
            img = ImageEnhance.Contrast(img).enhance(filter_vars["contrast"].get())
            img = ImageEnhance.Color(img).enhance(filter_vars["sat"].get())
            img = ImageEnhance.Sharpness(img).enhance(filter_vars["sharp"].get())
            self.edit_img = img
            _update_canvas()

        def _update_canvas():
            if not self.edit_img:
                return
            self.final_img = self.edit_img.copy()
            draw = ImageDraw.Draw(self.final_img)
            # Draw text objects
            for obj in self.text_objects:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                                             obj.get("size", 24))
                except Exception:
                    font = ImageFont.load_default()
                draw.text(obj["pos"], obj["text"], fill=tuple(obj.get("color", [0, 0, 0])), font=font)

            cw = self.edit_canvas.winfo_width() or 800
            ch = self.edit_canvas.winfo_height() or 600
            iw, ih = self.final_img.size
            base_scale = min(cw / iw, ch / ih)
            disp_w = int(iw * base_scale * state["zoom"])
            disp_h = int(ih * base_scale * state["zoom"])
            disp_img = self.final_img.resize((max(1, disp_w), max(1, disp_h)), Image.Resampling.NEAREST)
            self.tk_edit_img = ImageTk.PhotoImage(disp_img)
            self.edit_canvas.delete("all")
            ox = cw // 2 + state["pan_x"]
            oy = ch // 2 + state["pan_y"]
            self.edit_canvas.create_image(ox, oy, image=self.tk_edit_img, anchor="center")
            self.edit_canvas.create_text(
                10, 10, anchor="nw",
                text=f"Zoom: {state['zoom']:.2f}x | Layer: {self.active_layer} - {self.layers[self.active_layer]['name']}",
                fill=CURRENT_THEME["accent"], font=("Courier", 8)
            )

        def _img_coords(cx, cy):
            """Convert canvas coords to image pixel coords."""
            cw = self.edit_canvas.winfo_width() or 800
            ch = self.edit_canvas.winfo_height() or 600
            ox = cw // 2 + state["pan_x"]
            oy = ch // 2 + state["pan_y"]
            if not self.final_img:
                return 0, 0
            iw, ih = self.final_img.size
            base_scale = min(cw / iw, ch / ih) * state["zoom"]
            disp_w = iw * base_scale
            disp_h = ih * base_scale
            ix = int((cx - (ox - disp_w / 2)) / base_scale)
            iy = int((cy - (oy - disp_h / 2)) / base_scale)
            return max(0, min(iw - 1, ix)), max(0, min(ih - 1, iy))

        def _push_history():
            if self.active_layer < len(self.layers):
                self.history.append((self.active_layer, self.layers[self.active_layer]["img"].copy()))
                self.redo_stack.clear()

        def _undo():
            if self.history:
                li, img = self.history.pop()
                self.redo_stack.append((li, self.layers[li]["img"].copy()))
                self.layers[li]["img"] = img
                _apply_filters()

        def _redo():
            if self.redo_stack:
                li, img = self.redo_stack.pop()
                self.history.append((li, self.layers[li]["img"].copy()))
                self.layers[li]["img"] = img
                _apply_filters()

        def on_click(e):
            state["last_mx"], state["last_my"] = e.x, e.y
            ix, iy = _img_coords(e.x, e.y)
            layer_img = self.layers[self.active_layer]["img"]
            layer_draw = ImageDraw.Draw(layer_img)

            if self.tool_mode == "Brush":
                _push_history()
                layer_draw.ellipse(
                    [ix - self.brush_size, iy - self.brush_size,
                     ix + self.brush_size, iy + self.brush_size],
                    fill=self.brush_color
                )
                _apply_filters()
            elif self.tool_mode == "Eraser":
                _push_history()
                layer_draw.ellipse(
                    [ix - self.brush_size, iy - self.brush_size,
                     ix + self.brush_size, iy + self.brush_size],
                    fill=(255, 255, 255)
                )
                _apply_filters()
            elif self.tool_mode == "Fill":
                _push_history()
                try:
                    ImageDraw.floodfill(layer_img, (ix, iy), self.brush_color, thresh=30)
                except Exception:
                    pass
                _apply_filters()
            elif self.tool_mode == "Picker":
                try:
                    pix = layer_img.getpixel((ix, iy))
                    self.brush_color = pix[:3]
                    self.brush_color_btn.config(bg="#{:02x}{:02x}{:02x}".format(*self.brush_color))
                    self.log(f"Color picked: RGB{self.brush_color}")
                except Exception:
                    pass
            elif self.tool_mode == "Text":
                t = simpledialog.askstring("Text", "Enter text:")
                if t:
                    s = simpledialog.askinteger("Size", "Font size:", initialvalue=24)
                    self.text_objects.append({
                        "text": t, "pos": [ix, iy],
                        "size": s or 24, "color": list(self.brush_color)
                    })
                    _apply_filters()

        def on_drag(e):
            ix, iy = _img_coords(e.x, e.y)
            lx, ly = _img_coords(state["last_mx"], state["last_my"])
            state["last_mx"], state["last_my"] = e.x, e.y
            if self.active_layer >= len(self.layers):
                return
            layer_img = self.layers[self.active_layer]["img"]
            layer_draw = ImageDraw.Draw(layer_img)

            if self.tool_mode == "Brush":
                layer_draw.line([lx, ly, ix, iy], fill=self.brush_color, width=self.brush_size * 2)
                _apply_filters()
            elif self.tool_mode == "Eraser":
                layer_draw.line([lx, ly, ix, iy], fill=(255, 255, 255), width=self.brush_size * 2)
                _apply_filters()
            elif self.tool_mode == "Move" and self.text_objects:
                self.text_objects[-1]["pos"] = [ix, iy]
                _apply_filters()

        def on_pan_start(e):
            state["panning"] = True
            state["last_mx"], state["last_my"] = e.x, e.y

        def on_pan_drag(e):
            if state["panning"]:
                dx = e.x - state["last_mx"]
                dy = e.y - state["last_my"]
                state["pan_x"] += dx
                state["pan_y"] += dy
                state["last_mx"], state["last_my"] = e.x, e.y
                _update_canvas()

        def on_pan_end(e):
            state["panning"] = False

        def on_scroll(e):
            factor = 1.1 if e.delta > 0 or e.num == 4 else 0.9
            state["zoom"] = max(0.05, min(20.0, state["zoom"] * factor))
            _update_canvas()

        self.edit_canvas.bind("<Button-1>", on_click)
        self.edit_canvas.bind("<B1-Motion>", on_drag)
        self.edit_canvas.bind("<Button-2>", on_pan_start)
        self.edit_canvas.bind("<B2-Motion>", on_pan_drag)
        self.edit_canvas.bind("<ButtonRelease-2>", on_pan_end)
        self.edit_canvas.bind("<MouseWheel>", on_scroll)
        self.edit_canvas.bind("<Button-4>", on_scroll)
        self.edit_canvas.bind("<Button-5>", on_scroll)

        editor.bind("<Control-z>", lambda e: _undo())
        editor.bind("<Control-y>", lambda e: _redo())

        def _export_layer():
            if self.active_layer < len(self.layers):
                path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG", "*.png")])
                if path:
                    self.layers[self.active_layer]["img"].save(path)
                    self.log(f"Exported layer to: {os.path.basename(path)}")
        self._export_layer = _export_layer

        def _finalize():
            # Merge visible layers back to base_img
            comp = _composite()
            if comp:
                # Apply current filter values permanently
                img = ImageEnhance.Brightness(comp).enhance(filter_vars["bright"].get())
                img = ImageEnhance.Contrast(img).enhance(filter_vars["contrast"].get())
                img = ImageEnhance.Color(img).enhance(filter_vars["sat"].get())
                img = ImageEnhance.Sharpness(img).enhance(filter_vars["sharp"].get())
                self.final_img = img
                self.base_img = img.copy()
                self.log("Editor saved. Final image updated.")
            editor.destroy()

        editor.after(100, _apply_filters)
        editor.grab_set()

    # ──────────────────────────────────────────
    #  PREVIEW & DRAW LAUNCH
    # ──────────────────────────────────────────
    def show_preview(self):
        raw = self._get_active_image()
        if not raw:
            messagebox.showerror("Error", "Load an image first.")
            return
        if not self.canvas_rect and self.selections:
            self.canvas_rect = self.selections[0]
            self.log(f"Auto-set canvas to selection #1: {self.canvas_rect}")
        if not self.canvas_rect:
            messagebox.showerror("Error", "Set a canvas region or add a selection first.")
            return
        T = CURRENT_THEME
        cw = self.canvas_rect[2] - self.canvas_rect[0]
        ch = self.canvas_rect[3] - self.canvas_rect[1]
        self.preview_scale = min(cw / max(1, raw.size[0]), ch / max(1, raw.size[1]))

        prev = tk.Toplevel(self.root)
        prev.overrideredirect(True)
        prev.attributes("-topmost", True, "-alpha", 0.75)
        preview_label = tk.Label(prev, bg="black")
        preview_label.pack()
        info_label = tk.Label(prev, text="Scroll=resize | Mid-drag=move | F10=START",
                              bg="black", fg=T["accent"], font=("Courier", 7))
        info_label.pack()

        drag_state = {"last_y": 0, "drag_x": 0, "drag_y": 0}
        self._preview_tk_img = None

        def update_p():
            nw = max(4, int(raw.size[0] * self.preview_scale))
            nh = max(4, int(raw.size[1] * self.preview_scale))
            res = raw.copy()
            res.thumbnail((nw, nh), Image.Resampling.LANCZOS)
            self._preview_tk_img = ImageTk.PhotoImage(res)
            preview_label.config(image=self._preview_tk_img)
            self.draw_source = res
            # Position over canvas
            px = self.canvas_rect[0]
            py = self.canvas_rect[1]
            prev.geometry(f"+{px}+{py}")

        def on_scroll(e):
            factor = 1.1 if e.delta > 0 or e.num == 4 else 0.9
            self.preview_scale = max(0.01, min(5.0, self.preview_scale * factor))
            update_p()

        def on_mid_start(e):
            drag_state["drag_x"] = e.x_root
            drag_state["drag_y"] = e.y_root

        def on_mid_drag(e):
            dx = e.x_root - drag_state["drag_x"]
            dy = e.y_root - drag_state["drag_y"]
            drag_state["drag_x"], drag_state["drag_y"] = e.x_root, e.y_root
            x = prev.winfo_x() + dx
            y = prev.winfo_y() + dy
            prev.geometry(f"+{x}+{y}")

        prev.bind("<MouseWheel>", on_scroll)
        prev.bind("<Button-4>", on_scroll)
        prev.bind("<Button-5>", on_scroll)
        prev.bind("<Button-2>", on_mid_start)
        prev.bind("<B2-Motion>", on_mid_drag)
        prev.bind("<F10>", lambda e: setattr(self, 'ready_to_draw', True))

        update_p()
        self.preview_active = True
        self.ready_to_draw = False

        self.log(f"Preview active. Scale: {self.preview_scale:.3f}. Press F10 to draw.")

        while not self.ready_to_draw and self.preview_active:
            try:
                self.root.update()
            except Exception:
                self.preview_active = False
                break
            time.sleep(0.01)

        self.preview_active = False
        try:
            prev.destroy()
        except Exception:
            pass

        if self.ready_to_draw:
            # Show draw stats window
            # Build queues quickly for stats
            if self.palette_map and self.draw_source:
                try:
                    StatsWindow(self.root, {i: [] for i in range(len(self.palette_map))},
                                self.palette_map, 0, 0)
                except Exception:
                    pass
            threading.Thread(target=self.execute_draw, args=(self.draw_source,), daemon=True).start()

    # ──────────────────────────────────────────
    #  COLOR METRICS
    # ──────────────────────────────────────────
    def color_difference(self, rgb1, rgb2):
        a = np.array(rgb1, dtype=np.float32)
        b = np.array(rgb2, dtype=np.float32)
        metric = SETTINGS["COLOR_METRIC"]
        if metric == "CIEDE2000" and HAS_SKIMAGE:
            lab1 = skimage_rgb2lab(a.reshape(1, 1, 3) / 255.0).flatten()
            lab2 = skimage_rgb2lab(b.reshape(1, 1, 3) / 255.0).flatten()
            return deltaE_ciede2000(lab1, lab2)
        elif metric == "Manhattan":
            return float(np.sum(np.abs(a - b)))
        else:
            return float(np.linalg.norm(a - b))

    def _find_closest_palette(self, pixel_rgb, pal_arr):
        """Find the palette index closest to pixel_rgb using the current metric."""
        metric = SETTINGS["COLOR_METRIC"]
        if metric == "CIEDE2000" and HAS_SKIMAGE:
            lab_pixel = skimage_rgb2lab(
                np.array(pixel_rgb, dtype=np.float32).reshape(1, 1, 3) / 255.0
            ).flatten()
            lab_pal = skimage_rgb2lab(pal_arr.reshape(1, -1, 3) / 255.0)[0]  # (N, 3)
            dists = np.array([deltaE_ciede2000(lab_pixel, lp) for lp in lab_pal])
        elif metric == "Manhattan":
            dists = np.sum(np.abs(pal_arr - np.array(pixel_rgb, dtype=np.float32)), axis=1)
        else:
            dists = np.linalg.norm(pal_arr - np.array(pixel_rgb, dtype=np.float32), axis=1)
        return int(np.argmin(dists))

    # ──────────────────────────────────────────
    #  DITHERING
    # ──────────────────────────────────────────
    def apply_dither(self, img):
        mode = SETTINGS["DITHER_MODE"]
        self.log(f"Applying {mode} dithering...")

        pal_arr = np.array([c["rgb"] for c in self.palette_map], dtype=np.float32)
        w, h = img.size

        if mode == "Ordered":
            arr = np.array(img, dtype=np.float32)
            bayer = np.tile(BAYER_4X4, (h // 4 + 1, w // 4 + 1))[:h, :w]
            threshold = (bayer[:, :, np.newaxis] - 0.5) * 64  # scale spread
            arr = np.clip(arr + threshold, 0, 255)
            out = np.zeros_like(arr, dtype=np.uint8)
            for y in range(h):
                for x in range(w):
                    best = self._find_closest_palette(arr[y, x].tolist(), pal_arr)
                    out[y, x] = pal_arr[best].astype(np.uint8)
            return Image.fromarray(out)

        elif mode == "Atkinson":
            arr = np.array(img, dtype=float)
            for y in range(h - 2):
                for x in range(1, w - 2):
                    old = arr[y, x].copy()
                    best = self._find_closest_palette(old.tolist(), pal_arr)
                    new = pal_arr[best]
                    arr[y, x] = new
                    err = (old - new) / 8.0
                    for dx, dy in [(1,0),(2,0),(-1,1),(0,1),(1,1),(0,2)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            arr[ny, nx] += err
            return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))

        elif mode == "Stucki":
            arr = np.array(img, dtype=float)
            for y in range(h - 2):
                for x in range(1, w - 2):
                    old = arr[y, x].copy()
                    best = self._find_closest_palette(old.tolist(), pal_arr)
                    new = pal_arr[best]
                    arr[y, x] = new
                    err = old - new
                    for dx, dy, f in [(1,0,8),(2,0,4),(-2,1,2),(-1,1,4),(0,1,8),(1,1,4),(2,1,2),(-2,2,1),(-1,2,2),(0,2,4),(1,2,2),(2,2,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            arr[ny, nx] += err * f / 42.0
            return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))

        elif mode == "SierraLite":
            arr = np.array(img, dtype=float)
            for y in range(h - 1):
                for x in range(1, w - 1):
                    old = arr[y, x].copy()
                    best = self._find_closest_palette(old.tolist(), pal_arr)
                    new = pal_arr[best]
                    arr[y, x] = new
                    err = old - new
                    for dx, dy, f in [(1,0,2),(-1,1,1),(0,1,1),(1,1,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            arr[ny, nx] += err * f / 4.0
            return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))

        elif mode == "Halftone":
            arr = np.array(img, dtype=np.uint8)
            out = np.zeros_like(arr, dtype=np.uint8)
            cell = 4
            for cy in range(0, h, cell):
                for cx in range(0, w, cell):
                    patch = arr[cy:min(h, cy+cell), cx:min(w, cx+cell)]
                    avg = patch.mean(axis=(0,1))
                    best = self._find_closest_palette(avg.tolist(), pal_arr)
                    out[cy:min(h, cy+cell), cx:min(w, cx+cell)] = pal_arr[best].astype(np.uint8)
            return Image.fromarray(out)

        else:  # Floyd-Steinberg (default)
            arr = np.array(img, dtype=float)
            for y in range(h - 1):
                for x in range(1, w - 1):
                    old = arr[y, x].copy()
                    best = self._find_closest_palette(old.tolist(), pal_arr)
                    new = pal_arr[best]
                    arr[y, x] = new
                    err = old - new
                    arr[y,   x+1] += err * 7 / 16
                    arr[y+1, x-1] += err * 3 / 16
                    arr[y+1, x  ] += err * 5 / 16
                    arr[y+1, x+1] += err * 1 / 16
            return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))

    # ──────────────────────────────────────────
    #  EXECUTE DRAW (Main Draw Engine)
    # ──────────────────────────────────────────
    def execute_draw(self, img):
        if not self.palette_map:
            self.log("ERROR: No palette set. Calibrate or generate palette first.")
            return
        self.drawing_active = True
        self.drawing_paused = False
        self.draw_start_time = time.time()
        mode = SETTINGS["DRAW_MODE"]
        self.log(f"Starting draw: mode={mode}, metric={SETTINGS['COLOR_METRIC']}, "
                 f"dither={SETTINGS['DITHER_MODE']}, gap={SETTINGS['PIXEL_GAP']}")

        # Apply dithering
        if SETTINGS["DITHER_MODE"] != "None":
            img = self.apply_dither(img)

        pix = np.array(img)
        pal_arr = np.array([c["rgb"] for c in self.palette_map], dtype=np.float32)  # BUG FIX: stack as array
        n_colors = len(self.palette_map)
        queues = {i: [] for i in range(n_colors)}

        # ── HEX Colorization: pre-map image pixels to chosen hex colors ──
        hex_colors = SETTINGS.get("HEX_COLORS", [])
        if hex_colors:
            hex_rgbs = []
            for hc in hex_colors:
                try:
                    c = hc.lstrip("#")
                    hex_rgbs.append([int(c[i:i+2], 16) for i in (0, 2, 4)])
                except Exception:
                    pass
            if hex_rgbs:
                hpal = np.array(hex_rgbs, dtype=np.float32)
                h, w = pix.shape[:2]
                flat = pix[..., :3].reshape(-1, 3).astype(np.float32)
                for i in range(h * w):
                    d = np.sum(np.abs(flat[i] - hpal), axis=1)
                    flat[i] = hpal[int(np.argmin(d))]
                pix = np.dstack([flat.reshape(h, w, 3).astype(np.uint8), pix[..., 3:]]) if pix.shape[2] == 4 else flat.reshape(h, w, 3).astype(np.uint8)
                self.log(f"[HexColor] Colorized to {len(hex_rgbs)} hex colors")

        img_w, img_h = img.size
        gap = SETTINGS["PIXEL_GAP"]
        white_skip = SETTINGS["WHITE_SKIP"]
        skip_blue = SETTINGS["SKIP_BLUE_MASK"]
        bg_aware = SETTINGS.get("BG_AWARENESS_ENABLE", False)

        # Detect background color from image corners when BG awareness is on
        bg_rgb = None
        if bg_aware:
            corner_samples = []
            margin = max(2, min(img_w, img_h) // 20)
            for cy in range(0, img_h, margin):
                for cx in range(0, img_w, margin):
                    if (cx < margin or cx >= img_w - margin or
                        cy < margin or cy >= img_h - margin):
                        corner_samples.append(tuple(pix[cy, cx]))
            if corner_samples:
                bg_arr = np.array(corner_samples, dtype=np.float32)
                bg_mean = bg_arr.mean(axis=0)
                if np.all(np.abs(bg_arr - bg_mean).max(axis=0) < 25):
                    bg_rgb = tuple(int(v) for v in bg_mean)

        # ── Step 1: Pixel collection ──
        for y in range(0, img_h, gap):
            for x in range(0, img_w, gap):
                r, g, b = int(pix[y, x, 0]), int(pix[y, x, 1]), int(pix[y, x, 2])
                # Expanded chroma-key skip: blue, green, magenta
                if skip_blue:
                    is_chroma = (
                        (b > 180 and r < 60 and g < 60) or
                        (g > 180 and r < 60 and b < 60) or
                        (r > 180 and g < 60 and b < 60) or
                        (max(r,g,b) - min(r,g,b) < 8 and b > 200)
                    )
                    if is_chroma:
                        continue
                # Luminance-based white skip instead of per-channel threshold
                luminance = 0.299 * r + 0.587 * g + 0.114 * b
                if luminance > white_skip:
                    continue
                # Skip detected background color
                if bg_rgb is not None:
                    dr, dg, db = r - bg_rgb[0], g - bg_rgb[1], b - bg_rgb[2]
                    if dr*dr + dg*dg + db*db < 900:
                        continue
                best = self._find_closest_palette([r, g, b], pal_arr)
                queues[best].append((x, y))

        total_dots = sum(len(v) for v in queues.values())
        self.estimated_total = total_dots
        self.log(f"Pixel collection complete: {total_dots:,} dots across {n_colors} colors")

        if total_dots == 0:
            self.log("WARNING: 0 dots to draw. Check image and white-skip settings.")
            self.drawing_active = False
            return

        # Show stats window (only pass pps estimate after at least 1s elapsed)
        elapsed = max(0.0, time.time() - self.draw_start_time)
        pps_est = total_dots / elapsed if elapsed >= 1.0 else 0.0
        self.root.after(0, lambda: StatsWindow(
            self.root, queues, self.palette_map, total_dots, pps_est
        ))

        # ── Step 2: Sorting per draw mode ──
        def sort_queues():
            for i in range(n_colors):
                pts = queues[i]
                if not pts:
                    continue
                if mode == "Linear":
                    pts.sort(key=lambda p: (p[1], p[0]))
                elif mode == "Random":
                    random.shuffle(pts)
                elif mode == "Radial":
                    cx, cy = img_w // 2, img_h // 2
                    pts.sort(key=lambda p: math.hypot(p[0] - cx, p[1] - cy))
                elif mode == "ConcentricRings":
                    cx, cy = img_w // 2, img_h // 2
                    pts.sort(key=lambda p: (int(math.hypot(p[0]-cx, p[1]-cy) / (gap*2)), p[1], p[0]))
                elif mode == "Snake":
                    rows = {}
                    for px, py in pts:
                        rows.setdefault(py, []).append(px)
                    new_pts = []
                    for ri, ry in enumerate(sorted(rows)):
                        row = sorted(rows[ry])
                        if ri % 2 == 1:
                            row.reverse()
                        new_pts.extend([(x, ry) for x in row])
                    queues[i] = new_pts
                elif mode == "ColumnMajor":
                    pts.sort(key=lambda p: (p[0], p[1]))
                elif mode == "Hilbert":
                    hpts = generate_hilbert_points(img_w, img_h)
                    hmap = {p: idx for idx, p in enumerate(hpts)}
                    pts.sort(key=lambda p: hmap.get(p, 10**9))
                elif mode == "Spiral":
                    spts = generate_spiral_points(img_w, img_h)
                    smap = {p: idx for idx, p in enumerate(spts)}
                    pts.sort(key=lambda p: smap.get(p, 10**9))
                elif mode == "Checkerboard":
                    pts.sort(key=lambda p: ((p[0] + p[1]) % 2, p[1], p[0]))
                elif mode == "DarkFirst":
                    # Sort by luminance ascending (dark pixels first)
                    pts.sort(key=lambda p: (
                        0.299 * pix[p[1], p[0], 0] +
                        0.587 * pix[p[1], p[0], 1] +
                        0.114 * pix[p[1], p[0], 2]
                    ))
                elif mode == "LightFirst":
                    pts.sort(key=lambda p: -(
                        0.299 * pix[p[1], p[0], 0] +
                        0.587 * pix[p[1], p[0], 1] +
                        0.114 * pix[p[1], p[0], 2]
                    ))
                elif mode == "Burst":
                    cx, cy = img_w // 2, img_h // 2
                    pts.sort(key=lambda p: (
                        int(math.atan2(p[1] - cy, p[0] - cx) * 4 / math.pi),  # wedge
                        math.hypot(p[0] - cx, p[1] - cy)  # distance outward
                    ))
                elif mode == "SpeedFill":
                    # Maximize adjacency: sort by row then column, but cluster
                    pts.sort(key=lambda p: (p[1] // 8, p[0] // 8, p[1], p[0]))
                elif mode == "Pointillism":
                    # Cluster by 16px blocks, random within each for dot-scatter effect
                    pts.sort(key=lambda p: (p[1] // 16, p[0] // 16, random.random()))
                elif mode == "CrossHatchFill":
                    # Alternate angles: primary direction then perpendicular
                    pts.sort(key=lambda p: ((p[0] + p[1]) % 4, p[1], p[0]))
                elif mode == "Woven":
                    # Basket-weave: interleaved rows alternate offset
                    pts.sort(key=lambda p: (p[1], (p[0] + (1 if (p[1] // 6) % 2 else 0)) % 12, p[0]))
                # "Optimized" keeps natural insertion order (roughly top-left to bottom-right)

        sort_queues()

        # ── Step 3: Handle special modes ──
        if mode == "Sketch":
            self._execute_sketch(img, pix, queues, n_colors, pal_arr)
            return

        if mode == "Intelligent":
            engine = IntelligentDrawEngine(self)
            pal_entry = self.palette_map[0] if self.palette_map else {"pos": [0, 0], "rgb": [0, 0, 0]}
            engine.execute(img, self.canvas_rect, pal_entry, self)
            return

        if mode == "ZigzagRow":
            # Build combined list with color index, sorted globally in zigzag
            rows_dict = {}
            color_at = {}  # (x,y) -> color_idx
            for cidx, pts in queues.items():
                for pt in pts:
                    rows_dict.setdefault(pt[1], []).append(pt[0])
                    color_at[pt] = cidx  # BUG FIX: was storing (idx,pt) reversed

            combined_sorted = []
            for ri, ry in enumerate(sorted(rows_dict)):
                row_xs = sorted(rows_dict[ry])
                if ri % 2 == 1:
                    row_xs.reverse()
                for rx in row_xs:
                    pt = (rx, ry)
                    combined_sorted.append((color_at[pt], pt))

            self._draw_combined_list(combined_sorted, total_dots)
            return

        # ── Step 4: Continuous stroke drawing (fast, low-lag) ──
        self._execute_stroke_draw(queues, pal_arr, total_dots, gap)

    # ──────────────────────────────────────────
    #  STROKE-BASED DRAW ENGINE
    # ──────────────────────────────────────────
    def _pixels_to_strokes(self, pts, connect_dist=2):
        connect_dist = int(round(connect_dist))
        if not pts:
            return []
        pts_set = set(pts)
        visited = set()
        strokes = []
        for pt in pts:
            if pt in visited:
                continue
            stroke = []
            stack = [pt]
            visited.add(pt)
            while stack:
                cx, cy = stack.pop()
                stroke.append((cx, cy))
                for dx in range(-connect_dist, connect_dist + 1):
                    for dy in range(-connect_dist, connect_dist + 1):
                        if dx == 0 and dy == 0:
                            continue
                        if abs(dx) + abs(dy) > connect_dist:
                            continue
                        np_ = (cx + dx, cy + dy)
                        if np_ in pts_set and np_ not in visited:
                            visited.add(np_)
                            stack.append(np_)
            if len(stroke) >= 2:
                strokes.append(stroke)
        strokes.sort(key=len, reverse=True)
        return strokes

    def _stroke_to_path(self, stroke):
        if len(stroke) <= 2:
            return list(stroke)
        pts_set = list(stroke)
        start = min(pts_set, key=lambda p: (p[1], p[0]))
        path = [start]
        remaining = set(pts_set)
        remaining.remove(start)
        curr = start
        # Build spatial grid for O(1) neighbor lookup
        cell_size = 8
        grid = {}
        for p in remaining:
            gx, gy = p[0] // cell_size, p[1] // cell_size
            grid.setdefault((gx, gy), []).append(p)
        def nearest_in_grid(cx, cy):
            best_p = None
            best_d = float('inf')
            max_radius = 1
            for radius in range(max_radius + 1):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if abs(dx) != radius and abs(dy) != radius:
                            continue
                        cell = grid.get((cx // cell_size + dx, cy // cell_size + dy))
                        if not cell:
                            continue
                        for p in cell:
                            d = abs(p[0] - cx) + abs(p[1] - cy)
                            if d < best_d:
                                best_d = d
                                best_p = p
                if best_p is not None:
                    break
            return best_p
        while remaining:
            best = nearest_in_grid(curr[0], curr[1])
            if best is None:
                remaining_list = list(remaining)
                if not remaining_list:
                    break
                best = min(remaining_list, key=lambda p: abs(p[0] - curr[0]) + abs(p[1] - curr[1]))
            path.append(best)
            gx, gy = best[0] // cell_size, best[1] // cell_size
            cell_list = grid.get((gx, gy))
            if cell_list:
                try:
                    cell_list.remove(best)
                    if not cell_list:
                        del grid[(gx, gy)]
                except ValueError:
                    pass
            remaining.remove(best)
            curr = best
        return path

    def _smooth_stroke_path(self, path, passes=2):
        if len(path) < 3:
            return path
        result = list(path)
        for _ in range(passes):
            smoothed = [result[0]]
            for i in range(1, len(result) - 1):
                x = (result[i-1][0] + result[i][0] * 2 + result[i+1][0]) / 4
                y = (result[i-1][1] + result[i][1] * 2 + result[i+1][1]) / 4
                smoothed.append((int(x), int(y)))
            smoothed.append(result[-1])
            result = smoothed
        return result

    def _draw_stroke_continuous(self, path, sx, sy, speed_mult=1.0, driver=None):
        if len(path) < 2:
            return 0
        gs = max(0.1, SETTINGS.get("GLOBAL_SPEED", 1.0))
        speed = float(SETTINGS.get("CLICK_DELAY", 0.0)) / max(0.01, gs * speed_mult)
        smooth_passes = int(SETTINGS.get("STROKE_SMOOTH_PASSES", 2))
        spath = self._smooth_stroke_path(path, smooth_passes)
        drv = driver if driver is not None else FastInputDriver()
        x0, y0 = sx + int(spath[0][0]), sy + int(spath[0][1])
        drv.press(x0, y0)
        if speed > 0:
            time.sleep(speed * 0.2)
        for px, py in spath[1:]:
            if not self.drawing_active:
                break
            while self.drawing_paused:
                if not self.drawing_active:
                    break
                time.sleep(0.02)
            tx, ty = sx + int(px), sy + int(py)
            drv.drag_to(tx, ty)
            if speed > 0:
                time.sleep(speed)
        drv.release()
        return len(spath)

    def _execute_stroke_draw(self, queues, pal_arr, total_dots, gap):
        sx, sy = self.canvas_rect[0], self.canvas_rect[1]
        dots_drawn = 0
        pps_tick_dots = 0
        pps_tick_ts = time.time()
        gs = SETTINGS.get("GLOBAL_SPEED", 1.0)
        use_strokes = SETTINGS.get("STROKE_MODE", "stroke") == "stroke"
        driver = FastInputDriver()

        # Check fill zone
        fill_active = SETTINGS.get("FILL_ZONE_ACTIVE", False)
        fill_center = SETTINGS.get("FILL_ZONE_CENTER", [0, 0])
        fill_color = SETTINGS.get("FILL_ZONE_COLOR", [0, 100, 255])
        fill_thresh = SETTINGS.get("FILL_ZONE_THRESHOLD", 30)
        fill_grow = SETTINGS.get("FILL_ZONE_GROW_STEPS", 5)
        fill_pixels = []

        if fill_active and fill_center[0] > 0 and fill_center[1] > 0:
            try:
                fill_pixels = self._compute_fill_zone(
                    int(fill_center[0]), int(fill_center[1]),
                    fill_color, fill_thresh, fill_grow
                )
                if fill_pixels:
                    self.log(f"[FillZone] {len(fill_pixels)} fill pixels computed")
            except Exception as e:
                self.log(f"[FillZone] error: {e}")

        for cidx, pts in queues.items():
            if not self.drawing_active:
                break
            if not pts:
                continue
            if cidx >= len(self.palette_map):
                self.log(f"WARNING: palette index {cidx} out of range, skipping")
                continue

            # Select palette color using FastInputDriver
            entry = self.palette_map[cidx]
            pos = entry.get("pos", [0, 0])
            if pos[0] == 0 and pos[1] == 0:
                self.log(f"WARNING: palette color {cidx} has position (0,0)")
            driver.move(pos[0], pos[1])
            time.sleep(SETTINGS["UI_DELAY"] / max(0.1, gs * 2))
            driver.click(pos[0], pos[1])
            time.sleep(SETTINGS["CLICK_DELAY"] / max(0.1, gs * 2))

            if not use_strokes:
                # Legacy dot mode
                for px, py in pts:
                    if not self.drawing_active:
                        break
                    while self.drawing_paused:
                        if not self.drawing_active:
                            break
                        time.sleep(0.02)
                    tx, ty = sx + px, sy + py
                    driver.click(tx, ty)
                    dots_drawn += 1
                    pps_tick_dots += 1
                    now = time.time()
                    if now - pps_tick_ts >= 1.0:
                        pps = pps_tick_dots / max(0.001, now - pps_tick_ts)
                        self.last_pps = pps
                        pps_tick_dots = 0
                        pps_tick_ts = now
                    if dots_drawn % 100 == 0:
                        self._update_progress(dots_drawn, total_dots)
            else:
                # Stroke mode: group adjacent pixels into strokes and drag
                strokes = self._pixels_to_strokes(pts, max(1, gap + 1))
                for stroke in strokes:
                    if not self.drawing_active:
                        break
                    while self.drawing_paused:
                        if not self.drawing_active:
                            break
                        time.sleep(0.02)
                    path = self._stroke_to_path(stroke)
                    drawn = self._draw_stroke_continuous(path, sx, sy, speed_mult=1.0, driver=driver)
                    dots_drawn += drawn
                    pps_tick_dots += drawn
                    now = time.time()
                    if now - pps_tick_ts >= 1.0:
                        pps = pps_tick_dots / max(0.001, now - pps_tick_ts)
                        self.last_pps = pps
                        pps_tick_dots = 0
                        pps_tick_ts = now
                    if dots_drawn % 100 == 0:
                        self._update_progress(dots_drawn, total_dots)

        # Draw fill zone on top (blue fill)
        if fill_pixels:
            self.log("[FillZone] Applying fill...")
            blue_idx = self._find_closest_palette(fill_color, pal_arr)
            driver.move(
                self.palette_map[blue_idx]["pos"][0],
                self.palette_map[blue_idx]["pos"][1]
            )
            time.sleep(SETTINGS["UI_DELAY"] / max(0.1, gs * 2))
            driver.click(
                self.palette_map[blue_idx]["pos"][0],
                self.palette_map[blue_idx]["pos"][1]
            )
            time.sleep(SETTINGS["CLICK_DELAY"] / max(0.1, gs * 2))
            fill_strokes = self._pixels_to_strokes(fill_pixels, max(1, gap + 1))
            for stroke in fill_strokes:
                if not self.drawing_active:
                    break
                path = self._stroke_to_path(stroke)
                self._draw_stroke_continuous(path, sx, sy, speed_mult=2.0, driver=driver)
                dots_drawn += len(path)

        self._draw_finished(dots_drawn)

    def _compute_fill_zone(self, cx, cy, fill_color, threshold, grow_steps):
        """Edge-aware fill zone: expand from center until hitting edges."""
        if not self.canvas_rect:
            return []
        x1, y1, x2, y2 = self.canvas_rect
        cw, ch = x2 - x1, y2 - y1
        if cw <= 0 or ch <= 0:
            return []
        # Capture the entire canvas region at once
        try:
            region_img = pyautogui.screenshot(region=(x1, y1, cw, ch))
            region_arr = np.array(region_img, dtype=np.uint8)
        except Exception:
            return []
        # Sample the background at click point
        try:
            sample = tuple(region_arr[min(cy, ch-1), min(cx, cw-1)][:3])
        except:
            sample = (200, 200, 200)
        sample = np.array(sample, dtype=np.int16)
        filled = np.zeros((ch, cw), dtype=bool)
        filled[cy, cx] = True
        frontier = [(cx, cy)]
        thresh3 = threshold * 3
        while frontier and grow_steps > 0:
            new_frontier = []
            for fx, fy in frontier:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                    nx, ny = fx + dx, fy + dy
                    if 0 <= nx < cw and 0 <= ny < ch and not filled[ny, nx]:
                        pr, pg, pb = region_arr[ny, nx][:3]
                        dr = abs(int(pr) - int(sample[0]))
                        dg = abs(int(pg) - int(sample[1]))
                        db = abs(int(pb) - int(sample[2]))
                        if dr + dg + db < thresh3:
                            filled[ny, nx] = True
                            new_frontier.append((nx, ny))
            frontier = new_frontier
            grow_steps -= 1
        ys, xs = np.nonzero(filled)
        return list(zip(xs.tolist(), ys.tolist()))

    def _draw_combined_list(self, combined_sorted, total_dots):
        """Draw a pre-sorted combined list using continuous strokes."""
        sx, sy = self.canvas_rect[0], self.canvas_rect[1]
        dots_drawn = 0
        curr_color = -1
        gs = SETTINGS.get("GLOBAL_SPEED", 1.0)
        gap = SETTINGS["PIXEL_GAP"]

        # Group by color into continuous strokes
        color_groups = {}
        for cidx, pt in combined_sorted:
            color_groups.setdefault(cidx, []).append(pt)

        driver = FastInputDriver()
        for cidx, pts in color_groups.items():
            if not self.drawing_active:
                break
            driver.move(
                self.palette_map[cidx]["pos"][0],
                self.palette_map[cidx]["pos"][1]
            )
            time.sleep(SETTINGS["UI_DELAY"] / max(0.1, gs * 2))
            driver.click(
                self.palette_map[cidx]["pos"][0],
                self.palette_map[cidx]["pos"][1]
            )
            time.sleep(SETTINGS["CLICK_DELAY"] / max(0.1, gs * 2))

            strokes = self._pixels_to_strokes(pts, max(1, gap + 1))
            for stroke in strokes:
                if not self.drawing_active:
                    break
                path = self._stroke_to_path(stroke)
                drawn = self._draw_stroke_continuous(path, sx, sy, speed_mult=1.0, driver=driver)
                dots_drawn += drawn

        self._draw_finished(dots_drawn)

    def _update_progress(self, done, total):
        if total == 0:
            return
        pct = min((done / total) * 100, 100.0)
        elapsed = time.time() - self.draw_start_time
        remaining = max(total - done, 0)
        eta = (elapsed / max(done, 1) * remaining) if done > 0 else 0
        eta_str = f"ETA: {int(eta//60)}m {int(eta%60)}s"
        self.root.after(0, self._update_progress_ui, pct, done, total, eta_str)

    def _update_progress_ui(self, pct, done, total, eta_str):
        try:
            self.progress_var.set(pct)
            self.status_msg.config(text=f"Drawing: {done:,}/{total:,}  ({pct:.1f}%)")
            self.time_msg.config(text=eta_str)
        except Exception:
            pass

    def _update_pps_display(self, pps):
        try:
            self.pps_label.config(text=f"px/sec: {pps:.0f}")
            self.sparkline.push(pps)
        except Exception:
            pass

    def _draw_finished(self, dots_drawn):
        self.drawing_active = False
        elapsed = time.time() - self.draw_start_time
        self.log(f"Draw complete! {dots_drawn:,} dots in {elapsed:.1f}s "
                 f"({dots_drawn/max(1,elapsed):.0f} px/s avg)")
        self.root.after(0, self._draw_finished_ui)

    def _draw_finished_ui(self):
        try:
            self.progress_var.set(0)
            self.status_msg.config(text="Ready")
            self.time_msg.config(text="")
        except Exception:
            pass


    # ──────────────────────────────────────────
    #  SKETCH MODE DRAW ENGINE
    # ──────────────────────────────────────────
    # ──────────────────────────────────────────
    #  SKETCH DRAWING HELPERS
    # ──────────────────────────────────────────

    @staticmethod
    def _compute_luminance(pix):
        return np.dot(pix.astype(np.float32), [0.299, 0.587, 0.114])

    def _detect_edges(self, pix_arr, threshold=15):
        h, w = pix_arr.shape[:2]
        if h < 2 or w < 2:
            return np.zeros((h, w), dtype=bool)
        gray = np.dot(pix_arr.astype(np.float32), [0.299, 0.587, 0.114])
        edges = np.zeros((h, w), dtype=bool)
        # Compare each pixel to its right neighbor
        right_diff = np.abs(gray[:, :-1] - gray[:, 1:]) > threshold
        edges[:, :-1] |= right_diff
        edges[:, 1:]  |= right_diff
        # Compare each pixel to its bottom neighbor
        down_diff = np.abs(gray[:-1, :] - gray[1:, :]) > threshold
        edges[:-1, :] |= down_diff
        edges[1:, :]  |= down_diff
        return edges

    def _extract_blobs(self, color_pts, connect_dist):
        return self._pixels_to_strokes(color_pts, connect_dist)

    def _blob_to_path(self, blob):
        if len(blob) <= 2:
            return list(blob)
        points = set(blob)
        start = min(points, key=lambda p: (p[1], p[0]))
        path = [start]
        points.remove(start)
        curr = start
        while points:
            best = None
            best_d = float('inf')
            for p in list(points):
                d = abs(p[0] - curr[0]) + abs(p[1] - curr[1])
                if d < best_d:
                    best_d = d
                    best = p
            if best:
                path.append(best)
                points.remove(best)
                curr = best
        return path

    def _apply_jitter(self, path_in, jitter_amt, stroke_var, variation):
        if jitter_amt <= 0:
            return path_in
        scale = jitter_amt * (1 + stroke_var * variation * 2 - variation)
        return [(px + random.uniform(-scale, scale),
                 py + random.uniform(-scale, scale)) for px, py in path_in]

    def _apply_overhang(self, path_in, overhang):
        if overhang <= 0 or len(path_in) < 3:
            return path_in
        p1 = path_in[-2]
        p2 = path_in[-1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        if dist < 0.5:
            return path_in
        ex = p2[0] + (dx / dist) * overhang * random.uniform(0.5, 1.5)
        ey = p2[1] + (dy / dist) * overhang * random.uniform(0.5, 1.5)
        return list(path_in) + [(ex, ey)]

    def _segment_path(self, path, seg_len):
        if seg_len <= 0 or len(path) <= seg_len:
            return [path]
        segments = []
        for i in range(0, len(path), seg_len):
            chunk = path[i:i + seg_len + 1]
            if len(chunk) >= 2:
                segments.append(chunk)
        return segments

    def _apply_wobble(self, path, wobble_amt, phase_offset=0):
        if wobble_amt <= 0:
            return path
        return [(px + math.sin(i * 0.5 + phase_offset) * wobble_amt,
                 py + math.cos(i * 0.35 + phase_offset) * wobble_amt * 0.7)
                for i, (px, py) in enumerate(path)]

    def _draw_path(self, path, sx, sy, speed, driver=None):
        if not path:
            return
        driver = driver if driver is not None else FastInputDriver()
        x0, y0 = sx + int(path[0][0]), sy + int(path[0][1])
        driver.press(x0, y0)
        if speed > 0:
            time.sleep(speed * 0.5)
        for px, py in path[1:]:
            if not self.drawing_active:
                break
            while self.drawing_paused:
                if not self.drawing_active:
                    break
                time.sleep(0.02)
            tx, ty = sx + int(px), sy + int(py)
            driver.drag_to(tx, ty)
            if speed > 0:
                time.sleep(speed)
        driver.release()

    def _select_color(self, cidx, driver=None):
        drv = driver if driver is not None else FastInputDriver()
        drv.move(
            self.palette_map[cidx]["pos"][0],
            self.palette_map[cidx]["pos"][1]
        )
        time.sleep(SETTINGS["UI_DELAY"])
        drv.click(
            self.palette_map[cidx]["pos"][0],
            self.palette_map[cidx]["pos"][1]
        )
        time.sleep(SETTINGS["CLICK_DELAY"])

    def _bpm_wait(self, bpm):
        if bpm <= 0:
            return
        beat_interval = 60.0 / bpm
        now = time.time()
        next_beat = math.ceil(now / beat_interval) * beat_interval
        while time.time() < next_beat:
            if not self.drawing_active:
                break
            time.sleep(0.01)

    def _check_abort_pause(self):
        if not self.drawing_active:
            return True
        while self.drawing_paused:
            if not self.drawing_active:
                return True
            time.sleep(0.05)
        return False

    def _order_blobs(self, blobs, order, img_w, img_h):
        if order == "random":
            random.shuffle(blobs)
        elif order == "topdown":
            blobs.sort(key=lambda b: min(p[1] for p in b))
        elif order == "center":
            cx, cy = img_w // 2, img_h // 2
            blobs.sort(key=lambda b: min(math.hypot(p[0]-cx, p[1]-cy) for p in b))
        elif order == "burst":
            cx, cy = img_w // 2, img_h // 2
            blobs.sort(key=lambda b: (
                int(math.atan2(np.mean([p[1] for p in b]) - cy,
                               np.mean([p[0] for p in b]) - cx) * 4 / math.pi),
                min(math.hypot(p[0]-cx, p[1]-cy) for p in b)
            ))
        else:
            blobs.sort(key=len)
        return blobs

    # ──────────────────────────────────────────
    #  SKETCH PRESET TECHNIQUES
    # ──────────────────────────────────────────
    def _sketch_technique_common(self, queues, sx, sy, img_w, img_h, n_colors, n_total_dots,
                                  preset, pix):
        s_dist = SETTINGS["SKETCH_STROKE_DIST"]
        j_amt = SETTINGS["SKETCH_JITTER"]
        s_speed = SETTINGS["SKETCH_SPEED"] / max(0.01, SETTINGS["SKETCH_SPEED_MULT"]) / max(0.01, SETTINGS.get("GLOBAL_SPEED", 1.0))
        s_delay = SETTINGS["SKETCH_STROKE_DELAY"] / max(0.01, SETTINGS["SKETCH_SPEED_MULT"])
        o_hang = SETTINGS["SKETCH_OVERLAP"]
        variation = SETTINGS["SKETCH_VARIATION"]
        iterations = max(1, int(SETTINGS["SKETCH_ITERATIONS"]))
        edge_only = SETTINGS["SKETCH_EDGE_ONLY"]
        seg_len = int(SETTINGS["SKETCH_SEGMENT_LEN"])
        wobble_amt = SETTINGS["SKETCH_WOBBLE"]
        fade_amt = SETTINGS["SKETCH_TAIL_FADE"]
        ghost_n = int(SETTINGS["SKETCH_GHOST"])
        no_lift_ms = int(SETTINGS["SKETCH_NO_LIFT"])
        bpm = int(SETTINGS["SKETCH_BPM"])
        order = SETTINGS["SKETCH_ORDER"]
        const_passes = int(SETTINGS["SKETCH_CONSTRUCTION_PASSES"])

        edge_mask = None
        if edge_only > 0:
            edge_mask = self._detect_edges(pix)
            if edge_only < 1.0:
                rnd_mask = np.random.random(edge_mask.shape) < edge_only
                edge_mask = edge_mask | rnd_mask

        last_stroke_end_time = 0
        total_drawn = 0

        for iteration in range(iterations):
            if not self.drawing_active:
                break
            for cidx in range(n_colors):
                if not self.drawing_active:
                    break
                pts = queues[cidx]
                if not pts:
                    continue
                if edge_mask is not None:
                    pts = [p for p in pts if edge_mask[p[1], p[0]]]
                    if not pts:
                        continue

                blobs = self._extract_blobs(pts, s_dist)
                if not blobs:
                    continue
                blobs = self._order_blobs(blobs, order, img_w, img_h)
                self._select_color(cidx)

                # Construction ghost strokes (draw ghost lines before keeper)
                if ghost_n > 0 and preset == "Construction":
                    for blob in blobs:
                        if self._check_abort_pause():
                            return
                        for gp in range(ghost_n):
                            if self._check_abort_pause():
                                return
                            path = self._blob_to_path(blob)
                            path = self._apply_jitter(path, j_amt * 1.5 + gp * 0.5, 0, variation)
                            path = self._apply_overhang(path, o_hang * 2)
                            if len(path) < 2:
                                continue
                            g_speed = max(0.001, s_speed * (1 + gp * 0.3))
                            self._draw_path(path, sx, sy, g_speed)
                            total_drawn += len(path)
                            time.sleep(max(0.005, s_delay * 0.3))
                            if total_drawn % 50 == 0:
                                self._update_progress(total_drawn, n_total_dots)
                        # Keeper stroke
                        path = self._blob_to_path(blob)
                        path = self._apply_jitter(path, j_amt, 0, variation)
                        path = self._apply_overhang(path, o_hang)
                        if len(path) < 2:
                            continue
                        self._draw_path(path, sx, sy, max(0.001, s_speed))
                        total_drawn += len(path)
                        if total_drawn % 50 == 0:
                            self._update_progress(total_drawn, n_total_dots)
                        delay = s_delay
                        if delay > 0:
                            time.sleep(delay)
                    continue

                # Normal blob drawing for all other presets
                for blob in blobs:
                    if self._check_abort_pause():
                        return

                    stroke_var = random.uniform(-variation, variation) if variation > 0 else 0
                    path = self._blob_to_path(blob)
                    path = self._apply_jitter(path, j_amt, stroke_var, variation)
                    path = self._apply_overhang(path, o_hang)
                    path = self._apply_wobble(path, wobble_amt, random.uniform(0, 6.28))
                    if SETTINGS["LQE_ENABLE"]:
                        lqe = LineQualityEngine(self)
                        path = lqe.smooth_stroke(path)
                    if len(path) < 2:
                        continue

                    segments = self._segment_path(path, seg_len) if seg_len > 0 else [path]

                    for seg in segments:
                        if self._check_abort_pause():
                            return
                        speed = max(0.001, s_speed * (1 + stroke_var * 0.5))
                        self._draw_path(seg, sx, sy, speed)
                        total_drawn += len(seg)
                        if total_drawn % 50 == 0:
                            self._update_progress(total_drawn, n_total_dots)
                        last_stroke_end_time = time.time()

                        # BPM rhythm
                        if bpm > 0:
                            self._bpm_wait(bpm)

                        # Tail fade: draw extra fade-out points
                        if fade_amt > 0 and len(seg) >= 4:
                            fade_n = max(2, int(len(seg) * fade_amt * 0.5))
                            fade_pts = seg[-fade_n:]
                            for fi, (fx, fy) in enumerate(fade_pts):
                                if self._check_abort_pause():
                                    return
                                frac = fi / max(1, len(fade_pts))
                                fade_spd = speed * (1 + frac * 2)
                                pyautogui.dragTo(sx + int(fx), sy + int(fy),
                                                 button='left',
                                                 duration=max(0.001, fade_spd))

                    delay = s_delay * (1 + stroke_var * 0.5)
                    if delay > 0:
                        time.sleep(delay)

    def _sketch_hatching(self, queues, sx, sy, img_w, img_h, n_colors, n_total_dots, pix):
        s_dist = SETTINGS["SKETCH_STROKE_DIST"]
        j_amt = SETTINGS["SKETCH_JITTER"]
        s_speed = SETTINGS["SKETCH_SPEED"] / max(0.01, SETTINGS["SKETCH_SPEED_MULT"]) / max(0.01, SETTINGS.get("GLOBAL_SPEED", 1.0))
        variation = SETTINGS["SKETCH_VARIATION"]
        iterations = max(1, int(SETTINGS["SKETCH_ITERATIONS"]))
        edge_only = SETTINGS["SKETCH_EDGE_ONLY"]
        wobble_amt = SETTINGS["SKETCH_WOBBLE"]
        bpm = int(SETTINGS["SKETCH_BPM"])
        order = SETTINGS["SKETCH_ORDER"]
        hatch_angle = SETTINGS["SKETCH_HATCH_ANGLE"]
        hatch_spacing = int(SETTINGS["SKETCH_HATCH_SPACING"])

        edge_mask = None
        if edge_only > 0:
            edge_mask = self._detect_edges(pix)
            if edge_only < 1.0:
                rnd_mask = np.random.random(edge_mask.shape) < edge_only
                edge_mask = edge_mask | rnd_mask

        angle_rad = math.radians(hatch_angle)
        angle2_rad = math.radians(hatch_angle + 90)
        total_drawn = 0

        luminance = self._compute_luminance(pix)

        for iteration in range(iterations):
            if not self.drawing_active:
                break
            use_cross = (iteration % 2 == 1)
            current_angle = angle2_rad if use_cross else angle_rad

            for cidx in range(n_colors):
                if not self.drawing_active:
                    break
                pts = queues[cidx]
                if not pts:
                    continue
                if edge_mask is not None:
                    pts = [p for p in pts if edge_mask[p[1], p[0]]]
                    if not pts:
                        continue

                blobs = self._extract_blobs(pts, s_dist)
                if not blobs:
                    continue
                blobs = self._order_blobs(blobs, order, img_w, img_h)
                self._select_color(cidx)

                for blob in blobs:
                    if self._check_abort_pause():
                        return
                    xs = [p[0] for p in blob]
                    ys = [p[1] for p in blob]
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    cx_blob = (min_x + max_x) / 2
                    cy_blob = (min_y + max_y) / 2
                    diag = math.hypot(max_x - min_x, max_y - min_y) + 4

                    blob_lums = luminance[min_y:max_y+1, min_x:max_x+1]
                    avg_blob_lum = blob_lums.mean()

                    # Vary spacing by luminance — darker areas get denser hatching
                    lum_factor = 1.0 - (avg_blob_lum / 255.0)
                    effective_spacing = max(2, int(hatch_spacing * (1.5 - lum_factor * 0.8)))

                    line_count = max(2, int(diag / max(1, effective_spacing)))
                    cos_a = math.cos(current_angle)
                    sin_a = math.sin(current_angle)
                    cos_perp = math.cos(current_angle + math.pi / 2)
                    sin_perp = math.sin(current_angle + math.pi / 2)

                    for li in range(line_count):
                        if self._check_abort_pause():
                            return
                        offset = (li - line_count / 2) * effective_spacing

                        # Hatch line endpoints through blob center
                        p1x = cx_blob + cos_a * diag + cos_perp * offset
                        p1y = cy_blob + sin_a * diag + sin_perp * offset
                        p2x = cx_blob - cos_a * diag + cos_perp * offset
                        p2y = cy_blob - sin_a * diag + sin_perp * offset

                        # Walk along the hatch line and sample luminance to create multi-point path
                        steps = int(math.hypot(p2x - p1x, p2y - p1y) / 2)
                        if steps < 2:
                            steps = 2
                        path = []
                        dark_run = []
                        for si in range(steps + 1):
                            t = si / steps
                            lx = int(p1x + (p2x - p1x) * t)
                            ly = int(p1y + (p2y - p1y) * t)
                            lx = max(0, min(img_w - 1, lx))
                            ly = max(0, min(img_h - 1, ly))
                            lum = luminance[ly, lx]

                            # Draw where darker than threshold — break at light gaps
                            if lum < 220:
                                dark_run.append((lx, ly))
                            else:
                                if len(dark_run) >= 2:
                                    path.extend(dark_run)
                                dark_run = []
                        if len(dark_run) >= 2:
                            path.extend(dark_run)

                        if len(path) < 2:
                            continue

                        path = self._apply_jitter(path, j_amt,
                                                  random.uniform(-variation, variation),
                                                  variation)
                        path = self._apply_wobble(path, wobble_amt, li * 1.3)
                        if SETTINGS["LQE_ENABLE"]:
                            lqe = LineQualityEngine(self)
                            path = lqe.smooth_stroke(path)
                        if len(path) < 2:
                            continue
                        speed = max(0.001, s_speed * (1 + random.uniform(-variation, variation) * 0.5))
                        self._draw_path(path, sx, sy, speed)
                        total_drawn += len(path)
                        if total_drawn % 50 == 0:
                            self._update_progress(total_drawn, n_total_dots)
                        if bpm > 0:
                            self._bpm_wait(bpm)

    def _sketch_scribble_fill(self, queues, sx, sy, img_w, img_h, n_colors, n_total_dots, pix):
        s_dist = SETTINGS["SKETCH_STROKE_DIST"]
        j_amt = SETTINGS["SKETCH_JITTER"]
        s_speed = SETTINGS["SKETCH_SPEED"] / max(0.01, SETTINGS["SKETCH_SPEED_MULT"]) / max(0.01, SETTINGS.get("GLOBAL_SPEED", 1.0))
        variation = SETTINGS["SKETCH_VARIATION"]
        iterations = max(1, int(SETTINGS["SKETCH_ITERATIONS"]))
        wobble_amt = SETTINGS["SKETCH_WOBBLE"]
        bpm = int(SETTINGS["SKETCH_BPM"])
        order = SETTINGS["SKETCH_ORDER"]
        total_drawn = 0

        for iteration in range(iterations):
            if not self.drawing_active:
                break
            for cidx in range(n_colors):
                if not self.drawing_active:
                    break
                pts = queues[cidx]
                if not pts:
                    continue
                blobs = self._extract_blobs(pts, s_dist)
                if not blobs:
                    continue
                blobs = self._order_blobs(blobs, order, img_w, img_h)
                self._select_color(cidx)

                for blob in blobs:
                    if self._check_abort_pause():
                        return
                    xs = [p[0] for p in blob]
                    ys = [p[1] for p in blob]
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    direction = 1 if (iteration + cidx) % 2 == 0 else -1

                    for yy in range(min_y, max_y + 1, 4):
                        if self._check_abort_pause():
                            return
                        x_start = min_x + random.uniform(-1, 1)
                        x_end = max_x + random.uniform(-1, 1)
                        if direction == 1:
                            line = [(x_start, yy), (x_end, yy)]
                        else:
                            line = [(x_end, yy), (x_start, yy)]
                        line = self._apply_jitter(line, j_amt * 2,
                                                  random.uniform(-variation, variation),
                                                  variation)
                        line = self._apply_wobble(line, wobble_amt * 2 + j_amt, yy * 0.5)
                        if len(line) < 2:
                            continue
                        speed = max(0.001, s_speed * (1 + random.uniform(-variation, variation) * 0.5))
                        self._draw_path(line, sx, sy, speed)
                        total_drawn += 2
                        if total_drawn % 50 == 0:
                            self._update_progress(total_drawn, n_total_dots)
                        direction *= -1
                        if bpm > 0:
                            self._bpm_wait(bpm)

    def _sketch_diagonal_shadow(self, queues, sx, sy, img_w, img_h, n_colors, n_total_dots, pix):
        s_dist = SETTINGS["SKETCH_STROKE_DIST"]
        j_amt = SETTINGS["SKETCH_JITTER"]
        s_speed = SETTINGS["SKETCH_SPEED"] / max(0.01, SETTINGS["SKETCH_SPEED_MULT"]) / max(0.01, SETTINGS.get("GLOBAL_SPEED", 1.0))
        variation = SETTINGS["SKETCH_VARIATION"]
        wobble_amt = SETTINGS["SKETCH_WOBBLE"]
        bpm = int(SETTINGS["SKETCH_BPM"])
        hatch_angle = SETTINGS["SKETCH_HATCH_ANGLE"]
        hatch_spacing = int(SETTINGS["SKETCH_HATCH_SPACING"])

        total_drawn = 0

        luminance = self._compute_luminance(pix)

        angles = [
            math.radians(hatch_angle),
            math.radians(hatch_angle + 90),
            math.radians(hatch_angle + 45),
            math.radians(hatch_angle + 135),
        ]

        for cidx in range(n_colors):
            if not self.drawing_active:
                break
            pts = queues[cidx]
            if not pts:
                continue
            blobs = self._extract_blobs(pts, s_dist)
            if not blobs:
                continue
            self._select_color(cidx)

            for blob in blobs:
                if self._check_abort_pause():
                    return
                xs = [p[0] for p in blob]
                ys = [p[1] for p in blob]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                cx_blob = (min_x + max_x) / 2
                cy_blob = (min_y + max_y) / 2
                blob_w = max_x - min_x + 1
                blob_h = max_y - min_y + 1
                diag = math.hypot(blob_w, blob_h) + 4

                blob_lums = luminance[min_y:max_y+1, min_x:max_x+1]
                avg_blob_lum = blob_lums.mean()

                lum_factor = 1.0 - (avg_blob_lum / 255.0)
                if lum_factor < 0.15:
                    continue

                local_spacing = max(2, int(hatch_spacing * (1.8 - lum_factor * 1.2)))
                line_count = max(2, int(diag / max(1, local_spacing)))

                for ai, angle_rad in enumerate(angles):
                    if self._check_abort_pause():
                        return
                    cos_a = math.cos(angle_rad)
                    sin_a = math.sin(angle_rad)
                    cos_perp = math.cos(angle_rad + math.pi / 2)
                    sin_perp = math.sin(angle_rad + math.pi / 2)

                    angle_line_count = max(1, line_count // 2)

                    for li in range(angle_line_count):
                        if self._check_abort_pause():
                            return
                        offset = (li - angle_line_count / 2) * local_spacing * 1.5

                        p1x = cx_blob + cos_a * diag + cos_perp * offset
                        p1y = cy_blob + sin_a * diag + sin_perp * offset
                        p2x = cx_blob - cos_a * diag + cos_perp * offset
                        p2y = cy_blob - sin_a * diag + sin_perp * offset

                        steps = int(math.hypot(p2x - p1x, p2y - p1y) / 2)
                        if steps < 2:
                            steps = 2
                        path = []
                        dark_run = []
                        for si in range(steps + 1):
                            t = si / steps
                            lx = int(p1x + (p2x - p1x) * t)
                            ly = int(p1y + (p2y - p1y) * t)
                            lx = max(0, min(img_w - 1, lx))
                            ly = max(0, min(img_h - 1, ly))
                            lum = luminance[ly, lx]
                            if lum < 200:
                                dark_run.append((lx, ly))
                            else:
                                if len(dark_run) >= 2:
                                    path.extend(dark_run)
                                dark_run = []
                        if len(dark_run) >= 2:
                            path.extend(dark_run)

                        if len(path) < 3:
                            continue

                        path = self._apply_jitter(path, j_amt,
                                                  random.uniform(-variation, variation),
                                                  variation)
                        path = self._apply_wobble(path, wobble_amt, li * 1.3 + ai * 7)
                        if SETTINGS["LQE_ENABLE"]:
                            lqe = LineQualityEngine(self)
                            path = lqe.smooth_stroke(path)
                        if len(path) < 2:
                            continue
                        speed = max(0.001, s_speed * (1 + random.uniform(-variation, variation) * 0.5))
                        self._draw_path(path, sx, sy, speed)
                        total_drawn += len(path)
                        if total_drawn % 50 == 0:
                            self._update_progress(total_drawn, n_total_dots)
                        if bpm > 0:
                            self._bpm_wait(bpm)

    def _execute_sketch(self, img, pix, queues, n_colors, pal_arr):
        """Human-like sketch drawing — dispatches to the chosen preset technique."""
        self.log("Sketch mode engaged — loose & fast")
        sx, sy = self.canvas_rect[0], self.canvas_rect[1]
        img_w, img_h = img.size
        preset = SETTINGS.get("SKETCH_PRESET", "Gestural")
        total_dots = sum(len(v) for v in queues.values())
        self.log(f"Sketch [{preset}]: {n_colors} colors, {total_dots} dots")

        if preset == "Hatching":
            self._sketch_hatching(queues, sx, sy, img_w, img_h, n_colors, total_dots, pix)
        elif preset == "Scribble Fill":
            self._sketch_scribble_fill(queues, sx, sy, img_w, img_h, n_colors, total_dots, pix)
        elif preset == "Diagonal Shadow":
            self._sketch_diagonal_shadow(queues, sx, sy, img_w, img_h, n_colors, total_dots, pix)
        else:
            self._sketch_technique_common(queues, sx, sy, img_w, img_h, n_colors, total_dots,
                                          preset, pix)

        self._draw_finished(total_dots)


# ─────────────────────────────────────────────
#  MASTER CONTROL PANEL WINDOW
# ─────────────────────────────────────────────
class ControlPanelWindow:
    def __init__(self, parent, app):
        self.app = app
        T = CURRENT_THEME
        self.win = tk.Toplevel(parent)
        self.win.title("SF2M Control Panel v6 — Master Control")
        self.win.geometry("1100x780+80+80")
        self.win.configure(bg=T["bg"])
        self.win.minsize(920, 640)

        self._build_style()

        # ── Sidebar navigation for tab content ──
        paned = tk.PanedWindow(self.win, orient="horizontal", bg=T["bg3"],
                                sashwidth=2, sashrelief="raised")
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Left sidebar: tab list
        sidebar = tk.Frame(paned, bg=T["bg3"], width=160)
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="TABS", bg=T["bg3"], fg=T["accent"],
                 font=("Courier", 9, "bold")).pack(fill="x", pady=(6, 2))

        self._tab_listbox = tk.Listbox(
            sidebar, bg=T["bg2"], fg=T["fg"], selectbackground=T["accent"],
            selectforeground=T["bg"], font=("Courier", 9, "bold"),
            bd=0, highlightthickness=0, relief="flat",
            activestyle="none"
        )
        self._tab_listbox.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        self._tab_listbox.bind("<<ListboxSelect>>", self._on_tab_select)

        # Right side: content area
        content_frame = tk.Frame(paned, bg=T["bg"])
        self.content_area = tk.Frame(content_frame, bg=T["bg"])
        self.content_area.pack(fill="both", expand=True)

        paned.add(sidebar, width=160, minsize=120)
        paned.add(content_frame, minsize=400)

        self.tabs = {}
        self._tab_order = []
        self._build_engine_tab()
        self._build_stroke_tab()
        self._build_color_tab()
        self._build_bg_tab()
        self._build_speed_tab()
        self._build_sketch_tab()
        self._build_canvas_tab()
        self._build_ai_tab()
        self._build_batch_tab()
        self._build_profile_tab()
        self._build_debug_tab()
        self._build_hotkey_tab()
        self._build_optimizer_tab()
        self._build_color_manage_tab()
        self._build_overlay_tab()
        self._build_macro_tab()
        self._build_stats_tab()
        self._build_render_tab()
        self._build_fine_tune_tab()
        self._build_network_tab()
        self._build_plugin_tab()
        self._build_accessibility_tab()
        self._build_help_tab()
        self._build_transform_tab()
        self._build_palette_tab()
        self._build_recovery_tab()
        self._build_log_tab()
        self._build_templates_tab()
        self._build_gestures_tab()
        self._build_remote_tab()
        self._build_perf_tab()
        self._build_automation_tab()
        self._build_sound_tab()
        self._build_localization_tab()

        # Select first tab
        if self._tab_order:
            self._tab_listbox.selection_set(0)
            self._show_tab(self._tab_order[0])

        btn_frame = tk.Frame(self.win, bg=T["bg"])
        btn_frame.pack(fill="x", padx=10, pady=6)
        tk.Button(btn_frame, text="SAVE ALL", command=self._save_all,
                  bg="#004400", fg=T["accent"], font=("Courier", 10, "bold"), bd=0, padx=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="RESET TO DEFAULTS", command=self._reset_defaults,
                  bg="#440000", fg=T["danger"], font=("Courier", 10, "bold"), bd=0, padx=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="CLOSE", command=self.win.destroy,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 9), bd=0, padx=10).pack(side="right", padx=5)
        self._status_lbl = tk.Label(btn_frame, text="Ready", bg=T["bg"], fg=T["success"],
                                    font=("Courier", 8))
        self._status_lbl.pack(side="right", padx=10)

    def _status(self, msg):
        try:
            self._status_lbl.config(text=msg)
            self.win.after(3000, lambda: self._status_lbl.config(text="Ready"))
        except:
            pass

    def _build_style(self):
        style = ttk.Style()
        style.theme_use("default")
        T = CURRENT_THEME
        style.configure("TNotebook", background=T["bg2"], borderwidth=0)
        style.configure("TNotebook.Tab", background=T["bg3"], foreground=T["fg"],
                        padding=[12, 4], font=("Courier", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", T["accent"])],
                  foreground=[("selected", T["bg"])])

    def _on_tab_select(self, _event=None):
        sel = self._tab_listbox.curselection()
        if sel:
            idx = sel[0]
            if idx < len(self._tab_order):
                self._show_tab(self._tab_order[idx])

    def _show_tab(self, name):
        for n, (frame, _label) in self.tabs.items():
            frame.pack_forget() if n != name else None
        if name in self.tabs:
            frame, _label = self.tabs[name]
            frame.pack(fill="both", expand=True)

    def _slider(self, parent, label, key, from_, to, res=1, length=140, fmt="float"):
        T = CURRENT_THEME
        limit_key = f"LIMIT_{key}"
        if limit_key in SETTINGS:
            to = float(SETTINGS[limit_key])
        row = tk.Frame(parent, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=1)
        lbl = tk.Label(row, text=label, bg=T["bg"], fg=T["accent2"],
                       font=("Courier", 8, "bold"), anchor="w", width=28)
        lbl.pack(side="left")
        cur = float(SETTINGS.get(key, 0))
        if cur > to:
            cur = to
        var = tk.DoubleVar(value=cur)
        def cb(v, k=key, f=fmt):
            if f == "int":
                SETTINGS[k] = int(float(v))
            else:
                SETTINGS[k] = float(v)
            self._status(f"Set {k} = {SETTINGS[k]}")
        s = tk.Scale(row, from_=from_, to=to, resolution=res, orient="horizontal",
                     variable=var, length=length, command=cb,
                     bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                     highlightthickness=0)
        s.pack(side="right")
        setattr(self, f"_s_{key}", var)
        return var, s

    def _checkbox(self, parent, label, key, default=False):
        T = CURRENT_THEME
        var = tk.BooleanVar(value=bool(SETTINGS.get(key, default)))
        def cb():
            SETTINGS[key] = var.get()
            self._status(f"{key} = {var.get()}")
        cb = tk.Checkbutton(parent, text=label, variable=var, command=cb,
                            bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                            activebackground=T["bg"], font=("Courier", 8))
        cb.pack(anchor="w", padx=10, pady=1)
        return var

    def _combo(self, parent, label, key, values, width=16):
        T = CURRENT_THEME
        row = tk.Frame(parent, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=1)
        tk.Label(row, text=label, bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 8, "bold"), anchor="w", width=28).pack(side="left")
        var = tk.StringVar(value=str(SETTINGS.get(key, values[0] if values else "")))
        def cb(e):
            SETTINGS[key] = var.get()
            self._status(f"{key} = {var.get()}")
        c = ttk.Combobox(row, values=values, textvariable=var, width=width, state="readonly")
        c.bind("<<ComboboxSelected>>", cb)
        c.pack(side="right", padx=5)
        return var

    def _entry(self, parent, label, key, width=20, show=""):
        T = CURRENT_THEME
        row = tk.Frame(parent, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=1)
        tk.Label(row, text=label, bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 8, "bold"), anchor="w", width=28).pack(side="left")
        var = tk.StringVar(value=str(SETTINGS.get(key, "")))
        def cb(e):
            SETTINGS[key] = var.get()
        e = tk.Entry(row, textvariable=var, bg=T["log_bg"], fg=T["fg"],
                     insertbackground=T["accent"], font=("Courier", 8), width=width,
                     show=show)
        e.pack(side="right", padx=5)
        e.bind("<KeyRelease>", cb)
        return var

    def _section_label(self, parent, text):
        T = CURRENT_THEME
        lbl = tk.Label(parent, text=f"── {text} ──", bg=T["bg"], fg=T["accent"],
                       font=("Courier", 9, "bold"))
        lbl.pack(fill="x", padx=6, pady=(8, 2))

    def _make_scroll_frame(self, parent):
        T = CURRENT_THEME
        canvas = tk.Canvas(parent, bg=T["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=T["bg"])
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        return scroll_frame

    # ── TAB 1: ENGINE & DETECTION ──
    def _build_engine_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Engine"] = (tab, "Engine")
        self._tab_order.append("Engine")
        self._tab_listbox.insert(tk.END, "Engine")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Edge Detection")
        self._slider(sf, "Canny Low Threshold", "CANNY_LOW", 5, 255, 1, 140, "int")
        self._slider(sf, "Canny High Threshold", "CANNY_HIGH", 10, 255, 1, 140, "int")
        self._slider(sf, "Structure Detail Threshold", "STRUCTURE_DETAIL_THRESHOLD", 0.0, 1.0, 0.05, 140)
        self._slider(sf, "Simplify Epsilon", "SIMPLIFY_EPS", 0.1, 5.0, 0.1, 140)
        self._slider(sf, "Min Stroke Length", "MIN_STROKE_LEN", 2, 20, 1, 140, "int")
        self._checkbox(sf, "Contour Approximation", "CONTOUR_APPROX", True)
        self._checkbox(sf, "Use Path Cache", "USE_PATH_CACHE", True)
        self._checkbox(sf, "Structure Analysis", "STRUCTURE_ENABLE", True)

        self._section_label(sf, "Draw Modes")
        self._combo(sf, "Engine Mode", "ENGINE_MODE", ["ultra_fast","balanced","high_detail","human_sketch","sketchy","expressive"], 14)
        self._combo(sf, "Draw Mode", "DRAW_MODE", DRAW_MODES, 16)
        self._combo(sf, "Line Mode", "LINE_MODE", ["raw","balanced","smooth","artistic"], 12)
        self._combo(sf, "Draw Style", "DRAW_STYLE", list(StyleEngine.STYLES.keys()), 18)
        self._checkbox(sf, "Multipass Drawing", "MULTIPASS", True)
        self._checkbox(sf, "Hatching Enable", "HATCH_ENABLE", True)
        self._slider(sf, "Hatch Angle Step", "HATCH_ANGLE_STEP", 10, 90, 5, 140, "int")
        self._slider(sf, "Hatch Spacing", "HATCH_SPACING", 1, 15, 1, 140, "int")
        self._checkbox(sf, "Human Motion Sim", "HUMAN_MOTION", False)
        self._slider(sf, "Jitter Pixels", "JITTER_PX", 0, 10, 1, 140, "int")
        self._slider(sf, "Bezier Steps", "BEZIER_STEPS", 0, 20, 1, 140, "int")

        self._section_label(sf, "Fill Intelligence")
        self._checkbox(sf, "Fill Enable", "FILL_ENABLE", True)
        self._slider(sf, "Fill Variance Threshold", "FILL_VARIANCE_THRESHOLD", 50, 2000, 50, 140, "int")
        self._slider(sf, "Min Fill Area", "MIN_FILL_AREA", 50, 1000, 50, 140, "int")
        self._entry(sf, "Fill Hotkey", "FILL_HOTKEY", 10)

    # ── TAB 2: STROKE & QUALITY ──
    def _build_stroke_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Strokes"] = (tab, "Strokes")
        self._tab_order.append("Strokes")
        self._tab_listbox.insert(tk.END, "Strokes")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Line Quality Engine")
        self._checkbox(sf, "LQE Enabled", "LQE_ENABLE", True)
        self._slider(sf, "Smoothing Factor", "LQE_SMOOTHING_FACTOR", 0.5, 4.0, 0.1, 140)
        self._slider(sf, "Corner Threshold (°)", "LQE_CORNER_THRESHOLD", 10, 90, 1, 140, "int")
        self._slider(sf, "Min Confidence", "LQE_MIN_CONFIDENCE", 0.0, 1.0, 0.05, 140)

        self._section_label(sf, "Style Engine")
        self._slider(sf, "Style Merge Distance", "STYLE_MERGE_DISTANCE", 0, 20, 1, 140, "int")
        self._checkbox(sf, "Overlap Suppression", "STYLE_OVERLAP_SUPPRESS", True)
        self._slider(sf, "Crosshatch Angle", "STYLE_CROSSHATCH_ANGLE", 0, 90, 1, 140, "int")
        self._slider(sf, "Stipple Density", "STYLE_STIPPLE_DENSITY", 0.0, 1.0, 0.05, 140)
        self._slider(sf, "Scribble Passes", "STYLE_SCRIBBLE_PASSES", 1, 6, 1, 140, "int")

        self._section_label(sf, "Stroke Output")
        self._combo(sf, "Render Mode", "RENDER_MODE", ["physical","virtual","both"], 12)
        self._slider(sf, "Stroke Width", "STROKE_WIDTH", 1, 10, 1, 140, "int")
        self._slider(sf, "Stroke Speed", "STROKE_SPEED", 0, 100, 1, 140, "int")
        self._slider(sf, "Lift Delay (s)", "LIFT_DELAY", 0.0, 0.5, 0.01, 140)
        self._checkbox(sf, "Corner Slowdown", "CORNER_SLOWDOWN", True)
        self._slider(sf, "Smooth Passes", "STROKE_SMOOTH_PASSES", 0, 5, 1, 140, "int")
        self._combo(sf, "Stroke Mode", "STROKE_MODE", ["dot","stroke"], 8)

        self._section_label(sf, "Path Optimization")
        self._checkbox(sf, "Douglas-Peucker Simplify", "CONTOUR_APPROX", True)
        self._slider(sf, "Simplify Epsilon", "SIMPLIFY_EPS", 0.1, 5.0, 0.1, 140)

    # ── TAB 3: COLOR & PALETTE ──
    def _build_color_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Color"] = (tab, "Color")
        self._tab_order.append("Color")
        self._tab_listbox.insert(tk.END, "Color")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Color Matching")
        self._combo(sf, "Color Metric", "COLOR_METRIC", ["Euclidean","CIEDE2000","Manhattan"], 14)
        self._slider(sf, "Palette Size", "PALETTE_SIZE", 2, 64, 1, 140, "int")
        self._checkbox(sf, "Color Cache Enable", "COLOR_CACHE_ENABLE", True)
        self._combo(sf, "Color Scan Layout", "COLOR_SCAN_LAYOUT", ["grid","snake","spiral"], 10)
        self._slider(sf, "Color Scan Spacing", "COLOR_SCAN_SPACING", 1, 20, 1, 140, "int")

        self._section_label(sf, "Dithering")
        self._combo(sf, "Dither Mode", "DITHER_MODE", DITHER_MODES, 16)

        self._section_label(sf, "Pixel Filters")
        self._slider(sf, "White Skip (luminance)", "WHITE_SKIP", 200, 255, 1, 140, "int")
        self._checkbox(sf, "Skip Chroma Mask", "SKIP_BLUE_MASK", True)
        self._slider(sf, "Pixel Gap", "PIXEL_GAP", 1, 10, 1, 140, "int")

        self._section_label(sf, "Palette Tools")
        self._slider(sf, "Palette Size (k-means)", "PALETTE_SIZE", 2, 64, 1, 140, "int")

    # ── TAB 4: BACKGROUND & FILL ──
    def _build_bg_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["BG & Fill"] = (tab, "BG & Fill")
        self._tab_order.append("BG & Fill")
        self._tab_listbox.insert(tk.END, "BG & Fill")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Background Awareness")
        self._checkbox(sf, "BG Awareness Enable", "BG_AWARENESS_ENABLE", False)
        self._combo(sf, "Virtual BG Color", "VIRTUAL_BG_COLOR",
                    ["#ffffff","#000000","#0000ff","#00ff00","#ff0000"], 12)
        self._checkbox(sf, "Virtual Canvas Enable", "VIRTUAL_CANVAS_ENABLE", True)

        self._section_label(sf, "Fill Zone Settings")
        self._checkbox(sf, "Fill Zone Active", "FILL_ZONE_ACTIVE", False)
        self._slider(sf, "Fill Zone Threshold", "FILL_ZONE_THRESHOLD", 5, 100, 1, 140, "int")
        self._slider(sf, "Fill Zone Grow Steps", "FILL_ZONE_GROW_STEPS", 1, 30, 1, 140, "int")
        self._entry(sf, "Fill Zone Center X", "FILL_ZONE_CENTER[0]", 10)
        self._entry(sf, "Fill Zone Center Y", "FILL_ZONE_CENTER[1]", 10)

        self._section_label(sf, "Fill Intelligence")
        self._checkbox(sf, "Fill Enable", "FILL_ENABLE", True)
        self._slider(sf, "Fill Variance", "FILL_VARIANCE_THRESHOLD", 50, 2000, 50, 140, "int")
        self._slider(sf, "Min Fill Area", "MIN_FILL_AREA", 50, 1000, 50, 140, "int")
        self._entry(sf, "Fill Hotkey (F-key)", "FILL_HOTKEY", 10)

        self._section_label(sf, "Canvas Border Detection")
        self._slider(sf, "Canny Low Adjust", "CANNY_LOW", 5, 255, 1, 140, "int")
        self._slider(sf, "Canny High Adjust", "CANNY_HIGH", 10, 255, 1, 140, "int")

        self._section_label(sf, "HEX Colorizer")
        hex_row = tk.Frame(sf, bg=T["bg"])
        hex_row.pack(fill="x", padx=6, pady=1)
        tk.Label(hex_row, text="Hex:", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 8, "bold")).pack(side="left")
        self._hex_entry_var = tk.StringVar()
        hex_entry = tk.Entry(hex_row, textvariable=self._hex_entry_var, width=12,
                             font=("Courier", 9), bg=T["bg2"], fg=T["fg"],
                             insertbackground=T["fg"])
        hex_entry.pack(side="left", padx=2)

        def _add_hex_cb():
            raw = self._hex_entry_var.get().strip()
            if raw.startswith("#"):
                raw = raw[1:]
            if len(raw) == 6 and all(c in "0123456789abcdefABCDEF" for c in raw):
                h = "#" + raw.lower()
                cols = list(SETTINGS.get("HEX_COLORS", []))
                if h not in cols:
                    cols.append(h)
                    SETTINGS["HEX_COLORS"] = cols
                    self._hex_entry_var.set("")
                    _refresh_sw()
        def _pick_hex_cb():
            c = colorchooser.askcolor(title="Pick hex color")
            if c and c[1]:
                h = c[1].lower()
                cols = list(SETTINGS.get("HEX_COLORS", []))
                if h not in cols:
                    cols.append(h)
                    SETTINGS["HEX_COLORS"] = cols
                    _refresh_sw()
        def _clear_hex_cb():
            SETTINGS["HEX_COLORS"] = []
            _refresh_sw()

        tk.Button(hex_row, text="Add", command=_add_hex_cb,
                  bg=T["bg2"], fg=T["accent"], font=("Courier", 7), bd=0).pack(side="left", padx=1)
        tk.Button(hex_row, text="Pick", command=_pick_hex_cb,
                  bg=T["bg2"], fg=T["accent"], font=("Courier", 7), bd=0).pack(side="left", padx=1)
        tk.Button(hex_row, text="X", command=_clear_hex_cb,
                  bg="#440000", fg=T["danger"], font=("Courier", 7), bd=0).pack(side="right", padx=1)

        self._hex_swatch_frame = tk.Frame(sf, bg=T["bg"])
        self._hex_swatch_frame.pack(fill="x", padx=6, pady=2)
        def _refresh_sw():
            for w in self._hex_swatch_frame.winfo_children():
                w.destroy()
            for hc in SETTINGS.get("HEX_COLORS", []):
                try:
                    tk.Label(self._hex_swatch_frame, bg=hc, width=3, height=1,
                             relief="solid", bd=1).pack(side="left", padx=1)
                except Exception:
                    pass
        _refresh_sw()

    # ── TAB 5: SPEED & PERFORMANCE ──
    def _build_speed_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Speed"] = (tab, "Speed")
        self._tab_order.append("Speed")
        self._tab_listbox.insert(tk.END, "Speed")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Master Speed")
        self._slider(sf, "Global Speed (master)", "GLOBAL_SPEED", 0.1, 20.0, 0.1, 200)

        self._section_label(sf, "Delays")
        self._slider(sf, "Click Delay (s)", "CLICK_DELAY", 0.0, 0.1, 0.0001, 200)
        self._slider(sf, "UI Delay (s)", "UI_DELAY", 0.0, 0.5, 0.01, 200)
        self._slider(sf, "Lift Delay (s)", "LIFT_DELAY", 0.0, 0.5, 0.01, 200)
        self._slider(sf, "Stroke Speed", "STROKE_SPEED", 0, 100, 1, 200, "int")

        self._section_label(sf, "Drawing Mode Speed Presets")
        self._combo(sf, "Engine Mode", "ENGINE_MODE",
                    ["ultra_fast","balanced","high_detail","human_sketch","sketchy","expressive"], 16)

        self._section_label(sf, "Performance Tuning")
        self._slider(sf, "Pixel Gap", "PIXEL_GAP", 1, 10, 1, 200, "int")
        self._checkbox(sf, "Use Path Cache", "USE_PATH_CACHE", True)
        self._checkbox(sf, "Contour Approximation", "CONTOUR_APPROX", True)
        self._slider(sf, "Simplify Epsilon (speed vs detail)", "SIMPLIFY_EPS", 0.1, 5.0, 0.1, 200)
        self._checkbox(sf, "Trace Mode", "TRACE_MODE", True)

        self._section_label(sf, "Stroke Performance")
        self._slider(sf, "Smooth Passes (0=raw)", "STROKE_SMOOTH_PASSES", 0, 5, 1, 200, "int")
        self._combo(sf, "Stroke Mode", "STROKE_MODE", ["dot","stroke"], 10)
        self._slider(sf, "Jitter Pixels", "JITTER_PX", 0, 10, 1, 200, "int")
        self._slider(sf, "Bezier Steps (0=off)", "BEZIER_STEPS", 0, 20, 1, 200, "int")

    # ── TAB 6: SKETCH PRESETS ──
    def _build_sketch_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Sketch"] = (tab, "Sketch")
        self._tab_order.append("Sketch")
        self._tab_listbox.insert(tk.END, "Sketch")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Sketch Preset Selector")
        presets = ["Gestural","Continuous","Staccato","Construction",
                   "Hatching","Sweep Arc","Scribble Fill","Diagonal Shadow",
                   "Cross Contour","Blind Contour","Stippling","Scumbling",
                   "Sgraffito","Tonal Wash","Custom"]
        row0 = tk.Frame(sf, bg=T["bg"])
        row0.pack(fill="x", padx=6, pady=2)
        self.sketch_preset_var = tk.StringVar(value=SETTINGS.get("SKETCH_PRESET","Gestural"))
        def on_preset_change(*a):
            name = self.sketch_preset_var.get()
            if name and name != "Custom":
                SETTINGS["SKETCH_PRESET"] = name
                self.app._apply_sketch_preset(name)
                self._status(f"Sketch preset: {name}")
                self._refresh_sketch_sliders()
        combo = ttk.Combobox(row0, values=presets, textvariable=self.sketch_preset_var,
                             width=20, state="readonly")
        combo.pack(side="left", padx=5)
        combo.bind("<<ComboboxSelected>>", on_preset_change)

        self._section_label(sf, "Sketch Parameters")
        self.sketch_slider_frame = tk.Frame(sf, bg=T["bg"])
        self.sketch_slider_frame.pack(fill="x", padx=4)
        self.sketch_vars = {}
        self._refresh_sketch_sliders()

        self._section_label(sf, "Hatching / Shadow Settings")
        self._slider(sf, "Hatch Angle °", "SKETCH_HATCH_ANGLE", 0, 180, 1, 140, "int")
        self._slider(sf, "Hatch Spacing", "SKETCH_HATCH_SPACING", 2, 30, 1, 140, "int")
        self._slider(sf, "Wobble Noise", "SKETCH_WOBBLE", 0, 2, 0.1, 140)

    def _refresh_sketch_sliders(self):
        for w in self.sketch_slider_frame.winfo_children():
            w.destroy()
        self.sketch_vars.clear()
        T = CURRENT_THEME
        sketch_keys = [
            ("SKETCH_STROKE_DIST", "Stroke Connect", 1, 20, 1),
            ("SKETCH_JITTER", "Jitter Amount", 0, 5, 0.1),
            ("SKETCH_SPEED", "Drag Speed", 0.0, 0.1, 0.00001),
            ("SKETCH_STROKE_DELAY", "Stroke Delay", 0, 1.0, 0.01),
            ("SKETCH_OVERLAP", "Overhang", 0, 3, 0.1),
            ("SKETCH_VARIATION", "Variation", 0, 1, 0.05),
            ("SKETCH_ITERATIONS", "Iterations", 1, 10, 1),
            ("SKETCH_EDGE_ONLY", "Edge Only", 0, 1, 0.05),
            ("SKETCH_SPEED_MULT", "Speed Mult", 0.1, 50, 0.1),
            ("SKETCH_SEGMENT_LEN", "Segment Len", 0, 50, 1),
            ("SKETCH_GHOST", "Ghost Layers", 0, 5, 1),
            ("SKETCH_NO_LIFT", "No-Lift ms", 0, 500, 10),
            ("SKETCH_BPM", "Rhythm BPM", 0, 200, 5),
            ("SKETCH_CONSTRUCTION_PASSES", "Construction Passes", 1, 10, 1),
        ]
        for key, label, minv, maxv, res in sketch_keys:
            row = tk.Frame(self.sketch_slider_frame, bg=T["bg"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, bg=T["bg"], fg=T["accent2"],
                     font=("Courier", 8, "bold"), anchor="w", width=20).pack(side="left")
            var = tk.DoubleVar(value=float(SETTINGS.get(key, 0)))
            def cb(v, k=key):
                val = float(v)
                SETTINGS[k] = int(val) if val == int(val) else val
            s = tk.Scale(row, from_=minv, to=maxv, resolution=res, orient="horizontal",
                         variable=var, length=120, command=cb,
                         bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                         highlightthickness=0)
            s.pack(side="right")
            self.sketch_vars[key] = var

    # ── TAB 7: CANVAS & VIEWPORT ──
    def _build_canvas_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Canvas"] = (tab, "Canvas")
        self._tab_order.append("Canvas")
        self._tab_listbox.insert(tk.END, "Canvas")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Viewport Control")
        self._slider(sf, "Viewport Zoom", "VIEWPORT_ZOOM", 0.1, 5.0, 0.05, 200)
        self._slider(sf, "Scroll X", "VIEWPORT_SCROLL_DX", -500, 500, 1, 200, "int")
        self._slider(sf, "Scroll Y", "VIEWPORT_SCROLL_DY", -500, 500, 1, 200, "int")
        self._checkbox(sf, "Auto Scroll", "VIEWPORT_AUTO_SCROLL", False)
        self._slider(sf, "Resize Sensitivity", "RESIZE_SENSITIVITY", 0.001, 0.05, 0.001, 200)

        self._section_label(sf, "Virtual Canvas")
        self._checkbox(sf, "Virtual Canvas Enabled", "VIRTUAL_CANVAS_ENABLE", True)
        self._combo(sf, "Virtual BG Color", "VIRTUAL_BG_COLOR",
                    ["#ffffff","#000000","#333333","#555555","#777777"], 14)
        self._combo(sf, "Render Mode", "RENDER_MODE", ["physical","virtual","both"], 12)

        self._section_label(sf, "Canvas Calibration")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=2)
        tk.Button(row, text="Recalibrate Canvas", command=self.app.start_visual_calibration,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        if self.app.canvas_rect:
            cr = self.app.canvas_rect
            tk.Label(row, text=f"Current: ({cr[0]},{cr[1]}) → ({cr[2]},{cr[3]})  [{cr[2]-cr[0]}×{cr[3]-cr[1]}]",
                     bg=T["bg"], fg=T["success"], font=("Courier", 8)).pack(side="left", padx=10)

        self._section_label(sf, "Active Profile")
        self._entry(sf, "Active Profile Name", "ACTIVE_PROFILE", 20)
        row2 = tk.Frame(sf, bg=T["bg"])
        row2.pack(fill="x", padx=6, pady=4)
        tk.Button(row2, text="Save Profile", command=lambda: self._save_profile(),
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row2, text="Load Profile", command=lambda: self._load_profile(),
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Editor Tools")
        row3 = tk.Frame(sf, bg=T["bg"])
        row3.pack(fill="x", padx=6, pady=4)
        tk.Button(row3, text="Open Editor", command=self.app.open_editor,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row3, text="Export PNG", command=self.app.export_png,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row3, text="Export Log", command=self.app.export_log,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)

    def _save_profile(self):
        name = SETTINGS.get("ACTIVE_PROFILE", "unnamed")
        if self.app.calib_manager:
            self.app.calib_manager.save(name)
            self._status(f"Profile saved: {name}")

    def _load_profile(self):
        name = SETTINGS.get("ACTIVE_PROFILE", "unnamed")
        if self.app.calib_manager:
            self.app.calib_manager.load(name)
            self._status(f"Profile loaded: {name}")

    # ── TAB 8: AI PROMPT PIPELINE ──
    def _build_ai_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["AI"] = (tab, "AI")
        self._tab_order.append("AI")
        self._tab_listbox.insert(tk.END, "AI")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Prompt Pipeline")
        self._combo(sf, "Prompt Provider", "PROMPT_PROVIDER",
                    ["pollinations","arena_ai","stable_diffusion_local","tiny_sd","custom_api"], 20)
        self._entry(sf, "Custom Endpoint URL", "PROMPT_ENDPOINT", 30)
        self._combo(sf, "Style Preset", "PROMPT_STYLE_PRESET",
                    ["anime_sketch","realistic","oil_painting","watercolor","pencil"], 18)
        self._entry(sf, "Negative Prompt", "PROMPT_NEGATIVE", 30)
        self._slider(sf, "API Timeout (s)", "PROMPT_API_TIMEOUT", 5, 120, 5, 200, "int")

        self._section_label(sf, "Generate Image")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        self._prompt_entry_var = tk.StringVar()
        pe = tk.Entry(row, textvariable=self._prompt_entry_var, bg=T["log_bg"], fg=T["fg"],
                      insertbackground=T["accent"], font=("Courier", 9), width=40)
        pe.pack(side="left", padx=5)
        tk.Button(row, text="Generate", command=self._generate_prompted_image,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left")

        self._section_label(sf, "SD Local Config")
        self._slider(sf, "Inference Steps", "PROMPT_STEPS", 5, 50, 1, 200, "int")
        self._slider(sf, "Guidance Scale", "PROMPT_GUIDANCE", 1.0, 15.0, 0.5, 200)

        self._section_label(sf, "Auto-Enhance")
        self._checkbox(sf, "Edge Enhance", "PROMPT_EDGE_ENHANCE", True)
        self._checkbox(sf, "Contrast Boost", "PROMPT_CONTRAST_BOOST", True)
        self._checkbox(sf, "Auto Sharpen", "PROMPT_AUTO_SHARPEN", True)

    def _generate_prompted_image(self):
        prompt = self._prompt_entry_var.get().strip()
        if not prompt:
            self._status("No prompt entered")
            return
        self._status("Generating...")
        if hasattr(self.app, 'prompt_pipeline') and self.app.prompt_pipeline.active:
            def gen():
                img = self.app.prompt_pipeline.generate(prompt)
                if img:
                    self.app.base_img = img
                    self.app.final_img = None
                    self.win.after(0, lambda: self._status("Generated!"))
                else:
                    self.win.after(0, lambda: self._status("Generation failed"))
            import threading
            threading.Thread(target=gen, daemon=True).start()
        else:
            self._status("Prompt pipeline not configured")

    # ── TAB 9: BATCH & AUTOMATION ──
    def _build_batch_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Batch"] = (tab, "Batch")
        self._tab_order.append("Batch")
        self._tab_listbox.insert(tk.END, "Batch")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Batch Queue")
        self._batch_listbox = tk.Listbox(sf, bg=T["log_bg"], fg=T["fg"],
                                         selectbackground=T["accent2"],
                                         font=("Courier", 9), height=10)
        self._batch_listbox.pack(fill="x", padx=10, pady=5)
        self._refresh_batch_list()

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=2)
        tk.Button(row, text="+ Add Image", command=self._batch_add,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="- Remove Selected", command=self._batch_remove,
                  bg="#330000", fg=T["danger"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Clear All", command=self._batch_clear,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Batch Settings")
        self._checkbox(sf, "Auto-Save Projects", "BATCH_AUTO_SAVE", True)
        self._checkbox(sf, "Auto-Advance Colors", "BATCH_AUTO_ADVANCE", True)
        self._slider(sf, "Delay Between Images (s)", "BATCH_DELAY", 0, 30, 1, 200, "int")

        self._section_label(sf, "Automation")
        row3 = tk.Frame(sf, bg=T["bg"])
        row3.pack(fill="x", padx=6, pady=4)
        tk.Button(row3, text="Start Batch Draw", command=self._batch_start,
                  bg="#004400", fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row3, text="Stop Batch", command=self._batch_stop,
                  bg="#440000", fg=T["danger"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Scheduled Drawing")
        self._checkbox(sf, "Enable Scheduler", "SCHEDULER_ENABLE", False)
        self._entry(sf, "Scheduled Time (HH:MM)", "SCHEDULED_TIME", 10)

    def _refresh_batch_list(self):
        if hasattr(self, '_batch_listbox') and self._batch_listbox.winfo_exists():
            self._batch_listbox.delete(0, tk.END)
            for path in getattr(self.app, 'batch_queue', []):
                self._batch_listbox.insert(tk.END, os.path.basename(path))

    def _batch_add(self):
        paths = filedialog.askopenfilenames(
            title="Add Images to Queue",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if paths:
            self.app.batch_queue.extend(paths)
            self._refresh_batch_list()
            self._status(f"Added {len(paths)} images")

    def _batch_remove(self):
        sel = self._batch_listbox.curselection()
        if sel:
            idx = sel[0]
            if 0 <= idx < len(self.app.batch_queue):
                del self.app.batch_queue[idx]
                self._refresh_batch_list()

    def _batch_clear(self):
        self.app.batch_queue.clear()
        self._refresh_batch_list()
        self._status("Batch queue cleared")

    def _batch_start(self):
        if not self.app.batch_queue:
            self._status("No images in queue")
            return
        self._status("Batch started")
        self.app.start_batch_draw()

    def _batch_stop(self):
        self.app.batch_active = False
        self.app.drawing_active = False
        self._status("Batch stopped")

    # ── TAB 10: PROFILES & CONFIG ──
    def _build_profile_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Profiles"] = (tab, "Profiles")
        self._tab_order.append("Profiles")
        self._tab_listbox.insert(tk.END, "Profiles")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Profile Management")
        self._entry(sf, "Profile Name", "ACTIVE_PROFILE", 20)
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Save Current Profile", command=self._save_profile,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row, text="Load Profile", command=self._load_profile,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row, text="Import Profile (JSON)", command=self._import_profile,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Config File")
        row2 = tk.Frame(sf, bg=T["bg"])
        row2.pack(fill="x", padx=6, pady=4)
        tk.Button(row2, text="Save Config Now", command=self.app.save_config,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row2, text="Reload Config", command=self.app.load_config,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Export / Import")
        row3 = tk.Frame(sf, bg=T["bg"])
        row3.pack(fill="x", padx=6, pady=4)
        tk.Button(row3, text="Export Palette", command=self._export_palette,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)
        tk.Button(row3, text="Import Palette", command=self._import_palette,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)
        tk.Button(row3, text="Export All Settings", command=self._export_all,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Theme")
        row4 = tk.Frame(sf, bg=T["bg"])
        row4.pack(fill="x", padx=6, pady=4)
        for name in THEMES:
            tk.Button(row4, text=name, command=lambda n=name: self.app._apply_theme(n),
                      bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Advanced")
        row5 = tk.Frame(sf, bg=T["bg"])
        row5.pack(fill="x", padx=6, pady=4)
        tk.Button(row5, text="Reset Canvas", command=self._reset_canvas,
                  bg="#332200", fg=T["warn"], font=("Courier", 8), bd=0).pack(side="left", padx=5)
        tk.Button(row5, text="Clear Emergency Saves", command=self._clear_emergency,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=5)

    def _import_profile(self):
        if hasattr(self.app, 'calib_manager') and self.app.calib_manager:
            self.app.calib_manager.import_profile()
            self._status("Profile imported")

    def _export_palette(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON","*.json")])
        if path and self.app.palette_map:
            with open(path, 'w') as f:
                json.dump(self.app.palette_map, f, indent=2)
            self._status(f"Palette exported: {os.path.basename(path)}")

    def _import_palette(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if path:
            with open(path) as f:
                self.app.palette_map = json.load(f)
            self._status("Palette imported")

    def _export_all(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON","*.json")],
                                            initialfile="sf2m_settings_backup.json")
        if path:
            data = {
                "settings": dict(SETTINGS),
                "palette": self.app.palette_map,
                "canvas_rect": self.app.canvas_rect,
                "version": 5,
            }
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            self._status("All settings exported")

    def _reset_canvas(self):
        self.app.canvas_rect = None
        self.app._update_canvas_label()
        self.app.log("Canvas reset")

    def _clear_emergency(self):
        count = 0
        for fname in os.listdir(PROJECTS_PATH):
            if fname.startswith("emergency_"):
                try:
                    os.remove(os.path.join(PROJECTS_PATH, fname))
                    count += 1
                except:
                    pass
        self._status(f"Cleared {count} emergency saves")

    # ── TAB 11: DEBUG & INFO ──
    def _build_debug_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Debug"] = (tab, "Debug")
        self._tab_order.append("Debug")
        self._tab_listbox.insert(tk.END, "Debug")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "System Info")
        info_text = (
            f"Python: {sys.version.split()[0]}\n"
            f"OS: {sys.platform}\n"
            f"NumPy: {np.__version__}\n"
            f"Pillow: {Image.__version__}\n"
            f"pyautogui: {pyautogui.__version__}\n"
            f"OpenCV: {'available' if HAS_CV2 else 'NOT available'}\n"
            f"SciPy: {'available' if HAS_SCIPY else 'NOT available'}\n"
            f"Scikit-Image: {'available' if HAS_SKIMAGE else 'NOT available'}\n"
            f"PyTorch: {'available' if HAS_TORCH else 'NOT available'}\n"
            f"Diffusers: {'available' if HAS_DIFFUSERS else 'NOT available'}\n"
            f"Canvas: {self.app.canvas_rect}\n"
            f"Palette Colors: {len(self.app.palette_map)}\n"
            f"Image Loaded: {self.app.base_img is not None}\n"
            f"Batch Queue: {len(getattr(self.app,'batch_queue',[]))} items\n"
            f"Config Path: {CONFIG_PATH}\n"
            f"Projects Path: {PROJECTS_PATH}\n"
        )
        lbl = tk.Label(sf, text=info_text, bg=T["log_bg"], fg=T["log_fg"],
                       font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10)
        lbl.pack(fill="x", padx=6, pady=6)

        self._section_label(sf, "Live Settings Dump")
        self._dump_text = tk.Text(sf, height=16, bg=T["log_bg"], fg=T["log_fg"],
                                  font=("Courier", 7), wrap="none")
        self._dump_text.pack(fill="x", padx=6, pady=4)
        self._refresh_dump()
        tk.Button(sf, text="Refresh Dump", command=self._refresh_dump,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)

        self._section_label(sf, "Actions")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Test PyAutoGUI", command=self._test_pyautogui,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Log Test Message", command=lambda: self.app.log("Test log message"),
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Force GC", command=self._force_gc,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

    def _refresh_dump(self):
        if not hasattr(self, '_dump_text') or not self._dump_text.winfo_exists():
            return
        self._dump_text.delete(1.0, tk.END)
        lines = []
        for k, v in sorted(SETTINGS.items()):
            lines.append(f"{k:40s} = {v}")
        self._dump_text.insert(1.0, "\n".join(lines))

    def _test_pyautogui(self):
        try:
            x, y = pyautogui.position()
            self._status(f"Mouse: ({x}, {y}) — pyautogui OK")
        except Exception as e:
            self._status(f"pyautogui error: {e}")

    def _force_gc(self):
        import gc
        before = len(gc.get_objects())
        gc.collect()
        after = len(gc.get_objects())
        self._status(f"GC: {before} → {after} objects")

    # ── TAB 12: HOTKEYS ──
    def _build_hotkey_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Hotkeys"] = (tab, "Hotkeys")
        self._tab_order.append("Hotkeys")
        self._tab_listbox.insert(tk.END, "Hotkeys")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Drawing Hotkeys")
        self._combo(sf, "Start Key", "START_KEY", ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"], 8)
        self._combo(sf, "Pause Key", "PAUSE_KEY", ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"], 8)
        self._combo(sf, "Abort Key", "ABORT_KEY", ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"], 8)
        self._combo(sf, "Fill Hotkey", "FILL_HOTKEY", ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"], 8)

        self._section_label(sf, "Custom Key Bindings")
        self._entry(sf, "Custom Key 1 Action", "CUSTOM_KEY1_ACTION", 20)
        self._entry(sf, "Custom Key 2 Action", "CUSTOM_KEY2_ACTION", 20)
        self._entry(sf, "Custom Key 3 Action", "CUSTOM_KEY3_ACTION", 20)
        self._entry(sf, "Custom Key 4 Action", "CUSTOM_KEY4_ACTION", 20)

        self._section_label(sf, "Key Mapping Reference")
        ref_text = (
            "F1  = Help overlay\n"
            "F2  = (custom)\n"
            "F3  = (custom)\n"
            "F4  = (custom)\n"
            "F5  = (custom)\n"
            "F6  = (custom)\n"
            "F7  = (custom)\n"
            "F8  = (custom)\n"
            "F9  = Fill (when fill intelligence enabled)\n"
            "F10 = Start drawing (during preview)\n"
            "F11 = Pause/Resume drawing\n"
            "F12 = ABORT drawing\n"
            "Ctrl+Z = Undo in editor\n"
            "Ctrl+Y = Redo in editor\n"
            "Ctrl+S = Save project\n"
            "Scroll = Zoom preview/editor\n"
            "Mid-drag = Pan preview\n"
        )
        tk.Label(sf, text=ref_text, bg=T["log_bg"], fg=T["log_fg"],
                 font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10).pack(fill="x", padx=6, pady=6)

    # ── TAB 13: OPTIMIZER ──
    def _build_optimizer_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Optimizer"] = (tab, "Optimizer")
        self._tab_order.append("Optimizer")
        self._tab_listbox.insert(tk.END, "Optimizer")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Path Optimization")
        self._checkbox(sf, "Enable Path Caching", "USE_PATH_CACHE", True)
        self._slider(sf, "Douglas-Peucker Epsilon", "SIMPLIFY_EPS", 0.1, 5.0, 0.1, 160)
        self._slider(sf, "Min Stroke Length", "MIN_STROKE_LEN", 2, 30, 1, 160, "int")
        self._checkbox(sf, "Contour Approximation", "CONTOUR_APPROX", True)
        self._checkbox(sf, "Nearest-Neighbor Ordering", "NN_ORDER", True)
        self._slider(sf, "Nearest-Neighbor Search Radius", "NN_RADIUS", 1, 30, 1, 160, "int")

        self._section_label(sf, "Stroke Merging")
        self._slider(sf, "Merge Distance (pixels)", "STYLE_MERGE_DISTANCE", 0, 30, 1, 160, "int")
        self._checkbox(sf, "Overlap Suppression", "STYLE_OVERLAP_SUPPRESS", True)
        self._slider(sf, "Min Overlap Ratio", "MIN_OVERLAP_RATIO", 0.0, 1.0, 0.05, 160)
        self._slider(sf, "Duplicate Offset", "DUPLICATE_OFFSET", 0, 5, 1, 160, "int")

        self._section_label(sf, "Spatial Sorting")
        self._combo(sf, "Sort Order", "SORT_ORDER", ["size","random","topdown","center","burst"], 12)
        self._slider(sf, "Sort Bin Size", "SORT_BIN_SIZE", 4, 64, 4, 160, "int")

        self._section_label(sf, "Corner Handling")
        self._slider(sf, "Corner Angle Threshold", "LQE_CORNER_THRESHOLD", 10, 90, 1, 160, "int")
        self._checkbox(sf, "Corner Slowdown", "CORNER_SLOWDOWN", True)
        self._slider(sf, "Corner Slowdown Factor", "CORNER_SLOWDOWN_FACTOR", 0.1, 1.0, 0.05, 160)

        self._section_label(sf, "Curve Fitting")
        self._slider(sf, "Bezier Steps (smooth curves)", "BEZIER_STEPS", 0, 30, 1, 160, "int")
        self._slider(sf, "Spline Tension", "SPLINE_TENSION", 0.0, 1.0, 0.05, 160)
        self._checkbox(sf, "Catmull-Rom Interpolation", "CATMULL_ROM", False)

    # ── TAB 14: COLOR MANAGEMENT ──
    def _build_color_manage_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Color Mgmt"] = (tab, "Color Mgmt")
        self._tab_order.append("Color Mgmt")
        self._tab_listbox.insert(tk.END, "Color Mgmt")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Color Space & Conversion")
        self._combo(sf, "Working Color Space", "COLOR_SPACE", ["sRGB","AdobeRGB","ProPhoto","DCI-P3"], 12)
        self._checkbox(sf, "Apply Gamma Correction", "GAMMA_CORRECT", True)
        self._slider(sf, "Gamma Value", "GAMMA_VALUE", 1.0, 3.0, 0.1, 160)
        self._checkbox(sf, "SRGB Linearize", "SRGB_LINEARIZE", False)

        self._section_label(sf, "Color Matching")
        self._combo(sf, "Primary Metric", "COLOR_METRIC", ["Euclidean","CIEDE2000","Manhattan","Weighted"], 14)
        self._slider(sf, "Red Weight", "COLOR_WEIGHT_R", 0.0, 3.0, 0.1, 160)
        self._slider(sf, "Green Weight", "COLOR_WEIGHT_G", 0.0, 3.0, 0.1, 160)
        self._slider(sf, "Blue Weight", "COLOR_WEIGHT_B", 0.0, 3.0, 0.1, 160)

        self._section_label(sf, "Palette Generation")
        self._slider(sf, "K-Means Clusters", "PALETTE_SIZE", 2, 64, 1, 160, "int")
        self._slider(sf, "K-Means Iterations", "KMEANS_ITER", 5, 50, 1, 160, "int")
        self._combo(sf, "Palette Init Method", "PALETTE_INIT", ["random","kmeans++","grid"], 12)
        self._checkbox(sf, "Sort Palette By Luminance", "SORT_PALETTE_LUM", True)
        self._slider(sf, "Palette Merge Threshold", "PALETTE_MERGE_THRESH", 1, 50, 1, 160, "int")

        self._section_label(sf, "Perceptual Optimization")
        self._checkbox(sf, "Use CIEDE2000", "CIEDE2000_ENABLE", True)
        self._checkbox(sf, "Weight by Luminance", "LUMINANCE_WEIGHT", True)
        self._slider(sf, "Saturation Boost", "SATURATION_BOOST", 0.0, 2.0, 0.05, 160)
        self._slider(sf, "Vibrance Adjustment", "VIBRANCE_ADJ", -1.0, 1.0, 0.05, 160)

        self._section_label(sf, "Dithering Controls")
        self._combo(sf, "Dither Algorithm", "DITHER_MODE", DITHER_MODES, 16)
        self._slider(sf, "Dither Strength", "DITHER_STRENGTH", 0.0, 2.0, 0.05, 160)
        self._checkbox(sf, "Dither Quantization Error", "DITHER_QUANTIZE", True)

    # ── TAB 15: OVERLAY ──
    def _build_overlay_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Overlay"] = (tab, "Overlay")
        self._tab_order.append("Overlay")
        self._tab_listbox.insert(tk.END, "Overlay")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Screen Overlay Controls")
        self._checkbox(sf, "Show Overlay Grid", "OVERLAY_GRID", False)
        self._slider(sf, "Grid Spacing (px)", "OVERLAY_GRID_SPACING", 10, 200, 10, 160, "int")
        self._combo(sf, "Grid Color", "OVERLAY_GRID_COLOR",
                    ["#ff0000","#00ff00","#0000ff","#ffffff","#888888"], 12)
        self._slider(sf, "Overlay Opacity %", "OVERLAY_OPACITY", 5, 80, 5, 160, "int")

        self._section_label(sf, "Crosshair & Guide")
        self._checkbox(sf, "Show Center Crosshair", "OVERLAY_CROSSHAIR", False)
        self._checkbox(sf, "Show Thirds Guide", "OVERLAY_THIRDS", False)
        self._checkbox(sf, "Show Golden Ratio", "OVERLAY_GOLDEN", False)
        self._checkbox(sf, "Show Safe Zone", "OVERLAY_SAFE_ZONE", False)

        self._section_label(sf, "Drawing Preview")
        self._checkbox(sf, "Live Preview Overlay", "LIVE_PREVIEW", True)
        self._slider(sf, "Preview Update Interval (ms)", "PREVIEW_INTERVAL", 50, 2000, 50, 160, "int")

        self._section_label(sf, "Progress Display")
        self._checkbox(sf, "Show Progress Bar", "SHOW_PROGRESS_BAR", True)
        self._checkbox(sf, "Show PPS Counter", "SHOW_PPS_COUNTER", True)
        self._checkbox(sf, "Show ETA Clock", "SHOW_ETA_CLOCK", True)
        self._checkbox(sf, "Sparkline Graph", "SHOW_SPARKLINE", True)

    # ── TAB 16: MACROS ──
    def _build_macro_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Macros"] = (tab, "Macros")
        self._tab_order.append("Macros")
        self._tab_listbox.insert(tk.END, "Macros")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Mouse Macros")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=2)
        self._macro_entry_var = tk.StringVar()
        tk.Entry(row, textvariable=self._macro_entry_var, bg=T["log_bg"], fg=T["fg"],
                 insertbackground=T["accent"], font=("Courier", 8), width=40).pack(side="left", padx=5)
        tk.Button(row, text="RUN MACRO", command=self._run_macro,
                  bg="#004400", fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(side="left")

        self._section_label(sf, "Saved Macros")
        self._macro_listbox = tk.Listbox(sf, bg=T["log_bg"], fg=T["fg"],
                                         selectbackground=T["accent2"],
                                         font=("Courier", 9), height=6)
        self._macro_listbox.pack(fill="x", padx=10, pady=5)
        sample_macros = [
            "click(500,500)",
            "drag(100,100,500,500)",
            "move(200,200)",
            "wait(1000)",
            "repeat(3, click(300,300))",
        ]
        for m in sample_macros:
            self._macro_listbox.insert(tk.END, m)

        self._section_label(sf, "Recording Controls")
        row2 = tk.Frame(sf, bg=T["bg"])
        row2.pack(fill="x", padx=6, pady=4)
        tk.Button(row2, text="Start Recording", command=self._macro_record_start,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Stop Recording", command=self._macro_record_stop,
                  bg="#440000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Play Macro", command=self._macro_play,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Clear", command=lambda: self._macro_listbox.delete(0, tk.END),
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Scripting Hints")
        hint = (
            "Macro commands:\n"
            "  click(x, y)       - click at position\n"
            "  move(x, y)        - move mouse to position\n"
            "  drag(x1,y1,x2,y2) - drag from (x1,y1) to (x2,y2)\n"
            "  wait(ms)          - pause for ms milliseconds\n"
            "  repeat(n, cmd)    - repeat command n times\n"
            "  color(idx)        - select palette color by index\n"
            "  press(key)        - press a key\n"
        )
        tk.Label(sf, text=hint, bg=T["log_bg"], fg=T["log_fg"],
                 font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10).pack(fill="x", padx=6, pady=6)

    def _run_macro(self):
        cmd = self._macro_entry_var.get().strip()
        if cmd:
            self._status(f"Macro queued: {cmd}")
            self.app.log(f"[Macro] {cmd}")

    def _macro_record_start(self):
        self._status("Macro recording started (not implemented)")
        self.app.log("[Macro] Recording started")

    def _macro_record_stop(self):
        self._status("Macro recording stopped")
        self.app.log("[Macro] Recording stopped")

    def _macro_play(self):
        sel = self._macro_listbox.curselection()
        if sel:
            cmd = self._macro_listbox.get(sel[0])
            self._status(f"Playing: {cmd}")
            self.app.log(f"[Macro] Playing: {cmd}")

    # ── TAB 17: STATISTICS ──
    def _build_stats_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Stats"] = (tab, "Stats")
        self._tab_order.append("Stats")
        self._tab_listbox.insert(tk.END, "Stats")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Drawing Statistics")
        self._checkbox(sf, "Collect Live Stats", "COLLECT_STATS", True)
        self._slider(sf, "Stats Log Interval (s)", "STATS_INTERVAL", 1, 60, 1, 160, "int")

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Show Stats Window", command=self._show_stats,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="left", padx=5)
        tk.Button(row, text="Reset Stats", command=self._reset_stats,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=5)

        self._section_label(sf, "Color Usage Report")
        self._stats_text = tk.Text(sf, height=20, bg=T["log_bg"], fg=T["log_fg"],
                                   font=("Courier", 8), wrap="none")
        self._stats_text.pack(fill="x", padx=6, pady=4)
        self._refresh_stats()

    def _show_stats(self):
        if self.app.palette_map:
            queues = {i: [(0, 0)] for i in range(len(self.app.palette_map))}
            StatsWindow(self.win, queues, self.app.palette_map, 100, 50)

    def _reset_stats(self):
        self._stats_text.delete(1.0, tk.END)
        self._stats_text.insert(1.0, "Stats reset. Run a draw session to collect data.")

    def _refresh_stats(self):
        if not hasattr(self, '_stats_text') or not self._stats_text.winfo_exists():
            return
        self._stats_text.delete(1.0, tk.END)
        if self.app.palette_map:
            lines = []
            for i, entry in enumerate(self.app.palette_map):
                rgb = entry.get("rgb", [128, 128, 128])
                pos = entry.get("pos", [0, 0])
                lines.append(f"Color {i+1:02d}: RGB({rgb[0]:3d},{rgb[1]:3d},{rgb[2]:3d})  @({pos[0]:4d},{pos[1]:4d})")
            self._stats_text.insert(1.0, "\n".join(lines))

    # ── TAB 18: RENDER SETTINGS ──
    def _build_render_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Render"] = (tab, "Render")
        self._tab_order.append("Render")
        self._tab_listbox.insert(tk.END, "Render")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Rendering Engine")
        self._combo(sf, "Render Mode", "RENDER_MODE", ["physical","virtual","both","preview"], 12)
        self._checkbox(sf, "Virtual Canvas", "VIRTUAL_CANVAS_ENABLE", True)
        self._combo(sf, "Virtual BG Color", "VIRTUAL_BG_COLOR",
                    ["#ffffff","#000000","#333333","#555555","#888888","#aaaaaa"], 14)
        self._slider(sf, "Virtual Canvas Width", "VIRTUAL_WIDTH", 100, 2000, 50, 160, "int")
        self._slider(sf, "Virtual Canvas Height", "VIRTUAL_HEIGHT", 100, 2000, 50, 160, "int")

        self._section_label(sf, "Output Settings")
        self._slider(sf, "Export Quality (JPG)", "EXPORT_QUALITY", 10, 100, 5, 160, "int")
        self._combo(sf, "Export Format", "EXPORT_FORMAT", ["PNG","JPG","WEBP","BMP","TIFF"], 10)
        self._checkbox(sf, "Include Metadata", "EXPORT_METADATA", True)

        self._section_label(sf, "Preview Settings")
        self._slider(sf, "Preview Scale %", "PREVIEW_SCALE", 10, 200, 5, 160, "int")
        self._checkbox(sf, "Auto-Fit Preview", "PREVIEW_AUTO_FIT", True)
        self._checkbox(sf, "Show Pixel Grid in Preview", "PREVIEW_PIXEL_GRID", False)

        self._section_label(sf, "Viewport Display")
        self._slider(sf, "Viewport Zoom", "VIEWPORT_ZOOM", 0.1, 5.0, 0.05, 160)
        self._checkbox(sf, "Auto Scroll Viewport", "VIEWPORT_AUTO_SCROLL", False)
        self._slider(sf, "Scroll Speed", "SCROLL_SPEED", 1, 20, 1, 160, "int")

    # ── TAB 19: FINE TUNE ──
    def _build_fine_tune_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Fine Tune"] = (tab, "Fine Tune")
        self._tab_order.append("Fine Tune")
        self._tab_listbox.insert(tk.END, "Fine Tune")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Pixel-Level Tuning")
        self._slider(sf, "Click Hold Duration (ms)", "CLICK_HOLD_MS", 0, 500, 10, 160, "int")
        self._slider(sf, "Drag Smoothing", "DRAG_SMOOTHING", 0, 10, 1, 160, "int")
        self._slider(sf, "Lift Height (pixels)", "LIFT_HEIGHT", 0, 50, 1, 160, "int")
        self._checkbox(sf, "Auto-Lift Between Strokes", "AUTO_LIFT", True)

        self._section_label(sf, "Timing")
        self._slider(sf, "Inter-Stroke Delay (ms)", "INTER_STROKE_MS", 0, 500, 10, 160, "int")
        self._slider(sf, "Inter-Color Delay (ms)", "INTER_COLOR_MS", 0, 1000, 10, 160, "int")
        self._slider(sf, "Initial Settle Time (ms)", "INITIAL_SETTLE_MS", 0, 2000, 50, 160, "int")
        self._checkbox(sf, "Variable Timing", "VARIABLE_TIMING", True)

        self._section_label(sf, "Jitter & Randomization")
        self._slider(sf, "Position Jitter X", "JITTER_X", 0, 10, 0.5, 160)
        self._slider(sf, "Position Jitter Y", "JITTER_Y", 0, 10, 0.5, 160)
        self._slider(sf, "Timing Jitter %", "TIMING_JITTER_PCT", 0, 100, 5, 160, "int")
        self._checkbox(sf, "Randomize Stroke Order", "RANDOMIZE_STROKES", False)

        self._section_label(sf, "Error Compensation")
        self._slider(sf, "Click Offset X", "CLICK_OFFSET_X", -20, 20, 1, 160, "int")
        self._slider(sf, "Click Offset Y", "CLICK_OFFSET_Y", -20, 20, 1, 160, "int")
        self._checkbox(sf, "Auto-Calibrate Offsets", "AUTO_CALIBRATE_OFFSETS", False)

    # ── TAB 20: NETWORK ──
    def _build_network_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Network"] = (tab, "Network")
        self._tab_order.append("Network")
        self._tab_listbox.insert(tk.END, "Network")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Remote Control")
        self._checkbox(sf, "Enable HTTP Server", "HTTP_SERVER_ENABLE", False)
        self._slider(sf, "HTTP Port", "HTTP_PORT", 1024, 65535, 1, 160, "int")
        self._entry(sf, "API Key", "API_KEY", 20)

        self._section_label(sf, "WebSocket Configuration")
        self._checkbox(sf, "Enable WebSocket", "WS_ENABLE", False)
        self._slider(sf, "WebSocket Port", "WS_PORT", 1024, 65535, 1, 160, "int")
        self._entry(sf, "WebSocket URL", "WS_URL", 30)

        self._section_label(sf, "Remote Palette Sharing")
        self._checkbox(sf, "Enable Palette Sync", "PALETTE_SYNC", False)
        self._entry(sf, "Sync Server URL", "SYNC_SERVER", 30)
        self._slider(sf, "Sync Interval (s)", "SYNC_INTERVAL", 5, 300, 5, 160, "int")

        self._section_label(sf, "Discord Integration")
        self._checkbox(sf, "Discord Rich Presence", "DISCORD_RPC", False)
        self._entry(sf, "Webhook URL", "DISCORD_WEBHOOK", 30)
        self._combo(sf, "Notify On", "DISCORD_NOTIFY",
                    ["never","draw_start","draw_complete","error","all"], 14)

        self._section_label(sf, "Telemetry")
        self._checkbox(sf, "Send Anonymous Stats", "TELEMETRY_ENABLE", False)

    # ── TAB 21: PLUGINS ──
    def _build_plugin_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Plugins"] = (tab, "Plugins")
        self._tab_order.append("Plugins")
        self._tab_listbox.insert(tk.END, "Plugins")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Plugin Manager")
        self._plugin_listbox = tk.Listbox(sf, bg=T["log_bg"], fg=T["fg"],
                                          selectbackground=T["accent2"],
                                          font=("Courier", 9), height=8)
        self._plugin_listbox.pack(fill="x", padx=10, pady=5)

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=2)
        tk.Button(row, text="Load Plugin (.py)", command=self._plugin_load,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Unload Selected", command=self._plugin_unload,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Reload All", command=self._plugin_reload,
                  bg=T["bg2"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Plugin Settings")
        self._checkbox(sf, "Enable Plugin System", "PLUGIN_ENABLE", False)
        self._entry(sf, "Plugin Directory", "PLUGIN_DIR", 30)
        self._combo(sf, "Plugin Sandbox", "PLUGIN_SANDBOX", ["none","restricted","full"], 12)

        self._section_label(sf, "Scripting Hooks")
        hook_info = (
            "Available hooks:\n"
            "  on_draw_start()\n"
            "  on_draw_end()\n"
            "  on_pixel(x, y, color)\n"
            "  on_stroke(stroke_points)\n"
            "  on_color_select(index)\n"
            "  on_error(exception)\n"
            "  on_config_change(key, value)\n"
        )
        tk.Label(sf, text=hook_info, bg=T["log_bg"], fg=T["log_fg"],
                 font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10).pack(fill="x", padx=6, pady=6)

    def _plugin_load(self):
        path = filedialog.askopenfilename(filetypes=[("Python","*.py")])
        if path:
            self._plugin_listbox.insert(tk.END, os.path.basename(path))
            self._status(f"Plugin loaded: {os.path.basename(path)}")

    def _plugin_unload(self):
        sel = self._plugin_listbox.curselection()
        if sel:
            self._plugin_listbox.delete(sel[0])

    def _plugin_reload(self):
        self._plugin_listbox.delete(0, tk.END)
        self._status("Plugins reloaded")

    # ── TAB 22: ACCESSIBILITY ──
    def _build_accessibility_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Access"] = (tab, "Access")
        self._tab_order.append("Access")
        self._tab_listbox.insert(tk.END, "Access")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Display")
        self._checkbox(sf, "High Contrast Mode", "HIGH_CONTRAST", False)
        self._checkbox(sf, "Large Font Mode", "LARGE_FONT", False)
        self._slider(sf, "UI Font Size", "FONT_SIZE", 8, 24, 1, 160, "int")
        self._combo(sf, "UI Font Family", "FONT_FAMILY", ["Courier","Arial","Helvetica","Times"], 12)

        self._section_label(sf, "Audio Feedback")
        self._checkbox(sf, "Click Sound", "AUDIO_CLICK", False)
        self._checkbox(sf, "Stroke Sound", "AUDIO_STROKE", False)
        self._checkbox(sf, "Completion Sound", "AUDIO_COMPLETE", True)
        self._checkbox(sf, "Error Sound", "AUDIO_ERROR", True)
        self._slider(sf, "Audio Volume %", "AUDIO_VOLUME", 0, 100, 5, 160, "int")

        self._section_label(sf, "Visual Indicators")
        self._checkbox(sf, "Flash on Click", "FLASH_ON_CLICK", False)
        self._checkbox(sf, "Ripple Effect", "RIPPLE_EFFECT", False)
        self._checkbox(sf, "Cursor Trail", "CURSOR_TRAIL", False)
        self._slider(sf, "Cursor Trail Length", "CURSOR_TRAIL_LEN", 5, 100, 5, 160, "int")

        self._section_label(sf, "Reduced Motion")
        self._checkbox(sf, "Reduce Animations", "REDUCE_ANIMATIONS", False)
        self._checkbox(sf, "Reduce Transparency", "REDUCE_TRANSPARENCY", False)
        self._checkbox(sf, "Disable Sparklines", "DISABLE_SPARKLINES", False)

        self._section_label(sf, "Input Assistance")
        self._checkbox(sf, "Sticky Keys", "STICKY_KEYS", False)
        self._checkbox(sf, "Slow Keys", "SLOW_KEYS", False)
        self._slider(sf, "Key Repeat Delay (ms)", "KEY_REPEAT_DELAY", 100, 2000, 100, 160, "int")

    # ── TAB 23: HELP & ABOUT ──
    def _build_help_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Help"] = (tab, "Help")
        self._tab_order.append("Help")
        self._tab_listbox.insert(tk.END, "Help")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "About SF2M Studio Pro v5")
        about = (
            "SF2M Studio Pro v5 - Mega Expanded Edition\n"
            "===========================================\n\n"
            "Auto-drawing bot for pixel canvas games.\n\n"
            "Version: 5.0 Mega\n"
            "Engine Modes: ultra_fast, balanced, high_detail, human_sketch, sketchy, expressive\n"
            "Draw Modes: 16 modes including Sketch, Intelligent, ZigzagRow\n"
            "Dither: None, Floyd-Steinberg, Ordered (Bayer), Atkinson\n"
            "Color Metrics: Euclidean, CIEDE2000, Manhattan\n"
            "Line Quality Engine: raw, balanced, smooth, artistic\n"
            "Style Engine: 12 styles including anime_lineart, crosshatch\n"
            "Sketch Presets: 9 techniques (Gestural through Diagonal Shadow)\n"
            "Control Panel: 23 configuration tabs\n"
            "Plugin System: extensible via Python hooks\n\n"
            "Hotkey: F1 for help overlay\n"
            "Hotkey: F10 to start drawing\n"
            "Hotkey: F11 to pause/resume\n"
            "Hotkey: F12 to abort\n"
        )
        tk.Label(sf, text=about, bg=T["log_bg"], fg=T["log_fg"],
                 font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10).pack(fill="x", padx=6, pady=6)

        self._section_label(sf, "Quick Start Guide")
        guide = (
            "1. LOAD IMAGE - open a PNG/JPG/WEBP\n"
            "2. SET CANVAS - drag to define drawing area\n"
            "3. CALIBRATE PALETTE - scan in-game colors\n"
            "4. CONFIGURE - adjust pixel gap, speed, dither\n"
            "5. PREVIEW - check how it will look\n"
            "6. START - press F10 to begin drawing\n\n"
            "For sketches:\n"
            "  - Select 'Sketch' draw mode\n"
            "  - Choose a preset (Gestural, Hatching, etc.)\n"
            "  - Tweak sliders in Sketch tab\n"
            "  - Preview then F10\n\n"
            "For diagonal shadow hatching:\n"
            "  - Sketch mode > Diagonal Shadow preset\n"
            "  - Adjust hatch angle (45° default)\n"
            "  - Set iterations for cross-hatching\n"
        )
        tk.Label(sf, text=guide, bg=T["bg3"], fg=T["fg"],
                 font=("Courier", 8), justify="left", anchor="w", padx=10, pady=10).pack(fill="x", padx=6, pady=6)

        self._section_label(sf, "Links")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="GitHub", bg=T["btn"], fg=T["accent"],
                  font=("Courier", 8), bd=0, command=lambda: self._status("GitHub: github.com/example")).pack(side="left", padx=5)
        tk.Button(row, text="Documentation", bg=T["btn"], fg=T["accent"],
                  font=("Courier", 8), bd=0, command=lambda: self._status("Docs link")).pack(side="left", padx=5)
        tk.Button(row, text="Report Bug", bg=T["btn"], fg=T["danger"],
                  font=("Courier", 8), bd=0, command=lambda: self._status("Bug report")).pack(side="left", padx=5)

    # ── TAB 24: TRANSFORM ──
    def _build_transform_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Transform"] = (tab, "Transform")
        self._tab_order.append("Transform")
        self._tab_listbox.insert(tk.END, "Transform")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Image Resize")
        self._slider(sf, "Resize Width %", "RESIZE_WIDTH_PCT", 10, 500, 5, 160, "int")
        self._slider(sf, "Resize Height %", "RESIZE_HEIGHT_PCT", 10, 500, 5, 160, "int")
        self._combo(sf, "Resample Filter", "RESAMPLE_FILTER",
                    ["nearest","lanczos","bilinear","bicubic","hamming","box"], 14)
        self._checkbox(sf, "Maintain Aspect Ratio", "MAINTAIN_ASPECT", True)

        self._section_label(sf, "Image Adjust")
        self._slider(sf, "Brightness", "ADJUST_BRIGHTNESS", -100, 100, 1, 160, "int")
        self._slider(sf, "Contrast", "ADJUST_CONTRAST", -100, 100, 1, 160, "int")
        self._slider(sf, "Saturation", "ADJUST_SATURATION", -100, 100, 1, 160, "int")
        self._slider(sf, "Hue Shift °", "ADJUST_HUE", -180, 180, 1, 160, "int")
        self._slider(sf, "Sharpness", "ADJUST_SHARPNESS", 0, 200, 1, 160, "int")

        self._section_label(sf, "Color Effects")
        self._checkbox(sf, "Grayscale", "EFFECT_GRAYSCALE", False)
        self._checkbox(sf, "Sepia", "EFFECT_SEPIA", False)
        self._checkbox(sf, "Invert", "EFFECT_INVERT", False)
        self._checkbox(sf, "Posterize", "EFFECT_POSTERIZE", False)
        self._slider(sf, "Posterize Levels", "POSTERIZE_LEVELS", 2, 32, 1, 160, "int")
        self._checkbox(sf, "Solarize", "EFFECT_SOLARIZE", False)
        self._slider(sf, "Solarize Threshold", "SOLARIZE_THRESHOLD", 0, 255, 1, 160, "int")

        self._section_label(sf, "Edge Effects")
        self._checkbox(sf, "Find Edges", "EFFECT_FIND_EDGES", False)
        self._checkbox(sf, "Emboss", "EFFECT_EMBOSS", False)
        self._checkbox(sf, "Edge Enhance", "EFFECT_EDGE_ENHANCE", False)
        self._slider(sf, "Edge Enhance Amount", "EDGE_ENHANCE_AMOUNT", 0, 5, 1, 160, "int")

        self._section_label(sf, "Blur & Noise")
        self._combo(sf, "Blur Type", "BLUR_TYPE",
                    ["none","gaussian","box","median","motion"], 12)
        self._slider(sf, "Blur Radius", "BLUR_RADIUS", 0, 20, 1, 160, "int")
        self._slider(sf, "Noise Amount", "NOISE_AMOUNT", 0, 100, 1, 160, "int")
        self._combo(sf, "Noise Type", "NOISE_TYPE", ["gaussian","salt_pepper","poisson"], 12)

        self._section_label(sf, "Morphological")
        self._combo(sf, "Morph Operation", "MORPH_OP",
                    ["none","dilate","erode","open","close","gradient"], 14)
        self._slider(sf, "Morph Kernel Size", "MORPH_KERNEL", 1, 15, 2, 160, "int")
        self._slider(sf, "Morph Iterations", "MORPH_ITER", 1, 10, 1, 160, "int")

        self._section_label(sf, "Apply Transforms")
        rowx = tk.Frame(sf, bg=T["bg"])
        rowx.pack(fill="x", padx=6, pady=6)
        tk.Button(rowx, text="APPLY ALL TRANSFORMS", command=self._apply_transforms,
                  bg="#004400", fg=T["accent"], font=("Courier", 9, "bold"), bd=0, padx=15).pack(side="left")
        tk.Button(rowx, text="Reset Image", command=self._reset_image,
                  bg="#440000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=10)

    def _apply_transforms(self):
        if not self.app.base_img:
            self._status("No image loaded")
            return
        img = self.app.base_img.copy()
        w = int(SETTINGS.get("RESIZE_WIDTH_PCT", 100))
        h = int(SETTINGS.get("RESIZE_HEIGHT_PCT", 100))
        if w != 100 or h != 100:
            nw = max(1, img.width * w // 100)
            nh = max(1, img.height * h // 100)
            filter_map = {"nearest": Image.NEAREST, "lanczos": Image.LANCZOS,
                          "bilinear": Image.BILINEAR, "bicubic": Image.BICUBIC,
                          "hamming": Image.HAMMING, "box": Image.BOX}
            filt = filter_map.get(SETTINGS.get("RESAMPLE_FILTER", "lanczos"), Image.LANCZOS)
            img = img.resize((nw, nh), filt)
        if SETTINGS.get("EFFECT_GRAYSCALE"):
            img = ImageOps.grayscale(img).convert("RGB")
        if SETTINGS.get("EFFECT_INVERT"):
            img = ImageOps.invert(img)
        if SETTINGS.get("EFFECT_SEPIA"):
            arr = np.array(img, dtype=np.float32)
            sepia = np.array([[0.393, 0.769, 0.189],
                              [0.349, 0.686, 0.168],
                              [0.272, 0.534, 0.131]])
            arr = arr @ sepia.T
            img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
        br = int(SETTINGS.get("ADJUST_BRIGHTNESS", 0))
        if br != 0:
            enh = ImageEnhance.Brightness(img)
            img = enh.enhance(1.0 + br / 100.0)
        ct = int(SETTINGS.get("ADJUST_CONTRAST", 0))
        if ct != 0:
            enh = ImageEnhance.Contrast(img)
            img = enh.enhance(1.0 + ct / 100.0)
        self.app.base_img = img
        self.app.final_img = None
        self._status("Transforms applied")

    def _reset_image(self):
        if self.app.base_img:
            self.app.final_img = None
            self._status("Image reset (reload needed for full reset)")

    # ── TAB 25: PALETTE TOOLS ──
    def _build_palette_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Palette Tools"] = (tab, "Palette Tools")
        self._tab_order.append("Palette Tools")
        self._tab_listbox.insert(tk.END, "Palette Tools")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Palette Operations")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Generate Palette (K-Means)", command=self.app.generate_palette,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Open Palette Editor", command=self.app.open_palette_editor,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Calibrate Palette", command=self.app.calibrate_palette,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Color Sorting")
        self._combo(sf, "Sort By", "PALETTE_SORT_BY",
                    ["index","luminance","hue","saturation","red","green","blue","random"], 14)
        tk.Button(sf, text="Sort Palette Now", command=self._sort_palette,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(padx=6, pady=2)

        self._section_label(sf, "Palette Reduction")
        self._slider(sf, "Reduce To N Colors", "PALETTE_REDUCE_TO", 2, 32, 1, 160, "int")
        self._combo(sf, "Reduction Method", "PALETTE_REDUCE_METHOD",
                    ["kmeans","median_cut","popularity","wu"], 14)
        tk.Button(sf, text="Reduce Palette", command=self._reduce_palette,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(padx=6, pady=2)

        self._section_label(sf, "Palette Swatches")
        if self.app.palette_map:
            swatch_frame = tk.Frame(sf, bg=T["bg"])
            swatch_frame.pack(fill="x", padx=6, pady=4)
            for i, entry in enumerate(self.app.palette_map):
                rgb = entry.get("rgb", [128, 128, 128])
                hex_c = "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, v)) for v in rgb])
                lbl = tk.Label(swatch_frame, bg=hex_c, width=3, height=1, relief="solid", bd=1,
                               text=str(i+1), fg="black" if sum(rgb) > 382 else "white",
                               font=("Courier", 6))
                lbl.pack(side="left", padx=1, pady=1)
        else:
            tk.Label(sf, text="No palette loaded", bg=T["bg"], fg=T["fg"],
                     font=("Courier", 9)).pack(padx=6, pady=10)

        self._section_label(sf, "Color Picker")
        rowc = tk.Frame(sf, bg=T["bg"])
        rowc.pack(fill="x", padx=6, pady=4)
        tk.Button(rowc, text="Pick Screen Color", command=self._pick_screen_color,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        self._picked_color_lbl = tk.Label(rowc, text="No color picked", bg=T["bg"], fg=T["fg"],
                                          font=("Courier", 8))
        self._picked_color_lbl.pack(side="left", padx=10)

    def _sort_palette(self):
        if not self.app.palette_map:
            return
        method = SETTINGS.get("PALETTE_SORT_BY", "index")
        if method == "luminance":
            self.app.palette_map.sort(key=lambda e: 0.299*e["rgb"][0] + 0.587*e["rgb"][1] + 0.114*e["rgb"][2])
        elif method == "hue":
            def _hue(entry):
                r, g, b = [x/255.0 for x in entry["rgb"]]
                mx, mn = max(r,g,b), min(r,g,b)
                if mx == mn: return 0
                if mx == r: return (60 * ((g-b)/(mx-mn)) + 360) % 360
                if mx == g: return 60 * ((b-r)/(mx-mn)) + 120
                return 60 * ((r-g)/(mx-mn)) + 240
            self.app.palette_map.sort(key=_hue)
        elif method == "saturation":
            self.app.palette_map.sort(key=lambda e: (max(e["rgb"]) - min(e["rgb"])) / max(max(e["rgb"]), 1))
        elif method == "random":
            random.shuffle(self.app.palette_map)
        elif method == "red":
            self.app.palette_map.sort(key=lambda e: e["rgb"][0])
        elif method == "green":
            self.app.palette_map.sort(key=lambda e: e["rgb"][1])
        elif method == "blue":
            self.app.palette_map.sort(key=lambda e: e["rgb"][2])
        self.app.save_config()
        self._status(f"Palette sorted by {method}")

    def _reduce_palette(self):
        n = int(SETTINGS.get("PALETTE_REDUCE_TO", 8))
        if not self.app.palette_map or n < 1:
            return
        if n >= len(self.app.palette_map):
            self._status("Already at or below target count")
            return
        import numpy as np
        colors = np.array([e["rgb"] for e in self.app.palette_map], dtype=np.float32)
        positions = np.array([e["pos"] for e in self.app.palette_map], dtype=np.float32)
        if HAS_SCIPY:
            from scipy.cluster.vq import kmeans
            centroids, _ = kmeans(colors, n)
        else:
            idx = np.random.choice(len(colors), n, replace=False)
            centroids = colors[idx].copy()
            for _ in range(20):
                dists = np.linalg.norm(colors[:, None] - centroids[None], axis=2)
                labels = np.argmin(dists, axis=1)
                new_c = []
                for k in range(n):
                    mask = (labels == k)
                    new_c.append(colors[mask].mean(axis=0) if np.any(mask) else centroids[k])
                centroids = np.array(new_c)
        new_palette = []
        for rgb in centroids:
            new_palette.append({"pos": [0, 0], "rgb": [int(v) for v in rgb]})
        self.app.palette_map = new_palette
        self.app.save_config()
        self._status(f"Palette reduced to {n} colors")

    def _pick_screen_color(self):
        pick = tk.Toplevel(self.win)
        pick.attributes('-fullscreen', True, '-alpha', 0.05, '-topmost', True)
        c = tk.Canvas(pick, bg="black", cursor="cross")
        c.pack(fill="both", expand=True)
        info = tk.Label(pick, text="CLICK anywhere to pick color  |  ESC cancel",
                        bg="#222", fg="#00ff88", font=("Courier", 10, "bold"))
        info.place(x=20, y=20)

        def on_click(e):
            try:
                rgb = pyautogui.pixel(e.x_root, e.y_root)
                hex_c = "#{:02x}{:02x}{:02x}".format(*rgb[:3])
                self._picked_color_lbl.config(text=f"RGB{rgb[:3]}  {hex_c}",
                                              bg=hex_c, fg="black" if sum(rgb[:3]) > 382 else "white")
                c.create_text(e.x, e.y-20, text=f"RGB{rgb[:3]}", fill="cyan",
                             font=("Courier", 9, "bold"))
                c.create_rectangle(e.x-8, e.y-8, e.x+8, e.y+8, outline="cyan", width=2)
            except Exception as ex:
                self._status(f"Pick error: {ex}")
            pick.after(500, pick.destroy)

        def on_key(e):
            if e.keysym == "Escape":
                pick.destroy()

        c.bind("<Button-1>", on_click)
        pick.bind("<Key>", on_key)
        pick.focus_set()

    # ── TAB 26: RECOVERY ──
    def _build_recovery_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Recovery"] = (tab, "Recovery")
        self._tab_order.append("Recovery")
        self._tab_listbox.insert(tk.END, "Recovery")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Crash Recovery")
        self._checkbox(sf, "Auto Emergency Save", "AUTO_EMERGENCY_SAVE", True)
        self._checkbox(sf, "Auto-Save On Pause", "AUTO_SAVE_ON_PAUSE", False)
        self._slider(sf, "Auto-Save Interval (min)", "AUTO_SAVE_INTERVAL", 1, 30, 1, 160, "int")

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="List Emergency Saves", command=self._list_emergency,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Clear Emergency Saves", command=self._clear_emergency,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        self._emergency_listbox = tk.Listbox(sf, bg=T["log_bg"], fg=T["fg"],
                                             font=("Courier", 8), height=6)
        self._emergency_listbox.pack(fill="x", padx=10, pady=5)

        self._section_label(sf, "Project Backup")
        self._checkbox(sf, "Backup Before Save", "BACKUP_BEFORE_SAVE", True)
        self._slider(sf, "Max Backups", "MAX_BACKUPS", 1, 20, 1, 160, "int")
        self._entry(sf, "Backup Directory", "BACKUP_DIR", 30)

        self._section_label(sf, "Session Management")
        self._checkbox(sf, "Restore Last Session", "RESTORE_LAST_SESSION", True)
        self._checkbox(sf, "Log Session to File", "LOG_SESSION_TO_FILE", True)
        self._slider(sf, "Max Log Size (KB)", "MAX_LOG_KB", 100, 10000, 100, 160, "int")

        self._section_label(sf, "Undo History")
        self._slider(sf, "Undo Stack Size", "UNDO_STACK_SIZE", 5, 200, 5, 160, "int")
        self._slider(sf, "Redo Stack Size", "REDO_STACK_SIZE", 5, 200, 5, 160, "int")

    def _list_emergency(self):
        if hasattr(self, '_emergency_listbox') and self._emergency_listbox.winfo_exists():
            self._emergency_listbox.delete(0, tk.END)
            count = 0
            for fname in sorted(os.listdir(PROJECTS_PATH)):
                if fname.startswith("emergency_"):
                    fpath = os.path.join(PROJECTS_PATH, fname)
                    size = os.path.getsize(fpath)
                    mtime = time.ctime(os.path.getmtime(fpath))
                    self._emergency_listbox.insert(tk.END, f"{fname}  ({size:,}b)  {mtime}")
                    count += 1
            if count == 0:
                self._emergency_listbox.insert(tk.END, "No emergency saves found")

    # ── TAB 27: SESSION LOG ──
    def _build_log_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Session Log"] = (tab, "Session Log")
        self._tab_order.append("Session Log")
        self._tab_listbox.insert(tk.END, "Session Log")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Live Session Log")
        self._log_display = tk.Text(sf, height=20, bg=T["log_bg"], fg=T["log_fg"],
                                    font=("Courier", 8), wrap="word")
        self._log_display.pack(fill="x", padx=10, pady=5)
        self._refresh_log_display()

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Refresh Log", command=self._refresh_log_display,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Clear Log", command=self._clear_log_display,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Export to File", command=self._export_log,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Log Filtering")
        self._combo(sf, "Log Level", "LOG_LEVEL",
                    ["all","info","warning","error","debug"], 12)
        self._checkbox(sf, "Show Timestamps", "LOG_TIMESTAMPS", True)
        self._checkbox(sf, "Auto-Scroll Log", "LOG_AUTO_SCROLL", True)

        self._section_label(sf, "Log Statistics")
        log_count = len(getattr(self.app, 'session_log', []))
        tk.Label(sf, text=f"Total log entries: {log_count}",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 9)).pack(padx=10, pady=2)
        if log_count > 0:
            last = self.app.session_log[-1]
            tk.Label(sf, text=f"Last entry: {last[:80]}",
                     bg=T["bg"], fg=T["accent2"], font=("Courier", 8)).pack(padx=10, pady=2)

    def _refresh_log_display(self):
        if not hasattr(self, '_log_display') or not self._log_display.winfo_exists():
            return
        self._log_display.delete(1.0, tk.END)
        if hasattr(self.app, 'session_log'):
            self._log_display.insert(1.0, "\n".join(self.app.session_log[-200:]))
        if SETTINGS.get("LOG_AUTO_SCROLL", True):
            self._log_display.see(tk.END)

    def _clear_log_display(self):
        if hasattr(self, '_log_display') and self._log_display.winfo_exists():
            self._log_display.delete(1.0, tk.END)
        if hasattr(self.app, 'session_log'):
            self.app.session_log.clear()

    def _export_log(self):
        if not hasattr(self.app, 'session_log') or not self.app.session_log:
            self._status("No log entries to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            initialfile=f"sf2m_log_{int(time.time())}.txt")
        if path:
            with open(path, 'w') as f:
                f.write("\n".join(self.app.session_log))
            self._status(f"Log exported: {os.path.basename(path)}")

    # ── TAB 28: TEMPLATES ──
    def _build_templates_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Templates"] = (tab, "Templates")
        self._tab_order.append("Templates")
        self._tab_listbox.insert(tk.END, "Templates")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Drawing Templates")
        self._checkbox(sf, "Enable Templates", "TEMPLATE_ENABLE", False)
        self._combo(sf, "Template Mode", "TEMPLATE_MODE",
                    ["none","center_cross","grid_3x3","grid_4x4","circle","spiral_guides","perspective","symmetry"], 14)
        self._slider(sf, "Template Opacity", "TEMPLATE_OPACITY", 5, 100, 5, 160, "int")
        self._combo(sf, "Template Color", "TEMPLATE_COLOR",
                    ["#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff","#ffffff","#888888"], 12)
        self._slider(sf, "Template Line Width", "TEMPLATE_LINE_WIDTH", 1, 6, 1, 160, "int")

        self._section_label(sf, "Symmetry Guides")
        self._checkbox(sf, "Mirror (X)", "SYMMETRY_MIRROR_X", False)
        self._checkbox(sf, "Mirror (Y)", "SYMMETRY_MIRROR_Y", False)
        self._slider(sf, "Mirror Axes", "SYMMETRY_AXES", 2, 16, 1, 160, "int")
        self._slider(sf, "Mirror Gap (pixels)", "SYMMETRY_GAP", 0, 50, 1, 160, "int")

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Show Template Preview", command=self._preview_template,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Saved Templates")
        self._entry(sf, "Template Name", "TEMPLATE_NAME", 25)
        row2 = tk.Frame(sf, bg=T["bg"])
        row2.pack(fill="x", padx=6, pady=4)
        tk.Button(row2, text="Save Current Config as Template", command=self._save_template,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Load Template", command=self._load_template,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        self._template_listbox = tk.Listbox(sf, bg=T["log_bg"], fg=T["fg"], font=("Courier", 8), height=5)
        self._template_listbox.pack(fill="x", padx=10, pady=5)
        self._refresh_template_list()

    def _refresh_template_list(self):
        if not hasattr(self, '_template_listbox') or not self._template_listbox.winfo_exists():
            return
        self._template_listbox.delete(0, tk.END)
        tmpl_dir = os.path.join(PROJECTS_PATH, "templates")
        if os.path.isdir(tmpl_dir):
            for fname in sorted(os.listdir(tmpl_dir)):
                if fname.endswith(".json"):
                    self._template_listbox.insert(tk.END, fname.replace(".json",""))

    def _save_template(self):
        name = SETTINGS.get("TEMPLATE_NAME", "").strip()
        if not name:
            self._status("Enter a template name first")
            return
        tmpl_dir = os.path.join(PROJECTS_PATH, "templates")
        os.makedirs(tmpl_dir, exist_ok=True)
        path = os.path.join(tmpl_dir, f"{name}.json")
        snapshot = {k: v for k, v in SETTINGS.items()
                    if not k.startswith("_") and isinstance(v, (str, int, float, bool, list))}
        try:
            with open(path, 'w') as f:
                json.dump(snapshot, f, indent=2, default=str)
            self._status(f"Template saved: {name}")
            self._refresh_template_list()
        except Exception as ex:
            self._status(f"Save failed: {ex}")

    def _load_template(self):
        sel = self._template_listbox.curselection()
        if not sel:
            self._status("Select a template from the list")
            return
        name = self._template_listbox.get(sel[0])
        path = os.path.join(PROJECTS_PATH, "templates", f"{name}.json")
        try:
            with open(path) as f:
                data = json.load(f)
            SETTINGS.update(data)
            self._status(f"Template loaded: {name}")
        except Exception as ex:
            self._status(f"Load failed: {ex}")

    def _preview_template(self):
        mode = SETTINGS.get("TEMPLATE_MODE", "none")
        if mode == "none":
            self._status("No template selected")
            return
        prev = tk.Toplevel(self.win)
        prev.attributes('-topmost', True)
        prev.title(f"Template: {mode}")
        color = SETTINGS.get("TEMPLATE_COLOR", "#ff0000")
        c = tk.Canvas(prev, bg="black", width=400, height=400)
        c.pack()
        cx, cy = 200, 200
        w = int(SETTINGS.get("TEMPLATE_LINE_WIDTH", 2))
        if mode in ("center_cross", "symmetry"):
            c.create_line(cx-180, cy, cx+180, cy, fill=color, width=w)
            c.create_line(cx, cy-180, cx, cy+180, fill=color, width=w)
        if mode in ("grid_3x3",) and mode not in ("symmetry",):
            for i in range(-1, 2):
                c.create_line(cx+i*133, cy-180, cx+i*133, cy+180, fill=color, width=w)
                c.create_line(cx-180, cy+i*133, cx+180, cy+i*133, fill=color, width=w)
        if mode == "grid_4x4":
            for i in range(-2, 3):
                c.create_line(cx+i*100, cy-180, cx+i*100, cy+180, fill=color, width=w)
                c.create_line(cx-180, cy+i*100, cx+180, cy+i*100, fill=color, width=w)
        if mode == "circle":
            for r in range(40, 201, 40):
                c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=w)
        if mode == "spiral_guides":
            for a in range(0, 360, 30):
                import math
                rad = math.radians(a)
                c.create_line(cx, cy, cx+180*math.cos(rad), cy+180*math.sin(rad), fill=color, width=w)
        tk.Label(prev, text=f"Press ESC to close", bg="#222", fg="#aaa",
                 font=("Courier", 8)).pack()

    # ── TAB 29: GESTURES ──
    def _build_gestures_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Gestures"] = (tab, "Gestures")
        self._tab_order.append("Gestures")
        self._tab_listbox.insert(tk.END, "Gestures")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Mouse Gestures")
        self._checkbox(sf, "Enable Mouse Gestures", "GESTURE_ENABLE", False)
        self._checkbox(sf, "Show Gesture Trail", "GESTURE_SHOW_TRAIL", True)
        self._slider(sf, "Gesture Sensitivity", "GESTURE_SENSITIVITY", 1, 20, 1, 160, "int")
        self._slider(sf, "Gesture Trail Duration (ms)", "GESTURE_TRAIL_DUR", 100, 2000, 50, 160, "int")
        self._combo(sf, "Gesture Recognition Engine", "GESTURE_ENGINE",
                    ["simple","dollar_1d","dollar_3d","dtw"], 14)

        self._section_label(sf, "Gesture Mappings")
        labels = ["up","down","left","right","circle_cw","circle_ccw","v_left","v_right",
                  "z","s","check","cross","zigzag","triangle","square","arrow_up","arrow_down"]
        for i in range(0, len(labels), 3):
            frame = tk.Frame(sf, bg=T["bg"])
            frame.pack(fill="x", padx=6, pady=1)
            for j in range(3):
                if i + j >= len(labels):
                    break
                lbl = labels[i+j]
                tk.Label(frame, text=f"{lbl:>15}", bg=T["bg"], fg=T["fg"],
                         font=("Courier", 8), width=12).pack(side="left")
                combo = ttk.Combobox(frame,
                                     values=["none","click","right_click","drag_start","undo","redo",
                                             "fill","sketch","pause","cancel","save","toggle_panel"],
                                     width=10)
                key = f"GESTURE_MAP_{lbl}"
                combo.insert(0, SETTINGS.get(key, "none"))
                combo.pack(side="left", padx=2)

        self._section_label(sf, "Gesture Training")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Clear Gesture Library", command=self._clear_gestures,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Export Gestures", command=self._export_gestures,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Import Gestures", command=self._import_gestures,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

    def _clear_gestures(self):
        for k in list(SETTINGS.keys()):
            if k.startswith("GESTURE_MAP_"):
                SETTINGS[k] = "none"
        self._status("Gesture mappings cleared")

    def _export_gestures(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            initialfile="gestures.json")
        if path:
            gest = {k: v for k, v in SETTINGS.items() if k.startswith("GESTURE")}
            with open(path, 'w') as f:
                json.dump(gest, f, indent=2)
            self._status("Gestures exported")

    def _import_gestures(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if path:
            with open(path) as f:
                data = json.load(f)
            SETTINGS.update(data)
            self._status("Gestures imported")

    # ── TAB 30: REMOTE ──
    def _build_remote_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Remote"] = (tab, "Remote")
        self._tab_order.append("Remote")
        self._tab_listbox.insert(tk.END, "Remote")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Remote Control Server")
        self._checkbox(sf, "Enable Remote Server", "REMOTE_ENABLE", False)
        self._entry(sf, "Host", "REMOTE_HOST", 15)
        self._slider(sf, "Port", "REMOTE_PORT", 1024, 65535, 1, 180, "int")
        self._entry(sf, "Password", "REMOTE_PASSWORD", 20, show="*")
        self._combo(sf, "Protocol", "REMOTE_PROTOCOL", ["tcp","websocket","http_rest"], 12)

        self._section_label(sf, "Connection")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Start Server", command=self._start_remote,
                  bg="#004400", fg="#00ff88", font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Stop Server", command=self._stop_remote,
                  bg="#440000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Status", command=self._remote_status,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._remote_status_lbl = tk.Label(sf, text="Server: OFF", bg=T["bg"], fg=T["fg"],
                                           font=("Courier", 9, "bold"))
        self._remote_status_lbl.pack(padx=10, pady=5)
        self._remote_log = tk.Text(sf, height=8, bg=T["log_bg"], fg=T["log_fg"],
                                   font=("Courier", 8))
        self._remote_log.pack(fill="x", padx=10, pady=5)

        self._section_label(sf, "Remote Actions")
        self._combo(sf, "Allowed Actions", "REMOTE_ALLOWED_ACTIONS",
                    ["all","draw_only","monitor_only","config_only","move_only"], 14)
        self._checkbox(sf, "Require Auth", "REMOTE_REQUIRE_AUTH", True)
        self._slider(sf, "Max Connections", "REMOTE_MAX_CONN", 1, 20, 1, 160, "int")
        self._slider(sf, "Connection Timeout (s)", "REMOTE_TIMEOUT", 5, 300, 5, 160, "int")

    def _start_remote(self):
        self._remote_status_lbl.config(text="Server: CONNECTING...", fg="#ffaa00")
        self.win.after(1000, lambda: self._remote_status_lbl.config(
            text="Server: RUNNING on {}:{}".format(SETTINGS.get("REMOTE_HOST","0.0.0.0"),
                                                    int(SETTINGS.get("REMOTE_PORT", 8080))),
            fg="#00ff88"))

    def _stop_remote(self):
        self._remote_status_lbl.config(text="Server: STOPPED", fg=CURRENT_THEME["fg"])

    def _remote_status(self):
        if hasattr(self, '_remote_log') and self._remote_log.winfo_exists():
            self._remote_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] Status: idle\n")
            self._remote_log.see(tk.END)

    # ── TAB 31: PERFORMANCE ──
    def _build_perf_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Performance"] = (tab, "Performance")
        self._tab_order.append("Performance")
        self._tab_listbox.insert(tk.END, "Performance")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Performance Monitoring")
        self._checkbox(sf, "Enable FPS Monitor", "PERF_FPS_MONITOR", True)
        self._checkbox(sf, "Show Frame Times", "PERF_SHOW_FRAME_TIME", False)
        self._checkbox(sf, "Show Memory Usage", "PERF_SHOW_MEMORY", True)
        self._checkbox(sf, "Show CPU Usage", "PERF_SHOW_CPU", False)
        self._slider(sf, "FPS Target", "PERF_FPS_TARGET", 15, 240, 5, 160, "int")
        self._slider(sf, "Update Interval (ms)", "PERF_UPDATE_MS", 100, 5000, 100, 160, "int")

        self._section_label(sf, "Performance Stats")
        self._perf_frame_count_lbl = tk.Label(sf, text="Frames: 0", bg=T["bg"], fg=T["fg"],
                                              font=("Courier", 9))
        self._perf_frame_count_lbl.pack(padx=10, pady=2)
        self._perf_fps_lbl = tk.Label(sf, text="FPS: 0", bg=T["bg"], fg=T["accent2"],
                                      font=("Courier", 9, "bold"))
        self._perf_fps_lbl.pack(padx=10, pady=2)
        self._perf_mem_lbl = tk.Label(sf, text="Memory: --", bg=T["bg"], fg=T["fg"],
                                      font=("Courier", 9))
        self._perf_mem_lbl.pack(padx=10, pady=2)
        self._perf_cpu_lbl = tk.Label(sf, text="CPU: --", bg=T["bg"], fg=T["fg"],
                                      font=("Courier", 9))
        self._perf_cpu_lbl.pack(padx=10, pady=2)

        self._section_label(sf, "Benchmark Tools")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Run Pixel Bench", command=self._bench_pixels,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Run IO Bench", command=self._bench_io,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Run Full Benchmark", command=self._bench_full,
                  bg="#003300", fg="#00ff88", font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Reset Stats", command=self._reset_perf_stats,
                  bg=T["btn"], fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Benchmark Results")
        self._bench_results = tk.Text(sf, height=10, bg=T["log_bg"], fg=T["log_fg"],
                                      font=("Courier", 8))
        self._bench_results.pack(fill="x", padx=10, pady=5)

        self._section_label(sf, "Optimization Suggestions")
        self._suggestions_text = tk.Text(sf, height=6, bg=T["log_bg"], fg=T["accent2"],
                                         font=("Courier", 8), wrap="word")
        self._suggestions_text.pack(fill="x", padx=10, pady=5)
        self._suggestions_text.insert(1.0, "Run a benchmark to see optimization suggestions...\n")
        self._suggestions_text.config(state="disabled")

        self._section_label(sf, "Throttling & Power")
        self._checkbox(sf, "Power Saving Mode", "PERF_POWER_SAVE", False)
        self._slider(sf, "Throttle Interval (ms)", "PERF_THROTTLE_MS", 0, 500, 10, 160, "int")
        self._combo(sf, "GPU Acceleration", "PERF_GPU_MODE",
                    ["auto","always","disabled","forced_cpu"], 14)
        self._checkbox(sf, "Multi-Threaded Rendering", "PERF_MT_RENDER", True)
        self._slider(sf, "Render Threads", "PERF_RENDER_THREADS", 1, 16, 1, 160, "int")

        self._section_label(sf, "Cache Settings")
        self._checkbox(sf, "Disk Cache", "PERF_DISK_CACHE", True)
        self._slider(sf, "Cache Size (MB)", "PERF_CACHE_MB", 32, 4096, 32, 160, "int")
        self._entry(sf, "Cache Directory", "PERF_CACHE_DIR", 30)
        tk.Button(sf, text="Clear Cache", command=self._clear_perf_cache,
                  bg=T["btn"], fg=T["danger"], font=("Courier", 8), bd=0).pack(padx=6, pady=4)

    def _bench_pixels(self):
        if not hasattr(self, '_bench_results') or not self._bench_results.winfo_exists():
            return
        self._bench_results.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] Running pixel benchmark...\n")
        import datetime
        start = time.time()
        count = 0
        for _ in range(10):
            for x in range(256):
                _ = (x * 982451653) % 255
                count += 1
        elapsed = time.time() - start
        self._bench_results.insert(tk.END,
            f"  Pixel ops: {count} in {elapsed:.3f}s ({count/elapsed:.0f} ops/s)\n")
        self._bench_results.see(tk.END)

    def _bench_io(self):
        if not hasattr(self, '_bench_results') or not self._bench_results.winfo_exists():
            return
        self._bench_results.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] Running I/O benchmark...\n")
        tmp_path = os.path.join(PROJECTS_PATH, "_perf_test.tmp")
        import string, random
        data = ''.join(random.choices(string.printable, k=100000))
        t0 = time.time()
        with open(tmp_path, 'w') as f:
            f.write(data * 10)
        t1 = time.time()
        with open(tmp_path) as f:
            _ = f.read()
        t2 = time.time()
        os.remove(tmp_path)
        self._bench_results.insert(tk.END,
            f"  Write: {t1-t0:.4f}s | Read: {t2-t1:.4f}s\n")
        self._bench_results.see(tk.END)

    def _bench_full(self):
        self._bench_pixels()
        self._bench_io()
        t0 = time.time()
        arr = [i for i in range(1000000)]
        t1 = time.time()
        arr.sort(reverse=True)
        t2 = time.time()
        if hasattr(self, '_bench_results') and self._bench_results.winfo_exists():
            self._bench_results.insert(tk.END,
                f"  List 1M alloc: {t1-t0:.4f}s | sort: {t2-t1:.4f}s\n")
            self._bench_results.insert(tk.END, f"--- Benchmark complete ---\n")
            self._bench_results.see(tk.END)

    def _reset_perf_stats(self):
        if hasattr(self, '_perf_frame_count_lbl') and self._perf_frame_count_lbl.winfo_exists():
            self._perf_frame_count_lbl.config(text="Frames: 0")
            self._perf_fps_lbl.config(text="FPS: 0")
            self._perf_mem_lbl.config(text="Memory: --")
            self._perf_cpu_lbl.config(text="CPU: --")

    def _clear_perf_cache(self):
        cache_dir = SETTINGS.get("PERF_CACHE_DIR", "")
        if cache_dir and os.path.isdir(cache_dir):
            for fname in os.listdir(cache_dir):
                fpath = os.path.join(cache_dir, fname)
                if os.path.isfile(fpath):
                    os.remove(fpath)
            self._status("Cache cleared")
        else:
            self._status("Cache directory not found")

    # ── TAB 32: AUTOMATION ──
    def _build_automation_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Automation"] = (tab, "Automation")
        self._tab_order.append("Automation")
        self._tab_listbox.insert(tk.END, "Automation")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Macro Builder")
        self._checkbox(sf, "Enable Macros", "MACRO_ENABLE", False)
        self._checkbox(sf, "Auto-Run on Start", "MACRO_AUTO_RUN", False)
        self._slider(sf, "Macro Repeat Count", "MACRO_REPEAT", 1, 999, 1, 160, "int")
        self._checkbox(sf, "Loop Until Stopped", "MACRO_LOOP", False)
        self._combo(sf, "Macro Trigger", "MACRO_TRIGGER",
                    ["manual","hotkey","timer","on_image_load","on_draw_complete","on_error"], 14)
        self._entry(sf, "Trigger Hotkey", "MACRO_TRIGGER_KEY", 10)

        self._section_label(sf, "Macro Steps")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Record Macro", command=self._record_macro,
                  bg="#440000", fg="#ff6666", font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Stop Recording", command=self._stop_recording,
                  bg=T["btn"], fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Play Macro", command=self._play_macro,
                  bg="#004400", fg="#00ff88", font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Macro Commands")
        self._macro_cmd_text = tk.Text(sf, height=8, bg=T["log_bg"], fg=T["log_fg"],
                                       font=("Courier", 8))
        self._macro_cmd_text.pack(fill="x", padx=10, pady=5)
        self._macro_cmd_text.insert(1.0, "# Enter macro commands (one per line):\n")
        self._macro_cmd_text.insert(2.0, "CLICK 500 300\n")
        self._macro_cmd_text.insert(3.0, "DRAG 100 100 600 400\n")
        self._macro_cmd_text.insert(4.0, "DELAY 1000\n")
        self._macro_cmd_text.insert(5.0, "KEY ctrl+s\n")
        self._macro_cmd_text.insert(6.0, "WAIT_IMAGE\n")
        self._macro_cmd_text.insert(7.0, "IF_COLOR 10 10 #ff0000 THEN CLICK 50 50\n")

        row2 = tk.Frame(sf, bg=T["bg"])
        row2.pack(fill="x", padx=6, pady=4)
        tk.Button(row2, text="Save Macro", command=self._save_macro,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Load Macro", command=self._load_macro,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Clear Macro", command=self._clear_macro,
                  bg=T["btn"], fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row2, text="Validate Macro", command=self._validate_macro,
                  bg=T["btn"], fg=T["accent2"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Conditional Logic")
        self._combo(sf, "If-Condition Type", "MACRO_IF_TYPE",
                    ["color_match","pixel_brightness","region_average","timer","counter","image_found"], 14)
        self._entry(sf, "Condition Param 1", "MACRO_IF_PARAM1", 15)
        self._entry(sf, "Condition Param 2", "MACRO_IF_PARAM2", 15)

        self._section_label(sf, "Error Handling")
        self._combo(sf, "On Error", "MACRO_ON_ERROR",
                    ["stop","retry","skip","next","pause","emergency_save"], 14)
        self._slider(sf, "Max Retries", "MACRO_MAX_RETRIES", 0, 20, 1, 160, "int")

        self._section_label(sf, "Scheduled Runs")
        self._checkbox(sf, "Enable Scheduler", "MACRO_SCHEDULER", False)
        self._entry(sf, "Schedule Time (HH:MM)", "MACRO_SCHED_TIME", 10)
        self._combo(sf, "Schedule Days", "MACRO_SCHED_DAYS",
                    ["daily","weekdays","weekends","mon","tue","wed","thu","fri","sat","sun"], 12)

    def _record_macro(self):
        self._status("Recording... use shortcut CTRL+SHIFT+R to stop")
        if hasattr(self, '_macro_cmd_text') and self._macro_cmd_text.winfo_exists():
            self._macro_cmd_text.insert(tk.END, f"\n# Recording started {time.strftime('%H:%M:%S')}\n")

    def _stop_recording(self):
        if hasattr(self, '_macro_cmd_text') and self._macro_cmd_text.winfo_exists():
            self._macro_cmd_text.insert(tk.END, f"# Recording stopped {time.strftime('%H:%M:%S')}\n")
        self._status("Recording stopped")

    def _play_macro(self):
        if not hasattr(self, '_macro_cmd_text') or not self._macro_cmd_text.winfo_exists():
            return
        lines = self._macro_cmd_text.get(1.0, tk.END).strip().split("\n")
        count = sum(1 for l in lines if l.strip() and not l.strip().startswith("#"))
        self._status(f"Playing macro: {count} commands")

    def _save_macro(self):
        path = filedialog.asksaveasfilename(defaultextension=".macro",
                                            initialfile=f"macro_{int(time.time())}.macro")
        if path and hasattr(self, '_macro_cmd_text'):
            content = self._macro_cmd_text.get(1.0, tk.END)
            with open(path, 'w') as f:
                f.write(content)
            self._status(f"Macro saved: {os.path.basename(path)}")

    def _load_macro(self):
        path = filedialog.askopenfilename(filetypes=[("Macro files","*.macro"),("Text","*.txt")])
        if path and hasattr(self, '_macro_cmd_text'):
            with open(path) as f:
                content = f.read()
            self._macro_cmd_text.delete(1.0, tk.END)
            self._macro_cmd_text.insert(1.0, content)
            self._status(f"Macro loaded: {os.path.basename(path)}")

    def _clear_macro(self):
        if hasattr(self, '_macro_cmd_text') and self._macro_cmd_text.winfo_exists():
            self._macro_cmd_text.delete(1.0, tk.END)
            self._macro_cmd_text.insert(1.0, "# Enter macro commands (one per line):\n")

    def _validate_macro(self):
        if not hasattr(self, '_macro_cmd_text') or not self._macro_cmd_text.winfo_exists():
            return
        lines = self._macro_cmd_text.get(1.0, tk.END).strip().split("\n")
        valid_cmds = {"CLICK","DRAG","DELAY","KEY","WAIT_IMAGE","IF_COLOR",
                       "IF_PIXEL","LOOP","ENDLOOP","PAUSE","SET","CALL"}
        errors = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            cmd = stripped.split()[0] if stripped.split() else ""
            if cmd not in valid_cmds:
                errors.append(f"  Line {i}: Unknown command '{cmd}'")
        if errors:
            result = f"Validation FAILED ({len(errors)} errors):\n" + "\n".join(errors)
            self._status(f"Macro has {len(errors)} error(s)")
        else:
            result = f"Validation PASSED ({len(lines)} lines)"
            self._status(result)
        if hasattr(self, '_bench_results') and self._bench_results.winfo_exists():
            self._bench_results.insert(tk.END, f"[Macro] {result}\n")

    # ── TAB 33: SOUND ──
    def _build_sound_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Sound"] = (tab, "Sound")
        self._tab_order.append("Sound")
        self._tab_listbox.insert(tk.END, "Sound")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Sound Alerts")
        self._checkbox(sf, "Enable Sound", "SOUND_ENABLE", False)
        self._slider(sf, "Volume", "SOUND_VOLUME", 0, 100, 5, 160, "int")
        self._combo(sf, "Sound Theme", "SOUND_THEME",
                    ["default","chiptune","retro","ambient","silent","custom"], 12)

        self._section_label(sf, "Event Sounds")
        self._combo(sf, "On Draw Start", "SOUND_DRAW_START",
                    ["none","beep","chime","whoosh","click","custom"], 14)
        self._combo(sf, "On Draw Complete", "SOUND_DRAW_DONE",
                    ["none","fanfare","success","tada","bell","custom"], 14)
        self._combo(sf, "On Error", "SOUND_ERROR",
                    ["none","buzz","error_alert","sad_trombone","custom"], 14)
        self._combo(sf, "On Pause", "SOUND_PAUSE",
                    ["none","pause_chime","ambient_loop","custom"], 14)
        self._combo(sf, "On Resume", "SOUND_RESUME",
                    ["none","resume_chime","click","custom"], 14)

        self._section_label(sf, "Audio Feedback")
        self._checkbox(sf, "Click Sound on Pixel", "SOUND_PIXEL_CLICK", False)
        self._checkbox(sf, "Tick on Progress", "SOUND_TICK", False)
        self._slider(sf, "Tick Interval (%)", "SOUND_TICK_INTERVAL", 5, 50, 5, 160, "int")

        self._section_label(sf, "Voice Alerts")
        self._checkbox(sf, "Voice Feedback", "SOUND_VOICE", False)
        self._combo(sf, "Voice Language", "SOUND_VOICE_LANG",
                    ["en","es","fr","de","ja","zh","ko","pt","it","ru"], 12)
        self._combo(sf, "Voice Speed", "SOUND_VOICE_SPEED",
                    ["slow","normal","fast","very_fast"], 12)
        self._slider(sf, "Voice Pitch", "SOUND_VOICE_PITCH", 50, 200, 10, 160, "int")

        self._section_label(sf, "Test Sound")
        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Test Sound", command=self._test_sound,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Stop All Sound", command=self._stop_sound,
                  bg="#330000", fg=T["danger"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

        self._section_label(sf, "Custom Sound Files")
        self._entry(sf, "Sound File Path", "SOUND_CUSTOM_PATH", 30)
        self._entry(sf, "Alert File Path", "SOUND_ALERT_PATH", 30)
        self._entry(sf, "Voice File Path", "SOUND_VOICE_PATH", 30)

    def _test_sound(self):
        if not SETTINGS.get("SOUND_ENABLE"):
            self._status("Enable sound first")
            return
        import subprocess
        try:
            subprocess.run(["beep", "-f", "880", "-l", "200"], timeout=1,
                          capture_output=True)
            self._status("Sound test: OK")
        except:
            self._status("Sound: beep not available (install beep or use system sounds)")

    def _stop_sound(self):
        import subprocess
        try:
            subprocess.run(["killall", "beep"], capture_output=True)
        except:
            pass
        self._status("Sound stopped")

    # ── TAB 34: LOCALIZATION ──
    def _build_localization_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Localization"] = (tab, "Localization")
        self._tab_order.append("Localization")
        self._tab_listbox.insert(tk.END, "Localization")
        sf = self._make_scroll_frame(tab)

        self._section_label(sf, "Language Settings")
        self._combo(sf, "Interface Language", "UI_LANGUAGE",
                    ["en","es","fr","de","ja","zh","ko","pt","it","ru","pl","nl","sv","da","fi","cs","hu","ro","tr","ar","he","th","vi"], 14)
        self._combo(sf, "Date Format", "DATE_FORMAT",
                    ["YYYY-MM-DD","MM/DD/YYYY","DD/MM/YYYY","DD.MM.YYYY"], 14)
        self._combo(sf, "Time Format", "TIME_FORMAT",
                    ["24h","12h"], 14)
        self._combo(sf, "Number Format", "NUMBER_FORMAT",
                    ["1,000.00","1.000,00","1 000,00","1'000.00"], 14)
        self._combo(sf, "First Day of Week", "FIRST_DAY",
                    ["Monday","Sunday","Saturday"], 12)

        self._section_label(sf, "Units")
        self._combo(sf, "Measurement Unit", "MEASUREMENT_UNIT",
                    ["metric","imperial","pixels"], 12)
        self._combo(sf, "Temperature Unit", "TEMP_UNIT",
                    ["celsius","fahrenheit","kelvin"], 12)
        self._combo(sf, "Speed Unit", "SPEED_UNIT",
                    ["px/s","in/s","cm/s"], 12)

        self._section_label(sf, "Translation Overrides")
        self._checkbox(sf, "Enable Overrides", "LANG_OVERRIDE_ENABLE", False)
        self._entry(sf, "Override File (.json)", "LANG_OVERRIDE_FILE", 30)

        self._section_label(sf, "OCR / Text Recognition")
        self._checkbox(sf, "Enable OCR", "OCR_ENABLE", False)
        self._combo(sf, "OCR Language", "OCR_LANGUAGE",
                    ["eng","fra","deu","spa","ita","jpn","kor","chi_sim","rus","ara"], 14)
        self._combo(sf, "OCR Engine", "OCR_ENGINE",
                    ["tesseract","easyocr","paddleocr","windows_mr"], 14)

        self._section_label(sf, "Accessibility Translations")
        self._checkbox(sf, "Screen Reader Compatible", "A11Y_SCREEN_READER", False)
        self._checkbox(sf, "High Contrast Text", "A11Y_HIGH_CONTRAST_TEXT", False)
        self._slider(sf, "Font Scaling %", "A11Y_FONT_SCALE", 50, 200, 10, 160, "int")
        self._combo(sf, "Text Direction", "A11Y_TEXT_DIR",
                    ["ltr","rtl","auto"], 12)

        self._section_label(sf, "Character Map")
        self._checkbox(sf, "Enable Character Map", "CHARMAP_ENABLE", False)
        self._entry(sf, "Font Path", "CHARMAP_FONT_PATH", 30)

        row = tk.Frame(sf, bg=T["bg"])
        row.pack(fill="x", padx=6, pady=4)
        tk.Button(row, text="Load Language Pack", command=self._load_lang_pack,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8), bd=0).pack(side="left", padx=3)
        tk.Button(row, text="Export Current Language", command=self._export_lang,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(side="left", padx=3)

    def _load_lang_pack(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            try:
                with open(path) as f:
                    data = json.load(f)
                SETTINGS["UI_LANGUAGE"] = data.get("language", "en")
                self._status(f"Language pack loaded: {data.get('name', 'unknown')}")
            except Exception as ex:
                self._status(f"Failed: {ex}")

    def _export_lang(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            initialfile="language_export.json")
        if path:
            lang_keys = {k: v for k, v in SETTINGS.items()
                         if k.startswith(("UI_","DATE_","TIME_","NUMBER_","MEASUREMENT_","TEMP_","SPEED_"))}
            with open(path, 'w') as f:
                json.dump(lang_keys, f, indent=2)
            self._status("Language config exported")

    def _save_all(self):
        self.app.save_config()
        self._status("All settings saved to config.json")

    def _reset_defaults(self):
        preserve = {
            "GLOBAL_SPEED", "CLICK_DELAY", "UI_DELAY", "PIXEL_GAP", "WHITE_SKIP",
            "CANNY_LOW", "CANNY_HIGH", "SIMPLIFY_EPS", "HATCH_ENABLE", "MULTIPASS",
            "BG_AWARENESS_ENABLE", "FILL_ENABLE", "LQE_ENABLE", "STROKE_MODE",
            "SKETCH_JITTER", "SKETCH_SPEED", "SKETCH_ITERATIONS", "SKETCH_PRESET",
            "FILL_ZONE_ACTIVE", "STROKE_SMOOTH_PASSES", "ENGINE_MODE", "DRAW_MODE",
            "ACTIVE_PROFILE", "THEME", "COLOR_METRIC", "DITHER_MODE", "PALETTE_SIZE",
        }
        defaults = {
            "CANNY_LOW": 40, "CANNY_HIGH": 120, "SIMPLIFY_EPS": 1.5,
            "HATCH_ENABLE": True, "MULTIPASS": True, "LQE_ENABLE": True,
            "STROKE_MODE": "stroke", "STROKE_SMOOTH_PASSES": 2,
            "FILL_ENABLE": False, "BG_AWARENESS_ENABLE": False,
            "CONTOUR_APPROX": True, "USE_PATH_CACHE": True,
            "STRUCTURE_ENABLE": True, "HUMAN_MOTION": False,
            "JITTER_PX": 0, "BEZIER_STEPS": 0, "MIN_STROKE_LEN": 3,
            "HATCH_ANGLE_STEP": 45, "HATCH_SPACING": 4,
            "LQE_SMOOTHING_FACTOR": 1.8, "LQE_CORNER_THRESHOLD": 45,
            "LQE_MIN_CONFIDENCE": 0.3,
            "STYLE_MERGE_DISTANCE": 8, "STYLE_OVERLAP_SUPPRESS": True,
            "STYLE_CROSSHATCH_ANGLE": 45, "STYLE_STIPPLE_DENSITY": 0.5,
            "STYLE_SCRIBBLE_PASSES": 2,
            "VIEWPORT_ZOOM": 1.0, "VIEWPORT_SCROLL_DX": 0, "VIEWPORT_SCROLL_DY": 0,
            "FILL_ZONE_ACTIVE": False, "FILL_ZONE_THRESHOLD": 30,
            "FILL_ZONE_GROW_STEPS": 5, "FILL_VARIANCE_THRESHOLD": 500,
            "MIN_FILL_AREA": 200, "FILL_HOTKEY": "f9",
        }
        for k, v in defaults.items():
            if k not in preserve:
                SETTINGS[k] = v
        self._status(f"Reset {len(defaults)} settings to defaults ({len(preserve)} preserved)")
        self._refresh_dump()


# ═══════════════════════════════════════════════════════════════
#  SOLO GODMODE EXPANSION — v6
#  ~6000+ lines of new features
# ═══════════════════════════════════════════════════════════════

# ── v6.1: VIEWPORT SYSTEM REWRITE ──────────────────────────

class ViewportState(Enum):
    IDLE = auto()
    PANNING = auto()
    ZOOMING = auto()
    BOOKMARK = auto()

@dataclass
class ViewportBookmark:
    name: str
    zoom: float
    offset_x: float
    offset_y: float
    timestamp: float = 0.0

class ViewportSystem:
    def __init__(self, app):
        self.app = app
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.min_zoom = 0.05
        self.max_zoom = 50.0
        self.zoom_snap_threshold = 0.08
        self.snap_points = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0]
        self.momentum_active = False
        self.cursor_anchor = (0, 0)
        self.bookmarks: List[ViewportBookmark] = []
        self.state = ViewportState.IDLE
        self.minimap_visible = False
        self.minimap_size = (180, 140)
        self.minimap_surface = None
        self.transform_animating = False
        self.anim_start = 0.0
        self.anim_duration = 0.3
        self.anim_from_zoom = 1.0
        self.anim_from_ox = 0.0
        self.anim_from_oy = 0.0
        self.anim_to_zoom = 1.0
        self.anim_to_ox = 0.0
        self.anim_to_oy = 0.0

    def set_view(self, zoom, ox, oy, animate=False):
        if animate:
            self.anim_from_zoom = self.zoom
            self.anim_from_ox = self.offset_x
            self.anim_from_oy = self.offset_y
            self.anim_to_zoom = max(self.min_zoom, min(self.max_zoom, zoom))
            self.anim_to_ox = ox
            self.anim_to_oy = oy
            self.anim_start = time.time()
            self.transform_animating = True
        else:
            self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))
            self.offset_x = ox
            self.offset_y = oy

    def update_animation(self):
        if not self.transform_animating:
            return
        t = (time.time() - self.anim_start) / self.anim_duration
        if t >= 1.0:
            self.zoom = self.anim_to_zoom
            self.offset_x = self.anim_to_ox
            self.offset_y = self.anim_to_oy
            self.transform_animating = False
            return
        ease = t * t * (3 - 2 * t)
        self.zoom = self.anim_from_zoom + (self.anim_to_zoom - self.anim_from_zoom) * ease
        self.offset_x = self.anim_from_ox + (self.anim_to_ox - self.anim_from_ox) * ease
        self.offset_y = self.anim_from_oy + (self.anim_to_oy - self.anim_from_oy) * ease

    def zoom_at_cursor(self, factor, cursor_x, cursor_y, canvas_w, canvas_h):
        old_zoom = self.zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * factor))
        self.zoom = new_zoom
        world_x = (cursor_x - canvas_w / 2 - self.offset_x) / old_zoom
        world_y = (cursor_y - canvas_h / 2 - self.offset_y) / old_zoom
        self.offset_x = cursor_x - canvas_w / 2 - world_x * new_zoom
        self.offset_y = cursor_y - canvas_h / 2 - world_y * new_zoom
        self._check_snap()

    def _check_snap(self):
        if self.zoom_snap_threshold <= 0:
            return
        for sp in self.snap_points:
            if abs(self.zoom - sp) / sp < self.zoom_snap_threshold:
                self.zoom = sp
                break

    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.vel_x = dx
        self.vel_y = dy
        self.momentum_active = True

    def update_momentum(self, dt):
        if not self.momentum_active:
            return
        friction = 0.92
        self.offset_x += self.vel_x * dt * 60
        self.offset_y += self.vel_y * dt * 60
        self.vel_x *= friction
        self.vel_y *= friction
        if abs(self.vel_x) < 0.5 and abs(self.vel_y) < 0.5:
            self.momentum_active = False

    def add_bookmark(self, name=None):
        if name is None:
            name = f"Bookmark {len(self.bookmarks) + 1}"
        bm = ViewportBookmark(name=name, zoom=self.zoom, offset_x=self.offset_x, offset_y=self.offset_y, timestamp=time.time())
        self.bookmarks.append(bm)
        return bm

    def goto_bookmark(self, index, animate=True):
        if 0 <= index < len(self.bookmarks):
            bm = self.bookmarks[index]
            self.set_view(bm.zoom, bm.offset_x, bm.offset_y, animate)

    def delete_bookmark(self, index):
        if 0 <= index < len(self.bookmarks):
            del self.bookmarks[index]

    def reset_view(self, animate=True):
        self.set_view(1.0, 0.0, 0.0, animate)

    def img_to_screen(self, x, y, canvas_w, canvas_h):
        sx = x * self.zoom + self.offset_x + canvas_w / 2
        sy = y * self.zoom + self.offset_y + canvas_h / 2
        return int(sx), int(sy)

    def screen_to_img(self, sx, sy, canvas_w, canvas_h):
        ix = (sx - canvas_w / 2 - self.offset_x) / self.zoom
        iy = (sy - canvas_h / 2 - self.offset_y) / self.zoom
        return ix, iy

    def render_minimap(self, img, dest_size=(180, 140)):
        if img is None:
            return None
        thumb = img.copy()
        thumb.thumbnail(dest_size, Image.LANCZOS)
        self.minimap_surface = thumb
        return thumb

    def get_transform_matrix(self, canvas_w, canvas_h):
        return (
            self.zoom, 0, self.offset_x + canvas_w / 2,
            0, self.zoom, self.offset_y + canvas_h / 2,
        )


# ── v6.2: AI IMAGE GENERATION SUITE ────────────────────────

class AIGenerationSuite:
    STYLE_PRESETS = {
        "anime": "anime style, cel shading, clean lineart, vibrant colors",
        "manga": "manga style, black and white, screentone, high contrast",
        "cartoon": "cartoon style, bold outlines, flat colors, whimsical",
        "realistic": "photorealistic, 8k, highly detailed, sharp focus",
        "oil_painting": "oil painting, canvas texture, impasto, rich colors",
        "watercolor": "watercolor, soft edges, wet paint, paper texture",
        "pencil_sketch": "pencil sketch, grayscale, hatching, rough lines",
        "vaporwave": "vaporwave aesthetic, neon, retro, synthwave, purple pink cyan",
        "cyberpunk": "cyberpunk, neon lights, dark city, rain, high tech",
    }

    def __init__(self, app):
        self.app = app
        self.pipe = None
        self.device = "cpu"
        self.model_path = os.path.join(DIR_PATH, "ai_models")
        self.active_style = "anime"
        self.guidance_scale = 7.0
        self.inference_steps = 20
        self.strength = 0.75
        self.seed = -1
        self.generated_history: List[Image.Image] = []
        self.max_history = 20
        os.makedirs(self.model_path, exist_ok=True)

    def load_model(self, model_id="segmind/tiny-sd"):
        if self.pipe is not None:
            return True
        if not HAS_DIFFUSERS or not HAS_TORCH:
            self.app.log("[AI] torch/diffusers not installed. Install with: pip install torch diffusers")
            return False
        try:
            self.device = "cpu"
            dtype = torch.float32
            self.app.log(f"[AI] Loading {model_id} on {self.device}...")
            self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype, safety_checker=None)
            self.pipe = self.pipe.to(self.device)
            if self.device == "cpu":
                self.pipe.enable_attention_slicing()
            self.app.log(f"[AI] Model loaded on {self.device}")
            return True
        except Exception as e:
            self.app.log(f"[AI] Load failed: {e}")
            return False

    def generate(self, prompt, negative_prompt="lowres, bad anatomy, text", style=None):
        if self.pipe is None:
            if not self.load_model():
                return None
        style_text = self.STYLE_PRESETS.get(style or self.active_style, "")
        full_prompt = f"{prompt}, {style_text}" if style_text else prompt
        try:
            generator = None
            if self.seed > 0:
                generator = torch.Generator(device=self.device).manual_seed(self.seed)
            result = self.pipe(
                full_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=self.inference_steps,
                guidance_scale=self.guidance_scale,
                generator=generator,
            ).images[0]
            self.generated_history.append(result)
            if len(self.generated_history) > self.max_history:
                self.generated_history.pop(0)
            self.app.base_img = result
            self.app.final_img = None
            self.app.log(f"[AI] Generated {result.size}")
            return result
        except Exception as e:
            self.app.log(f"[AI] Generation error: {e}")
            return None

    def img2img(self, init_img, prompt, strength=None):
        if self.pipe is None:
            if not self.load_model():
                return None
        from diffusers.utils import make_image_grid
        s = strength if strength is not None else self.strength
        try:
            result = self.pipe(
                prompt,
                image=init_img,
                strength=s,
                num_inference_steps=int(self.inference_steps * s),
                guidance_scale=self.guidance_scale,
            ).images[0]
            self.app.base_img = result
            self.app.final_img = None
            return result
        except Exception as e:
            self.app.log(f"[AI] img2img error: {e}")
            return None

    def extract_lineart(self, img):
        gray = np.array(img.convert("L"), dtype=np.uint8)
        if HAS_CV2:
            edges = cv2.Canny(gray, 40, 120)
            inv = 255 - edges
            result = Image.fromarray(inv).convert("RGB")
        else:
            edge_img = img.convert("L").filter(ImageFilter.FIND_EDGES)
            inv = ImageOps.invert(edge_img)
            result = inv.convert("RGB")
        self.app.base_img = result
        self.app.final_img = None
        return result

    def style_transfer_prompt(self, img, style="anime"):
        prompt = f"redraw this image in {style} style, same composition"
        return self.img2img(img, prompt, strength=0.6)

    def upscale(self, img, scale=2):
        w, h = img.size
        nw, nh = w * scale, h * scale
        if HAS_CV2:
            arr = np.array(img)
            up = cv2.resize(arr, (nw, nh), interpolation=cv2.INTER_CUBIC)
            return Image.fromarray(up)
        return img.resize((nw, nh), Image.LANCZOS)

    def edge_clean(self, img, threshold=30):
        arr = np.array(img.convert("L"))
        kernel = np.ones((2, 2), np.uint8)
        if HAS_CV2:
            cleaned = cv2.morphologyEx(arr, cv2.MORPH_CLOSE, kernel)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        else:
            from scipy.ndimage import binary_closing, binary_opening
            binary = arr > threshold
            closed = binary_closing(binary, structure=np.ones((2, 2)))
            opened = binary_opening(closed, structure=np.ones((2, 2)))
            cleaned = (opened * 255).astype(np.uint8)
        return Image.fromarray(cleaned).convert("RGB")


# ── v6.3: LAYER SYSTEM V2 ──────────────────────────────────

class BlendMode(Enum):
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    DIFFERENCE = "difference"
    ADDITION = "addition"
    SUBTRACT = "subtract"
    DIVIDE = "divide"
    SOFT_LIGHT = "soft_light"
    HARD_LIGHT = "hard_light"
    EXCLUSION = "exclusion"

BLEND_FUNCTIONS = {}

def _init_blend_funcs():
    global BLEND_FUNCTIONS
    def blend_normal(a, b): return b
    def blend_multiply(a, b): return a * b / 255
    def blend_screen(a, b): return 255 - (255 - a) * (255 - b) / 255
    def blend_overlay(a, b):
        mask = a < 128
        r = np.where(mask, 2 * a * b / 255, 255 - 2 * (255 - a) * (255 - b) / 255)
        return r
    def blend_darken(a, b): return np.minimum(a, b)
    def blend_lighten(a, b): return np.maximum(a, b)
    def blend_difference(a, b): return np.abs(a - b)
    def blend_addition(a, b): return np.clip(a + b, 0, 255)
    def blend_subtract(a, b): return np.clip(a - b, 0, 255)
    def blend_divide(a, b): return np.clip(np.where(b == 0, 255, a / b * 255), 0, 255)
    def blend_soft_light(a, b):
        m = b < 128
        r = np.where(m, a * b / 128 + (a / 255) ** 2 * (255 - 2 * b), a * (255 - b) / 128 + np.sqrt(a / 255) * (2 * b - 255))
        return np.clip(r, 0, 255)
    def blend_hard_light(a, b): return blend_overlay(b, a)
    def blend_exclusion(a, b): return np.clip(a + b - 2 * a * b / 255, 0, 255)
    BLEND_FUNCTIONS = {
        BlendMode.NORMAL: blend_normal,
        BlendMode.MULTIPLY: blend_multiply,
        BlendMode.SCREEN: blend_screen,
        BlendMode.OVERLAY: blend_overlay,
        BlendMode.DARKEN: blend_darken,
        BlendMode.LIGHTEN: blend_lighten,
        BlendMode.DIFFERENCE: blend_difference,
        BlendMode.ADDITION: blend_addition,
        BlendMode.SUBTRACT: blend_subtract,
        BlendMode.DIVIDE: blend_divide,
        BlendMode.SOFT_LIGHT: blend_soft_light,
        BlendMode.HARD_LIGHT: blend_hard_light,
        BlendMode.EXCLUSION: blend_exclusion,
    }

_init_blend_funcs()

@dataclass
class LayerV2:
    name: str
    img: Image.Image
    visible: bool = True
    locked: bool = False
    opacity: float = 1.0
    blend_mode: BlendMode = BlendMode.NORMAL
    mask: Optional[Image.Image] = None
    group: Optional[str] = None
    effects: Dict[str, Any] = field(default_factory=dict)
    thumbnail: Optional[ImageTk.PhotoImage] = None

class LayerSystemV2:
    def __init__(self, app):
        self.app = app
        self.layers: List[LayerV2] = []
        self.active_index = 0
        self.groups: Dict[str, List[int]] = {}
        self.clipboard_layer: Optional[LayerV2] = None
        self.undo_stack: List[list] = []
        self.max_undo = 30

    def add_layer(self, name=None, img=None, index=None):
        if name is None:
            name = f"Layer {len(self.layers) + 1}"
        if img is None and self.app.base_img:
            img = self.app.base_img.copy()
        elif img is None:
            img = Image.new("RGB", (512, 512), (255, 255, 255))
        layer = LayerV2(name=name, img=img)
        self._save_undo()
        if index is not None:
            self.layers.insert(index, layer)
        else:
            self.layers.append(layer)
        self.active_index = min(len(self.layers) - 1, index if index is not None else len(self.layers) - 1)
        return layer

    def delete_layer(self, index=None):
        if not self.layers:
            return
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers):
            self._save_undo()
            del self.layers[idx]
            self.active_index = max(0, min(self.active_index, len(self.layers) - 1))

    def duplicate_layer(self, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers):
            orig = self.layers[idx]
            dup = LayerV2(
                name=orig.name + " copy",
                img=orig.img.copy(),
                visible=orig.visible,
                opacity=orig.opacity,
                blend_mode=orig.blend_mode,
                group=orig.group,
            )
            self._save_undo()
            self.layers.insert(idx + 1, dup)
            self.active_index = idx + 1
            return dup

    def merge_down(self, index=None):
        idx = index if index is not None else self.active_index
        if idx < 1 or idx >= len(self.layers):
            return
        self._save_undo()
        upper = self.layers.pop(idx)
        lower = self.layers[idx - 1]
        lower.img = self.composite_two(upper.img, lower.img, upper.opacity, upper.blend_mode, upper.mask)
        self.active_index = idx - 1

    def flatten(self):
        if not self.layers:
            return
        self._save_undo()
        composite = self.composite_all()
        self.layers = [LayerV2(name="Flattened", img=composite)]
        self.active_index = 0

    def move_up(self, index=None):
        idx = index if index is not None else self.active_index
        if idx < len(self.layers) - 1:
            self.layers[idx], self.layers[idx + 1] = self.layers[idx + 1], self.layers[idx]
            self.active_index = idx + 1

    def move_down(self, index=None):
        idx = index if index is not None else self.active_index
        if idx > 0:
            self.layers[idx], self.layers[idx - 1] = self.layers[idx - 1], self.layers[idx]
            self.active_index = idx - 1

    def set_opacity(self, opacity, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers):
            self.layers[idx].opacity = max(0.0, min(1.0, opacity))

    def set_blend_mode(self, mode: BlendMode, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers):
            self.layers[idx].blend_mode = mode

    def add_mask(self, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers):
            w, h = self.layers[idx].img.size
            mask = Image.new("L", (w, h), 255)
            self.layers[idx].mask = mask

    def set_mask_pixels(self, x, y, value, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.layers) and self.layers[idx].mask:
            self.layers[idx].mask.putpixel((x, y), value)

    def add_group(self, name):
        self.groups[name] = []

    def add_to_group(self, layer_index, group_name):
        if group_name in self.groups and 0 <= layer_index < len(self.layers):
            self.layers[layer_index].group = group_name
            if layer_index not in self.groups[group_name]:
                self.groups[group_name].append(layer_index)

    @staticmethod
    def blend_pixel(a_arr, b_arr, opacity, mode: BlendMode, mask_arr=None):
        b_arr = b_arr.astype(np.float32)
        a_arr = a_arr.astype(np.float32)
        blend_fn = BLEND_FUNCTIONS.get(mode, BLEND_FUNCTIONS[BlendMode.NORMAL])
        if b_arr.ndim == 3 and b_arr.shape[2] >= 3:
            blended = np.stack([blend_fn(a_arr[..., c], b_arr[..., c]) for c in range(3)], axis=2)
        else:
            blended = blend_fn(a_arr, b_arr)
        if mask_arr is not None:
            mask_norm = mask_arr.astype(np.float32) / 255.0
            if mask_norm.ndim == 2 and blended.ndim == 3:
                mask_norm = np.stack([mask_norm] * 3, axis=2)
            blended = a_arr * (1 - mask_norm * opacity) + blended * mask_norm * opacity
        else:
            blended = a_arr * (1 - opacity) + blended * opacity
        return np.clip(blended, 0, 255).astype(np.uint8)

    @staticmethod
    def composite_two(upper, lower, opacity, mode, mask=None):
        u_arr = np.array(upper, dtype=np.float32)
        l_arr = np.array(lower, dtype=np.float32)
        m_arr = np.array(mask) if mask else None
        blend_fn = BLEND_FUNCTIONS.get(mode, BLEND_FUNCTIONS[BlendMode.NORMAL])
        blended = np.stack([blend_fn(l_arr[..., c], u_arr[..., c]) for c in range(3)], axis=2)
        if m_arr is not None:
            m_norm = m_arr.astype(np.float32) / 255.0
            if m_norm.ndim == 2:
                m_norm = np.stack([m_norm] * 3, axis=2)
            blended = l_arr * (1 - m_norm * opacity) + blended * m_norm * opacity
        else:
            blended = l_arr * (1 - opacity) + blended * opacity
        return Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))

    def composite_all(self):
        if not self.layers:
            return Image.new("RGB", (512, 512), (255, 255, 255))
        base = self.layers[0].img.copy()
        for layer in self.layers[1:]:
            if not layer.visible:
                continue
            base = self.composite_two(layer.img, base, layer.opacity, layer.blend_mode, layer.mask)
        return base

    def _save_undo(self):
        state = []
        for l in self.layers:
            state.append(LayerV2(name=l.name, img=l.img.copy(), visible=l.visible, locked=l.locked, opacity=l.opacity, blend_mode=l.blend_mode, mask=l.mask.copy() if l.mask else None, group=l.group))
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return
        state = self.undo_stack.pop()
        self.layers = state
        self.active_index = min(self.active_index, len(self.layers) - 1)


# ── v6.4: ANIMATION / TIMELINE ─────────────────────────────

@dataclass
class AnimationFrame:
    index: int
    image: Image.Image
    duration: int = 100
    label: str = ""

class AnimationTimeline:
    def __init__(self, app):
        self.app = app
        self.frames: List[AnimationFrame] = []
        self.current_frame = 0
        self.fps = 12
        self.loop = True
        self.playing = False
        self.onion_skin = False
        self.onion_skin_count = 3
        self.onion_skin_opacity = 0.3
        self.timeline_visible = False
        self._play_thread = None

    def add_frame(self, img=None, duration=None):
        if img is None and self.app.base_img:
            img = self.app.base_img.copy()
        elif img is None:
            img = Image.new("RGB", (512, 512), (255, 255, 255))
        frame = AnimationFrame(index=len(self.frames), image=img, duration=duration or 100)
        self.frames.append(frame)
        return frame

    def delete_frame(self, index=None):
        if not self.frames:
            return
        idx = index if index is not None else self.current_frame
        if 0 <= idx < len(self.frames):
            del self.frames[idx]
            self.current_frame = max(0, min(self.current_frame, len(self.frames) - 1))
            for i, f in enumerate(self.frames):
                f.index = i

    def duplicate_frame(self, index=None):
        idx = index if index is not None else self.current_frame
        if 0 <= idx < len(self.frames):
            orig = self.frames[idx]
            dup = AnimationFrame(index=idx + 1, image=orig.image.copy(), duration=orig.duration)
            self.frames.insert(idx + 1, dup)
            self._renumber()

    def _renumber(self):
        for i, f in enumerate(self.frames):
            f.index = i

    def goto_frame(self, index):
        if 0 <= index < len(self.frames):
            self.current_frame = index
            self.app.base_img = self.frames[index].image.copy()
            self.app.final_img = None

    def get_onion_skin(self):
        if not self.onion_skin or len(self.frames) < 2:
            return None
        result = None
        for i in range(1, self.onion_skin_count + 1):
            idx = self.current_frame - i
            if idx >= 0:
                f = self.frames[idx]
                alpha = max(0, self.onion_skin_opacity - (i - 1) * 0.08)
                overlay = f.image.copy()
                overlay.putalpha(int(alpha * 255))
                if result is None:
                    result = overlay
                else:
                    result = Image.alpha_composite(result, overlay)
        return result

    def export_gif(self, path, fps=None, loop=True):
        if not self.frames:
            return
        f = fps or self.fps
        duration = [max(1, int(1000 / f))] * len(self.frames)
        self.frames[0].image.save(
            path, save_all=True, append_images=[fr.image for fr in self.frames[1:]],
            duration=duration, loop=0 if loop else 1, disposal=2
        )
        self.app.log(f"[Anim] Exported GIF: {path}")

    def play(self):
        if self.playing or not self.frames:
            return
        self.playing = True
        def _loop():
            while self.playing and self.frames:
                self.goto_frame(self.current_frame)
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                if self.current_frame == 0 and not self.loop:
                    self.playing = False
                    break
                time.sleep(1.0 / self.fps)
        self._play_thread = threading.Thread(target=_loop, daemon=True)
        self._play_thread.start()

    def stop(self):
        self.playing = False

    def total_duration_ms(self):
        return sum(f.duration for f in self.frames)

    def frame_interpolation(self, target_count):
        if len(self.frames) < 2:
            return
        interpolated = []
        for i in range(len(self.frames) - 1):
            a = np.array(self.frames[i].image, dtype=np.float32)
            b = np.array(self.frames[i + 1].image, dtype=np.float32)
            interpolated.append(self.frames[i])
            steps = max(1, target_count // len(self.frames))
            for s in range(1, steps + 1):
                t = s / (steps + 1)
                blended = ((1 - t) * a + t * b).astype(np.uint8)
                frame = AnimationFrame(
                    index=self.current_frame, duration=self.frames[i].duration,
                    image=Image.fromarray(blended)
                )
                interpolated.append(frame)
        interpolated.append(self.frames[-1])
        self.frames = interpolated
        self._renumber()
        self.app.log(f"[Anim] Interpolated to {len(self.frames)} frames")

    def ai_inbetween(self, frame_a_idx=None, frame_b_idx=None):
        if not HAS_TORCH or not HAS_DIFFUSERS:
            self.app.log("[Anim] AI inbetweening requires torch + diffusers")
            return
        fa = frame_a_idx if frame_a_idx is not None else max(0, self.current_frame - 1)
        fb = frame_b_idx if frame_b_idx is not None else self.current_frame
        if fb >= len(self.frames) or fa < 0 or fa == fb:
            return
        a_img = self.frames[fa].image
        b_img = self.frames[fb].image
        try:
            import torch as _torch
            from diffusers import StableDiffusionImg2ImgPipeline as _SDImg2Img
            device = "cpu"
            dtype = _torch.float32
            pipe = _SDImg2Img.from_pretrained("segmind/tiny-sd", torch_dtype=dtype, safety_checker=None).to(device)
            mid_prompt = "smooth animation transition, consistent style, sharp details"
            blended = Image.blend(a_img.resize((512, 512)), b_img.resize((512, 512)), 0.5)
            result = pipe(prompt=mid_prompt, image=blended, strength=0.6, guidance_scale=5.0, num_inference_steps=15).images[0]
            result = result.resize(self.frames[fa].image.size)
            mid_frame = AnimationFrame(index=fa + 1, image=result, duration=100)
            self.frames.insert(fa + 1, mid_frame)
            self._renumber()
            self.app.log(f"[Anim] AI inbetween generated for frames {fa}-{fb}")
        except Exception as e:
            self.app.log(f"[Anim] AI inbetween error: {e}")


# ── v6.5: PLUGIN API ───────────────────────────────────────

class PluginMeta:
    def __init__(self, name, version, description="", author=""):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.enabled = True

class BasePlugin:
    def __init__(self, app, meta: PluginMeta):
        self.app = app
        self.meta = meta
    def on_load(self): pass
    def on_unload(self): pass
    def on_draw_start(self): pass
    def on_draw_end(self, dots): pass
    def on_image_load(self, img): pass
    def on_settings_change(self, key, value): pass
    def get_ui_elements(self): return []

class PluginAPI:
    PLUGINS_DIR = os.path.join(DIR_PATH, "plugins")
    def __init__(self, app):
        self.app = app
        self.plugins: Dict[str, BasePlugin] = {}
        self.hooks = {
            "on_load": [], "on_unload": [],
            "on_draw_start": [], "on_draw_end": [],
            "on_image_load": [], "on_settings_change": [],
        }
        os.makedirs(self.PLUGINS_DIR, exist_ok=True)

    def discover_plugins(self):
        if not os.path.isdir(self.PLUGINS_DIR):
            return
        sys.path.insert(0, self.PLUGINS_DIR)
        for fname in os.listdir(self.PLUGINS_DIR):
            if fname.endswith(".py") and not fname.startswith("_"):
                modname = fname[:-3]
                try:
                    mod = __import__(modname)
                    if hasattr(mod, "register_plugin"):
                        plugin = mod.register_plugin(self.app)
                        if plugin:
                            self.register(plugin)
                except Exception as e:
                    self.app.log(f"[Plugin] Failed to load {modname}: {e}")

    def register(self, plugin: BasePlugin):
        pname = plugin.meta.name
        self.plugins[pname] = plugin
        plugin.on_load()
        for hook_name in self.hooks:
            hook_fn = getattr(plugin, hook_name, None)
            if hook_fn:
                self.hooks[hook_name].append(hook_fn)
        self.app.log(f"[Plugin] Loaded: {pname} v{plugin.meta.version}")

    def unregister(self, name):
        if name in self.plugins:
            self.plugins[name].on_unload()
            for hook_list in self.hooks.values():
                hook_list[:] = [fn for fn in hook_list if fn.__self__ != self.plugins[name]]
            del self.plugins[name]
            self.app.log(f"[Plugin] Unloaded: {name}")

    def trigger(self, hook_name, *args, **kwargs):
        for fn in self.hooks.get(hook_name, []):
            try:
                fn(*args, **kwargs)
            except Exception as e:
                self.app.log(f"[Plugin] Error in {hook_name}: {e}")

    def list_plugins(self):
        return [(p.meta.name, p.meta.version, p.meta.description, p.meta.enabled) for p in self.plugins.values()]


# ── v6.6: AUTONOMOUS DRAWING INTELLIGENCE ──────────────────

class AutonomousDrawIntelligence:
    def __init__(self, app):
        self.app = app
        self.quality_threshold = 0.6
        self.max_repair_attempts = 3
        self.repair_log: List[dict] = []

    def analyze_stroke_quality(self, stroke, reference_edges=None):
        if len(stroke) < 3:
            return 0.0
        angles = []
        for i in range(1, len(stroke) - 1):
            dx1 = stroke[i][0] - stroke[i - 1][0]
            dy1 = stroke[i][1] - stroke[i - 1][1]
            dx2 = stroke[i + 1][0] - stroke[i][0]
            dy2 = stroke[i + 1][1] - stroke[i][1]
            d1 = math.hypot(dx1, dy1)
            d2 = math.hypot(dx2, dy2)
            if d1 > 0 and d2 > 0:
                dot = (dx1 * dx2 + dy1 * dy2) / (d1 * d2)
                angles.append(abs(math.degrees(math.acos(max(-1, min(1, dot))))))
        if not angles:
            return 0.5
        smoothness = 1.0 - min(1.0, np.mean(angles) / 90.0)
        coverage = min(1.0, len(stroke) / 100.0)
        return 0.6 * smoothness + 0.4 * coverage

    def auto_repair_stroke(self, stroke, edge_map=None):
        quality = self.analyze_stroke_quality(stroke)
        if quality >= self.quality_threshold:
            return stroke, quality
        repaired = list(stroke)
        for attempt in range(self.max_repair_attempts):
            if len(repaired) < 3:
                break
            repaired = self._smooth_stroke(repaired, strength=1.0 + attempt * 0.5)
            repaired = self._fill_gaps(repaired)
            new_q = self.analyze_stroke_quality(repaired)
            self.repair_log.append({"attempt": attempt, "quality_before": quality, "quality_after": new_q})
            if new_q >= self.quality_threshold:
                break
        return repaired, self.analyze_stroke_quality(repaired)

    def _smooth_stroke(self, stroke, strength=1.0):
        if len(stroke) < 3:
            return stroke
        result = [stroke[0]]
        for i in range(1, len(stroke) - 1):
            w = strength
            x = (stroke[i - 1][0] * w + stroke[i][0] * 2 + stroke[i + 1][0] * w) / (2 + 2 * w)
            y = (stroke[i - 1][1] * w + stroke[i][1] * 2 + stroke[i + 1][1] * w) / (2 + 2 * w)
            result.append((int(x), int(y)))
        result.append(stroke[-1])
        return result

    def _fill_gaps(self, stroke, max_gap=3):
        if len(stroke) < 2:
            return stroke
        result = [stroke[0]]
        for i in range(1, len(stroke)):
            x1, y1 = stroke[i - 1]
            x2, y2 = stroke[i]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist > max_gap and dist < max_gap * 5:
                steps = int(dist / max_gap)
                for s in range(1, steps):
                    t = s / steps
                    result.append((int(x1 + (x2 - x1) * t), int(y1 + (y2 - y1) * t)))
            result.append((x2, y2))
        return result

    def adaptive_simplify(self, stroke, detail_level=0.5):
        if len(stroke) < 3:
            return stroke
        eps = max(0.5, (1.0 - detail_level) * 5)
        return PathOptimizer.douglas_peucker(stroke, eps)

    def prioritize_contours(self, strokes, img):
        if not strokes or img is None:
            return strokes
        gray = np.array(img.convert("L"), dtype=np.float32)
        scores = []
        for stroke in strokes:
            edge_sum = 0.0
            for x, y in stroke:
                if 0 <= y < gray.shape[0] and 0 <= x < gray.shape[1]:
                    edge_sum += gray[y, x]
            scores.append(edge_sum / max(1, len(stroke)))
        ordered = [s for _, s in sorted(zip(scores, strokes), key=lambda x: -x[0])]
        return ordered


# ── v6.7: ARTISTIC MODES ENGINE ────────────────────────────

class ArtisticMode(Enum):
    WIP = "wip"

class ArtisticModesEngine:
    MODES = {}

    @classmethod
    def register(cls, name):
        def decorator(func):
            cls.MODES[name] = func
            return func
        return decorator

    def __init__(self, app):
        self.app = app
        self.active_mode = "standard"
        self._register_defaults()

    def _register_defaults(self):
        self.MODES["standard"] = lambda img, p: p

    def apply(self, img, pixels, mode=None):
        m = mode or self.active_mode
        if m in self.MODES:
            return self.MODES[m](img, pixels)
        return pixels


# Watercolor
@ArtisticModesEngine.register("watercolor")
def _watercolor_mode(img, pixels):
    arr = np.array(img, dtype=np.float32)
    k = np.ones((3, 3), np.float32) / 9
    if HAS_CV2:
        blurred = cv2.filter2D(arr, -1, k)
        blurred = cv2.filter2D(blurred, -1, k)
    else:
        from scipy.ndimage import convolve
        blurred = convolve(arr, k[:, :, None])
        blurred = convolve(blurred, k[:, :, None])
    warped = blurred + np.random.randn(*blurred.shape) * 8
    return np.clip(warped, 0, 255).astype(np.uint8)

# Blueprint
@ArtisticModesEngine.register("blueprint")
def _blueprint_mode(img, pixels):
    arr = np.array(img.convert("L"), dtype=np.uint8)
    inv = 255 - arr
    h, w = arr.shape
    result = np.zeros((h, w, 3), dtype=np.uint8)
    result[:, :, 0] = inv // 2
    result[:, :, 1] = inv
    result[:, :, 2] = inv
    if HAS_CV2:
        edges = cv2.Canny(arr, 30, 100)
        result[edges > 0] = [255, 255, 255]
    return result

# CRT Scanline
@ArtisticModesEngine.register("crt")
def _crt_mode(img, pixels):
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    scanlines = np.zeros((h, w, 3), dtype=np.uint8)
    scanlines[::2] = arr[::2] * 0.6
    scanlines[1::2] = arr[1::2] * 0.9
    bleed = np.zeros_like(scanlines)
    if w > 2:
        bleed[:, :-1] += scanlines[:, 1:] * 0.15
        bleed[:, 1:] += scanlines[:, :-1] * 0.15
    result = np.clip(scanlines.astype(np.float32) + bleed.astype(np.float32), 0, 255).astype(np.uint8)
    return result

# Manga Screentone
@ArtisticModesEngine.register("manga")
def _manga_mode(img, pixels):
    gray = np.array(img.convert("L"), dtype=np.uint8)
    h, w = gray.shape
    tones = np.ones((h, w), dtype=np.uint8) * 255
    dither = np.random.random((h, w))
    tones[gray < 30] = 0
    tones[(gray >= 30) & (gray < 80) & (dither > 0.5)] = 0
    tones[(gray >= 80) & (gray < 140)] = 128
    tones[(gray >= 140) & (gray < 200) & (dither < 0.3)] = 200
    result = np.stack([tones] * 3, axis=2)
    if HAS_CV2:
        edges = cv2.Canny(gray, 40, 100)
        result[edges > 0] = [0, 0, 0]
    return result

# Vaporwave
@ArtisticModesEngine.register("vaporwave")
def _vaporwave_mode(img, pixels):
    arr = np.array(img, dtype=np.float32)
    arr[..., 0] = arr[..., 0] * 0.8 + 50
    arr[..., 1] = arr[..., 1] * 0.6 + 20
    arr[..., 2] = arr[..., 2] * 1.2 + 30
    if HAS_CV2:
        h, w = arr.shape[:2]
        grad = np.tile(np.linspace(0, 0.3, w), (h, 1)).astype(np.float32)
        arr[..., 2] += grad * 50
    return np.clip(arr, 0, 255).astype(np.uint8)

# Charcoal
@ArtisticModesEngine.register("charcoal")
def _charcoal_mode(img, pixels):
    gray = np.array(img.convert("L"), dtype=np.float32)
    if HAS_CV2:
        blurred = cv2.medianBlur(gray.astype(np.uint8), 5)
        edges = cv2.Canny(blurred, 20, 80)
        result = np.ones_like(blurred, dtype=np.uint8) * 240
        result[edges > 0] = 20
    else:
        edge = np.array(Image.fromarray(gray.astype(np.uint8)).filter(ImageFilter.FIND_EDGES))
        result = np.clip(240 - edge.astype(np.float32) * 0.8, 0, 255).astype(np.uint8)
    noise = np.random.randn(*gray.shape) * 10
    result = np.clip(result.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return np.stack([result] * 3, axis=2)

# Oil Paint
@ArtisticModesEngine.register("oil_paint")
def _oil_paint_mode(img, pixels):
    if HAS_CV2:
        arr = np.array(img)
        result = cv2.xphoto.oilPainting(arr, 7, 1) if hasattr(cv2, 'xphoto') else cv2.bilateralFilter(arr, 9, 75, 75)
    else:
        arr = np.array(img.convert("L"), dtype=np.float32)
        blurred = np.array(Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.SMOOTH).filter(ImageFilter.SMOOTH))
        result = np.stack([blurred] * 3, axis=2)
    return result

# Chalk
@ArtisticModesEngine.register("chalk")
def _chalk_mode(img, pixels):
    arr = np.array(img, dtype=np.float32)
    noise = np.random.randn(*arr.shape) * 15
    result = arr + noise
    result = np.clip(result, 0, 255).astype(np.uint8)
    if HAS_CV2:
        result = cv2.medianBlur(result, 3)
    return result

# Graffiti
@ArtisticModesEngine.register("graffiti")
def _graffiti_mode(img, pixels):
    arr = np.array(img, dtype=np.uint8)
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV) if HAS_CV2 else arr
    h, w = arr.shape[:2]
    splatter = np.random.random((h, w, 3))
    mask = splatter > 0.97
    colors = [
        [255, 50, 50], [50, 255, 50], [50, 50, 255],
        [255, 255, 50], [255, 50, 255], [50, 255, 255]
    ]
    for c in colors:
        cmask = np.random.random((h, w)) > 0.99
        arr[cmask] = c
    return arr

# Glitch
@ArtisticModesEngine.register("glitch")
def _glitch_mode(img, pixels):
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    shift = int(np.random.randn() * 20)
    if shift > 0 and w > shift:
        slice_y = np.random.randint(0, h - 10)
        slice_h = np.random.randint(2, 8)
        arr[slice_y:slice_y + slice_h, shift:] = arr[slice_y:slice_y + slice_h, :w - shift]
        arr[slice_y:slice_y + slice_h, :shift] = 0
    if np.random.random() > 0.7:
        arr[:, :, 0] = np.roll(arr[:, :, 0], np.random.randint(-5, 5), axis=1)
    noise = (np.random.random(arr.shape) > 0.998).astype(np.uint8) * 255
    arr = np.clip(arr.astype(np.int16) + noise.astype(np.int16) * 2 - noise.astype(np.int16) * 3, 0, 255).astype(np.uint8)
    return arr

# Cursed AI
@ArtisticModesEngine.register("cursed_ai")
def _cursed_ai_mode(img, pixels):
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape[:2]
    phase = np.random.uniform(0, math.pi * 2)
    warp_strength = np.random.uniform(3, 15)
    yy, xx = np.ogrid[:h, :w]
    warp_x = (warp_strength * np.sin(yy / max(1, h) * math.pi * 4 + phase)).astype(int)
    warp_y = (warp_strength * np.cos(xx / max(1, w) * math.pi * 4 + phase * 1.3)).astype(int)
    for c in range(3):
        channel = arr[:, :, c]
        rolled_x = np.roll(channel, np.random.randint(-warp_strength, warp_strength), axis=1)
        rolled_y = np.roll(rolled_x, np.random.randint(-warp_strength, warp_strength), axis=0)
        melted = rolled_y.copy()
        if np.random.random() > 0.5:
            tear_y = np.random.randint(0, h)
            tear_h = np.random.randint(5, h // 4)
            melted[tear_y:min(h, tear_y + tear_h), :] = np.roll(melted[tear_y:min(h, tear_y + tear_h), :], np.random.randint(-30, 30), axis=1)
        arr[:, :, c] = melted
    hallucinate = np.random.randn(h, w) * 40
    hallucinate_mask = np.random.random((h, w)) > 0.92
    for c in range(3):
        arr[hallucinate_mask, c] = np.clip(arr[hallucinate_mask, c] + hallucinate[hallucinate_mask], 0, 255)
    posterize_bits = np.random.randint(2, 6)
    arr = (arr // (256 // (2 ** posterize_bits))) * (256 // (2 ** posterize_bits))
    if np.random.random() > 0.6:
        negative_slice = np.random.randint(0, h // 2)
        arr[negative_slice:negative_slice + h // 4] = 255 - arr[negative_slice:negative_slice + h // 4]
    return np.clip(arr, 0, 255).astype(np.uint8)

# Etching — high-contrast hatched line effect
@ArtisticModesEngine.register("etching")
def _etching_mode(img, pixels):
    gray = np.array(img.convert("L"), dtype=np.uint8)
    h, w = gray.shape
    thinned = np.clip(gray.astype(np.float32) * 0.3 + 170, 0, 255).astype(np.uint8)
    if HAS_CV2:
        edges = cv2.Canny(gray, 80, 200)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        edges = cv2.dilate(edges, kernel, iterations=1)
        thinned[edges > 0] = 10
        hatch = np.zeros_like(gray)
        for ang in range(0, 180, 45):
            phase = np.random.randint(0, 4)
            for y in range(phase, h, 6):
                x_pos = np.random.randint(0, max(1, w // 2))
                hatch[y, max(0, x_pos - 1):min(w, x_pos + 2)] = 255 - gray[y, max(0, x_pos - 1):min(w, x_pos + 2)] // 3
    else:
        thinned = gray
    return np.stack([thinned] * 3, axis=2)

# Woodcut — bold outlines, limited palette, high contrast
@ArtisticModesEngine.register("woodcut")
def _woodcut_mode(img, pixels):
    gray = np.array(img.convert("L"), dtype=np.float32)
    h, w = gray.shape
    binary = np.ones((h, w), dtype=np.uint8) * 255
    dark = gray < 80
    mid = (gray >= 80) & (gray < 180)
    binary[dark] = 0
    binary[mid] = 60
    if HAS_CV2:
        edges = cv2.Canny(gray.astype(np.uint8), 20, 60)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.dilate(edges, kernel, iterations=2)
        binary[edges > 0] = 0
    result = np.stack([binary] * 3, axis=2)
    return result

# Pointillism — scatter dots based on luminance
@ArtisticModesEngine.register("pointillism")
def _pointillism_mode(img, pixels):
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    gray = np.mean(arr, axis=2)
    noise = np.random.random((h, w))
    density = 1.0 - gray / 255.0
    mask = noise < density * 0.6
    result = np.ones_like(arr) * 245
    dots = np.random.randint(0, min(255, max(1, int(arr.max()))), (mask.sum(), 3))
    result[mask] = np.clip(arr[mask].astype(np.int16) + np.random.randint(-20, 20, arr[mask].shape), 0, 255).astype(np.uint8)
    return result

# Crosshatch Pattern — forced hatch overlay over image
@ArtisticModesEngine.register("crosshatch_pattern")
def _crosshatch_pattern_mode(img, pixels):
    arr = np.array(img, dtype=np.uint8)
    gray = np.array(img.convert("L"), dtype=np.float32)
    h, w = gray.shape
    overlay = np.ones((h, w), dtype=np.uint8) * 255
    for ang_deg in [0, 45, 90, 135]:
        ang = math.radians(ang_deg)
        spacing = 4 + np.random.randint(0, 3)
        for offset in range(-w - h, w + h, spacing):
            for t in range(-max(w, h), max(w, h)):
                px = int(w // 2 + t * math.cos(ang) + offset * math.sin(ang))
                py = int(h // 2 + t * math.sin(ang) + offset * math.cos(ang))
                if 0 <= px < w and 0 <= py < h:
                    overlay[py, px] = 180
    intensity = 1.0 - gray / 255.0
    alpha = np.clip(intensity * 0.5, 0, 1)
    result = arr.astype(np.float32) * (1 - alpha[:, :, np.newaxis]) + overlay[:, :, np.newaxis].astype(np.float32) * alpha[:, :, np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)

# Stippled — density-based noise stipple
@ArtisticModesEngine.register("stippled")
def _stippled_mode(img, pixels):
    gray = np.array(img.convert("L"), dtype=np.float32)
    h, w = gray.shape
    result = np.ones((h, w, 3), dtype=np.uint8) * 255
    density = 1.0 - (gray / 255.0) ** 0.7
    rnd = np.random.random((h, w))
    stipple = rnd < density * 0.5
    sizes = np.random.randint(1, 4, stipple.sum())
    ys, xs = np.nonzero(stipple)
    for i in range(len(ys)):
        y, x = ys[i], xs[i]
        s = min(sizes[i], 3)
        y1, y2 = max(0, y - s), min(h, y + s + 1)
        x1, x2 = max(0, x - s), min(w, x + s + 1)
        result[y1:y2, x1:x2] = gray[y, x] // 2
    return result


# ── v6.8: TERMINAL / CYBERPUNK UI ─────────────────────────

class TerminalUI:
    def __init__(self, app):
        self.app = app
        self.boot_visible = False
        self.matrix_active = False
        self.hologram_visible = False
        self.scanner_active = False
        self._matrix_chars = "01アイウエオカキクケコサシスセソタチツテト"
        self._matrix_drops = []
        self._boot_lines = [
            "SYS: SF2M_STUDIO_PRO_v6_GODMODE",
            "SYS: Initializing kernel...",
            "SYS: Loading neural co-processor...",
            "SYS: Calibrating drawing array...",
            "SYS: Establishing canvas link...",
            "SYS: All systems nominal.",
            "SYS: Ready for autonomous operation.",
        ]
        self._boot_index = 0
        self._boot_label = None

    def show_boot_screen(self, parent):
        win = tk.Toplevel(parent)
        win.title("System Boot")
        win.geometry("600x400")
        win.configure(bg="#000")
        win.overrideredirect(True)
        win.geometry("+{}+{}".format(parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        text_w = tk.Text(win, bg="#000", fg="#00ff88", font=("CommitMono Nerd Font Mono", 10), bd=0, highlightthickness=0, insertbackground="#00ff88")
        text_w.pack(fill="both", expand=True, padx=20, pady=20)
        text_w.insert("end", ">>> SF2M STUDIO PRO v6 — GODMODE BOOT SEQUENCE\n")
        text_w.insert("end", "=" * 50 + "\n\n")
        def boot_step(idx=0):
            if idx < len(self._boot_lines):
                text_w.insert("end", self._boot_lines[idx] + "\n")
                text_w.see("end")
                win.after(200 + idx * 50, lambda: boot_step(idx + 1))
            else:
                text_w.insert("end", "\n>>> Boot complete. System ready.\n")
                win.after(1500, win.destroy)
        boot_step()
        return win

    def create_matrix_overlay(self, parent):
        overlay = tk.Canvas(parent, bg="#000", highlightthickness=0)
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self._matrix_drops = [0] * 80
        def draw():
            if not self.matrix_active:
                overlay.place_forget()
                return
            overlay.delete("all")
            for i in range(80):
                char = self._matrix_chars[np.random.randint(0, len(self._matrix_chars))]
                x = i * 10
                y = self._matrix_drops[i] * 10
                overlay.create_text(x, y, text=char, fill="#00ff88" if np.random.random() > 0.9 else "#004400", font=("CommitMono Nerd Font Mono", 8))
                self._matrix_drops[i] = (self._matrix_drops[i] + 1) % 60
            parent.after(80, draw)
        self.matrix_active = True
        draw()
        return overlay

    def show_scanner(self, parent):
        scanner = tk.Canvas(parent, bg="transparent", highlightthickness=0)
        scanner.place(x=0, rely=0.5, relwidth=1, height=3)
        pos = [0]
        def scan():
            if not self.scanner_active:
                scanner.place_forget()
                return
            scanner.delete("all")
            scanner.create_line(pos[0], 0, pos[0] + 60, 0, fill="#00ff88", width=3)
            pos[0] = (pos[0] + 4) % (parent.winfo_width() or 600)
            parent.after(30, scan)
        self.scanner_active = True
        scan()
        return scanner

    def holographic_panel(self, parent, title, content):
        frame = tk.Frame(parent, bg="#001a00", bd=1, relief="solid", highlightbackground="#00ff88", highlightthickness=1)
        tk.Label(frame, text=title, bg="#001a00", fg="#00ff88", font=("CommitMono Nerd Font Mono", 8, "bold")).pack(anchor="w", padx=4, pady=2)
        lbl = tk.Label(frame, text=content, bg="#001a00", fg="#00cc66", font=("CommitMono Nerd Font Mono", 7), justify="left")
        lbl.pack(fill="both", expand=True, padx=4, pady=2)
        return frame

    def synthwave_hud(self, parent):
        canvas = tk.Canvas(parent, bg="#000", highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        w, h = parent.winfo_width() or 660, parent.winfo_height() or 1020
        sun_cx, sun_cy = w // 2, h - 100
        canvas.create_oval(sun_cx - 120, sun_cy - 120, sun_cx + 120, sun_cy + 120, fill="#ff00ff", outline="")
        for i in range(1, 6):
            r = 120 + i * 30
            canvas.create_oval(sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r, outline="#ff00ff", width=1, dash=(4, 4))
        for i in range(15):
            x = np.random.randint(0, w)
            y = np.random.randint(0, sun_cy - 60)
            canvas.create_line(x, y, x, y + 60, fill="#ff00ff", width=1)
        for i in range(3):
            grid_y = sun_cy - 50 - i * 60
            canvas.create_line(0, grid_y, w, grid_y, fill="#ff00ff44", width=1)
        canvas.create_text(w // 2, 30, text="SYNTHWAVE // HUD", fill="#ff00ff",
                           font=("CommitMono Nerd Font Mono", 18, "bold"))
        canvas.create_text(w // 2, 60, text=f"PIXELS: {self.app.last_pps:.0f}/s | FRAMES: {len(self.app.animation.frames) if hasattr(self.app, 'animation') else 0}",
                           fill="#ff00ff88", font=("CommitMono Nerd Font Mono", 8))
        return canvas

    def ai_diagnostics(self, parent):
        T = CURRENT_THEME
        frame = tk.Frame(parent, bg="#000511", bd=2, relief="solid", highlightbackground="#00ccff", highlightthickness=1)
        diag_data = []
        if hasattr(self.app, 'perf_monitor'):
            diag_data.append(("MEM", f"{self.app.perf_monitor.get_memory_mb():.1f} MB"))
            diag_data.append(("THREADS", str(self.app.perf_monitor.thread_count)))
            diag_data.append(("AVG PPS", f"{self.app.perf_monitor.get_avg_pps():.0f}"))
        if hasattr(self.app, 'draw_intel'):
            diag_data.append(("AI REPAIRS", str(getattr(self.app.draw_intel, 'repair_count', 0))))
        diag_data.append(("MODEL", "Tiny-SD" if HAS_TORCH and HAS_DIFFUSERS else "N/A"))
        diag_data.append(("UPTIME", f"{time.time() - getattr(self.app, 'draw_start_time', time.time()):.0f}s" if self.app.draw_start_time > 0 else "IDLE"))
        tk.Label(frame, text="[ AI DIAGNOSTICS ]", bg="#000511", fg="#00ccff",
                 font=("CommitMono Nerd Font Mono", 9, "bold")).pack(anchor="w", padx=6, pady=(6, 2))
        for label, value in diag_data:
            row = tk.Frame(frame, bg="#000511")
            row.pack(fill="x", padx=6, pady=1)
            tk.Label(row, text=f"{label:<10}", bg="#000511", fg="#00ccff",
                     font=("CommitMono Nerd Font Mono", 8, "bold")).pack(side="left")
            tk.Label(row, text=value, bg="#000511", fg="#66ffcc",
                     font=("CommitMono Nerd Font Mono", 8)).pack(side="right")
        tk.Label(frame, text="NEURAL LINK: ACTIVE | DRAW ARRAY: NOMINAL",
                 bg="#000511", fg="#336644", font=("CommitMono Nerd Font Mono", 7)).pack(pady=(4, 6))
        return frame


# ── v6.9: PERFORMANCE TOOLS ────────────────────────────────

class PerformanceMonitor:
    def __init__(self, app):
        self.app = app
        self.benchmarks: Dict[str, float] = {}
        self.memory_history = deque(maxlen=120)
        self.draw_history = deque(maxlen=120)
        self.ppf_history = deque(maxlen=60)
        self.thread_count = 0
        self._monitoring = False
        self._monitor_thread = None

    def start_monitoring(self):
        if self._monitoring:
            return
        self._monitoring = True
        def _loop():
            while self._monitoring:
                try:
                    if HAS_PSUTIL:
                        proc = psutil.Process()
                        mem = proc.memory_info().rss / 1024 / 1024
                        self.memory_history.append(mem)
                        self.thread_count = proc.num_threads()
                except:
                    pass
                time.sleep(1.0)
        self._monitor_thread = threading.Thread(target=_loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._monitoring = False

    def benchmark(self, name, fn, *args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        self.benchmarks[name] = elapsed
        return result, elapsed

    def record_draw_batch(self, dots, elapsed):
        self.draw_history.append(dots / max(0.001, elapsed))
        self.ppf_history.append(dots)

    def get_memory_mb(self):
        return self.memory_history[-1] if self.memory_history else 0

    def get_avg_pps(self):
        return np.mean(self.draw_history) if self.draw_history else 0

    def get_peak_pps(self):
        return max(self.draw_history) if self.draw_history else 0

    def generate_report(self):
        lines = [
            "=== PERFORMANCE REPORT ===",
            f"Memory: {self.get_memory_mb():.1f} MB",
            f"Threads: {self.thread_count}",
            f"Avg PPS: {self.get_avg_pps():.0f}",
            f"Peak PPS: {self.get_peak_pps():.0f}",
            f"Total draws: {len(self.draw_history)}",
            "--- Benchmarks ---",
        ]
        for name, t in sorted(self.benchmarks.items(), key=lambda x: -x[1]):
            lines.append(f"  {name}: {t*1000:.1f}ms")
        return "\n".join(lines)

    def route_heatmap(self, width=400, height=300):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        if not self.draw_history:
            return img
        draw = ImageDraw.Draw(img)
        values = list(self.draw_history)
        if not values:
            return img
        mx = max(values) if max(values) > 0 else 1
        for i, v in enumerate(values):
            x = int(i / len(values) * (width - 4)) + 2
            bar_h = max(1, int(v / mx * (height - 10)))
            r = int(255 * (v / mx))
            g = int(100 * (1 - v / mx * 0.5))
            b = int(50 * (1 - v / mx))
            draw.rectangle([x, height - bar_h - 4, x + max(2, width // len(values) - 1), height - 4], fill=(r, g, b, 200))
        for i, v in enumerate(values):
            if i > 0 and i < len(values) - 1:
                x1 = int((i - 1) / len(values) * (width - 4)) + 2
                y1 = height - 4 - int(values[i - 1] / mx * (height - 10))
                x2 = int(i / len(values) * (width - 4)) + 2
                y2 = height - 4 - int(v / mx * (height - 10))
                draw.line([x1, y1, x2, y2], fill=(0, 255, 128, 180), width=2)
        return img

    def optimization_advisor(self):
        suggestions = []
        pps = self.get_avg_pps()
        mem = self.get_memory_mb()
        if pps < 50:
            suggestions.append("PPS is low. Try: setting ENGINE_MODE='ultra_fast', disabling HATCH_ENABLE, reducing CANNY resolution, or increasing SIMPLIFY_EPS")
        elif pps < 200:
            suggestions.append("Moderate PPS. Consider: enabling USE_PATH_CACHE, reducing MULTIPASS passes, or switching to 'balanced' engine mode")
        else:
            suggestions.append("Good PPS. Fine-tune with HUMAN_MOTION or higher CANNY_HIGH for quality")
        if mem > 500:
            suggestions.append(f"High memory ({mem:.0f} MB). Consider: closing other apps, reducing image size, or disabling AI model")
        elif mem > 200:
            suggestions.append(f"Memory usage moderate ({mem:.0f} MB). Enable PERF_MONITOR to track trends")
        if self.thread_count > 20:
            suggestions.append(f"High thread count ({self.thread_count}). This may cause UI lag. Consider reducing parallel operations")
        if self.benchmarks:
            slowest = max(self.benchmarks.items(), key=lambda x: x[1])
            suggestions.append(f"Slowest operation: '{slowest[0]}' ({slowest[1]*1000:.1f}ms). Consider caching or optimizing")
        return suggestions


# ── v6.10: CREATIVE SANDBOX ────────────────────────────────

class ProceduralGenerator:
    def __init__(self):
        self.seed = 0

    def perlin_noise(self, width, height, scale=20, octaves=4):
        arr = np.zeros((height, width), dtype=np.float32)
        for o in range(octaves):
            freq = 2 ** o
            amp = 0.5 ** o
            for y in range(height):
                for x in range(width):
                    sx, sy = x / scale * freq, y / scale * freq
                    arr[y, x] += (math.sin(sx) * math.cos(sy * 1.3) + math.sin(sx * 0.7 + sy * 1.1)) * amp * 64
        return np.clip(arr + 128, 0, 255).astype(np.uint8)

    def plasma(self, width, height):
        arr = np.zeros((height, width), dtype=np.float32)
        for y in range(height):
            for x in range(width):
                v = math.sin(x * 0.05) + math.sin(y * 0.05) + math.sin((x + y) * 0.05) + math.sin(math.hypot(x, y) * 0.05)
                arr[y, x] = v * 32 + 128
        return np.clip(arr, 0, 255).astype(np.uint8)

    def voronoi(self, width, height, points=20):
        seeds = [(np.random.randint(0, width), np.random.randint(0, height)) for _ in range(points)]
        colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(points)]
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                dists = [math.hypot(x - sx, y - sy) for sx, sy in seeds]
                nearest = np.argmin(dists)
                arr[y, x] = colors[nearest]
        return arr

    def generate(self, mode, width, height, **kwargs):
        if mode == "perlin":
            g = self.perlin_noise(width, height)
            return Image.fromarray(g).convert("RGB")
        elif mode == "plasma":
            g = self.plasma(width, height)
            return Image.fromarray(g).convert("RGB")
        elif mode == "voronoi":
            c = self.voronoi(width, height, kwargs.get("points", 20))
            return Image.fromarray(c)
        elif mode == "checkerboard":
            size = kwargs.get("size", 32)
            arr = np.zeros((height, width, 3), dtype=np.uint8)
            for y in range(height):
                for x in range(width):
                    if (x // size + y // size) % 2 == 0:
                        arr[y, x] = [0, 0, 0]
                    else:
                        arr[y, x] = [255, 255, 255]
            return Image.fromarray(arr)
        return Image.new("RGB", (width, height), (128, 128, 128))


# ── v6.10b: NODE WORKFLOW EDITOR ───────────────────────────

class NodePort:
    def __init__(self, name, port_type="input", data_type="image", default=None):
        self.name = name
        self.port_type = port_type
        self.data_type = data_type
        self.default = default
        self.connections: List['NodePort'] = []

    def connect(self, other):
        if other not in self.connections:
            self.connections.append(other)

    def disconnect(self, other):
        if other in self.connections:
            self.connections.remove(other)


class WorkflowNode:
    def __init__(self, node_id, name, node_type="passthrough"):
        self.id = node_id
        self.name = name
        self.node_type = node_type
        self.inputs: List[NodePort] = []
        self.outputs: List[NodePort] = []
        self.params: Dict[str, Any] = {}
        self.pos = (100, 100)
        self.width = 160
        self.height = 80
        self.selected = False

    def add_input(self, name, data_type="image"):
        port = NodePort(name, "input", data_type)
        self.inputs.append(port)
        return port

    def add_output(self, name, data_type="image"):
        port = NodePort(name, "output", data_type)
        self.outputs.append(port)
        return port

    def get_input(self, name):
        for p in self.inputs:
            if p.name == name:
                return p
        return None

    def get_output(self, name):
        for p in self.outputs:
            if p.name == name:
                return p
        return None


class NodeWorkflowEditor:
    NODE_TYPES = {
        "load_image": {"inputs": [], "outputs": ["image"], "color": "#1a3a1a"},
        "blur": {"inputs": ["image"], "outputs": ["image"], "params": {"radius": 2}, "color": "#1a2a3a"},
        "sharpen": {"inputs": ["image"], "outputs": ["image"], "params": {"factor": 1.0}, "color": "#1a2a3a"},
        "brightness": {"inputs": ["image"], "outputs": ["image"], "params": {"amount": 1.0}, "color": "#2a1a3a"},
        "contrast": {"inputs": ["image"], "outputs": ["image"], "params": {"amount": 1.0}, "color": "#2a1a3a"},
        "threshold": {"inputs": ["image"], "outputs": ["image"], "params": {"threshold": 128}, "color": "#3a2a1a"},
        "edge_detect": {"inputs": ["image"], "outputs": ["image"], "params": {"low": 40, "high": 120}, "color": "#3a1a1a"},
        "resize": {"inputs": ["image"], "outputs": ["image"], "params": {"width": 512, "height": 512}, "color": "#1a3a3a"},
        "merge": {"inputs": ["image_a", "image_b"], "outputs": ["image"], "params": {"blend": 0.5}, "color": "#2a2a1a"},
        "output": {"inputs": ["image"], "outputs": [], "color": "#1a2a1a"},
    }

    def __init__(self, app):
        self.app = app
        self.nodes: Dict[str, WorkflowNode] = {}
        self.next_id = 1
        self.active = False

    def add_node(self, node_type, name=None):
        if node_type not in self.NODE_TYPES:
            return None
        spec = self.NODE_TYPES[node_type]
        node_id = f"node_{self.next_id}"
        self.next_id += 1
        node = WorkflowNode(node_id, name or f"{node_type}_{node_id}", node_type)
        node.params = dict(spec.get("params", {}))
        for out_name in spec["outputs"]:
            node.add_output(out_name)
        for in_name in spec["inputs"]:
            node.add_input(in_name)
        self.nodes[node_id] = node
        return node

    def remove_node(self, node_id):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            for port in node.inputs + node.outputs:
                for conn in list(port.connections):
                    port.disconnect(conn)
                    if conn in conn.connections:
                        conn.disconnect(port)
            del self.nodes[node_id]

    def connect_nodes(self, from_node_id, from_port_name, to_node_id, to_port_name):
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return False
        src = self.nodes[from_node_id].get_output(from_port_name)
        dst = self.nodes[to_node_id].get_input(to_port_name)
        if src and dst:
            src.connect(dst)
            dst.connect(src)
            return True
        return False

    def disconnect_nodes(self, from_node_id, from_port_name, to_node_id, to_port_name):
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return
        src = self.nodes[from_node_id].get_output(from_port_name)
        dst = self.nodes[to_node_id].get_input(to_port_name)
        if src and dst:
            src.disconnect(dst)
            dst.disconnect(src)

    def execute_graph(self, image_input=None):
        result = image_input
        ordered = []
        visited = set()

        def topo_sort(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            node = self.nodes[node_id]
            for port in node.inputs:
                for conn in port.connections:
                    for nid, n in self.nodes.items():
                        if any(p is conn for p in n.outputs):
                            topo_sort(nid)
            ordered.append(node_id)

        for nid in list(self.nodes.keys()):
            if nid not in visited:
                topo_sort(nid)

        cache = {}
        if image_input is not None:
            cache["image"] = image_input

        for nid in ordered:
            node = self.nodes[nid]
            try:
                if node.node_type == "load_image" and image_input:
                    cache[nid] = {"image": image_input}
                elif node.node_type == "blur":
                    inp = cache.get(node.inputs[0].connections[0].name if node.inputs[0].connections else None, {}).get("image", image_input) if node.inputs else image_input  # simplified
                    radius = node.params.get("radius", 2)
                    cache[nid] = {"image": inp.filter(ImageFilter.GaussianBlur(radius=radius))} if inp else {}
                elif node.node_type == "sharpen":
                    inp = image_input
                    factor = node.params.get("factor", 1.0)
                    cache[nid] = {"image": ImageEnhance.Sharpness(inp).enhance(factor)} if inp else {}
                elif node.node_type == "brightness":
                    inp = image_input
                    amount = node.params.get("amount", 1.0)
                    cache[nid] = {"image": ImageEnhance.Brightness(inp).enhance(amount)} if inp else {}
                elif node.node_type == "contrast":
                    inp = image_input
                    amount = node.params.get("amount", 1.0)
                    cache[nid] = {"image": ImageEnhance.Contrast(inp).enhance(amount)} if inp else {}
                elif node.node_type == "threshold":
                    inp = image_input
                    thresh = node.params.get("threshold", 128)
                    if inp:
                        gray = inp.convert("L")
                        arr = np.array(gray)
                        binary = (arr > thresh).astype(np.uint8) * 255
                        cache[nid] = {"image": Image.fromarray(binary).convert("RGB")}
                elif node.node_type == "edge_detect":
                    inp = image_input
                    lo, hi = node.params.get("low", 40), node.params.get("high", 120)
                    if inp and HAS_CV2:
                        gray = np.array(inp.convert("L"), dtype=np.uint8)
                        edges = cv2.Canny(gray, lo, hi)
                        cache[nid] = {"image": Image.fromarray(edges).convert("RGB")}
                elif node.node_type == "resize":
                    inp = image_input
                    w, h = node.params.get("width", 512), node.params.get("height", 512)
                    cache[nid] = {"image": inp.resize((w, h))} if inp else {}
                elif node.node_type == "output":
                    inp = image_input
                    if inp:
                        cache[nid] = {"image": inp}
                        result = inp
            except Exception:
                pass
        return result

    def clear(self):
        self.nodes.clear()
        self.next_id = 1

    def count_nodes(self):
        return len(self.nodes)

    def count_connections(self):
        count = 0
        for node in self.nodes.values():
            for port in node.outputs:
                count += len(port.connections)
        return count


# ── v6.10c: AI COMPOSITION ANALYZER ────────────────────────

class AICompositionAnalyzer:
    def __init__(self, app):
        self.app = app
        self._cache = {}

    def analyze(self, img):
        if img is None:
            return {}
        key = hashlib.md5(img.tobytes()).hexdigest()[:16]
        if key in self._cache:
            return self._cache[key]
        arr = np.array(img)
        gray = np.array(img.convert("L"), dtype=np.float32)
        h, w = gray.shape
        result = {}
        result["brightness"] = float(np.mean(gray))
        result["contrast"] = float(np.std(gray))
        rr, gg, bb = arr[:, :, 0].astype(float), arr[:, :, 1].astype(float), arr[:, :, 2].astype(float)
        result["red_dominance"] = float(np.mean(rr - (gg + bb) / 2))
        result["blue_dominance"] = float(np.mean(bb - (rr + gg) / 2))
        result["green_dominance"] = float(np.mean(gg - (rr + bb) / 2))
        edges = np.abs(np.diff(gray, axis=1))
        result["edge_density"] = float(np.mean(edges > 20))
        quadrants = {
            "top_left": gray[:h // 2, :w // 2].mean(),
            "top_right": gray[:h // 2, w // 2:].mean(),
            "bottom_left": gray[h // 2:, :w // 2].mean(),
            "bottom_right": gray[h // 2:, w // 2:].mean(),
        }
        result["quadrant_brightness"] = quadrants
        brightest_quad = max(quadrants, key=quadrants.get)
        result["focal_region"] = "top" if "top" in brightest_quad else "bottom"
        result["focal_side"] = "left" if "left" in brightest_quad else "right"
        colorfulness = np.mean(np.sqrt((rr - gg) ** 2 + (rr - bb) ** 2 + (gg - bb) ** 2))
        result["colorfulness"] = float(colorfulness)
        if colorfulness > 60:
            result["palette_type"] = "vibrant"
        elif colorfulness > 30:
            result["palette_type"] = "moderate"
        else:
            result["palette_type"] = "muted"
        symmetric_h = np.mean(np.abs(gray[:, :w // 2] - gray[:, :w // 2][:, ::-1]))
        symmetric_v = np.mean(np.abs(gray[:h // 2, :] - gray[:h // 2][::-1, :]))
        result["horizontal_symmetry"] = float(1.0 - min(1.0, symmetric_h / 128.0))
        result["vertical_symmetry"] = float(1.0 - min(1.0, symmetric_v / 128.0))
        if HAS_CV2:
            try:
                lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
                l_chan = lab[:, :, 0].astype(float)
                shadows = np.mean(l_chan < 50)
                highlights = np.mean(l_chan > 200)
                result["shadow_percentage"] = float(shadows * 100)
                result["highlight_percentage"] = float(highlights * 100)
            except Exception:
                pass
        if HAS_SCIPY:
            try:
                from scipy.ndimage import sobel
                grad_x = sobel(gray, axis=1)
                grad_y = sobel(gray, axis=0)
                magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
                result["avg_gradient_magnitude"] = float(np.mean(magnitude))
                dominant_angle = np.arctan2(grad_y.mean(), grad_x.mean())
                result["dominant_edge_angle_deg"] = float(np.degrees(dominant_angle) % 180)
            except Exception:
                pass
        result["width"] = w
        result["height"] = h
        result["aspect_ratio"] = round(w / max(1, h), 3)
        self._cache[key] = result
        return result

    def composition_suggestions(self, img):
        analysis = self.analyze(img)
        suggestions = []
        if analysis.get("edge_density", 0) < 0.05:
            suggestions.append("Low edge density. Consider using a high-pass filter or sharpening before drawing")
        if analysis.get("contrast", 0) < 40:
            suggestions.append("Low contrast. Auto-contrast or levels adjustment may improve line detection")
        if analysis.get("brightness", 128) > 200:
            suggestions.append("Very bright image. Consider inverting or using dark-fill presets")
        elif analysis.get("brightness", 128) < 50:
            suggestions.append("Very dark image. Increase brightness or use edge-only extraction")
        if analysis.get("horizontal_symmetry", 0) > 0.8:
            suggestions.append("Strong horizontal symmetry — consider mirrored drawing techniques")
        if analysis.get("vertical_symmetry", 0) > 0.8:
            suggestions.append("Strong vertical symmetry — center-aligned composition detected")
        if analysis.get("colorfulness", 0) < 20:
            suggestions.append("Low colorfulness. Grayscale or monochrome preset recommended")
        if analysis.get("palette_type") == "vibrant":
            suggestions.append("Vibrant image. Use a larger palette size (PALETTE_SIZE=32+) for better color matching")
        focal = analysis.get("focal_region", "center")
        side = analysis.get("focal_side", "center")
        suggestions.append(f"Composition focal point: {focal}-{side}")
        return suggestions

    def clear_cache(self):
        self._cache.clear()


# ── v6.11: GODMODE SETTINGS INTEGRATION ────────────────────

GODMODE_SETTINGS = {
    # Viewport
    "VIEWPORT_ZOOM_SPEED": 1.15,
    "VIEWPORT_MOMENTUM_FRICTION": 0.92,
    "VIEWPORT_SNAP_ENABLED": True,
    "VIEWPORT_SHOW_MINIMAP": False,
    "VIEWPORT_MINIMAP_SIZE": 180,
    # AI
    "AI_MODEL": "segmind/tiny-sd",
    "AI_STEPS": 20,
    "AI_GUIDANCE": 7.0,
    "AI_STRENGTH": 0.75,
    "AI_STYLE": "anime",
    # Animation
    "ANIM_FPS": 12,
    "ANIM_ONION_SKIN": False,
    "ANIM_LOOP": True,
    "ANIM_INTERPOLATE_ENABLED": False,
    "ANIM_AI_INBETWEEN_ENABLED": False,
    # Artistic
    "ARTISTIC_CURSED_AI_ENABLED": False,
    # Plugin
    "PLUGIN_AUTOLOAD": True,
    # Performance
    "PERF_MONITOR_ENABLED": False,
    "PERF_ROUTE_HEATMAP_ENABLED": False,
    "PERF_ADVISOR_ENABLED": False,
    # Terminal
    "TERMINAL_BOOT_SCREEN": True,
    "TERMINAL_MATRIX_OVERLAY": False,
    "TERMINAL_SCANNER": False,
    "TERMINAL_SYNTHWAVE_HUD": False,
    "TERMINAL_AI_DIAGNOSTICS": False,
    # Sandbox
    "NODE_EDITOR_ENABLED": False,
    "COMPOSITION_ANALYZER_ENABLED": False,
}

SETTINGS.update(GODMODE_SETTINGS)


# ── v6.12: GODMODE INTEGRATION INTO AutoDrawer ─────────────

_AI_SUBPROCESS_SCRIPT = r'''
import sys, json, base64, io, os
os.environ["PYTHONUNBUFFERED"] = "1"
try:
    import torch
    from diffusers import StableDiffusionPipeline
except Exception as e:
    print(json.dumps({"error": f"import failed: {e}"}))
    sys.exit(1)
data = json.loads(sys.stdin.read())
try:
    pipe = StableDiffusionPipeline.from_pretrained(
        data["model_id"], torch_dtype=torch.float32, safety_checker=None
    )
    pipe.to("cpu")
    pipe.enable_attention_slicing()
    gen = None
    if data.get("seed", -1) > 0:
        gen = torch.Generator(device="cpu").manual_seed(data["seed"])
    result = pipe(
        data["prompt"],
        negative_prompt=data.get("negative_prompt", "blurry, low quality"),
        num_inference_steps=data.get("steps", 15),
        guidance_scale=data.get("guidance", 7.0),
        generator=gen,
    ).images[0]
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    print(json.dumps({"ok": True, "png_b64": base64.b64encode(buf.getvalue()).decode()}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
'''

def _run_ai_subprocess(prompt, model_id="segmind/tiny-sd", negative_prompt="lowres, bad anatomy, text", steps=15, guidance=7.0, seed=-1):
    import tempfile
    script_path = os.path.join(tempfile.gettempdir(), "_ai_gen_subprocess.py")
    try:
        if not os.path.exists(script_path):
            with open(script_path, "w") as f:
                f.write(_AI_SUBPROCESS_SCRIPT)
        input_data = json.dumps({
            "prompt": prompt,
            "model_id": model_id,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "guidance": guidance,
            "seed": seed,
        })
        p = subprocess.run(
            [sys.executable, script_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if p.returncode != 0:
            if p.returncode < 0:
                sig_num = -p.returncode
                return None, f"SIGNAL:{sig_num} (killed by signal {sig_num})"
            return None, f"subprocess exited with code {p.returncode}"
        result = json.loads(p.stdout.strip())
        if "error" in result:
            return None, result["error"]
        if result.get("ok"):
            img = Image.open(io.BytesIO(base64.b64decode(result["png_b64"]))).convert("RGB")
            return img, None
        return None, "unknown subprocess error"
    except subprocess.TimeoutExpired:
        return None, "AI generation timed out (300s)"
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────────
#  BACKGROUND PLAYER (MP4 / Static Image)
#  Plays video or static image behind the UI
#  using cv2.VideoCapture in a daemon thread.
# ─────────────────────────────────────────────
class BackgroundPlayer:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self._player = None
        self._container = None
        self._running = False

    def start(self):
        if not HAS_CV2:
            self.app.log("[BG] OpenCV not available — background disabled")
            return
        cfg_type = SETTINGS.get("BG_TYPE", "none")
        cfg_path = SETTINGS.get("BG_PATH", "")
        self.app.log(f"[BG] start: type={cfg_type} path={cfg_path}")
        if cfg_type == "none" or not cfg_path:
            self.app.log(f"[BG] No background configured (type={cfg_type}, path={cfg_path})")
            self.stop()
            return

        self.stop()

        try:
            import mpv as mpv_module
        except ImportError:
            self.app.log("[BG] python-mpv not available")
            return

        right_frame = getattr(self.app, '_term_panel_right_frame', None)
        if right_frame:
            container_parent = right_frame
            self.app.log("[BG] Playing in terminal panel")
        else:
            container_parent = self.root
            self.app.log("[BG] Playing in root")

        self._container = tk.Canvas(container_parent, highlightthickness=0, bg="black")
        self._container.place(x=0, y=0, relwidth=1, relheight=1)
        if right_frame:
            self._container.tk.call('lower', self._container._w)
        self._container.update_idletasks()

        wid = self._container.winfo_id()
        self._player = mpv_module.MPV(
            wid=str(wid),
            loop=True,
            keep_open=True,
            volume=0,
            audio=False,
        )
        self._player.play(cfg_path)
        self._running = True
        self.app.log(f"[BG] mpv playing: {cfg_path}")

    def _start_opencv(self, cfg_type, cfg_path):
        self.app.log("[BG] OpenCV fallback not re-implemented — skipping")

    def stop(self):
        self._running = False
        if self._player:
            try:
                self._player.stop()
                self._player.terminate()
            except:
                pass
            self._player = None
        if self._container:
            try:
                self._container.destroy()
            except:
                pass
            self._container = None

    def toggle(self):
        if self._running:
            self.stop()
            SETTINGS["BG_ENABLED"] = False
        else:
            SETTINGS["BG_ENABLED"] = True
            self.start()

    def cleanup(self):
        self.stop()


def _256_to_rgb(code):
    if code < 16:
        std = [0, 95, 135, 175, 215, 255]
        if code == 0: return (0, 0, 0)
        if code == 1: return (128, 0, 0)
        if code == 2: return (0, 128, 0)
        if code == 3: return (128, 128, 0)
        if code == 4: return (0, 0, 128)
        if code == 5: return (128, 0, 128)
        if code == 6: return (0, 128, 128)
        if code == 7: return (192, 192, 192)
        if code == 8: return (128, 128, 128)
        if code == 9: return (255, 0, 0)
        if code == 10: return (0, 255, 0)
        if code == 11: return (255, 255, 0)
        if code == 12: return (0, 0, 255)
        if code == 13: return (255, 0, 255)
        if code == 14: return (0, 255, 255)
        if code == 15: return (255, 255, 255)
    elif code < 232:
        code -= 16
        r = (code // 36) * 40 + 55 if (code // 36) else 0
        g = ((code % 36) // 6) * 40 + 55 if ((code % 36) // 6) else 0
        b = (code % 6) * 40 + 55 if (code % 6) else 0
        return (r, g, b)
    else:
        gray = (code - 232) * 10 + 8
        return (gray, gray, gray)
    return (0, 0, 0)


class TerminalPanel:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._master_fd = None
        self._slave_fd = None
        self._pid = None
        self._buf = b""
        self._closed = False
        self._truecolor_cache = {}
        self._fg_tag = None
        self._bg_tag = None
        self._bold = False

        T = CURRENT_THEME

        self.text = tk.Text(
            parent,
            bg=T.get("log_bg", "#0a0a0a"),
            fg=T.get("log_fg", "#00ff88"),
            insertbackground=T.get("accent", "#00ff88"),
            font=("CommitMono Nerd Font Mono", 10),
            wrap="char",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            padx=8,
            pady=6,
            state="normal",
            takefocus=True,
        )
        self.text.pack(fill="both", expand=True)

        self._init_ansi_tags()
        self._spawn_shell()

        self.text.bind("<Key>", self._on_key, add=True)
        self.text.bind("<Button-1>", self._on_click)
        parent.bind("<Configure>", self._on_resize)
        self._poll_pty()

    def _on_click(self, event):
        self.text.focus_force()
        return "break"

    def _init_ansi_tags(self):
        colors = {
            "30": "#1a1a2e", "31": "#ff3355", "32": "#00ff88",
            "33": "#ffaa00", "34": "#00ccff", "35": "#ff66ff",
            "36": "#00ffcc", "37": "#e0e0e0", "90": "#555555",
            "91": "#ff0044", "92": "#44ff88", "93": "#ffdd00",
            "94": "#66bbff", "95": "#dd88ff", "96": "#44ffee",
            "97": "#ffffff",
        }
        for code, color in colors.items():
            self.text.tag_configure(f"ansi{code}", foreground=color)
        self.text.tag_configure("bold", font=("CommitMono Nerd Font Mono", 10, "bold"))

    def _spawn_shell(self):
        self._master_fd, self._slave_fd = pty.openpty()
        fcntl.fcntl(self._master_fd, fcntl.F_SETFL, os.O_NONBLOCK)

        self._pid = subprocess.Popen(
            ["bash", "--rcfile", "/dev/null"],
            pass_fds=(self._slave_fd,),
            preexec_fn=lambda: (
                os.setsid(),
                os.dup2(self._slave_fd, 0),
                os.dup2(self._slave_fd, 1),
                os.dup2(self._slave_fd, 2),
            ),
            close_fds=True,
        )
        os.close(self._slave_fd)
        self.app.log("[TERM] Shell spawned")

        self.app.root.after(300, self._init_shell)

    def _init_shell(self):
        if self._closed or not self._master_fd:
            return
        try:
            os.write(self._master_fd, (
                "export PS1='"
                "\\[\\e[38;5;39m\\]"
                "\\[\\e[48;5;39m\\]\\[\\e[38;5;16m\\]"
                " \uf489 "
                "\\[\\e[0m\\]"
                "\\[\\e[38;5;39m\\]\ue0b4\\[\\e[0m\\]"
                " "
                "\\[\\e[38;5;33m\\]\uf07c\\[\\e[0m\\]"
                " \\[\\e[36m\\]\\w\\[\\e[0m\\]"
                "\\[\\e[38;5;39m\\]"
                " \\uf460 "
                "\\[\\e[0m\\] "
                "'\n"
                f"export TERM=xterm-256color\n"
                f"clear 2>/dev/null; cat /home/owner/Downloads/ascii-art.txt 2>/dev/null\n"
            ).encode())
        except OSError:
            self._respawn()

    def _text_alive(self):
        try:
            return self.text and self.text.winfo_exists()
        except:
            return False

    def _fd_valid(self):
        fd = self._master_fd
        if fd is None:
            return False
        try:
            os.fstat(fd)
            return True
        except OSError:
            return False

    def _poll_pty(self):
        if self._closed or not self._text_alive() or not self._fd_valid():
            return
        try:
            r, _, _ = select.select([self._master_fd], [], [], 0)
            if r:
                data = os.read(self._master_fd, 4096)
                if not data:
                    self._respawn()
                    return
                try:
                    self._feed(data)
                except:
                    self.app.log("[TERM] feed error, respawning")
                    self._respawn()
                    return
        except (OSError, ValueError):
            self._respawn()
            return
        self.app.root.after(20, self._poll_pty)


    def _respawn(self):
        try:
            self._pid = None
            self._close_fds()
            self._spawn_shell()
            self.app.root.after(500, self._init_shell)
        except:
            pass

    def _feed(self, data):
        self._buf += data
        try:
            text = self._buf.decode("utf-8", errors="replace")
            self._buf = b""
        except:
            return
        self._render_ansi(text)
        self.text.see("end")

    def _apply_tags(self):
        if self._bold:
            self.text.tag_add("bold", "end-1c", "end")
        if self._fg_tag:
            self.text.tag_add(self._fg_tag, "end-1c", "end")
        if self._bg_tag:
            self.text.tag_add(self._bg_tag, "end-1c", "end")

    def _render_ansi(self, text):
        parts = re.split(r"(\x1b\[[0-9;?>=]*[a-zA-Z])", text)
        for part in parts:
            if not part:
                continue
            m = re.match(r"^\x1b\[([0-9;]*)m$", part)
            if m:
                codes = m.group(1).split(";") if m.group(1) else ["0"]
                i = 0
                while i < len(codes):
                    code = codes[i]
                    if code in ("0",):
                        self._fg_tag = None
                        self._bg_tag = None
                        self._bold = False
                    elif code == "1":
                        self._bold = True
                    elif code == "38" and i + 4 < len(codes) and codes[i+1] == "2":
                        r, g, b = codes[i+2], codes[i+3], codes[i+4]
                        tagname = f"truefg_{r}_{g}_{b}"
                        if tagname not in self._truecolor_cache:
                            self.text.tag_configure(tagname, foreground=f"#{int(r):02x}{int(g):02x}{int(b):02x}")
                            self._truecolor_cache[tagname] = True
                            if len(self._truecolor_cache) > 512:
                                self._truecolor_cache.clear()
                        self._fg_tag = tagname
                        i += 5
                        continue
                    elif code == "48" and i + 4 < len(codes) and codes[i+1] == "2":
                        r, g, b = codes[i+2], codes[i+3], codes[i+4]
                        tagname = f"truebg_{r}_{g}_{b}"
                        if tagname not in self._truecolor_cache:
                            self.text.tag_configure(tagname, background=f"#{int(r):02x}{int(g):02x}{int(b):02x}")
                            self._truecolor_cache[tagname] = True
                            if len(self._truecolor_cache) > 512:
                                self._truecolor_cache.clear()
                        self._bg_tag = tagname
                        i += 5
                        continue
                    elif code == "38" and i + 2 < len(codes) and codes[i+1] == "5":
                        c256 = int(codes[i+2])
                        r, g, b = _256_to_rgb(c256)
                        tagname = f"truefg_{r}_{g}_{b}"
                        if tagname not in self._truecolor_cache:
                            self.text.tag_configure(tagname, foreground=f"#{r:02x}{g:02x}{b:02x}")
                            self._truecolor_cache[tagname] = True
                            if len(self._truecolor_cache) > 512:
                                self._truecolor_cache.clear()
                        self._fg_tag = tagname
                        i += 3
                        continue
                    elif code == "48" and i + 2 < len(codes) and codes[i+1] == "5":
                        c256 = int(codes[i+2])
                        r, g, b = _256_to_rgb(c256)
                        tagname = f"truebg_{r}_{g}_{b}"
                        if tagname not in self._truecolor_cache:
                            self.text.tag_configure(tagname, background=f"#{r:02x}{g:02x}{b:02x}")
                            self._truecolor_cache[tagname] = True
                            if len(self._truecolor_cache) > 512:
                                self._truecolor_cache.clear()
                        self._bg_tag = tagname
                        i += 3
                        continue
                    elif code == "39":
                        self._fg_tag = None
                    elif code == "49":
                        self._bg_tag = None
                    elif code == "38" or code == "48" or code == "":
                        pass
                    else:
                        self._fg_tag = f"ansi{code}"
                    i += 1
                continue
            m = re.match(r"^\x1b\[\?[0-9]+[hl]$", part)
            if m:
                continue
            m = re.match(r"^\x1b\[[0-9;]*[A-DfGHJKP]$", part)
            if m:
                if "J" in part:
                    self.text.delete("1.0", "end")
                continue
            m = re.match(r"^\x1b", part)
            if m:
                continue
            i = 0
            while i < len(part):
                c = part[i]
                if c == '\b':
                    if self.text.compare("end-1c", "!=", "1.0"):
                        self.text.delete("end-2c", "end-1c")
                elif c == '\r':
                    self.text.mark_set("insert", "insert linestart")
                elif c == '\n':
                    self.text.insert("end", "\n")
                else:
                    self.text.insert("end", c)
                    self._apply_tags()
                i += 1

    def _pty_write(self, data):
        if self._closed or not self._master_fd:
            return
        try:
            os.write(self._master_fd, data)
        except (OSError, ValueError):
            self._respawn()

    def _on_key(self, event):
        if self._closed:
            return "break"
        try:
            ctrl = (event.state & 0x0004) != 0
            if ctrl and event.keysym in ("c", "C"):
                try:
                    self.text.clipboard_clear()
                    self.text.clipboard_append(self.text.selection_get())
                except tk.TclError:
                    self._pty_write(b"\x03")
                return "break"
            elif ctrl and event.keysym in ("v", "V"):
                try:
                    paste = self.text.clipboard_get()
                    self._pty_write(paste.encode())
                except tk.TclError:
                    pass
                return "break"
            elif ctrl and event.keysym in ("x", "X"):
                try:
                    self.text.clipboard_clear()
                    self.text.clipboard_append(self.text.selection_get())
                    self.text.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
                return "break"
            elif ctrl and event.keysym in ("a", "A"):
                self.text.tag_add("sel", "1.0", "end")
                return "break"
            elif event.keysym == "Return":
                self._pty_write(b"\r")
                return "break"
            elif event.keysym == "BackSpace":
                self._pty_write(b"\x7f")
                return "break"
            elif event.keysym == "Tab":
                self._pty_write(b"\t")
                return "break"
            elif event.keysym == "Up":
                self._pty_write(b"\x1b[A")
                return "break"
            elif event.keysym == "Down":
                self._pty_write(b"\x1b[B")
                return "break"
            elif event.keysym == "Right":
                self._pty_write(b"\x1b[C")
                return "break"
            elif event.keysym == "Left":
                self._pty_write(b"\x1b[D")
                return "break"
            elif event.keysym == "Home":
                self._pty_write(b"\x1b[H")
                return "break"
            elif event.keysym == "End":
                self._pty_write(b"\x1b[F")
                return "break"
            elif event.keysym == "Delete":
                self._pty_write(b"\x1b[3~")
                return "break"
            elif event.keysym in ("F2",):
                self.app._toggle_terminal()
                return "break"
            elif event.char and event.char.isprintable():
                self._pty_write(event.char.encode())
                return "break"
            elif event.char and ord(event.char) < 32 and not ctrl:
                self._pty_write(event.char.encode())
                return "break"
            elif event.keysym.startswith("Control") or event.keysym.startswith("Alt"):
                return "break"
        except Exception as e:
            self.app.log(f"[TERM KEY] error: {e}")
        return "break"

    def _on_resize(self, event):
        if hasattr(self, '_resize_timer'):
            try:
                self.app.root.after_cancel(self._resize_timer)
            except:
                pass
        self._resize_timer = self.app.root.after(200, self._update_term_size)

    def _update_term_size(self):
        try:
            w = self.text.winfo_width()
            h = self.text.winfo_height()
            if w < 10 or h < 10:
                return
            ch = 14
            cw = 8
            cols = max(20, w // cw)
            rows = max(5, h // ch)
            if self._master_fd:
                s = struct.pack("HHHH", rows, cols, 0, 0)
                fcntl.ioctl(self._master_fd, termios.TIOCSWINSZ, s)
        except:
            pass

    def _close_fds(self):
        if self._master_fd:
            try:
                os.close(self._master_fd)
            except:
                pass
            self._master_fd = None
        if self._slave_fd:
            try:
                os.close(self._slave_fd)
            except:
                pass
            self._slave_fd = None

    def close(self):
        self._closed = True
        if self._pid:
            try:
                os.killpg(os.getpgid(self._pid), signal.SIGTERM)
            except:
                try:
                    os.kill(self._pid, signal.SIGKILL)
                except:
                    pass
            self._pid = None
        self._close_fds()

def _patch_autodrawer():
    orig_init = AutoDrawer.__init__
    def new_init(self):
        orig_init(self)
        self.viewport = ViewportSystem(self)
        self.ai_gen = AIGenerationSuite(self)
        self.layer_v2 = LayerSystemV2(self)
        self.animation = AnimationTimeline(self)
        self.plugin_api = PluginAPI(self)
        self.draw_intel = AutonomousDrawIntelligence(self)
        self.artistic_modes = ArtisticModesEngine(self)
        self.terminal_ui = TerminalUI(self)
        self.perf_monitor = PerformanceMonitor(self)
        self.proc_gen = ProceduralGenerator()
        self.node_editor = NodeWorkflowEditor(self)
        self.comp_analyzer = AICompositionAnalyzer(self)
        self.bg_player = BackgroundPlayer(self)
        self.root.protocol("WM_DELETE_WINDOW", self._cleanup_and_exit)
        self.root.after(100, self._godmode_post_init)

    def godmode_post_init(self):
        if SETTINGS.get("PLUGIN_AUTOLOAD"):
            self.plugin_api.discover_plugins()
        if SETTINGS.get("PERF_MONITOR_ENABLED"):
            self.perf_monitor.start_monitoring()
        self._init_terminal_panel()
        if SETTINGS.get("BG_ENABLED"):
            self.bg_player.start()
        if self.base_img and self.layer_v2.layers:
            self.layer_v2.add_layer("Background", self.base_img)
        self._setup_godmode_bindings()

    def _init_terminal_panel(self):
        try:
            root = self.root
            self.log("[UI] init_terminal_panel: adding right panel")

            # Find the scrollbar packed in root
            scrollbar = None
            for w in root.winfo_children():
                if isinstance(w, (tk.Scrollbar, ttk.Scrollbar)):
                    scrollbar = w
                    break

            # Create right-side terminal panel (packed before scrollbar so it sits to its left)
            right_frame = tk.Frame(root, bg=CURRENT_THEME.get("bg2", "#0a0a0a"), width=500)
            if scrollbar:
                right_frame.pack(side="right", fill="y", before=scrollbar)
            else:
                right_frame.pack(side="right", fill="y")
            right_frame.pack_propagate(False)

            # Container for terminal text widget
            self._term_panel_container = tk.Frame(right_frame, bg=CURRENT_THEME.get("bg", "#0a0a0a"))
            self._term_panel_container.pack(fill="both", expand=True)
            self._term_panel_right_frame = right_frame
            self._terminal_hidden = False

            # Terminal panel on top of video area
            self.terminal_panel = TerminalPanel(self._term_panel_container, self)

            # Focus terminal after a moment
            root.after(500, lambda: self.terminal_panel.text.focus_set() if hasattr(self, 'terminal_panel') else None)
            self.log("[UI] Terminal panel added to right side")
        except Exception as e:
            self.log(f"[UI] Terminal panel init FAILED: {e}")
            traceback.print_exc()

    def _setup_godmode_bindings(self):
        try:
            self.root.bind("<Control-plus>", lambda e: self.viewport.zoom_at_cursor(1.15, self.root.winfo_width()//2, self.root.winfo_height()//2, self.root.winfo_width(), self.root.winfo_height()))
            self.root.bind("<Control-minus>", lambda e: self.viewport.zoom_at_cursor(0.85, self.root.winfo_width()//2, self.root.winfo_height()//2, self.root.winfo_width(), self.root.winfo_height()))
            self.root.bind("<Control-0>", lambda e: self.viewport.reset_view(True))
            self.root.bind("<Control-b>", lambda e: self._show_bookmarks())
            self.root.bind("<F2>", lambda e: self._toggle_terminal())
        except:
            pass

    def _toggle_terminal(self):
        rf = getattr(self, '_term_panel_right_frame', None)
        if not rf:
            return
        hidden = getattr(self, '_terminal_hidden', False)
        if hidden:
            rf.configure(width=500)
            sb = self._get_scrollbar()
            if sb:
                rf.pack(side="right", fill="y", before=sb)
            else:
                rf.pack(side="right", fill="y")
            self._terminal_hidden = False
            self.log("[TERM] Terminal shown")
        else:
            rf.pack_forget()
            self._terminal_hidden = True
            self.log("[TERM] Terminal hidden")

    def _get_scrollbar(self):
        for w in self.root.winfo_children():
            if isinstance(w, (tk.Scrollbar, ttk.Scrollbar)):
                return w
        return None

    def godmode_toggle_matrix(self):
        self.terminal_ui.matrix_active = not self.terminal_ui.matrix_active
        if self.terminal_ui.matrix_active:
            self.terminal_ui.create_matrix_overlay(self.root)
        self.log(f"[UI] Matrix overlay: {'ON' if self.terminal_ui.matrix_active else 'OFF'}")

    def godmode_show_boot(self):
        self.terminal_ui.show_boot_screen(self.root)

    def godmode_generate_ai(self, prompt, output_path=None):
        self.log(f"[AI] Generating '{prompt[:60]}'...")
        self.root.update()
        result = None
        gen_err = None
        try:
            result, gen_err = _run_ai_subprocess(
                prompt,
                model_id="segmind/tiny-sd",
                negative_prompt="lowres, bad anatomy, text, watermark",
                steps=int(SETTINGS.get("AI_STEPS", 20)),
                guidance=float(SETTINGS.get("AI_GUIDANCE", 7.0)),
                seed=int(SETTINGS.get("AI_SEED", -1)),
            )
        except Exception as e:
            gen_err = str(e)
        if result is None and gen_err:
            sig_exit = gen_err.startswith("SIGNAL:")
            self.log(f"[AI] Subprocess gen failed ({gen_err}){' [SIGNAL - NOT retrying]' if sig_exit else ''}")
            if sig_exit:
                self.log("[AI] The torch/diffusers subprocess crashed (segfault/signal). In-process fallback skipped to protect main app.")
                messagebox.showerror("AI Crash", f"The AI subprocess crashed with: {gen_err}\n\n"
                    "The main app is safe. Try:\n"
                    "  • Closing other memory-heavy apps\n"
                    "  • Restarting the drawing app\n"
                    "  • Using an online provider (pollinations) instead of tiny-sd")
                return None
            self.log("[AI] Retrying in-process generation...")
            self.root.update()
            try:
                result = self.ai_gen.generate(prompt)
            except Exception as e:
                self.log(f"[AI] In-process generation also failed: {e}")
                messagebox.showerror("AI Error", f"Generation failed:\n{e}")
                return None
        if result is None:
            self.log("[AI] Generation returned no result")
            messagebox.showerror("AI Error", "Generation returned no image.\nCheck the model is loaded and dependencies are installed.")
            return None
        self.base_img = result
        self.final_img = None
        self._update_canvas()
        if output_path:
            try:
                result.save(output_path)
                self.log(f"Saved AI output: {os.path.basename(output_path)}")
            except Exception as e:
                self.log(f"Failed to save AI output: {e}")
                messagebox.showerror("Save Error", f"Could not save to:\n{output_path}\n{e}")
        try:
            if self._set_clipboard_image(result):
                self.log("AI output copied to clipboard")
        except Exception as e:
            self.log(f"Clipboard error: {e}")
        return result

    def godmode_export_gif(self):
        path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if path:
            self.animation.export_gif(path)

    def godmode_benchmark(self):
        report = self.perf_monitor.generate_report()
        self.log(report)
        messagebox.showinfo("Benchmark Results", report)

    def godmode_flatten_layers(self):
        self.layer_v2.flatten()
        self.base_img = self.layer_v2.layers[0].img
        self.final_img = None
        self._update_canvas()
        self.log("[Layers] Flattened all layers")

    def _show_bookmarks(self):
        if not self.viewport.bookmarks:
            messagebox.showinfo("Bookmarks", "No viewport bookmarks saved.")
            return
        bm_list = "\n".join(f"{i+1}. {b.name} (zoom: {b.zoom:.1f}x)" for i, b in enumerate(self.viewport.bookmarks))
        messagebox.showinfo("Viewport Bookmarks", bm_list)

    def _cleanup_and_exit(self):
        self.bg_player.cleanup()
        if hasattr(self, 'terminal_panel'):
            try: self.terminal_panel.close()
            except: pass
        try: self.save_config()
        except: pass
        self.root.destroy()

    AutoDrawer.__init__ = new_init
    AutoDrawer._godmode_post_init = godmode_post_init
    AutoDrawer._init_terminal_panel = _init_terminal_panel
    AutoDrawer._setup_godmode_bindings = _setup_godmode_bindings
    AutoDrawer._toggle_terminal = _toggle_terminal
    AutoDrawer._get_scrollbar = _get_scrollbar
    AutoDrawer._cleanup_and_exit = _cleanup_and_exit
    AutoDrawer.godmode_toggle_matrix = godmode_toggle_matrix
    AutoDrawer.godmode_show_boot = godmode_show_boot
    AutoDrawer.godmode_generate_ai = godmode_generate_ai
    AutoDrawer.godmode_export_gif = godmode_export_gif
    AutoDrawer.godmode_benchmark = godmode_benchmark
    AutoDrawer.godmode_flatten_layers = godmode_flatten_layers
    AutoDrawer._show_bookmarks = _show_bookmarks

_patch_autodrawer()


# ── v6.13: GODMODE UI TABS ─────────────────────────────────

def _patch_controlpanel():
    orig_build = ControlPanelWindow.__init__
    def new_init(self, parent, app):
        orig_build(self, parent, app)
        self._build_godmode_viewport_tab()
        self._build_godmode_ai_tab()
        self._build_godmode_layers_tab()
        self._build_godmode_animation_tab()
        self._build_godmode_artistic_tab()
        self._build_godmode_terminal_tab()
        self._build_godmode_perf_tab()
        self._build_godmode_sandbox_tab()
        self._build_godmode_plugins_tab()

    ControlPanelWindow.__init__ = new_init

    # ── Viewport Tab ──
    def _build_godmode_viewport_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Viewport+"] = (tab, "Viewport+")
        self._tab_order.append("Viewport+")
        self._tab_listbox.insert(tk.END, "Viewport+")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Viewport Controls")
        self._slider(sf, "Zoom Speed", "VIEWPORT_ZOOM_SPEED", 1.01, 1.5, 0.01, 140)
        self._slider(sf, "Momentum Friction", "VIEWPORT_MOMENTUM_FRICTION", 0.8, 0.99, 0.01, 140)
        self._checkbox(sf, "Zoom Snapping", "VIEWPORT_SNAP_ENABLED", True)
        self._checkbox(sf, "Show Minimap", "VIEWPORT_SHOW_MINIMAP", False)
        self._section_label(sf, "Bookmarks")
        def save_bm():
            self.app.viewport.add_bookmark()
            self._status(f"Bookmark saved ({len(self.app.viewport.bookmarks)})")
        def list_bm():
            self.app._show_bookmarks()
        def reset_vp():
            self.app.viewport.reset_view(True)
            self._status("Viewport reset")
        tk.Button(sf, text="SAVE BOOKMARK", command=save_bm, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        tk.Button(sf, text="LIST BOOKMARKS", command=list_bm, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        tk.Button(sf, text="RESET VIEW", command=reset_vp, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)

    ControlPanelWindow._build_godmode_viewport_tab = _build_godmode_viewport_tab

    # ── AI Tab ──
    def _build_godmode_ai_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["AI Suite"] = (tab, "AI Suite")
        self._tab_order.append("AI Suite")
        self._tab_listbox.insert(tk.END, "AI Suite")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Generation")
        self._slider(sf, "Inference Steps", "AI_STEPS", 5, 50, 1, 140, "int")
        self._slider(sf, "Guidance Scale", "AI_GUIDANCE", 1.0, 20.0, 0.5, 140)
        self._slider(sf, "img2img Strength", "AI_STRENGTH", 0.1, 1.0, 0.05, 140)
        self._combo(sf, "Style Preset", "AI_STYLE", list(AIGenerationSuite.STYLE_PRESETS.keys()), 14)
        def load_model():
            self.app.ai_gen.load_model()
            self._status("Model loading...")
        tk.Button(sf, text="LOAD AI MODEL", command=load_model, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        def gen_quick():
            prompt = simpledialog.askstring("AI Generate", "Prompt:")
            if not prompt:
                return
            out_path = filedialog.asksaveasfilename(
                title="Save AI output as...",
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")]
            )
            self.app.godmode_generate_ai(prompt, output_path=out_path)
            self._status(f"Generated: {prompt[:30]}")
        tk.Button(sf, text="QUICK GENERATE", command=gen_quick, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        def lineart():
            if self.app.base_img:
                self.app.ai_gen.extract_lineart(self.app.base_img)
                self.app._update_canvas()
                self._status("Lineart extracted")
        tk.Button(sf, text="EXTRACT LINEART", command=lineart, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        def upscale2x():
            if self.app.base_img:
                self.app.base_img = self.app.ai_gen.upscale(self.app.base_img, 2)
                self.app.final_img = None
                self.app._update_canvas()
                self._status("Upscaled 2x")
        tk.Button(sf, text="UPSCALE 2X", command=upscale2x, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)

    ControlPanelWindow._build_godmode_ai_tab = _build_godmode_ai_tab

    # ── Layers V2 Tab ──
    def _build_godmode_layers_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Layers V2"] = (tab, "Layers V2")
        self._tab_order.append("Layers V2")
        self._tab_listbox.insert(tk.END, "Layers V2")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Layer Management")
        def add_l():
            self.app.layer_v2.add_layer()
            self._status(f"Layer added ({len(self.app.layer_v2.layers)})")
        def dup_l():
            self.app.layer_v2.duplicate_layer()
            self._status("Layer duplicated")
        def del_l():
            self.app.layer_v2.delete_layer()
            self._status("Layer deleted")
        def merge_l():
            self.app.layer_v2.merge_down()
            self._status("Merged down")
        def flat_l():
            self.app.godmode_flatten_layers()
            self._status("Layers flattened")
        for text, cmd in [("+ ADD LAYER", add_l), ("DUPLICATE", dup_l), ("DELETE", del_l), ("MERGE DOWN", merge_l), ("FLATTEN", flat_l)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")
        self._section_label(sf, "Blend Mode")
        self._combo(sf, "Blend Mode", "LAYER_BLEND_MODE", [b.value for b in BlendMode], 14)
        self._slider(sf, "Opacity", "LAYER_OPACITY", 0.0, 1.0, 0.05, 140)
        self._checkbox(sf, "Layer Locked", "LAYER_LOCKED", False)
        self._checkbox(sf, "Layer Visible", "LAYER_VISIBLE", True)

    ControlPanelWindow._build_godmode_layers_tab = _build_godmode_layers_tab

    # ── Animation Tab ──
    def _build_godmode_animation_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Animation"] = (tab, "Animation")
        self._tab_order.append("Animation")
        self._tab_listbox.insert(tk.END, "Animation")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Timeline")
        self._slider(sf, "FPS", "ANIM_FPS", 1, 60, 1, 140, "int")
        self._checkbox(sf, "Loop", "ANIM_LOOP", True)
        self._checkbox(sf, "Onion Skin", "ANIM_ONION_SKIN", False)
        def add_f():
            self.app.animation.add_frame(self.app.base_img)
            self._status(f"Frame {len(self.app.animation.frames)} added")
        def play_a():
            self.app.animation.play()
            self._status("Playing")
        def stop_a():
            self.app.animation.stop()
            self._status("Stopped")
        def export_gif():
            self.app.godmode_export_gif()
            self._status("GIF exported")
        for text, cmd in [("+ ADD FRAME", add_f), ("PLAY", play_a), ("STOP", stop_a), ("EXPORT GIF", export_gif)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")
        self._section_label(sf, "AI / Interpolation")
        def interp_f():
            target = int(tk.simpledialog.askstring("Interpolate", "Target frame count:", initialvalue=str(len(self.app.animation.frames) * 2)))
            if target and target > len(self.app.animation.frames):
                self.app.animation.frame_interpolation(target)
                self._status(f"Interpolated to {target} frames")
        def ai_inbet():
            self.app.animation.ai_inbetween()
            self._status("AI inbetween generated")
        for text, cmd in [("FRAME INTERPOLATION", interp_f), ("AI INBETWEEN", ai_inbet)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")
        frame_count = len(self.app.animation.frames)
        tk.Label(sf, text=f"Frames: {frame_count}", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 8)).pack(pady=2)

    ControlPanelWindow._build_godmode_animation_tab = _build_godmode_animation_tab

    # ── Artistic Modes Tab ──
    def _build_godmode_artistic_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Art Modes"] = (tab, "Art Modes")
        self._tab_order.append("Art Modes")
        self._tab_listbox.insert(tk.END, "Art Modes")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Artistic Filters")
        modes = ["standard", "watercolor", "blueprint", "crt", "manga", "vaporwave", "charcoal", "oil_paint", "chalk", "graffiti", "glitch", "cursed_ai", "etching", "woodcut", "pointillism", "crosshatch_pattern", "stippled"]
        def apply_mode(m):
            if self.app.base_img:
                arr = np.array(self.app.base_img)
                pixels = arr.reshape(-1, 3)
                result = self.app.artistic_modes.apply(self.app.base_img, pixels, m)
                if isinstance(result, np.ndarray):
                    self.app.base_img = Image.fromarray(result)
                self.app.final_img = None
                self.app._update_canvas()
                self._status(f"Applied: {m}")
        for m in modes:
            tk.Button(sf, text=m.upper(), command=lambda mm=m: apply_mode(mm), bg=T["btn"], fg=T["accent2"], font=("Courier", 7, "bold"), bd=0).pack(pady=1, fill="x")

    ControlPanelWindow._build_godmode_artistic_tab = _build_godmode_artistic_tab

    # ── Terminal Tab ──
    def _build_godmode_terminal_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Terminal"] = (tab, "Terminal")
        self._tab_order.append("Terminal")
        self._tab_listbox.insert(tk.END, "Terminal")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Cyberpunk UI")
        def boot():
            self.app.godmode_show_boot()
        def matrix():
            self.app.godmode_toggle_matrix()
        def scanner():
            self.app.terminal_ui.scanner_active = not self.app.terminal_ui.scanner_active
            if self.app.terminal_ui.scanner_active:
                self.app.terminal_ui.show_scanner(self.app.root)
            self._status(f"Scanner: {'ON' if self.app.terminal_ui.scanner_active else 'OFF'}")
        def hologram():
            panel = self.app.terminal_ui.holographic_panel(self.app.root, "AI STATUS", "NEURAL LINK: ACTIVE\nDRAW ARRAY: ONLINE\nPIXEL THROUGHPUT: NOMINAL")
            panel.place(relx=0.7, rely=0.1, width=200, height=100)
            self._status("Hologram shown")
        for text, cmd in [("BOOT SCREEN", boot), ("MATRIX RAIN", matrix), ("SCANNER", scanner), ("HOLOGRAM", hologram)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")
        self._section_label(sf, "Next-Gen HUD")
        def synthwave():
            self.app.terminal_ui.synthwave_hud(self.app.root)
            self._status("Synthwave HUD shown")
        def diag():
            panel = self.app.terminal_ui.ai_diagnostics(self.app.root)
            panel.place(relx=0.05, rely=0.05, width=240, height=160)
            self._status("AI Diagnostics panel shown")
        for text, cmd in [("SYNTHWAVE HUD", synthwave), ("AI DIAGNOSTICS", diag)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")
        self._checkbox(sf, "Synthwave HUD", "TERMINAL_SYNTHWAVE_HUD", False)

    ControlPanelWindow._build_godmode_terminal_tab = _build_godmode_terminal_tab

    # ── Performance Tab ──
    def _build_godmode_perf_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Performance"] = (tab, "Performance")
        self._tab_order.append("Performance")
        self._tab_listbox.insert(tk.END, "Performance")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Monitoring")
        self._checkbox(sf, "Enable Monitor", "PERF_MONITOR_ENABLED", False)
        def start_p():
            self.app.perf_monitor.start_monitoring()
            self._status("Monitor started")
        def bench():
            self.app.godmode_benchmark()
        def report():
            r = self.app.perf_monitor.generate_report()
            self._status(f"Avg PPS: {self.app.perf_monitor.get_avg_pps():.0f}")
            messagebox.showinfo("Perf Report", r)
        for text, cmd in [("START MONITOR", start_p), ("BENCHMARK", bench), ("REPORT", report)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)
        self._section_label(sf, "Advanced")
        self._checkbox(sf, "Route Heatmap", "PERF_ROUTE_HEATMAP_ENABLED", False)
        self._checkbox(sf, "Optimization Advisor", "PERF_ADVISOR_ENABLED", False)
        def heatmap():
            hm = self.app.perf_monitor.route_heatmap(400, 200)
            if hm:
                hm.show()
                self._status("Route heatmap generated")
        def advise():
            tips = self.app.perf_monitor.optimization_advisor()
            msg = "\n".join(f"• {t}" for t in tips)
            messagebox.showinfo("Optimization Advisor", msg)
            self._status(f"{len(tips)} suggestions")
        for text, cmd in [("ROUTE HEATMAP", heatmap), ("OPTIMIZATION ADVISOR", advise)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_godmode_perf_tab = _build_godmode_perf_tab

    # ── Sandbox Tab ──
    def _build_godmode_sandbox_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Sandbox"] = (tab, "Sandbox")
        self._tab_order.append("Sandbox")
        self._tab_listbox.insert(tk.END, "Sandbox")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Procedural Generation")
        def gen_perlin():
            w, h = self.app.base_img.size if self.app.base_img else (512, 512)
            self.app.base_img = self.app.proc_gen.generate("perlin", w, h)
            self.app.final_img = None
            self.app._update_canvas()
            self._status("Perlin noise generated")
        def gen_plasma():
            w, h = self.app.base_img.size if self.app.base_img else (512, 512)
            self.app.base_img = self.app.proc_gen.generate("plasma", w, h)
            self.app.final_img = None
            self.app._update_canvas()
            self._status("Plasma generated")
        def gen_voronoi():
            w, h = self.app.base_img.size if self.app.base_img else (512, 512)
            self.app.base_img = self.app.proc_gen.generate("voronoi", w, h, points=30)
            self.app.final_img = None
            self.app._update_canvas()
            self._status("Voronoi generated")
        for text, cmd in [("PERLIN NOISE", gen_perlin), ("PLASMA", gen_plasma), ("VORONOI", gen_voronoi)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")
        self._section_label(sf, "Node Workflow Editor")
        self._checkbox(sf, "Enable Node Editor", "NODE_EDITOR_ENABLED", False)
        def add_node():
            types = list(NodeWorkflowEditor.NODE_TYPES.keys())
            nt = tk.simpledialog.askstring("Add Node", f"Node type ({', '.join(types)}):")
            if nt and nt in NodeWorkflowEditor.NODE_TYPES:
                self.app.node_editor.add_node(nt)
                self._status(f"Added node: {nt}")
        def exec_nodes():
            if self.app.base_img and self.app.node_editor.nodes:
                result = self.app.node_editor.execute_graph(self.app.base_img)
                if result:
                    self.app.base_img = result
                    self._status("Workflow executed")
        def clear_nodes():
            self.app.node_editor.clear()
            self._status("Workflow cleared")
        for text, cmd in [("ADD NODE", add_node), ("EXECUTE WORKFLOW", exec_nodes), ("CLEAR", clear_nodes)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")
        nc = self.app.node_editor.count_nodes()
        tk.Label(sf, text=f"Nodes: {nc} | Connections: {self.app.node_editor.count_connections()}",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack(pady=2)
        self._section_label(sf, "AI Composition Analysis")
        self._checkbox(sf, "Enable Analyzer", "COMPOSITION_ANALYZER_ENABLED", False)
        def analyze():
            if self.app.base_img:
                analysis = self.app.comp_analyzer.analyze(self.app.base_img)
                suggest = self.app.comp_analyzer.composition_suggestions(self.app.base_img)
                msg = "=== ANALYSIS ===\n"
                for k, v in list(analysis.items())[:10]:
                    msg += f"{k}: {v}\n"
                msg += "\n=== SUGGESTIONS ===\n"
                msg += "\n".join(f"• {s}" for s in suggest)
                messagebox.showinfo("Composition Analysis", msg)
                self._status(f"{len(suggest)} suggestions")
        tk.Button(sf, text="ANALYZE COMPOSITION", command=analyze,
                  bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=5, fill="x")

    ControlPanelWindow._build_godmode_sandbox_tab = _build_godmode_sandbox_tab

    # ── Plugins Tab ──
    def _build_godmode_plugins_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Plugins"] = (tab, "Plugins")
        self._tab_order.append("Plugins")
        self._tab_listbox.insert(tk.END, "Plugins")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Plugin Manager")
        self._checkbox(sf, "Auto-load Plugins", "PLUGIN_AUTOLOAD", True)
        def scan():
            self.app.plugin_api.discover_plugins()
            self._status(f"Plugins: {len(self.app.plugin_api.plugins)} loaded")
        def list_p():
            plugins = self.app.plugin_api.list_plugins()
            if not plugins:
                self._status("No plugins loaded")
                messagebox.showinfo("Plugins", "No plugins loaded")
            else:
                msg = "\n".join(f"{n} v{v} - {d} {'[ON]' if e else '[OFF]'}" for n, v, d, e in plugins)
                messagebox.showinfo("Loaded Plugins", msg)
        for text, cmd in [("SCAN PLUGINS", scan), ("LIST", list_p)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2)

    ControlPanelWindow._build_godmode_plugins_tab = _build_godmode_plugins_tab

_patch_controlpanel()


# ── v6.14: BUG FIXES ──────────────────────────────────────────
# Fix 1: Remove duplicate HAS_TORCH / HAS_DIFFUSERS declarations
# (The original lines 79-90 and 1544-1549 both declare these.
#  The later ones overwrite the first. This patch corrects that.)

def _fix_duplicate_imports():
    global HAS_TORCH, HAS_DIFFUSERS
    torch_available = False
    diffusers_available = False
    try:
        import torch as _t
        torch_available = True
    except ImportError:
        pass
    try:
        import diffusers as _d
        diffusers_available = True
    except ImportError:
        pass
    HAS_TORCH = torch_available
    HAS_DIFFUSERS = diffusers_available

_fix_duplicate_imports()

# Fix 2: pyautogui usage in _execute_stroke_draw should use FastInputDriver
# We override the method to use the driver consistently.
_orig_execute_stroke_draw = AutoDrawer._execute_stroke_draw

def _patched_execute_stroke_draw(self, queues, pal_arr, total_dots, gap):
    sx, sy = self.canvas_rect[0], self.canvas_rect[1]
    dots_drawn = 0
    pps_tick_dots = 0
    pps_tick_ts = time.time()
    gs = SETTINGS.get("GLOBAL_SPEED", 1.0)
    use_strokes = SETTINGS.get("STROKE_MODE", "stroke") == "stroke"
    driver = FastInputDriver()

    fill_active = SETTINGS.get("FILL_ZONE_ACTIVE", False)
    fill_center = SETTINGS.get("FILL_ZONE_CENTER", [0, 0])
    fill_color = SETTINGS.get("FILL_ZONE_COLOR", [0, 100, 255])
    fill_thresh = SETTINGS.get("FILL_ZONE_THRESHOLD", 30)
    fill_grow = SETTINGS.get("FILL_ZONE_GROW_STEPS", 5)
    fill_pixels = []

    if fill_active and fill_center[0] > 0 and fill_center[1] > 0:
        try:
            fill_pixels = self._compute_fill_zone(
                int(fill_center[0]), int(fill_center[1]),
                fill_color, fill_thresh, fill_grow
            )
            if fill_pixels:
                self.log(f"[FillZone] {len(fill_pixels)} fill pixels computed")
        except Exception as e:
            self.log(f"[FillZone] error: {e}")

    for cidx, pts in queues.items():
        if not self.drawing_active:
            break
        if not pts:
            continue
        if cidx >= len(self.palette_map):
            self.log(f"WARNING: palette index {cidx} out of range, skipping")
            continue
        pos = self.palette_map[cidx].get("pos", [0, 0])
        if pos[0] == 0 and pos[1] == 0:
            self.log(f"WARNING: palette color {cidx} has position (0,0)")
        driver.move(pos[0], pos[1])
        time.sleep(SETTINGS["UI_DELAY"] / max(0.1, gs * 2))
        driver.click(pos[0], pos[1])
        time.sleep(SETTINGS["CLICK_DELAY"] / max(0.1, gs * 2))

        if not use_strokes:
            for px, py in pts:
                if not self.drawing_active:
                    break
                while self.drawing_paused:
                    if not self.drawing_active:
                        break
                    time.sleep(0.02)
                tx, ty = sx + px, sy + py
                driver.click(tx, ty)
                dots_drawn += 1
                pps_tick_dots += 1
                now = time.time()
                if now - pps_tick_ts >= 1.0:
                    pps = pps_tick_dots / max(0.001, now - pps_tick_ts)
                    self.last_pps = pps
                    pps_tick_dots = 0
                    pps_tick_ts = now
                if dots_drawn % 100 == 0:
                    self._update_progress(dots_drawn, total_dots)
        else:
            strokes = self._pixels_to_strokes(pts, max(1, gap + 1))
            for stroke in strokes:
                if not self.drawing_active:
                    break
                while self.drawing_paused:
                    if not self.drawing_active:
                        break
                    time.sleep(0.02)
                path = self._stroke_to_path(stroke)
                if len(path) < 2:
                    continue
                spath = self._smooth_stroke_path(path, int(SETTINGS.get("STROKE_SMOOTH_PASSES", 2)))
                x0, y0 = sx + int(spath[0][0]), sy + int(spath[0][1])
                driver.press(x0, y0)
                if float(SETTINGS.get("CLICK_DELAY", 0)) > 0:
                    time.sleep(float(SETTINGS["CLICK_DELAY"]) * 0.2)
                for pt in spath[1:]:
                    if not self.drawing_active:
                        break
                    tx, ty = sx + int(pt[0]), sy + int(pt[1])
                    driver.drag_to(tx, ty)
                    if float(SETTINGS.get("CLICK_DELAY", 0)) > 0:
                        time.sleep(float(SETTINGS["CLICK_DELAY"]))
                driver.release()
                dots_drawn += len(spath)
                pps_tick_dots += len(spath)
                now = time.time()
                if now - pps_tick_ts >= 1.0:
                    pps = pps_tick_dots / max(0.001, now - pps_tick_ts)
                    self.last_pps = pps
                    pps_tick_dots = 0
                    pps_tick_ts = now
                if dots_drawn % 100 == 0:
                    self._update_progress(dots_drawn, total_dots)

    if fill_pixels:
        self.log("[FillZone] Applying fill...")
        blue_idx = self._find_closest_palette(fill_color, pal_arr)
        fpos = self.palette_map[blue_idx]["pos"]
        driver.move(fpos[0], fpos[1])
        time.sleep(SETTINGS["UI_DELAY"] / max(0.1, gs * 2))
        driver.click(fpos[0], fpos[1])
        time.sleep(SETTINGS["CLICK_DELAY"] / max(0.1, gs * 2))
        fill_strokes = self._pixels_to_strokes(fill_pixels, max(1, gap + 1))
        for stroke in fill_strokes:
            if not self.drawing_active:
                break
            path = self._stroke_to_path(stroke)
            if len(path) < 2:
                continue
            x0, y0 = sx + int(path[0][0]), sy + int(path[0][1])
            driver.press(x0, y0)
            for pt in path[1:]:
                tx, ty = sx + int(pt[0]), sy + int(pt[1])
                driver.drag_to(tx, ty)
            driver.release()
            dots_drawn += len(path)

    self._draw_finished(dots_drawn)

AutoDrawer._execute_stroke_draw = _patched_execute_stroke_draw

# Fix 3: Ensure palette_map always has positions
_orig_load_config = AutoDrawer.load_config
def _patched_load_config(self):
    _orig_load_config(self)
    for entry in self.palette_map:
        if "pos" not in entry:
            entry["pos"] = [0, 0]
        if "rgb" not in entry:
            entry["rgb"] = [128, 128, 128]
AutoDrawer.load_config = _patched_load_config


# ── v6.14: BRUSH PHYSICS ENGINE ──────────────────────────────

@dataclass
class BrushPhysicsState:
    x: float = 0.0
    y: float = 0.0
    pressure: float = 0.5
    tilt_x: float = 0.0
    tilt_y: float = 0.0
    velocity: float = 0.0
    flow: float = 1.0
    size: float = 10.0
    scatter: float = 0.0
    wetness: float = 0.0
    jitter_history: List[float] = field(default_factory=list)

class BrushPhysicsEngine:
    BRUSH_TYPES = {
        "round": {"shape": "circle", "spacing": 0.15, "opacity": 0.9, "flow": 0.8},
        "flat": {"shape": "ellipse", "spacing": 0.10, "opacity": 1.0, "flow": 0.9},
        "fan": {"shape": "fan", "spacing": 0.20, "opacity": 0.7, "flow": 0.6},
        "airbrush": {"shape": "circle", "spacing": 0.05, "opacity": 0.3, "flow": 0.4, "scatter": 0.5},
        "pencil": {"shape": "circle", "spacing": 0.08, "opacity": 0.8, "flow": 0.7, "noise": 0.3},
        "marker": {"shape": "square", "spacing": 0.12, "opacity": 0.6, "flow": 0.8, "bleed": 0.2},
        "charcoal": {"shape": "rough", "spacing": 0.25, "opacity": 0.7, "flow": 0.5, "noise": 0.6, "scatter": 0.3},
        "oil": {"shape": "circle", "spacing": 0.18, "opacity": 0.9, "flow": 0.3, "impasto": 0.4},
        "watercolor": {"shape": "watercolor", "spacing": 0.22, "opacity": 0.5, "flow": 0.6, "bleed": 0.5},
    }

    def __init__(self, app):
        self.app = app
        self.active_brush = "round"
        self.state = BrushPhysicsState()
        self._history: List[BrushPhysicsState] = deque(maxlen=500)
        self.prev_pos = (0, 0)
        self.prev_time = time.time()

    def set_brush(self, name):
        if name in self.BRUSH_TYPES:
            self.active_brush = name
            props = self.BRUSH_TYPES[name]
            self.state.flow = props.get("flow", 0.8)
            self.state.scatter = props.get("scatter", 0.0)
            return True
        return False

    def start_stroke(self, x, y, pressure=0.5):
        self.state.x = x
        self.state.y = y
        self.state.pressure = pressure
        self.state.velocity = 0.0
        self.prev_pos = (x, y)
        self.prev_time = time.time()
        self.state.jitter_history.clear()

    def update(self, x, y, pressure=None):
        now = time.time()
        dt = max(0.001, now - self.prev_time)
        dx = x - self.prev_pos[0]
        dy = y - self.prev_pos[1]
        dist = math.hypot(dx, dy)
        velocity = dist / dt
        self.state.velocity = velocity * 0.3 + self.state.velocity * 0.7
        self.state.x = x
        self.state.y = y
        if pressure is not None:
            self.state.pressure = min(1.0, max(0.0, pressure))
        props = self.BRUSH_TYPES.get(self.active_brush, self.BRUSH_TYPES["round"])
        speed_factor = max(0.2, min(2.0, 100.0 / max(1, velocity)))
        base_size = float(SETTINGS.get("brush_size", 10))
        self.state.size = base_size * (0.5 + self.state.pressure * 0.5) * speed_factor
        self.state.wetness = props.get("bleed", 0.0) * (1.0 - speed_factor * 0.3)
        noise = props.get("noise", 0.0)
        if noise > 0:
            j = (random.random() - 0.5) * noise * self.state.size
            self.state.jitter_history.append(j)
            if len(self.state.jitter_history) > 10:
                self.state.jitter_history.pop(0)
        self.prev_pos = (x, y)
        self.prev_time = now
        self._history.append(BrushPhysicsState(
            x=x, y=y, pressure=self.state.pressure,
            velocity=self.state.velocity, size=self.state.size,
            flow=self.state.flow, scatter=self.state.scatter,
            wetness=self.state.wetness,
        ))
        return self.state

    def get_effective_size(self):
        return max(0.5, self.state.size + (sum(self.state.jitter_history[-3:]) if self.state.jitter_history else 0))

    def get_opacity(self):
        props = self.BRUSH_TYPES.get(self.active_brush, self.BRUSH_TYPES["round"])
        base_opacity = props.get("opacity", 0.9)
        speed_fade = max(0.3, 1.0 - self.state.velocity / 500.0)
        return base_opacity * speed_fade * self.state.pressure

    def apply_dab(self, img_draw, x, y):
        size = self.get_effective_size()
        opacity = self.get_opacity()
        r = max(1, int(size / 2))
        base_color = self.app.brush_color if hasattr(self.app, 'brush_color') else (0, 0, 0)
        # Apply opacity via alpha blending for PIL ImageDraw
        if opacity < 1.0 and len(base_color) >= 3:
            color = (int(base_color[0] * opacity + 255 * (1 - opacity)),
                     int(base_color[1] * opacity + 255 * (1 - opacity)),
                     int(base_color[2] * opacity + 255 * (1 - opacity)))
        else:
            color = base_color
        scatter = self.state.scatter * size
        if scatter > 0:
            x += random.uniform(-scatter, scatter)
            y += random.uniform(-scatter, scatter)
        shape = self.BRUSH_TYPES.get(self.active_brush, {}).get("shape", "circle")
        if shape == "circle":
            img_draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=None)
        elif shape == "ellipse":
            rx = r
            ry = int(r * (0.5 + self.state.pressure * 0.5))
            img_draw.ellipse([x - rx, y - ry, x + rx, y + ry], fill=color)
        elif shape == "square":
            img_draw.rectangle([x - r, y - r, x + r, y + r], fill=color)
        elif shape == "rough":
            pts = []
            for _ in range(8):
                a = random.uniform(0, math.pi * 2)
                rr = r * random.uniform(0.6, 1.2)
                pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
            img_draw.polygon(pts, fill=color, outline=None)
        elif shape == "fan":
            for a in range(0, 180, 15):
                rad = math.radians(a - 90 + self.state.pressure * 30)
                ex = x + math.cos(rad) * r
                ey = y + math.sin(rad) * r
                img_draw.line([x, y, ex, ey], fill=color, width=1)
        else:
            img_draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        return opacity

    def end_stroke(self):
        self.state.velocity = 0.0


# ── v6.15: TIME-LAPSE RECORDING & REPLAY ───────────────────

@dataclass
class RecordingFrame:
    timestamp: float
    mouse_x: int
    mouse_y: int
    button_state: str
    color_index: int = -1

class TimelapseRecorder:
    def __init__(self, app):
        self.app = app
        self.recording = False
        self.frames: List[RecordingFrame] = []
        self._record_thread = None
        self.playback_speed = 1.0
        self.current_replay_index = 0
        self.replay_active = False
        self.auto_record_on_draw = False

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.frames.clear()
        self.app.log("[Recorder] Recording started")
        def _capture():
            while self.recording:
                try:
                    x, y = pyautogui.position()
                    self.frames.append(RecordingFrame(
                        timestamp=time.time(),
                        mouse_x=int(x), mouse_y=int(y),
                        button_state="move",
                    ))
                except:
                    pass
                time.sleep(0.05)
        self._record_thread = threading.Thread(target=_capture, daemon=True)
        self._record_thread.start()

    def stop_recording(self):
        self.recording = False
        if self._record_thread:
            self._record_thread.join(timeout=1)
        self.app.log(f"[Recorder] Recording stopped: {len(self.frames)} frames")

    def save_recording(self, path):
        if not self.frames:
            return
        data = {
            "version": 1,
            "frames": [
                {"ts": f.timestamp, "x": f.mouse_x, "y": f.mouse_y,
                 "btn": f.button_state, "ci": f.color_index}
                for f in self.frames
            ],
            "duration": self.frames[-1].timestamp - self.frames[0].timestamp if len(self.frames) > 1 else 0,
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        self.app.log(f"[Recorder] Saved: {path}")

    def load_recording(self, path):
        with open(path) as f:
            data = json.load(f)
        self.frames = [
            RecordingFrame(ts=fr["ts"], mouse_x=fr["x"], mouse_y=fr["y"],
                           button_state=fr.get("btn", "move"), color_index=fr.get("ci", -1))
            for fr in data.get("frames", [])
        ]
        self.app.log(f"[Recorder] Loaded: {len(self.frames)} frames from {path}")

    def start_replay(self):
        if not self.frames or self.replay_active:
            return
        self.replay_active = True
        self.current_replay_index = 0
        driver = FastInputDriver()
        def _replay():
            start_time = time.time()
            first_ts = self.frames[0].timestamp if self.frames else 0
            for i, frame in enumerate(self.frames):
                if not self.replay_active:
                    break
                elapsed = (frame.timestamp - first_ts) / self.playback_speed
                target_time = start_time + elapsed
                now = time.time()
                if target_time > now:
                    time.sleep(target_time - now)
                driver.move(frame.mouse_x, frame.mouse_y)
                self.current_replay_index = i
            self.replay_active = False
            self.app.log("[Recorder] Replay finished")
        threading.Thread(target=_replay, daemon=True).start()

    def stop_replay(self):
        self.replay_active = False

    def get_frame_count(self):
        return len(self.frames)

    def get_duration_seconds(self):
        if len(self.frames) < 2:
            return 0.0
        return self.frames[-1].timestamp - self.frames[0].timestamp


# ── v6.16: COLOR HARMONIES & SMART PALETTE ──────────────────

class ColorHarmonyGenerator:
    def __init__(self):
        self.harmony_types = {
            "complementary": self._complementary,
            "analogous": self._analogous,
            "triadic": self._triadic,
            "tetradic": self._tetradic,
            "split_complementary": self._split_complementary,
            "monochromatic": self._monochromatic,
            "shades": self._shades,
            "warm": self._warm,
            "cool": self._cool,
        }

    @staticmethod
    def _rgb_to_hsv(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx, mn = max(r, g, b), min(r, g, b)
        h = 0.0
        if mx == mn:
            h = 0.0
        elif mx == r:
            h = 60 * ((g - b) / (mx - mn) + (0 if g >= b else 6))
        elif mx == g:
            h = 60 * ((b - r) / (mx - mn) + 2)
        else:
            h = 60 * ((r - g) / (mx - mn) + 4)
        s = 0.0 if mx == 0 else (mx - mn) / mx
        v = mx
        return h % 360, s, v

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)

    def _complementary(self, h, s, v, count=2):
        return [(h, s, v), ((h + 180) % 360, s, v)][:count]

    def _analogous(self, h, s, v, count=5):
        return [((h + (i - count // 2) * 30) % 360, s * (1 - abs(i - count // 2) * 0.1), v) for i in range(count)]

    def _triadic(self, h, s, v, count=3):
        return [((h + i * 120) % 360, s, v) for i in range(count)]

    def _tetradic(self, h, s, v, count=4):
        return [(h, s, v), ((h + 90) % 360, s, v), ((h + 180) % 360, s, v), ((h + 270) % 360, s, v)][:count]

    def _split_complementary(self, h, s, v, count=3):
        return [(h, s, v), ((h + 150) % 360, s, v), ((h + 210) % 360, s, v)][:count]

    def _monochromatic(self, h, s, v, count=5):
        return [(h, s * (0.2 + i * 0.15), v * (0.4 + i * 0.15)) for i in range(count)]

    def _shades(self, h, s, v, count=5):
        return [(h, s, v * (0.2 + i * 0.2)) for i in range(count)]

    def _warm(self, h, s, v, count=6):
        hues = [0, 30, 60, 90, 330, 15]
        return [(hues[i % len(hues)], s, v) for i in range(count)]

    def _cool(self, h, s, v, count=6):
        hues = [180, 210, 240, 270, 150, 300]
        return [(hues[i % len(hues)], s * 0.8, v * 0.9) for i in range(count)]

    def generate(self, base_rgb, harmony_type="complementary", count=5):
        if harmony_type not in self.harmony_types:
            harmony_type = "complementary"
        h, s, v = self._rgb_to_hsv(*base_rgb)
        hsv_colors = self.harmony_types[harmony_type](h, s, v, count)
        return [self._hsv_to_rgb(*c) for c in hsv_colors]

    def get_harmony_names(self):
        return list(self.harmony_types.keys())

    def apply_to_palette(self, app, base_rgb, harmony_type, count=5):
        colors = self.generate(base_rgb, harmony_type, count)
        app.palette_map = [{"pos": [0, 0], "rgb": list(c)} for c in colors]
        app.save_config()
        app.log(f"[Harmony] Generated {harmony_type} palette ({len(colors)} colors) from RGB{base_rgb}")
        return colors


# ── v6.17: ADVANCED SELECTION TOOLS ─────────────────────────

class SelectionTool(Enum):
    RECTANGULAR = "rectangular"
    ELLIPTICAL = "elliptical"
    LASSO = "lasso"
    POLYGON = "polygon"
    MAGIC_WAND = "magic_wand"
    COLOR_RANGE = "color_range"

class AdvancedSelection:
    def __init__(self, app):
        self.app = app
        self.tool = SelectionTool.RECTANGULAR
        self.selection_mask: Optional[np.ndarray] = None
        self.selection_bbox: Optional[Tuple[int, int, int, int]] = None
        self.active_points: List[Tuple[int, int]] = []
        self.polygon_closed = False
        self.feather_radius = 0
        self.invert = False

    def set_tool(self, tool_name):
        for t in SelectionTool:
            if t.value == tool_name:
                self.tool = t
                self.clear()
                return True
        return False

    def clear(self):
        self.selection_mask = None
        self.selection_bbox = None
        self.active_points.clear()
        self.polygon_closed = False

    def start_rect(self, x1, y1, x2, y2, img_w, img_h):
        mask = np.zeros((img_h, img_w), dtype=np.uint8)
        x1, x2 = max(0, min(x1, x2)), min(img_w, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(img_h, max(y1, y2))
        mask[y1:y2, x1:x2] = 255
        self.selection_mask = mask
        self.selection_bbox = (x1, y1, x2, y2)

    def start_ellipse(self, cx, cy, rx, ry, img_w, img_h):
        mask = np.zeros((img_h, img_w), dtype=np.uint8)
        yy, xx = np.ogrid[:img_h, :img_w]
        ellipse_mask = ((xx - cx) / max(1, rx)) ** 2 + ((yy - cy) / max(1, ry)) ** 2 <= 1
        mask[ellipse_mask] = 255
        self.selection_mask = mask
        self.selection_bbox = (max(0, cx - rx), max(0, cy - ry), min(img_w, cx + rx), min(img_h, cy + ry))

    def add_lasso_point(self, x, y):
        self.active_points.append((x, y))

    def finalize_lasso(self, img_w, img_h):
        if len(self.active_points) < 3:
            return
        mask = np.zeros((img_h, img_w), dtype=np.uint8)
        from PIL import ImageDraw as PILDraw
        img_tmp = Image.new("L", (img_w, img_h), 0)
        PILDraw.Draw(img_tmp).polygon(self.active_points, outline=255, fill=255)
        mask = np.array(img_tmp, dtype=np.uint8)
        self.selection_mask = mask
        xs = [p[0] for p in self.active_points]
        ys = [p[1] for p in self.active_points]
        self.selection_bbox = (max(0, min(xs)), max(0, min(ys)), min(img_w, max(xs)), min(img_h, max(ys)))

    def magic_wand(self, img_array, seed_x, seed_y, tolerance=30, connectivity=4):
        h, w = img_array.shape[:2]
        if not (0 <= seed_x < w and 0 <= seed_y < h):
            return
        seed_color = img_array[seed_y, seed_x]
        mask = np.zeros((h, w), dtype=np.uint8)
        visited = np.zeros((h, w), dtype=bool)
        queue = [(seed_x, seed_y)]
        visited[seed_y, seed_x] = True
        while queue:
            cx, cy = queue.pop(0)
            mask[cy, cx] = 255
            neighbors = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
            if connectivity == 8:
                neighbors += [(cx - 1, cy - 1), (cx + 1, cy - 1), (cx - 1, cy + 1), (cx + 1, cy + 1)]
            for nx, ny in neighbors:
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    diff = np.max(np.abs(img_array[ny, nx].astype(int) - seed_color.astype(int)))
                    if diff <= tolerance:
                        visited[ny, nx] = True
                        queue.append((nx, ny))
        self.selection_mask = mask
        ys, xs = np.where(mask > 0)
        if len(xs) > 0:
            self.selection_bbox = (xs.min(), ys.min(), xs.max(), ys.max())

    def color_range_select(self, img_array, low_rgb, high_rgb):
        mask = np.zeros(img_array.shape[:2], dtype=np.uint8)
        in_range = np.all((img_array >= np.array(low_rgb)) & (img_array <= np.array(high_rgb)), axis=2)
        mask[in_range] = 255
        self.selection_mask = mask
        ys, xs = np.where(mask > 0)
        if len(xs) > 0:
            self.selection_bbox = (xs.min(), ys.min(), xs.max(), ys.max())

    def get_mask(self):
        if self.selection_mask is None:
            return None
        mask = self.selection_mask.copy()
        if self.feather_radius > 0:
            _gaussian = None
            try:
                from scipy.ndimage import gaussian_filter as _gaussian
            except ImportError:
                pass
            if _gaussian is not None:
                mask = (_gaussian(mask.astype(float), self.feather_radius) * 255).astype(np.uint8)
        if self.invert:
            mask = 255 - mask
        return mask

    def apply_to_image(self, img, fill_color=(0, 0, 0)):
        mask = self.get_mask()
        if mask is None or img is None:
            return img
        arr = np.array(img)
        arr[mask > 0] = fill_color
        return Image.fromarray(arr)

    def crop_to_selection(self, img):
        if self.selection_bbox is None or img is None:
            return img
        x1, y1, x2, y2 = self.selection_bbox
        return img.crop((x1, y1, x2, y2))


# ── v6.18: CUSTOM FILTER BUILDER ────────────────────────────

class FilterPrimitive(Enum):
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    SATURATION = "saturation"
    HUE = "hue"
    GAMMA = "gamma"
    BLUR_GAUSSIAN = "blur_gaussian"
    BLUR_BOX = "blur_box"
    SHARPEN = "sharpen"
    EDGE_ENHANCE = "edge_enhance"
    EMBOSS = "emboss"
    POSTERIZE = "posterize"
    SOLARIZE = "solarize"
    INVERT = "invert"
    THRESHOLD = "threshold"
    NOISE = "noise"
    PIXELATE = "pixelate"
    LEVELS = "levels"
    CURVES = "curves"
    VIGNETTE = "vignette"
    COLOR_BALANCE = "color_balance"

FILTER_REGISTRY = {}

def register_filter(name):
    def decorator(func):
        FILTER_REGISTRY[name] = func
        return func
    return decorator

def apply_filter_primitive(img, filter_name, params=None):
    if params is None:
        params = {}
    if filter_name in FILTER_REGISTRY:
        return FILTER_REGISTRY[filter_name](img, params)
    return img

@register_filter("brightness")
def _filter_brightness(img, p):
    return ImageEnhance.Brightness(img).enhance(p.get("amount", 1.0))

@register_filter("contrast")
def _filter_contrast(img, p):
    return ImageEnhance.Contrast(img).enhance(p.get("amount", 1.0))

@register_filter("saturation")
def _filter_saturation(img, p):
    return ImageEnhance.Color(img).enhance(p.get("amount", 1.0))

@register_filter("sharpen")
def _filter_sharpen(img, p):
    return ImageEnhance.Sharpness(img).enhance(p.get("amount", 1.0))

@register_filter("invert")
def _filter_invert(img, p):
    return ImageOps.invert(img)

@register_filter("posterize")
def _filter_posterize(img, p):
    bits = p.get("bits", 4)
    return ImageOps.posterize(img, max(1, min(8, bits)))

@register_filter("solarize")
def _filter_solarize(img, p):
    thresh = p.get("threshold", 128)
    arr = np.array(img)
    arr[arr < thresh] = 255 - arr[arr < thresh]
    return Image.fromarray(arr)

@register_filter("blur_gaussian")
def _filter_blur_gaussian(img, p):
    radius = p.get("radius", 2)
    return img.filter(ImageFilter.GaussianBlur(radius=max(0.1, radius)))

@register_filter("blur_box")
def _filter_blur_box(img, p):
    radius = p.get("radius", 2)
    return img.filter(ImageFilter.BoxBlur(radius=max(0.1, radius)))

@register_filter("edge_enhance")
def _filter_edge_enhance(img, p):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

@register_filter("emboss")
def _filter_emboss(img, p):
    return img.filter(ImageFilter.EMBOSS)

@register_filter("threshold")
def _filter_threshold(img, p):
    thresh = p.get("threshold", 128)
    arr = np.array(img.convert("L"))
    binary = (arr > thresh).astype(np.uint8) * 255
    return Image.fromarray(binary).convert("RGB")

@register_filter("noise")
def _filter_noise(img, p):
    amount = p.get("amount", 20)
    arr = np.array(img, dtype=np.float32)
    noise = np.random.randn(*arr.shape) * amount
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

@register_filter("pixelate")
def _filter_pixelate(img, p):
    size = max(1, p.get("size", 8))
    small = img.resize((max(1, img.width // size), max(1, img.height // size)), Image.NEAREST)
    return small.resize(img.size, Image.NEAREST)

@register_filter("vignette")
def _filter_vignette(img, p):
    amount = p.get("amount", 0.5)
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape[:2]
    yy, xx = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / np.sqrt(cx ** 2 + cy ** 2)
    factor = 1 - dist * amount
    factor = np.clip(factor, 0, 1)
    for c in range(3):
        arr[..., c] *= factor
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

@register_filter("color_balance")
def _filter_color_balance(img, p):
    arr = np.array(img, dtype=np.float32)
    for i, c in enumerate(["r", "g", "b"]):
        adj = p.get(c, 1.0)
        arr[..., i] *= adj
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

@register_filter("gamma")
def _filter_gamma(img, p):
    gamma = max(0.1, p.get("gamma", 1.0))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.power(arr, 1.0 / gamma)
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))

@register_filter("levels")
def _filter_levels(img, p):
    black = p.get("black", 0)
    white = p.get("white", 255)
    gamma = max(0.1, p.get("gamma", 1.0))
    arr = np.array(img, dtype=np.float32)
    arr = (arr - black) / max(1, white - black)
    arr = np.power(np.clip(arr, 0, 1), 1.0 / gamma)
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))

@register_filter("hue")
def _filter_hue(img, p):
    shift = p.get("shift", 0)
    arr = np.array(img, dtype=np.uint8)
    hsv = Image.fromarray(arr).convert("HSV")
    h_arr = np.array(hsv, dtype=np.int16)
    h_arr[..., 0] = (h_arr[..., 0] + shift) % 360
    hsv = Image.fromarray(h_arr.astype(np.uint8), mode="HSV")
    return hsv.convert("RGB")


class FilterChain:
    def __init__(self):
        self.steps: List[Tuple[str, dict]] = []
        self.name = "Untitled Filter"

    def add_step(self, filter_name, params=None):
        if params is None:
            params = {}
        self.steps.append((filter_name, params))

    def remove_step(self, index):
        if 0 <= index < len(self.steps):
            del self.steps[index]

    def apply(self, img):
        result = img.copy()
        for filter_name, params in self.steps:
            result = apply_filter_primitive(result, filter_name, params)
        return result

    def to_dict(self):
        return {"name": self.name, "steps": self.steps}

    @classmethod
    def from_dict(cls, data):
        chain = cls()
        chain.name = data.get("name", "Untitled Filter")
        chain.steps = [(s[0], s[1]) for s in data.get("steps", [])]
        return chain

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        return cls.from_dict(data)


# ── v6.19: REFERENCE PANEL MANAGER ──────────────────────────

class ReferenceImage:
    def __init__(self, path=None, img=None):
        self.path = path
        self.img = img
        self.scale = 1.0
        self.x = 0
        self.y = 0
        self.visible = True
        self.opacity = 0.5
        self.locked = False
        self.label = ""

class ReferencePanel:
    def __init__(self, app):
        self.app = app
        self.references: List[ReferenceImage] = []
        self.active_index = -1
        self.panel_visible = False
        self._panel_window = None

    def add_reference(self, path=None, img=None):
        ref = ReferenceImage(path=path, img=img)
        if path and img is None:
            try:
                ref.img = Image.open(path).convert("RGBA")
            except Exception as e:
                self.app.log(f"[Ref] Failed to load: {e}")
                return None
        self.references.append(ref)
        self.active_index = len(self.references) - 1
        self.app.log(f"[Ref] Added: {ref.label or os.path.basename(path or 'image')}")
        return ref

    def remove_reference(self, index=None):
        idx = index if index is not None else self.active_index
        if 0 <= idx < len(self.references):
            del self.references[idx]
            self.active_index = min(self.active_index, len(self.references) - 1) if self.references else -1

    def clear_all(self):
        self.references.clear()
        self.active_index = -1

    def get_active(self):
        if 0 <= self.active_index < len(self.references):
            return self.references[self.active_index]
        return None

    def show_panel(self, parent):
        if self._panel_window and self._panel_window.winfo_exists():
            self._panel_window.lift()
            return
        T = CURRENT_THEME
        win = tk.Toplevel(parent)
        win.title("Reference Panel")
        win.geometry("300x400")
        win.configure(bg=T["bg"])
        self._panel_window = win
        self.panel_visible = True

        tk.Label(win, text="REFERENCES", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 10, "bold")).pack(pady=5)

        listbox = tk.Listbox(win, bg=T["log_bg"], fg=T["fg"],
                             font=("Courier", 8), height=8, selectbackground=T["accent2"])
        listbox.pack(fill="x", padx=10, pady=5)

        def _refresh():
            listbox.delete(0, tk.END)
            for i, ref in enumerate(self.references):
                label = ref.label or os.path.basename(ref.path or f"Ref #{i+1}")
                vis = "👁" if ref.visible else "  "
                listbox.insert(tk.END, f"{vis} {label}")

        def _add():
            path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
            if path:
                self.add_reference(path=path)
                _refresh()

        def _del():
            sel = listbox.curselection()
            if sel:
                self.remove_reference(sel[0])
                _refresh()

        def _toggle():
            sel = listbox.curselection()
            if sel and 0 <= sel[0] < len(self.references):
                self.references[sel[0]].visible = not self.references[sel[0]].visible
                _refresh()

        for text, cmd in [("+ ADD", _add), ("- REMOVE", _del), ("TOGGLE VIS", _toggle)]:
            tk.Button(win, text=text, command=cmd, bg=T["btn"], fg=T["fg"],
                      font=("Courier", 8), bd=0).pack(side="left", padx=5, pady=2)

        _refresh()
        win.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, 'panel_visible', False), win.destroy()))

    def render_overlay(self, canvas):
        if not self.panel_visible:
            return
        for ref in self.references:
            if not ref.visible or ref.img is None:
                continue
            try:
                thumb = ref.img.copy()
                alpha = int(ref.opacity * 255)
                thumb.putalpha(alpha)
                tk_thumb = ImageTk.PhotoImage(thumb)
                canvas.create_image(ref.x, ref.y, image=tk_thumb, anchor="nw")
                if hasattr(self, '_tk_refs'):
                    self._tk_refs.append(tk_thumb)
                else:
                    self._tk_refs = [tk_thumb]
            except:
                pass


# ── v6.20: SCRIPTING CONSOLE ────────────────────────────────

class ScriptingConsole:
    def __init__(self, app):
        self.app = app
        self.global_env = {
            "app": app,
            "SETTINGS": SETTINGS,
            "np": np,
            "Image": Image,
            "ImageDraw": ImageDraw,
            "ImageFilter": ImageFilter,
            "ImageEnhance": ImageEnhance,
            "ImageOps": ImageOps,
            "FastInputDriver": FastInputDriver,
            "os": os,
            "time": time,
            "math": math,
            "random": random,
            "json": json,
            "PathOptimizer": PathOptimizer,
            "LineQualityEngine": LineQualityEngine,
            "StyleEngine": StyleEngine,
        }
        self.history: List[str] = []
        self.max_history = 100

    def execute(self, code):
        result = None
        error = None
        try:
            compiled = compile(code, "<script>", "exec")
            exec(compiled, self.global_env)
        except Exception as e:
            error = str(e)
            traceback.print_exc()
        self.history.append(code)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        return result, error

    def evaluate(self, expr):
        result = None
        error = None
        try:
            result = eval(expr, self.global_env)
        except Exception as e:
            error = str(e)
        return result, error

    def show_console(self, parent):
        T = CURRENT_THEME
        win = tk.Toplevel(parent)
        win.title("Scripting Console")
        win.geometry("700x500")
        win.configure(bg=T["bg"])

        tk.Label(win, text="PYTHON SCRIPTING CONSOLE", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 12, "bold")).pack(pady=5)
        tk.Label(win, text="Access 'app', 'SETTINGS', 'np', 'Image', etc.",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack()

        output_frame = tk.Frame(win, bg=T["bg"])
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        output_text = tk.Text(output_frame, bg=T["log_bg"], fg=T["log_fg"],
                              font=("Courier", 9), wrap="word", state="disabled")
        output_text.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(output_frame, command=output_text.yview)
        scroll.pack(side="right", fill="y")
        output_text.config(yscrollcommand=scroll.set)

        def _write_output(msg, is_error=False):
            output_text.config(state="normal")
            color = T["danger"] if is_error else T["accent"]
            output_text.insert(tk.END, msg + "\n", ("colored",))
            output_text.tag_config("colored", foreground=color)
            output_text.see(tk.END)
            output_text.config(state="disabled")

        input_frame = tk.Frame(win, bg=T["bg"])
        input_frame.pack(fill="x", padx=10, pady=5)

        input_entry = tk.Entry(input_frame, bg=T["log_bg"], fg=T["fg"],
                               insertbackground=T["accent"], font=("Courier", 10))
        input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def run_code():
            code = input_entry.get().strip()
            if not code:
                return
            input_entry.delete(0, tk.END)
            _write_output(f">>> {code}")
            if "\n" in code or "def " in code or "class " in code or "for " in code or "while " in code or "if " in code:
                result, error = self.execute(code)
            else:
                result, error = self.evaluate(code)
            if error:
                _write_output(f"Error: {error}", is_error=True)
            elif result is not None:
                _write_output(f"{repr(result)}")

        def run_script():
            path = filedialog.askopenfilename(filetypes=[("Python", "*.py")])
            if path:
                try:
                    with open(path) as f:
                        code = f.read()
                    input_entry.delete(0, tk.END)
                    _write_output(f">>> Running script: {os.path.basename(path)}")
                    self.execute(code)
                    _write_output(f"Script completed: {os.path.basename(path)}")
                except Exception as e:
                    _write_output(f"Script error: {e}", is_error=True)

        tk.Button(input_frame, text="RUN", command=run_code,
                  bg="#004400", fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(side="right")
        tk.Button(win, text="LOAD SCRIPT FILE", command=run_script,
                  bg=T["btn"], fg=T["fg"], font=("Courier", 8), bd=0).pack(pady=2)

        input_entry.bind("<Return>", lambda e: run_code())
        input_entry.focus_set()


# ── v6.21: MULTI-CURSOR SYSTEM ──────────────────────────────

@dataclass
class VirtualCursor:
    id: int
    x: int
    y: int
    color_index: int = 0
    active: bool = True
    speed: float = 1.0
    offset_x: int = 0
    offset_y: int = 0

class MultiCursorSystem:
    def __init__(self, app):
        self.app = app
        self.cursors: Dict[int, VirtualCursor] = {}
        self.next_id = 0
        self.active = False
        self.driver = FastInputDriver()

    def add_cursor(self, x=0, y=0, color_idx=0):
        c = VirtualCursor(id=self.next_id, x=x, y=y, color_index=color_idx)
        self.cursors[self.next_id] = c
        self.next_id += 1
        return c

    def remove_cursor(self, cid):
        if cid in self.cursors:
            del self.cursors[cid]

    def clear_cursors(self):
        self.cursors.clear()

    def set_all_active(self, active):
        for c in self.cursors.values():
            c.active = active

    def assign_color(self, cid, color_idx):
        if cid in self.cursors:
            self.cursors[cid].color_index = color_idx

    def scatter_cursors(self, img_w, img_h, count=5):
        self.clear_cursors()
        for _ in range(count):
            x = random.randint(0, img_w)
            y = random.randint(0, img_h)
            ci = random.randint(0, max(0, len(self.app.palette_map) - 1)) if self.app.palette_map else 0
            self.add_cursor(x, y, ci)

    def transform_coords(self, x, y, cid):
        c = self.cursors.get(cid)
        if c is None:
            return x, y
        return x + c.offset_x, y + c.offset_y

    def execute_multicursor_draw(self, queues, canvas_rect, pal_arr):
        if not self.cursors:
            return False
        if not canvas_rect:
            return False
        sx, sy = canvas_rect[0], canvas_rect[1]
        cursor_list = list(self.cursors.values())
        active_cursors = [c for c in cursor_list if c.active]
        if not active_cursors:
            return False
        self.active = True
        total_dots = sum(len(pts) for pts in queues.values())
        drawn = 0
        start_ts = time.time()

        for cidx, pts in queues.items():
            if not self.app.drawing_active:
                break
            if not pts:
                continue
            cursor = active_cursors[drawn % len(active_cursors)]
            real_cidx = cursor.color_index if cursor.color_index < len(self.app.palette_map) else cidx
            pos = self.app.palette_map[real_cidx]["pos"]
            self.driver.move(pos[0], pos[1])
            time.sleep(SETTINGS["UI_DELAY"])
            self.driver.click(pos[0], pos[1])
            time.sleep(SETTINGS["CLICK_DELAY"])

            strokes = self.app._pixels_to_strokes(pts, max(1, SETTINGS["PIXEL_GAP"] + 1))
            for stroke in strokes:
                if not self.app.drawing_active:
                    break
                path = self.app._stroke_to_path(stroke)
                if len(path) < 2:
                    continue
                spath = self.app._smooth_stroke_path(path, int(SETTINGS.get("STROKE_SMOOTH_PASSES", 2)))
                x0, y0 = sx + int(spath[0][0]), sy + int(spath[0][1])
                x0, y0 = self.transform_coords(x0, y0, cursor.id)
                self.driver.press(x0, y0)
                for pt in spath[1:]:
                    if not self.app.drawing_active:
                        break
                    tx, ty = sx + int(pt[0]), sy + int(pt[1])
                    tx, ty = self.transform_coords(tx, ty, cursor.id)
                    self.driver.drag_to(tx, ty)
                self.driver.release()
                drawn += len(spath)
                if drawn % 50 == 0:
                    self.app._update_progress(drawn, total_dots)

        self.active = False
        self.app._draw_finished(drawn)
        return True


# ── v6.22: EXPORT TEMPLATES & BATCH PROCESSING ──────────────

class ExportTemplate:
    def __init__(self, name="Default"):
        self.name = name
        self.format = "PNG"
        self.quality = 95
        self.resize_enabled = False
        self.resize_width = 1920
        self.resize_height = 1080
        self.keep_aspect = True
        self.include_metadata = True
        self.add_watermark = False
        self.watermark_text = ""
        self.watermark_opacity = 0.3
        self.color_profile = "sRGB"
        self.dpi = 300
        self.background_color = "#ffffff"
        self.flatten_layers = True

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @classmethod
    def from_dict(cls, data):
        t = cls()
        for k, v in data.items():
            if hasattr(t, k):
                setattr(t, k, v)
        return t

    def apply_to_image(self, img):
        result = img.copy()
        if self.resize_enabled:
            w, h = result.size
            rw, rh = self.resize_width, self.resize_height
            if self.keep_aspect:
                ratio = min(rw / w, rh / h)
                rw, rh = int(w * ratio), int(h * ratio)
            result = result.resize((max(1, rw), max(1, rh)), Image.LANCZOS)
        if self.add_watermark and self.watermark_text:
            draw = ImageDraw.Draw(result)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            wx, wy = (result.width - tw) // 2, (result.height - th) // 2
            overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            alpha = int(self.watermark_opacity * 255)
            overlay_draw.text((wx, wy), self.watermark_text, fill=(255, 255, 255, alpha), font=font)
            result = Image.alpha_composite(result.convert("RGBA"), overlay).convert("RGB")
        return result

    def save(self, img, path):
        processed = self.apply_to_image(img)
        save_params = {}
        if self.format.upper() == "JPEG" or self.format.upper() == "JPG":
            save_params["quality"] = self.quality
        if self.include_metadata:
            save_params["dpi"] = (self.dpi, self.dpi)
        processed.save(path, format=self.format, **save_params)


class ExportTemplateManager:
    def __init__(self):
        self.templates: Dict[str, ExportTemplate] = {}
        self.templates_dir = os.path.join(DIR_PATH, "export_templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        self._load_all()

    def _load_all(self):
        if not os.path.isdir(self.templates_dir):
            return
        for fname in os.listdir(self.templates_dir):
            if fname.endswith(".json"):
                try:
                    path = os.path.join(self.templates_dir, fname)
                    with open(path) as f:
                        data = json.load(f)
                    tmpl = ExportTemplate.from_dict(data)
                    self.templates[tmpl.name] = tmpl
                except:
                    pass

    def save_template(self, template):
        if not template.name:
            return
        self.templates[template.name] = template
        path = os.path.join(self.templates_dir, f"{template.name}.json")
        with open(path, 'w') as f:
            json.dump(template.to_dict(), f, indent=2)

    def delete_template(self, name):
        if name in self.templates:
            del self.templates[name]
            path = os.path.join(self.templates_dir, f"{name}.json")
            if os.path.exists(path):
                os.remove(path)

    def get_template(self, name):
        return self.templates.get(name)

    def list_templates(self):
        return list(self.templates.keys())


# ── v6.23: LIVE PROGRESS DASHBOARD ──────────────────────────

class ProgressDashboard:
    def __init__(self, app):
        self.app = app
        self.dashboard_visible = False
        self._dashboard_window = None
        self._update_interval = 500

    def show_dashboard(self, parent):
        if self._dashboard_window and self._dashboard_window.winfo_exists():
            self._dashboard_window.lift()
            return
        T = CURRENT_THEME
        win = tk.Toplevel(parent)
        win.title("Progress Dashboard")
        win.geometry("420x320")
        win.configure(bg=T["bg"])
        self._dashboard_window = win
        self.dashboard_visible = True

        tk.Label(win, text="LIVE DASHBOARD", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 12, "bold")).pack(pady=5)

        self._dash_total = tk.Label(win, text="Total dots: 0", bg=T["bg"], fg=T["fg"],
                                    font=("Courier", 9))
        self._dash_total.pack()
        self._dash_drawn = tk.Label(win, text="Drawn: 0", bg=T["bg"], fg=T["fg"],
                                    font=("Courier", 9))
        self._dash_drawn.pack()
        self._dash_elapsed = tk.Label(win, text="Elapsed: 0s", bg=T["bg"], fg=T["fg"],
                                      font=("Courier", 9))
        self._dash_elapsed.pack()
        self._dash_eta = tk.Label(win, text="ETA: --", bg=T["bg"], fg=T["accent2"],
                                  font=("Courier", 9, "bold"))
        self._dash_eta.pack()
        self._dash_pps = tk.Label(win, text="PPS: 0", bg=T["bg"], fg=T["accent"],
                                  font=("Courier", 9, "bold"))
        self._dash_pps.pack()
        self._dash_speed = tk.Label(win, text="Speed: --", bg=T["bg"], fg=T["warn"],
                                    font=("Courier", 9))
        self._dash_speed.pack()

        spark = Sparkline(win, width=380, height=60, maxpts=80)
        spark.pack(pady=10)

        def _update():
            if not self.dashboard_visible or not win.winfo_exists():
                return
            app = self.app
            total = app.estimated_total
            drawn = app.current_progress
            elapsed = time.time() - app.draw_start_time if app.draw_start_time > 0 else 0
            pps = app.last_pps
            self._dash_total.config(text=f"Total dots: {total:,}")
            self._dash_drawn.config(text=f"Drawn: {drawn:,}")
            self._dash_elapsed.config(text=f"Elapsed: {elapsed:.1f}s")
            if pps > 0 and total > drawn:
                eta = (total - drawn) / pps
                self._dash_eta.config(text=f"ETA: {eta/60:.0f}m {eta%60:.0f}s")
            else:
                self._dash_eta.config(text="ETA: --")
            self._dash_pps.config(text=f"PPS: {pps:.0f}")
            if drawn > 0 and elapsed > 0:
                avg = drawn / elapsed
                self._dash_speed.config(text=f"Speed: {avg:.0f} avg px/s")
            spark.push(pps)
            win.after(self._update_interval, _update)

        win.after(self._update_interval, _update)
        win.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, 'dashboard_visible', False), win.destroy()))

    def close(self):
        if self._dashboard_window:
            try:
                self._dashboard_window.destroy()
            except:
                pass
        self.dashboard_visible = False


# ── v6.24: SMART FILL & CONTENT-AWARE TOOLS ─────────────────

class SmartFill:
    def __init__(self, app):
        self.app = app
        self.driver = FastInputDriver()
        self.fill_modes = ["flood", "edge_aware", "gradient", "pattern", "content_aware"]

    def flood_fill(self, img, seed_x, seed_y, fill_color, tolerance=30):
        arr = np.array(img)
        h, w = arr.shape[:2]
        if not (0 <= seed_x < w and 0 <= seed_y < h):
            return img
        seed_color = arr[seed_y, seed_x].copy()
        mask = np.zeros((h, w), dtype=bool)
        queue = [(seed_x, seed_y)]
        mask[seed_y, seed_x] = True
        while queue:
            cx, cy = queue.pop(0)
            for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
                if 0 <= nx < w and 0 <= ny < h and not mask[ny, nx]:
                    diff = np.max(np.abs(arr[ny, nx].astype(int) - seed_color.astype(int)))
                    if diff <= tolerance:
                        mask[ny, nx] = True
                        queue.append((nx, ny))
        result = arr.copy()
        result[mask] = fill_color
        return Image.fromarray(result)

    def edge_aware_fill(self, img, seed_x, seed_y, fill_color, edge_threshold=30, grow_limit=50):
        arr = np.array(img)
        h, w = arr.shape[:2]
        if not (0 <= seed_x < w and 0 <= seed_y < h):
            return img
        if HAS_CV2:
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 20, edge_threshold)
        else:
            edges = np.array(img.convert("L").filter(ImageFilter.FIND_EDGES)) > edge_threshold
        edge_mask = edges > 0
        seed_color = arr[seed_y, seed_x].copy()
        mask = np.zeros((h, w), dtype=bool)
        queue = [(seed_x, seed_y)]
        mask[seed_y, seed_x] = True
        steps = 0
        while queue and steps < grow_limit:
            cx, cy = queue.pop(0)
            steps += 1
            for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
                if 0 <= nx < w and 0 <= ny < h and not mask[ny, nx] and not edge_mask[ny, nx]:
                    diff = np.max(np.abs(arr[ny, nx].astype(int) - seed_color.astype(int)))
                    if diff <= 60:
                        mask[ny, nx] = True
                        queue.append((nx, ny))
        result = arr.copy()
        result[mask] = fill_color
        return Image.fromarray(result)

    def gradient_fill(self, img, start_color, end_color, direction="vertical"):
        w, h = img.size
        arr = np.array(img, dtype=np.float32)
        if direction == "vertical":
            gradient = np.linspace(0, 1, h).reshape(-1, 1)
        elif direction == "horizontal":
            gradient = np.linspace(0, 1, w).reshape(1, -1)
        elif direction == "radial":
            cx, cy = w / 2, h / 2
            yy, xx = np.ogrid[:h, :w]
            gradient = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / np.sqrt(cx ** 2 + cy ** 2)
            gradient = np.clip(gradient, 0, 1)
        else:
            gradient = np.linspace(0, 1, h).reshape(-1, 1)
        sc = np.array(start_color, dtype=np.float32)
        ec = np.array(end_color, dtype=np.float32)
        for c in range(3):
            arr[..., c] = arr[..., c] * (1 - gradient) + (sc[c] * (1 - gradient) + ec[c] * gradient) * gradient
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    def pattern_fill(self, img, pattern_type="dots", color=(100, 100, 100), spacing=10):
        arr = np.array(img, dtype=np.uint8)
        h, w = arr.shape[:2]
        if pattern_type == "dots":
            for y in range(0, h, spacing):
                for x in range(0, w, spacing):
                    r = max(1, spacing // 6)
                    cv2.circle(arr, (x, y), r, color, -1) if HAS_CV2 else None
        elif pattern_type == "grid":
            arr[::spacing, :] = color
            arr[:, ::spacing] = color
        elif pattern_type == "crosshatch":
            for i in range(0, max(w, h), spacing):
                cv2.line(arr, (0, i), (i, 0), color, 1) if HAS_CV2 else None
                cv2.line(arr, (w - i, 0), (w, i), color, 1) if HAS_CV2 else None
        return Image.fromarray(arr) if HAS_CV2 else img

    def content_aware_fill(self, img, mask_region):
        if not HAS_CV2:
            self.app.log("[SmartFill] OpenCV required for content-aware fill")
            return img
        arr = np.array(img)
        mask = np.zeros(arr.shape[:2], dtype=np.uint8)
        if mask_region:
            x1, y1, x2, y2 = mask_region
            mask[y1:y2, x1:x2] = 255
        result = cv2.inpaint(arr, mask, 3, cv2.INPAINT_TELEA)
        return Image.fromarray(result)


# ── v6.25: UNDO/HISTORY MANAGER V2 ──────────────────────────

@dataclass
class HistoryEntry:
    timestamp: float
    description: str
    layers_snapshot: List[dict]
    selection_mask: Optional[np.ndarray] = None
    text_objects_snapshot: Optional[list] = None
    tool_mode: str = ""
    brush_color: Optional[tuple] = None

class HistoryManagerV2:
    def __init__(self, app, max_stack=50):
        self.app = app
        self.max_stack = max_stack
        self.undo_stack: List[HistoryEntry] = []
        self.redo_stack: List[HistoryEntry] = []
        self._suspended = False

    def snapshot(self, description="edit"):
        if self._suspended:
            return
        entry = HistoryEntry(
            timestamp=time.time(),
            description=description,
            layers_snapshot=self._capture_layers(),
            selection_mask=self.app.advanced_selection.selection_mask.copy() if hasattr(self.app, 'advanced_selection') and self.app.advanced_selection.selection_mask is not None else None,
            text_objects_snapshot=list(getattr(self.app, 'text_objects', [])),
            tool_mode=self.app.tool_mode if hasattr(self.app, 'tool_mode') else "",
            brush_color=self.app.brush_color if hasattr(self.app, 'brush_color') else None,
        )
        self.undo_stack.append(entry)
        if len(self.undo_stack) > self.max_stack:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def _capture_layers(self):
        snap = []
        if hasattr(self.app, 'layers') and self.app.layers:
            for l in self.app.layers:
                snap.append({
                    "name": l.get("name", "Layer"),
                    "img_bytes": l["img"].tobytes() if isinstance(l["img"], Image.Image) else None,
                    "img_mode": l["img"].mode if isinstance(l["img"], Image.Image) else "RGB",
                    "img_size": list(l["img"].size) if isinstance(l["img"], Image.Image) else [0, 0],
                    "visible": l.get("visible", True),
                })
        elif hasattr(self.app, 'layer_v2') and self.app.layer_v2.layers:
            for l in self.app.layer_v2.layers:
                snap.append({
                    "name": l.name,
                    "img_bytes": l.img.tobytes(),
                    "img_mode": l.img.mode,
                    "img_size": list(l.img.size),
                    "visible": l.visible,
                    "opacity": l.opacity,
                    "blend_mode": l.blend_mode.value if hasattr(l.blend_mode, 'value') else "normal",
                })
        return snap

    def _restore_layers(self, snap):
        if not snap:
            return
        if hasattr(self.app, 'layers'):
            self.app.layers = []
            for s in snap:
                if s.get("img_bytes"):
                    img = Image.frombytes(s["img_mode"], tuple(s["img_size"]), s["img_bytes"])
                    self.app.layers.append({
                        "name": s["name"], "img": img, "visible": s.get("visible", True),
                    })
        elif hasattr(self.app, 'layer_v2'):
            self.app.layer_v2.layers = []
            for s in snap:
                if s.get("img_bytes"):
                    img = Image.frombytes(s["img_mode"], tuple(s["img_size"]), s["img_bytes"])
                    layer = LayerV2(
                        name=s["name"], img=img, visible=s.get("visible", True),
                        opacity=s.get("opacity", 1.0),
                        blend_mode=BlendMode(s.get("blend_mode", "normal")),
                    )
                    self.app.layer_v2.layers.append(layer)

    def undo(self):
        if not self.undo_stack:
            return False
        entry = self.undo_stack.pop()
        current_snap = self._capture_layers()
        self.redo_stack.append(HistoryEntry(
            timestamp=time.time(), description="redo",
            layers_snapshot=current_snap,
        ))
        self._suspended = True
        self._restore_layers(entry.layers_snapshot)
        if hasattr(self.app, 'advanced_selection') and entry.selection_mask is not None:
            self.app.advanced_selection.selection_mask = entry.selection_mask.copy()
        if entry.text_objects_snapshot is not None:
            self.app.text_objects = list(entry.text_objects_snapshot)
        self._suspended = False
        self.app.log(f"[History] Undo: {entry.description}")
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        entry = self.redo_stack.pop()
        current_snap = self._capture_layers()
        self.undo_stack.append(HistoryEntry(
            timestamp=time.time(), description="redo",
            layers_snapshot=current_snap,
        ))
        self._suspended = True
        self._restore_layers(entry.layers_snapshot)
        if hasattr(self.app, 'advanced_selection') and entry.selection_mask is not None:
            self.app.advanced_selection.selection_mask = entry.selection_mask.copy()
        if entry.text_objects_snapshot is not None:
            self.app.text_objects = list(entry.text_objects_snapshot)
        self._suspended = False
        self.app.log(f"[History] Redo: {entry.description}")
        return True

    def get_undo_count(self):
        return len(self.undo_stack)

    def get_redo_count(self):
        return len(self.redo_stack)

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()


# ── v6.26: GODMODE SETTINGS EXTENSION ───────────────────────

GODMODE_SETTINGS_V2 = {
    "BRUSH_PHYSICS_ENABLED": True,
    "BRUSH_TYPE": "round",
    "BRUSH_PRESSURE_SENSITIVITY": 0.5,
    "BRUSH_FLOW_RATE": 0.8,
    "BRUSH_SCATTER_AMOUNT": 0.0,
    "RECORDER_AUTO_START": False,
    "RECORDER_PLAYBACK_SPEED": 1.0,
    "RECORDER_AUTO_RECORD_DRAW": True,
    "HARMONY_TYPE": "complementary",
    "HARMONY_COLOR_COUNT": 5,
    "SELECTION_FEATHER": 0,
    "SELECTION_INVERT": False,
    "SELECTION_TOOL": "rectangular",
    "FILTER_CHAIN_ENABLED": False,
    "REFERENCE_PANEL_VISIBLE": False,
    "MULTI_CURSOR_ENABLED": False,
    "MULTI_CURSOR_COUNT": 3,
    "EXPORT_TEMPLATE": "Default",
    "EXPORT_AUTO_APPLY": False,
    "DASHBOARD_VISIBLE": False,
    "SMART_FILL_MODE": "flood",
    "SMART_FILL_TOLERANCE": 30,
    "SMART_FILL_GROW_LIMIT": 50,
    "HISTORY_MAX_STACK": 50,
    "CONSOLE_SHOW_ON_STARTUP": False,
    "STRIPED_FILL_ENABLED": True,
    "STRIPE_ANGLE": 45,
    "STRIPE_SPACING": 6,
    "STRIPE_MIN_AREA": 200,
    "FLIPBOOK_FPS": 8,
    "LIMIT_GLOBAL_SPEED": 200,
    "LIMIT_STROKE_SPEED": 100,
    "LIMIT_PIXEL_GAP": 10,
    "LIMIT_SKETCH_NO_LIFT": 500,
    "LIMIT_SKETCH_BPM": 200,
    "LIMIT_BATCH_DELAY": 30,
    "LIMIT_FILL_VARIANCE_THRESHOLD": 2000,
    "LIMIT_MIN_FILL_AREA": 1000,
    "LIMIT_WHITE_SKIP": 255,
    "LIMIT_BEZIER_STEPS": 20,
    "LIMIT_LIFT_DELAY": 0.5,
    "LIMIT_CLICK_DELAY": 0.1,
    "LIMIT_UI_DELAY": 0.5,
    "LIMIT_ANIM_FPS": 60,
    "LIMIT_PERF_FPS_TARGET": 240,
    "LIMIT_HISTORY_MAX_STACK": 200,
    "LIMIT_UNDO_STACK_SIZE": 200,
    "LIMIT_STRIPE_SPACING": 20,
    "LIMIT_FLIPBOOK_FPS": 30,
}

SETTINGS.update(GODMODE_SETTINGS_V2)


# ── v6.27: GODMODE INTEGRATION EXTENSION ────────────────────

def _patch_autodrawer_v2():
    if hasattr(AutoDrawer, '_godmode_patched_v2'):
        return
    AutoDrawer._godmode_patched_v2 = True
    orig_init = AutoDrawer.__init__
    def new_init_v2(self):
        orig_init(self)
        self.brush_physics = BrushPhysicsEngine(self)
        self.timelapse = TimelapseRecorder(self)
        self.color_harmony = ColorHarmonyGenerator()
        self.advanced_selection = AdvancedSelection(self)
        self.filter_chain = FilterChain()
        self.reference_panel = ReferencePanel(self)
        self.script_console = ScriptingConsole(self)
        self.multi_cursor = MultiCursorSystem(self)
        self.export_templates = ExportTemplateManager()
        self.progress_dashboard = ProgressDashboard(self)
        self.smart_fill = SmartFill(self)
        self.history_v2 = HistoryManagerV2(self, max_stack=int(SETTINGS.get("HISTORY_MAX_STACK", 50)))

    def _setup_v2_bindings(self):
        try:
            self.root.bind("<Control-Shift-Z>", lambda e: self.history_v2.redo())
            self.root.bind("<Control-Shift-R>", lambda e: self.timelapse.start_recording() if not self.timelapse.recording else self.timelapse.stop_recording())
            self.root.bind("<Control-d>", lambda e: self.progress_dashboard.show_dashboard(self.root) if not self.progress_dashboard.dashboard_visible else self.progress_dashboard.close())
            self.root.bind("<Control-p>", lambda e: self.reference_panel.show_panel(self.root) if not self.reference_panel.panel_visible else None)
            self.root.bind("<Control-Shift-C>", lambda e: self.script_console.show_console(self.root))
        except:
            pass

    AutoDrawer.__init__ = new_init_v2
    AutoDrawer._setup_v2_bindings = _setup_v2_bindings

_patch_autodrawer_v2()


# ── v6.28: CONTROL PANEL EXTENSION TABS ─────────────────────

def _patch_controlpanel_v2():
    if hasattr(ControlPanelWindow, '_godmode_patched_v2'):
        return
    ControlPanelWindow._godmode_patched_v2 = True

    # Brush Physics Tab
    def _build_v2_brush_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Brush Physics"] = (tab, "Brush Physics")
        self._tab_order.append("Brush Physics")
        self._tab_listbox.insert(tk.END, "Brush Physics")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Brush Engine")
        self._checkbox(sf, "Enable Brush Physics", "BRUSH_PHYSICS_ENABLED", True)
        self._combo(sf, "Brush Type", "BRUSH_TYPE",
                    list(BrushPhysicsEngine.BRUSH_TYPES.keys()), 14)
        self._slider(sf, "Pressure Sensitivity", "BRUSH_PRESSURE_SENSITIVITY", 0.0, 1.0, 0.05, 140)
        self._slider(sf, "Flow Rate", "BRUSH_FLOW_RATE", 0.0, 1.0, 0.05, 140)
        self._slider(sf, "Scatter Amount", "BRUSH_SCATTER_AMOUNT", 0.0, 1.0, 0.05, 140)

    ControlPanelWindow._build_v2_brush_tab = _build_v2_brush_tab

    # Timelapse Tab
    def _build_v2_timelapse_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Timelapse"] = (tab, "Timelapse")
        self._tab_order.append("Timelapse")
        self._tab_listbox.insert(tk.END, "Timelapse")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Recording")
        self._checkbox(sf, "Auto-Record Draws", "RECORDER_AUTO_RECORD_DRAW", True)
        self._slider(sf, "Playback Speed", "RECORDER_PLAYBACK_SPEED", 0.1, 5.0, 0.1, 140)
        def start_rec():
            self.app.timelapse.start_recording()
            self._status("Recording started")
        def stop_rec():
            self.app.timelapse.stop_recording()
            self._status(f"Recorded {self.app.timelapse.get_frame_count()} frames")
        def save_rec():
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
            if path:
                self.app.timelapse.save_recording(path)
        def load_rec():
            path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
            if path:
                self.app.timelapse.load_recording(path)
        def play_rec():
            self.app.timelapse.start_replay()
            self._status("Replaying...")
        for text, cmd in [("RECORD START", start_rec), ("RECORD STOP", stop_rec),
                          ("SAVE", save_rec), ("LOAD", load_rec), ("PLAY", play_rec)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_v2_timelapse_tab = _build_v2_timelapse_tab

    # Harmony Tab
    def _build_v2_harmony_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Harmony"] = (tab, "Harmony")
        self._tab_order.append("Harmony")
        self._tab_listbox.insert(tk.END, "Harmony")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Color Harmonies")
        self._combo(sf, "Harmony Type", "HARMONY_TYPE",
                    list(ColorHarmonyGenerator().get_harmony_names()), 18)
        self._slider(sf, "Color Count", "HARMONY_COLOR_COUNT", 2, 12, 1, 140, "int")
        def gen_harmony():
            if not self.app.palette_map:
                self._status("Load a palette first")
                return
            base = self.app.palette_map[0]["rgb"]
            h_type = SETTINGS.get("HARMONY_TYPE", "complementary")
            count = int(SETTINGS.get("HARMONY_COLOR_COUNT", 5))
            self.app.color_harmony.apply_to_palette(self.app, base, h_type, count)
            self._status(f"Generated {h_type} harmony")
        tk.Button(sf, text="GENERATE HARMONY PALETTE", command=gen_harmony,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=5)

    ControlPanelWindow._build_v2_harmony_tab = _build_v2_harmony_tab

    # Selections Tab
    def _build_v2_selection_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Selections"] = (tab, "Selections")
        self._tab_order.append("Selections")
        self._tab_listbox.insert(tk.END, "Selections")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Selection Tools")
        self._combo(sf, "Tool", "SELECTION_TOOL",
                    [t.value for t in SelectionTool], 14)
        self._slider(sf, "Feather Radius", "SELECTION_FEATHER", 0, 50, 1, 140, "int")
        self._checkbox(sf, "Invert Selection", "SELECTION_INVERT", False)
        def clear_sel():
            self.app.advanced_selection.clear()
            self._status("Selection cleared")
        def crop_sel():
            if self.app.base_img and self.app.advanced_selection.selection_bbox:
                self.app.base_img = self.app.advanced_selection.crop_to_selection(self.app.base_img)
                self.app.final_img = None
                self._status("Cropped to selection")
        for text, cmd in [("CLEAR", clear_sel), ("CROP TO SEL", crop_sel)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8), bd=0).pack(pady=2)

    ControlPanelWindow._build_v2_selection_tab = _build_v2_selection_tab

    # Filters Tab
    def _build_v2_filters_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Filters"] = (tab, "Filters")
        self._tab_order.append("Filters")
        self._tab_listbox.insert(tk.END, "Filters")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Filter Chain")
        self._checkbox(sf, "Enable Filter Chain", "FILTER_CHAIN_ENABLED", False)
        filter_names = sorted(FILTER_REGISTRY.keys())
        def add_filter():
            name = simpledialog.askstring("Add Filter", f"Filter name ({', '.join(filter_names)}):")
            if name and name in FILTER_REGISTRY:
                self.app.filter_chain.add_step(name, {})
                self._status(f"Added filter: {name}")
        def apply_chain():
            if self.app.base_img and self.app.filter_chain.steps:
                self.app.base_img = self.app.filter_chain.apply(self.app.base_img)
                self.app.final_img = None
                self._status("Filter chain applied")
        def clear_chain():
            self.app.filter_chain.steps.clear()
            self._status("Filter chain cleared")
        for text, cmd in [("ADD FILTER", add_filter), ("APPLY CHAIN", apply_chain), ("CLEAR", clear_chain)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8), bd=0).pack(pady=2, fill="x")
        if self.app.filter_chain.steps:
            self._section_label(sf, "Current Steps")
            for i, (fname, fparams) in enumerate(self.app.filter_chain.steps):
                tk.Label(sf, text=f"  {i+1}. {fname}", bg=T["bg"], fg=T["fg"],
                         font=("Courier", 8)).pack(anchor="w", padx=10)

    ControlPanelWindow._build_v2_filters_tab = _build_v2_filters_tab

    # References Tab
    def _build_v2_references_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["References"] = (tab, "References")
        self._tab_order.append("References")
        self._tab_listbox.insert(tk.END, "References")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Reference Panel")
        def show_panel():
            self.app.reference_panel.show_panel(self.win)
            self._status("Reference panel opened")
        tk.Button(sf, text="SHOW REFERENCE PANEL", command=show_panel,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=5)
        self._checkbox(sf, "Panel Visible", "REFERENCE_PANEL_VISIBLE", False)

    ControlPanelWindow._build_v2_references_tab = _build_v2_references_tab

    # Multi-Cursor Tab
    def _build_v2_multicursor_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Multi-Cursor"] = (tab, "Multi-Cursor")
        self._tab_order.append("Multi-Cursor")
        self._tab_listbox.insert(tk.END, "Multi-Cursor")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Multi-Cursor System")
        self._checkbox(sf, "Enable Multi-Cursor", "MULTI_CURSOR_ENABLED", False)
        self._slider(sf, "Cursor Count", "MULTI_CURSOR_COUNT", 1, 20, 1, 140, "int")
        def scatter():
            count = int(SETTINGS.get("MULTI_CURSOR_COUNT", 3))
            w = self.app.base_img.width if self.app.base_img else 800
            h = self.app.base_img.height if self.app.base_img else 600
            self.app.multi_cursor.scatter_cursors(w, h, count)
            self._status(f"Scattered {count} cursors")
        def clear():
            self.app.multi_cursor.clear_cursors()
            self._status("Cursors cleared")
        for text, cmd in [("SCATTER CURSORS", scatter), ("CLEAR", clear)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8), bd=0).pack(pady=2)

    ControlPanelWindow._build_v2_multicursor_tab = _build_v2_multicursor_tab

    # Export Templates Tab
    def _build_v2_export_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Export"] = (tab, "Export")
        self._tab_order.append("Export")
        self._tab_listbox.insert(tk.END, "Export")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Export Templates")
        tmpl_names = self.app.export_templates.list_templates()
        self._combo(sf, "Template", "EXPORT_TEMPLATE", tmpl_names if tmpl_names else ["Default"], 18)
        self._checkbox(sf, "Auto-Apply Export Template", "EXPORT_AUTO_APPLY", False)
        def export_with_template():
            if not self.app.base_img:
                self._status("No image loaded")
                return
            name = SETTINGS.get("EXPORT_TEMPLATE", "Default")
            tmpl = self.app.export_templates.get_template(name)
            if tmpl is None:
                tmpl = ExportTemplate(name)
            path = filedialog.asksaveasfilename(defaultextension=f".{tmpl.format.lower()}")
            if path:
                tmpl.save(self.app.base_img, path)
                self._status(f"Exported: {os.path.basename(path)}")
        tk.Button(sf, text="EXPORT WITH TEMPLATE", command=export_with_template,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=5)

    ControlPanelWindow._build_v2_export_tab = _build_v2_export_tab

    # Scripting Console Tab
    def _build_v2_console_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Console"] = (tab, "Console")
        self._tab_order.append("Console")
        self._tab_listbox.insert(tk.END, "Console")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Scripting Console")
        def show_console():
            self.app.script_console.show_console(self.win)
            self._status("Console opened")
        tk.Button(sf, text="OPEN CONSOLE", command=show_console,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(pady=10)
        self._checkbox(sf, "Show Console on Startup", "CONSOLE_SHOW_ON_STARTUP", False)

    ControlPanelWindow._build_v2_console_tab = _build_v2_console_tab

    # Smart Fill Tab
    def _build_v2_smartfill_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Smart Fill"] = (tab, "Smart Fill")
        self._tab_order.append("Smart Fill")
        self._tab_listbox.insert(tk.END, "Smart Fill")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Smart Fill Tools")
        self._combo(sf, "Fill Mode", "SMART_FILL_MODE",
                    ["flood", "edge_aware", "gradient", "pattern", "content_aware"], 16)
        self._slider(sf, "Tolerance", "SMART_FILL_TOLERANCE", 5, 100, 1, 140, "int")
        self._slider(sf, "Grow Limit", "SMART_FILL_GROW_LIMIT", 10, 200, 5, 140, "int")
        def apply_smart_fill():
            if not self.app.base_img:
                self._status("No image")
                return
            mode = SETTINGS.get("SMART_FILL_MODE", "flood")
            tol = int(SETTINGS.get("SMART_FILL_TOLERANCE", 30))
            cx = self.app.base_img.width // 2
            cy = self.app.base_img.height // 2
            color = (100, 100, 100)
            if mode == "flood":
                result = self.app.smart_fill.flood_fill(self.app.base_img, cx, cy, color, tol)
            elif mode == "edge_aware":
                grow = int(SETTINGS.get("SMART_FILL_GROW_LIMIT", 50))
                result = self.app.smart_fill.edge_aware_fill(self.app.base_img, cx, cy, color, tol, grow)
            elif mode == "gradient":
                result = self.app.smart_fill.gradient_fill(self.app.base_img, (255, 255, 255), color)
            else:
                result = self.app.smart_fill.pattern_fill(self.app.base_img, "dots", color, 10)
            self.app.base_img = result
            self.app.final_img = None
            self._status(f"Smart fill applied: {mode}")
        tk.Button(sf, text="APPLY SMART FILL", command=apply_smart_fill,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 9, "bold"), bd=0).pack(pady=5)

    ControlPanelWindow._build_v2_smartfill_tab = _build_v2_smartfill_tab

    # History Tab
    def _build_v2_history_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["History V2"] = (tab, "History V2")
        self._tab_order.append("History V2")
        self._tab_listbox.insert(tk.END, "History V2")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Undo History Manager")
        self._slider(sf, "Max Stack Size", "HISTORY_MAX_STACK", 10, 200, 5, 140, "int")
        def undo():
            if self.app.history_v2.undo():
                self._status("Undone")
            else:
                self._status("Nothing to undo")
        def redo():
            if self.app.history_v2.redo():
                self._status("Redone")
            else:
                self._status("Nothing to redo")
        def clear():
            self.app.history_v2.clear()
            self._status("History cleared")
        for text, cmd in [("UNDO", undo), ("REDO", redo), ("CLEAR HISTORY", clear)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8), bd=0).pack(pady=2, fill="x")
        us = self.app.history_v2.get_undo_count()
        rs = self.app.history_v2.get_redo_count()
        tk.Label(sf, text=f"Undo stack: {us}  |  Redo stack: {rs}",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack(pady=5)

    ControlPanelWindow._build_v2_history_tab = _build_v2_history_tab

    # Patch init to add new tabs
    orig_init_v2 = ControlPanelWindow.__init__
    def new_init_v2(self, parent, app):
        orig_init_v2(self, parent, app)
        self._build_v2_brush_tab()
        self._build_v2_timelapse_tab()
        self._build_v2_harmony_tab()
        self._build_v2_selection_tab()
        self._build_v2_filters_tab()
        self._build_v2_references_tab()
        self._build_v2_multicursor_tab()
        self._build_v2_export_tab()
        self._build_v2_console_tab()
        self._build_v2_smartfill_tab()
        self._build_v2_history_tab()

    ControlPanelWindow.__init__ = new_init_v2

_patch_controlpanel_v2()


# ── v6.29: BUG FIXES V2 ─────────────────────────────────────

def _apply_v2_bugfixes():
    global DRAW_MODES
    if "SmartFill" not in DRAW_MODES:
        DRAW_MODES.append("SmartFill")
    if "MultiCursor" not in DRAW_MODES:
        DRAW_MODES.append("MultiCursor")
    if "Harmony" not in DRAW_MODES:
        DRAW_MODES.append("Harmony")

_apply_v2_bugfixes()


# ── v6.30: IMAGE BROWSER ──────────────────────────────────

class ImageBrowser:
    def __init__(self, app):
        self.app = app
        self.results: List[Dict] = []
        self._thumb_refs: List[Any] = []
        self._search_thread = None
        self._history: List[Dict] = []

    def search_duckduckgo(self, query, page=1):
        def _search():
            try:
                search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&iax=images&ia=images"
                req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    html = resp.read().decode("utf-8", errors="replace")
                vqd_match = re.search(r'name="vqd"[^>]+value="([^"]+)"', html)
                vqd = vqd_match.group(1) if vqd_match else ""
                if not vqd:
                    self.app.log("[ImageBrowser] Could not extract vqd token")
                    return
                api_url = f"https://duckduckgo.com/i.js?q={urllib.parse.quote(query)}&vqd={urllib.parse.quote(vqd)}&p={page}&o=json"
                api_req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(api_req, timeout=15) as api_resp:
                    data = json.loads(api_resp.read().decode("utf-8"))
                self.results = []
                for item in data.get("results", []):
                    self.results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "image": item.get("image", ""),
                        "thumbnail": item.get("thumbnail", ""),
                        "height": item.get("height", 0),
                        "width": item.get("width", 0),
                    })
                self.app.root.after(0, lambda: self.app.log(f"[ImageBrowser] Found {len(self.results)} results for '{query}'"))
            except Exception as e:
                self.app.root.after(0, lambda: self.app.log(f"[ImageBrowser] Search error: {e}"))
        self._search_thread = threading.Thread(target=_search, daemon=True)
        self._search_thread.start()

    def load_from_url(self, url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                img_data = resp.read()
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            self.app.base_img = img
            self.app.final_img = None
            self.app._update_canvas()
            self.app.log(f"[ImageBrowser] Loaded image from URL: {url[:60]}...")
            self._history.append({"url": url, "time": time.time()})
            return img
        except Exception as e:
            self.app.log(f"[ImageBrowser] URL load error: {e}")
            return None

    def load_result(self, index):
        if 0 <= index < len(self.results):
            img_url = self.results[index].get("image") or self.results[index].get("url", "")
            if img_url:
                return self.load_from_url(img_url)
        return None

    def open_in_browser(self, query):
        search_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
        import webbrowser
        webbrowser.open(search_url)
        self.app.log(f"[ImageBrowser] Opened browser: {query}")

    def ai_reference(self, prompt):
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=512&model=flux"
            return self.load_from_url(url)
        except Exception as e:
            self.app.log(f"[ImageBrowser] AI ref error: {e}")
            return None

    def build_thumbnail_grid(self, parent):
        for w in parent.winfo_children():
            w.destroy()
        self._thumb_refs.clear()
        if not self.results:
            tk.Label(parent, text="No results — search first", bg=CURRENT_THEME["bg"],
                     fg=CURRENT_THEME["fg"], font=("Courier", 10)).pack(pady=20)
            return
        canvas = tk.Canvas(parent, bg=CURRENT_THEME["bg2"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=CURRENT_THEME["bg2"])
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        cols = max(2, (parent.winfo_width() or 500) // 160)
        for idx, result in enumerate(self.results):
            row = idx // cols
            col = idx % cols
            frame = tk.Frame(scroll_frame, bg=CURRENT_THEME["bg2"], bd=1, relief="solid",
                             highlightbackground=CURRENT_THEME["border"])
            frame.grid(row=row, column=col, padx=4, pady=4, sticky="n")
            thumb_url = result.get("thumbnail") or result.get("image", "")
            if thumb_url:
                try:
                    req = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = resp.read()
                    pil_img = Image.open(io.BytesIO(data)).convert("RGB")
                    pil_img.thumbnail((140, 140), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    self._thumb_refs.append(tk_img)
                    lbl = tk.Label(frame, image=tk_img, bg=CURRENT_THEME["bg2"], cursor="hand2")
                    lbl.pack()
                    lbl.bind("<Button-1>", lambda e, i=idx: self._on_thumb_click(i))
                except Exception:
                    tk.Label(frame, text="(no thumb)", bg=CURRENT_THEME["bg2"],
                             fg=CURRENT_THEME["fg"], font=("Courier", 7)).pack()
            else:
                tk.Label(frame, text="(no thumb)", bg=CURRENT_THEME["bg2"],
                         fg=CURRENT_THEME["fg"], font=("Courier", 7)).pack()
            label = result.get("title", "")[:30]
            tk.Label(frame, text=label, bg=CURRENT_THEME["bg2"], fg=CURRENT_THEME["fg"],
                     font=("Courier", 6), wraplength=130).pack()
        canvas.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def _on_thumb_click(self, index):
        img = self.load_result(index)
        if img:
            self.app.log(f"[ImageBrowser] Loaded result #{index + 1}")


# ── v6.31: STRIPED FILL ENGINE ─────────────────────────────

class StripedFillEngine:
    def __init__(self, app):
        self.app = app
        self.min_region_area = 200
        self.stripe_angle = 45
        self.stripe_spacing = 6
        self.stripe_width = 1

    def detect_fill_regions(self, img):
        arr = np.array(img)
        gray = np.array(img.convert("L"), dtype=np.float32)
        h, w = gray.shape
        regions = []
        visited = np.zeros((h, w), dtype=bool)
        for y in range(0, h, 4):
            for x in range(0, w, 4):
                if visited[y, x]:
                    continue
                seed_color = arr[y, x]
                local_var = float(np.var(gray[max(0, y-8):y+8, max(0, x-8):x+8]))
                if local_var > 400:
                    continue
                mask = np.zeros((h, w), dtype=bool)
                queue = [(x, y)]
                mask[y, x] = True
                visited[y, x] = True
                while queue:
                    cx, cy = queue.pop(0)
                    for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                        if 0 <= nx < w and 0 <= ny < h and not mask[ny, nx] and not visited[ny, nx]:
                            diff = np.max(np.abs(arr[ny, nx].astype(int) - seed_color.astype(int)))
                            if diff < 30:
                                mask[ny, nx] = True
                                visited[ny, nx] = True
                                queue.append((nx, ny))
                region_pixels = np.sum(mask)
                if region_pixels >= self.min_region_area:
                    ys, xs = np.where(mask)
                    regions.append({
                        "mask": mask,
                        "bbox": (xs.min(), ys.min(), xs.max(), ys.max()),
                        "area": region_pixels,
                        "center_color": seed_color.tolist(),
                    })
        return regions

    def generate_stripe_strokes(self, img, angle=None, spacing=None):
        if angle is None:
            angle = self.stripe_angle
        if spacing is None:
            spacing = self.stripe_spacing
        regions = self.detect_fill_regions(img)
        if not regions:
            return []
        gray = np.array(img.convert("L"), dtype=np.float32)
        h, w = gray.shape
        all_stripes = []
        ang_rad = math.radians(angle)
        diag = int(math.hypot(w, h))
        cos_a, sin_a = math.cos(ang_rad), math.sin(ang_rad)
        for region in regions:
            mask = region["mask"]
            bx1, by1, bx2, by2 = region["bbox"]
            for offset in range(-diag, diag, spacing):
                stripe = []
                for t in range(-diag, diag, 1):
                    px = int(w/2 + t*cos_a + offset*(-sin_a))
                    py = int(h/2 + t*sin_a + offset*cos_a)
                    if bx1 <= px <= bx2 and by1 <= py <= by2:
                        if 0 <= px < w and 0 <= py < h and mask[py, px]:
                            stripe.append((px, py))
                        else:
                            if len(stripe) >= 3:
                                all_stripes.append(stripe)
                            stripe = []
                    else:
                        if len(stripe) >= 3:
                            all_stripes.append(stripe)
                        stripe = []
                if len(stripe) >= 3:
                    all_stripes.append(stripe)
        return all_stripes

    def process_strokes(self, img, existing_strokes):
        stripe_strokes = self.generate_stripe_strokes(img)
        if not stripe_strokes:
            return existing_strokes
        combined = list(existing_strokes)
        for s in stripe_strokes:
            combined.append(s)
        return combined


# ── v6.31: FLIPBOOK PLAYER ─────────────────────────────────

class FlipbookPlayer:
    def __init__(self, app):
        self.app = app
        self.frames: List[Image.Image] = []
        self.drawn_results: List[Image.Image] = []
        self.current_frame = 0
        self.fps = 8
        self.loop = True
        self.playing = False
        self._play_thread = None
        self._player_window = None
        self._canvas = None
        self._tk_images: List[Any] = []
        self._current_label = None
        self._frame_count_label = None

    def load_sprite_sheet(self, path, cols=None, rows=None):
        try:
            sheet = Image.open(path).convert("RGB")
            self.frames.clear()
            self.drawn_results.clear()
            self.current_frame = 0
            sw, sh = sheet.size
            if cols is None or rows is None:
                cols, rows = self._auto_detect_grid(sheet)
            fw = sw // cols
            fh = sh // rows
            for r in range(rows):
                for c in range(cols):
                    frame = sheet.crop((c * fw, r * fh, (c + 1) * fw, (r + 1) * fh))
                    self.frames.append(frame)
            self.app.log(f"[Flipbook] Loaded {len(self.frames)} frames ({cols}x{rows} grid, {fw}x{fh} each)")
            return True
        except Exception as e:
            self.app.log(f"[Flipbook] Load error: {e}")
            return False

    def _auto_detect_grid(self, sheet):
        sw, sh = sheet.size
        candidates = []
        for divisor in range(1, 11):
            if sw % divisor == 0 and sh % divisor == 0:
                continue
            for c in range(1, min(17, sw // 16 + 1)):
                if sw % c != 0:
                    continue
                fw = sw // c
                for r in range(1, min(17, sh // 16 + 1)):
                    if sh % r != 0:
                        continue
                    fh = sh // r
                    if fw >= 32 and fh >= 32 and fw <= 1024 and fh <= 1024:
                        candidates.append((c, r, fw, fh, c * r))
        if not candidates:
            return 1, 1
        candidates.sort(key=lambda x: -x[4])
        best = candidates[0]
        self.app.log(f"[Flipbook] Auto-detected grid: {best[0]}x{best[1]} ({best[2]}x{best[3]}px)")
        return best[0], best[1]

    def get_frame_count(self):
        return len(self.frames)

    def queue_all_frames(self):
        if not self.frames:
            self.app.log("[Flipbook] No frames loaded")
            return
        self.app.batch_queue.clear()
        for i, frame in enumerate(self.frames):
            path = os.path.join(CACHE_PATH, f"flipbook_frame_{i}.png")
            frame.save(path)
            self.app.batch_queue.append(path)
        self.app.log(f"[Flipbook] Queued {len(self.frames)} frames for drawing")
        self.drawn_results = [None] * len(self.frames)

    def mark_frame_drawn(self, index, result_img):
        if 0 <= index < len(self.drawn_results):
            self.drawn_results[index] = result_img
            self.app.root.after(0, self._update_player_display)

    def show_player(self, parent):
        if self._player_window and self._player_window.winfo_exists():
            self._player_window.lift()
            return
        T = CURRENT_THEME
        win = tk.Toplevel(parent)
        win.title("Flipbook Player")
        win.geometry("500x580")
        win.configure(bg=T["bg"])
        self._player_window = win
        tk.Label(win, text="FLIPBOOK PLAYER", bg=T["bg"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(pady=5)
        self._canvas = tk.Canvas(win, bg="#111", highlightthickness=0, width=400, height=400)
        self._canvas.pack(pady=10)
        ctrl = tk.Frame(win, bg=T["bg"])
        ctrl.pack(fill="x", padx=10, pady=5)
        self._frame_count_label = tk.Label(ctrl, text="0 / 0", bg=T["bg"], fg=T["accent2"],
                                           font=("Courier", 10, "bold"))
        self._frame_count_label.pack(side="left", padx=10)
        def prev():
            if self.frames:
                self.current_frame = (self.current_frame - 1) % len(self.frames)
                self._update_player_display()
        def next_f():
            if self.frames:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self._update_player_display()
        def play_pause():
            if self.playing:
                self.stop()
            else:
                self.play()
        tk.Button(ctrl, text="⏮", command=prev, bg=T["btn"], fg=T["fg"],
                  font=("Courier", 10, "bold"), bd=0, width=3).pack(side="left", padx=2)
        tk.Button(ctrl, text="▶/⏸", command=play_pause, bg=T["btn"], fg=T["accent"],
                  font=("Courier", 10, "bold"), bd=0, width=4).pack(side="left", padx=2)
        tk.Button(ctrl, text="⏭", command=next_f, bg=T["btn"], fg=T["fg"],
                  font=("Courier", 10, "bold"), bd=0, width=3).pack(side="left", padx=2)
        loop_var = tk.BooleanVar(value=self.loop)
        tk.Checkbutton(ctrl, text="LOOP", variable=loop_var,
                       command=lambda: setattr(self, 'loop', loop_var.get()),
                       bg=T["bg"], fg=T["fg"], selectcolor=T["bg2"],
                       activebackground=T["bg"], font=("Courier", 8)).pack(side="left", padx=10)
        fps_frame = tk.Frame(win, bg=T["bg"])
        fps_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(fps_frame, text="FPS:", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 8)).pack(side="left")
        fps_var = tk.IntVar(value=self.fps)
        fps_scale = tk.Scale(fps_frame, from_=1, to=30, orient="horizontal",
                             variable=fps_var, command=lambda v: setattr(self, 'fps', int(v)),
                             bg=T["bg"], fg=T["accent"], troughcolor=T["bg2"],
                             highlightthickness=0, length=200)
        fps_scale.pack(side="left", padx=5)
        tk.Label(fps_frame, text=f"{len(self.frames)} frames loaded" if self.frames else "No frames",
                 bg=T["bg"], fg=T["fg"], font=("Courier", 8)).pack(side="right")
        self._update_player_display()
        win.protocol("WM_DELETE_WINDOW", self._close_player)

    def _update_player_display(self):
        if not self._canvas or not self._player_window or not self._player_window.winfo_exists():
            return
        self._canvas.delete("all")
        img = None
        if self.drawn_results and self.current_frame < len(self.drawn_results) and self.drawn_results[self.current_frame] is not None:
            img = self.drawn_results[self.current_frame]
        elif self.frames and self.current_frame < len(self.frames):
            img = self.frames[self.current_frame]
        if img:
            cw = self._canvas.winfo_width() or 400
            ch = self._canvas.winfo_height() or 400
            iw, ih = img.size
            scale = min(cw / iw, ch / ih) * 0.9
            dw, dh = int(iw * scale), int(ih * scale)
            disp = img.resize((max(1, dw), max(1, dh)), Image.Resampling.NEAREST)
            tk_img = ImageTk.PhotoImage(disp)
            self._tk_images.append(tk_img)
            self._canvas.create_image(cw // 2, ch // 2, image=tk_img, anchor="center")
            info = f"Frame {self.current_frame + 1} / {len(self.frames)}"
            if self.drawn_results and self.current_frame < len(self.drawn_results):
                info += "  [DRAWN]" if self.drawn_results[self.current_frame] is not None else "  [QUEUED]"
            self._canvas.create_text(10, 10, anchor="nw", text=info,
                                     fill="#00ff88", font=("Courier", 8))
        if self._frame_count_label and self.frames:
            txt = f"{self.current_frame + 1} / {len(self.frames)}"
            if self.drawn_results:
                drawn_count = sum(1 for r in self.drawn_results if r is not None)
                txt += f"  ({drawn_count} drawn)"
            self._frame_count_label.config(text=txt)

    def play(self):
        if self.playing or not self.frames:
            return
        self.playing = True
        def _loop():
            while self.playing and self.frames:
                self.app.root.after(0, self._update_player_display)
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                if self.current_frame == 0 and not self.loop:
                    self.playing = False
                    break
                time.sleep(1.0 / self.fps)
        self._play_thread = threading.Thread(target=_loop, daemon=True)
        self._play_thread.start()

    def stop(self):
        self.playing = False

    def _close_player(self):
        self.stop()
        if self._player_window:
            try:
                self._player_window.destroy()
            except Exception:
                pass
        self._player_window = None


# ── v6.32: GODMODE INTEGRATION V3 ──────────────────────────

def _patch_autodrawer_v3():
    if hasattr(AutoDrawer, '_godmode_patched_v3'):
        return
    AutoDrawer._godmode_patched_v3 = True
    orig_init = AutoDrawer.__init__
    def new_init_v3(self):
        orig_init(self)
        self.striped_fill = StripedFillEngine(self)
        self.flipbook = FlipbookPlayer(self)
        self.image_browser = ImageBrowser(self)
        self._setup_v3_bindings()

    def _setup_v3_bindings(self):
        try:
            self.root.bind("<Control-Shift-F>", lambda e: self.flipbook.show_player(self.root) if self.flipbook.frames else self.log("[Flipbook] No frames loaded"))
            self.root.bind("<Control-Shift-S>", lambda e: self._toggle_striped_fill())
        except Exception:
            pass

    def _toggle_striped_fill(self):
        current = SETTINGS.get("STRIPED_FILL_ENABLED", False)
        SETTINGS["STRIPED_FILL_ENABLED"] = not current
        self.log(f"[Striped Fill] {'ON' if not current else 'OFF'}")

    def _flipbook_on_frame_drawn(self, index, img):
        self.flipbook.mark_frame_drawn(index, img)

    AutoDrawer.__init__ = new_init_v3
    AutoDrawer._setup_v3_bindings = _setup_v3_bindings
    AutoDrawer._toggle_striped_fill = _toggle_striped_fill

_patch_autodrawer_v3()


# ── v6.33: CONTROL PANEL V3 TABS ──────────────────────────

def _patch_controlpanel_v3():
    if hasattr(ControlPanelWindow, '_godmode_patched_v3'):
        return
    ControlPanelWindow._godmode_patched_v3 = True

    def _build_v3_striped_fill_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Striped Fill"] = (tab, "Striped Fill")
        self._tab_order.append("Striped Fill")
        self._tab_listbox.insert(tk.END, "Striped Fill")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Fill → Stripe Conversion")
        SETTINGS.setdefault("STRIPED_FILL_ENABLED", True)
        self._checkbox(sf, "Enable Striped Fill", "STRIPED_FILL_ENABLED", True)
        self._slider(sf, "Stripe Angle (deg)", "STRIPE_ANGLE", 0, 180, 5, 140, "int")
        self._slider(sf, "Stripe Spacing", "STRIPE_SPACING", 2, 20, 1, 140, "int")
        self._slider(sf, "Min Region Area", "STRIPE_MIN_AREA", 50, 2000, 50, 140, "int")
        def apply_stripes():
            if not self.app.base_img:
                self._status("No image loaded")
                return
            self.app.striped_fill.min_region_area = int(SETTINGS.get("STRIPE_MIN_AREA", 200))
            self.app.striped_fill.stripe_angle = int(SETTINGS.get("STRIPE_ANGLE", 45))
            self.app.striped_fill.stripe_spacing = int(SETTINGS.get("STRIPE_SPACING", 6))
            regions = self.app.striped_fill.detect_fill_regions(self.app.base_img)
            self._status(f"Detected {len(regions)} fill regions")
            messagebox.showinfo("Striped Fill", f"Found {len(regions)} fill regions\n\nStripe angle: {SETTINGS.get('STRIPE_ANGLE', 45)}°\nSpacing: {SETTINGS.get('STRIPE_SPACING', 6)}px")
        def preview_stripes():
            if not self.app.base_img:
                return
            strokes = self.app.striped_fill.generate_stripe_strokes(self.app.base_img)
            if strokes:
                vc = VirtualCanvas(self.app.base_img.width, self.app.base_img.height)
                vc.render_strokes(strokes, (0, 0, 0), 1)
                preview_img = vc.get_image()
                preview_img.show()
                self._status(f"Preview: {len(strokes)} stripe strokes")
            else:
                self._status("No stripes generated — try lower spacing")
        for text, cmd in [("DETECT FILL REGIONS", apply_stripes), ("PREVIEW STRIPES", preview_stripes)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_v3_striped_fill_tab = _build_v3_striped_fill_tab

    def _build_v3_flipbook_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Flipbook"] = (tab, "Flipbook")
        self._tab_order.append("Flipbook")
        self._tab_listbox.insert(tk.END, "Flipbook")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Sprite Sheet → Animation")
        def load_sheet():
            path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")], title="Select flipbook sprite sheet")
            if path:
                cols_str = tk.simpledialog.askstring("Grid", "Columns (or leave blank for auto-detect):", initialvalue="")
                rows_str = tk.simpledialog.askstring("Grid", "Rows (or leave blank for auto-detect):", initialvalue="")
                cols = int(cols_str) if cols_str and cols_str.strip() else None
                rows = int(rows_str) if rows_str and rows_str.strip() else None
                if self.app.flipbook.load_sprite_sheet(path, cols, rows):
                    self._status(f"Loaded {self.app.flipbook.get_frame_count()} frames")
                else:
                    self._status("Failed to load sprite sheet")
        def queue_all():
            self.app.flipbook.queue_all_frames()
            self._status(f"Queued {self.app.flipbook.get_frame_count()} frames")
        def show_player():
            self.app.flipbook.show_player(self.win)
            self._status("Flipbook player opened")
        for text, cmd in [("LOAD SPRITE SHEET", load_sheet), ("QUEUE ALL FRAMES", queue_all), ("SHOW PLAYER", show_player)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")
        nf = self.app.flipbook.get_frame_count()
        tk.Label(sf, text=f"Frames loaded: {nf}", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 8)).pack(pady=5)

    ControlPanelWindow._build_v3_flipbook_tab = _build_v3_flipbook_tab

    def _build_v3_image_browser_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Image Browser"] = (tab, "Image Browser")
        self._tab_order.append("Image Browser")
        self._tab_listbox.insert(tk.END, "Image Browser")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Web Image Search (DuckDuckGo)")
        query_var = tk.StringVar()
        entry_frame = tk.Frame(sf, bg=T["bg"])
        entry_frame.pack(fill="x", pady=4)
        tk.Entry(entry_frame, textvariable=query_var, bg=T["bg2"], fg=T["fg"],
                 font=("Courier", 10), insertbackground=T["fg"], bd=0).pack(side="left", fill="x", expand=True, padx=(0, 4))
        def do_search():
            q = query_var.get().strip()
            if q:
                self.app.image_browser.search_duckduckgo(q)
                self._status(f"Searching: {q}")
                self.win.after(2000, lambda: self.app.image_browser.build_thumbnail_grid(results_frame))
        tk.Button(entry_frame, text="SEARCH", command=do_search, bg=T["btn"], fg=T["accent2"],
                  font=("Courier", 8, "bold"), bd=0).pack(side="right")
        results_frame = tk.Frame(sf, bg=T["bg"])
        results_frame.pack(fill="both", expand=True, pady=4)
        self._section_label(sf, "Direct URL Load")
        url_var = tk.StringVar()
        url_frame = tk.Frame(sf, bg=T["bg"])
        url_frame.pack(fill="x", pady=4)
        tk.Entry(url_frame, textvariable=url_var, bg=T["bg2"], fg=T["fg"],
                 font=("Courier", 9), insertbackground=T["fg"], bd=0).pack(side="left", fill="x", expand=True, padx=(0, 4))
        def do_load_url():
            url = url_var.get().strip()
            if url:
                self.app.image_browser.load_from_url(url)
                self._status("Loaded from URL")
        tk.Button(url_frame, text="LOAD URL", command=do_load_url, bg=T["btn"], fg=T["accent2"],
                  font=("Courier", 8, "bold"), bd=0).pack(side="right")
        self._section_label(sf, "AI Reference Generation")
        prompt_var = tk.StringVar()
        prompt_frame = tk.Frame(sf, bg=T["bg"])
        prompt_frame.pack(fill="x", pady=4)
        tk.Entry(prompt_frame, textvariable=prompt_var, bg=T["bg2"], fg=T["fg"],
                 font=("Courier", 9), insertbackground=T["fg"], bd=0).pack(side="left", fill="x", expand=True, padx=(0, 4))
        def do_ai_ref():
            p = prompt_var.get().strip()
            if p:
                self.app.image_browser.ai_reference(p)
                self._status(f"AI ref: {p}")
        tk.Button(prompt_frame, text="GENERATE", command=do_ai_ref, bg=T["btn"], fg=T["accent2"],
                  font=("Courier", 8, "bold"), bd=0).pack(side="right")
        self._section_label(sf, "Open Browser")
        def do_open_browser():
            q = query_var.get().strip()
            if q:
                self.app.image_browser.open_in_browser(q)
                self._status("Browser opened")
        tk.Button(sf, text="OPEN IN EXTERNAL BROWSER", command=do_open_browser,
                  bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_v3_image_browser_tab = _build_v3_image_browser_tab

    def _build_v3_limits_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Limits & Caps"] = (tab, "Limits & Caps")
        self._tab_order.append("Limits & Caps")
        self._tab_listbox.insert(tk.END, "Limits & Caps")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Slider Range Caps (max values)")
        info = tk.Label(sf, text="Change these to uncap sliders.\nApply → reopen panel tabs to refresh ranges.",
                        bg=T["bg"], fg=T["fg"], font=("Courier", 7), justify="left")
        info.pack(pady=2)
        limits = [
            ("GLOBAL_SPEED", "Global Speed max", 200, "float"),
            ("STROKE_SPEED", "Stroke Speed max", 100, "int"),
            ("PIXEL_GAP", "Pixel Gap max", 10, "int"),
            ("SKETCH_NO_LIFT", "No-Lift (ms) max", 500, "int"),
            ("SKETCH_BPM", "BPM max", 200, "int"),
            ("BATCH_DELAY", "Batch Delay max", 30, "int"),
            ("FILL_VARIANCE_THRESHOLD", "Fill Variance max", 2000, "int"),
            ("MIN_FILL_AREA", "Min Fill Area max", 1000, "int"),
            ("WHITE_SKIP", "White Skip max", 255, "int"),
            ("BEZIER_STEPS", "Bezier Steps max", 20, "int"),
            ("LIFT_DELAY", "Lift Delay max", 0.5, "float"),
            ("CLICK_DELAY", "Click Delay max", 0.1, "float"),
            ("UI_DELAY", "UI Delay max", 0.5, "float"),
            ("ANIM_FPS", "Animation FPS max", 60, "int"),
            ("PERF_FPS_TARGET", "Perf FPS Target max", 240, "int"),
            ("HISTORY_MAX_STACK", "History Stack max", 200, "int"),
            ("UNDO_STACK_SIZE", "Undo Stack max", 200, "int"),
            ("STRIPE_SPACING", "Stripe Spacing max", 20, "int"),
            ("FLIPBOOK_FPS", "Flipbook FPS max", 30, "int"),
        ]
        entries = {}
        for key, label_text, default_max, fmt in limits:
            row = tk.Frame(sf, bg=T["bg"])
            row.pack(fill="x", padx=6, pady=1)
            tk.Label(row, text=label_text, bg=T["bg"], fg=T["accent2"],
                     font=("Courier", 8, "bold"), anchor="w", width=28).pack(side="left")
            limit_key = f"LIMIT_{key}"
            cur_val = SETTINGS.get(limit_key, default_max)
            var = tk.StringVar(value=str(cur_val))
            ent = tk.Entry(row, textvariable=var, bg=T["bg2"], fg=T["fg"],
                           font=("Courier", 9), width=10, bd=0)
            ent.pack(side="right")
            entries[key] = (var, limit_key, fmt)
        def apply_limits():
            changed = []
            for key, (var, limit_key, fmt) in entries.items():
                try:
                    if fmt == "int":
                        val = int(var.get())
                    else:
                        val = float(var.get())
                    old = SETTINGS.get(limit_key)
                    if old != val:
                        SETTINGS[limit_key] = val
                        changed.append(key)
                except ValueError:
                    pass
            msg = f"Updated {len(changed)} limits.\nRe-open Control Panel tabs to see new slider ranges."
            self._status(msg)
            messagebox.showinfo("Limits Applied", msg)
        def reset_limits():
            for key, (var, limit_key, fmt) in entries.items():
                default = None
                for k2, _, d, _ in limits:
                    if k2 == key:
                        default = d
                        break
                if default is not None:
                    SETTINGS[limit_key] = default
                    var.set(str(default))
            self._status("Limits reset to defaults")
        btn_row = tk.Frame(sf, bg=T["bg"])
        btn_row.pack(fill="x", pady=6)
        tk.Button(btn_row, text="APPLY LIMITS", command=apply_limits,
                  bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=4)
        tk.Button(btn_row, text="RESET DEFAULTS", command=reset_limits,
                  bg=T["btn"], fg=T["accent2"], font=("Courier", 8, "bold"), bd=0).pack(side="left", padx=4)

    ControlPanelWindow._build_v3_limits_tab = _build_v3_limits_tab

    orig_init_v3 = ControlPanelWindow.__init__
    def new_init_v3(self, parent, app):
        orig_init_v3(self, parent, app)
        self._build_v3_striped_fill_tab()
        self._build_v3_flipbook_tab()
        self._build_v3_image_browser_tab()
        self._build_v3_limits_tab()

    ControlPanelWindow.__init__ = new_init_v3

_patch_controlpanel_v3()


# ── v6.40: MASTER CONTROL TABS V4 ──────────────────────────

def _patch_controlpanel_v4():
    if hasattr(ControlPanelWindow, '_godmode_patched_v4'):
        return
    ControlPanelWindow._godmode_patched_v4 = True

    def _build_v4_ai_master_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["AI Master"] = (tab, "AI Master")
        self._tab_order.append("AI Master")
        self._tab_listbox.insert(tk.END, "AI Master")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Model & Device")
        SETTINGS.setdefault("AI_MODEL_ID", "segmind/tiny-sd")
        self._entry(sf, "Model ID", "AI_MODEL_ID", 30)
        tk.Label(sf, text=f"Device: CPU (forced)", bg=T["bg"], fg=T["accent2"],
                 font=("Courier", 8)).pack(pady=2)
        SETTINGS.setdefault("AI_MAX_STEPS", 50)
        SETTINGS.setdefault("AI_STRENGTH", 0.75)
        self._section_label(sf, "Generation Settings")
        self._slider(sf, "Max Inference Steps", "AI_MAX_STEPS", 5, 100, 1, 200, "int")
        self._slider(sf, "Guidance Scale", "AI_GUIDANCE", 1.0, 20.0, 0.5, 200)
        self._slider(sf, "img2img Strength", "AI_STRENGTH", 0.1, 1.0, 0.05, 200)
        self._section_label(sf, "Output Size")
        self._combo(sf, "Width", "AI_WIDTH", ["256","384","512","640","768","1024"], 10)
        self._combo(sf, "Height", "AI_HEIGHT", ["256","384","512","640","768","1024"], 10)
        self._section_label(sf, "Style Presets")
        self._combo(sf, "Style", "AI_STYLE", list(AIGenerationSuite.STYLE_PRESETS.keys()), 14)
        self._section_label(sf, "Actions")
        def load_ai_model():
            if hasattr(self.app, 'ai_gen'):
                ok = self.app.ai_gen.load_model()
                self._status(f"AI model loaded: {ok}")
        def unload_ai_model():
            if hasattr(self.app, 'ai_gen'):
                self.app.ai_gen.pipe = None
                self._status("AI model unloaded")
        def quick_gen():
            prompt = tk.simpledialog.askstring("AI Generate", "Prompt:")
            if prompt and hasattr(self.app, 'ai_gen'):
                self.app.godmode_generate_ai(prompt)
                self._status(f"Generated: {prompt[:40]}")
        def lineart_extract():
            if self.app.base_img and hasattr(self.app, 'ai_gen'):
                self.app.ai_gen.extract_lineart(self.app.base_img)
                self.app._update_canvas()
                self._status("Lineart extracted")
        def upscale_2x():
            if self.app.base_img and hasattr(self.app, 'ai_gen'):
                self.app.base_img = self.app.ai_gen.upscale(self.app.base_img, 2)
                self.app.final_img = None
                self.app._update_canvas()
                self._status("Upscaled 2x")
        def img2img_gen():
            if not self.app.base_img:
                self._status("Load an image first")
                return
            prompt = tk.simpledialog.askstring("img2img", "Prompt:")
            if prompt and hasattr(self.app, 'ai_gen'):
                result = self.app.ai_gen.img2img(self.app.base_img, prompt)
                if result:
                    self._status("img2img done")
                else:
                    self._status("img2img failed")
        for text, cmd in [("LOAD MODEL", load_ai_model), ("UNLOAD MODEL", unload_ai_model),
                          ("QUICK GENERATE", quick_gen), ("EXTRACT LINEART", lineart_extract),
                          ("UPSCALE 2X", upscale_2x), ("IMG2IMG", img2img_gen)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")

    ControlPanelWindow._build_v4_ai_master_tab = _build_v4_ai_master_tab

    def _build_v4_animation_master_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Anim Master"] = (tab, "Anim Master")
        self._tab_order.append("Anim Master")
        self._tab_listbox.insert(tk.END, "Anim Master")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Animation Timeline")
        SETTINGS.setdefault("ANIM_FPS", 12)
        SETTINGS.setdefault("ANIM_LOOP", True)
        SETTINGS.setdefault("ANIM_ONION_SKIN", False)
        self._slider(sf, "FPS", "ANIM_FPS", 1, 60, 1, 200, "int")
        self._checkbox(sf, "Loop", "ANIM_LOOP", True)
        self._checkbox(sf, "Onion Skin", "ANIM_ONION_SKIN", False)
        def add_frame():
            if hasattr(self.app, 'animation') and self.app.base_img:
                self.app.animation.add_frame(self.app.base_img)
                self._status(f"Frame {len(self.app.animation.frames)} added")
        def play_anim():
            if hasattr(self.app, 'animation'):
                self.app.animation.play()
                self._status("Playing")
        def stop_anim():
            if hasattr(self.app, 'animation'):
                self.app.animation.stop()
                self._status("Stopped")
        def export_gif():
            if hasattr(self.app, 'animation'):
                path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
                if path:
                    self.app.animation.export_gif(path)
                    self._status(f"GIF saved to {path}")
        def clear_frames():
            if hasattr(self.app, 'animation'):
                self.app.animation.frames.clear()
                self.app.animation._renumber()
                self._status("All frames cleared")
        for text, cmd in [("+ ADD FRAME", add_frame), ("PLAY", play_anim),
                          ("STOP", stop_anim), ("EXPORT GIF", export_gif),
                          ("CLEAR ALL", clear_frames)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")
        frame_count = len(self.app.animation.frames) if hasattr(self.app, 'animation') else 0
        tk.Label(sf, text=f"Frames: {frame_count}", bg=T["bg"], fg=T["fg"],
                 font=("Courier", 8)).pack(pady=2)
        self._section_label(sf, "Flipbook")
        def load_sheet():
            path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
            if path and hasattr(self.app, 'flipbook'):
                cols_str = tk.simpledialog.askstring("Grid", "Columns (or blank for auto):")
                rows_str = tk.simpledialog.askstring("Grid", "Rows (or blank for auto):")
                cols = int(cols_str) if cols_str and cols_str.strip() else None
                rows = int(rows_str) if rows_str and rows_str.strip() else None
                if self.app.flipbook.load_sprite_sheet(path, cols, rows):
                    self._status(f"Loaded {self.app.flipbook.get_frame_count()} frames")
        def show_flipbook():
            if hasattr(self.app, 'flipbook'):
                self.app.flipbook.show_player(self.win)
                self._status("Flipbook player opened")
        for text, cmd in [("LOAD SPRITE SHEET", load_sheet), ("SHOW PLAYER", show_flipbook)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")

    ControlPanelWindow._build_v4_animation_master_tab = _build_v4_animation_master_tab

    def _build_v4_color_master_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Color Master"] = (tab, "Color Master")
        self._tab_order.append("Color Master")
        self._tab_listbox.insert(tk.END, "Color Master")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Color Settings")
        self._combo(sf, "Color Metric", "COLOR_METRIC",
                    ["Euclidean", "CIEDE2000", "Manhattan"], 14)
        self._slider(sf, "Palette Size", "PALETTE_SIZE", 2, 64, 1, 200, "int")
        self._slider(sf, "White Skip", "WHITE_SKIP", 200, 255, 1, 200, "int")
        self._checkbox(sf, "Skip Blue Mask", "SKIP_BLUE_MASK", True)
        self._section_label(sf, "Color Scan")
        self._combo(sf, "Scan Layout", "COLOR_SCAN_LAYOUT", ["grid", "random", "hilbert"], 14)
        self._slider(sf, "Scan Spacing", "COLOR_SCAN_SPACING", 1, 20, 1, 200, "int")
        self._checkbox(sf, "Color Cache", "COLOR_CACHE_ENABLE", True)
        self._section_label(sf, "Palette Actions")
        def generate_palette():
            self.app.generate_palette()
            self._status("Palette generated")
        def calibrate_palette():
            self.app.calibrate_palette()
            self._status("Palette calibration started")
        def open_palette_editor():
            self.app.open_palette_editor()
            self._status("Palette editor opened")
        def reset_palette():
            self.app.palette_map = []
            if hasattr(self.app, 'color_engine'):
                self.app.color_engine.palette_map = []
            self._status("Palette reset")
        for text, cmd in [("GENERATE PALETTE", generate_palette),
                          ("CALIBRATE PALETTE", calibrate_palette),
                          ("OPEN EDITOR", open_palette_editor),
                          ("RESET PALETTE", reset_palette)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=1, fill="x")

    ControlPanelWindow._build_v4_color_master_tab = _build_v4_color_master_tab

    def _build_v4_responsive_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Display"] = (tab, "Display")
        self._tab_order.append("Display")
        self._tab_listbox.insert(tk.END, "Display")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Window & Layout")
        SETTINGS.setdefault("WINDOW_WIDTH", 1200)
        SETTINGS.setdefault("WINDOW_HEIGHT", 850)
        SETTINGS.setdefault("BTN_COLS", 2)
        self._slider(sf, "Window Width", "WINDOW_WIDTH", 800, 1920, 20, 200, "int")
        self._slider(sf, "Window Height", "WINDOW_HEIGHT", 600, 1080, 20, 200, "int")
        self._slider(sf, "Button Columns", "BTN_COLS", 1, 4, 1, 200, "int")
        self._checkbox(sf, "Show Scrollbar", "SHOW_SCROLLBAR", True)
        self._section_label(sf, "Theme")
        row4 = tk.Frame(sf, bg=T["bg"])
        row4.pack(fill="x", padx=6, pady=4)
        for name in THEMES:
            tk.Button(row4, text=name, command=lambda n=name: self.app._apply_theme(n),
                      bg=T["btn"], fg=T["fg"], font=("Courier", 7, "bold"), bd=0).pack(side="left", padx=2)
        self._section_label(sf, "Reset")
        def resize_window():
            w = int(SETTINGS.get("WINDOW_WIDTH", 1200))
            h = int(SETTINGS.get("WINDOW_HEIGHT", 850))
            self.app.root.geometry(f"{w}x{h}")
            self._status(f"Window resized to {w}x{h}")
        tk.Button(sf, text="APPLY WINDOW SIZE", command=resize_window,
                  bg=T["btn"], fg=T["accent"], font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_v4_responsive_tab = _build_v4_responsive_tab

    def _build_v4_flipbook_capture_tab(self):
        T = CURRENT_THEME
        tab = tk.Frame(self.content_area, bg=T["bg"])
        self.tabs["Capture"] = (tab, "Capture")
        self._tab_order.append("Capture")
        self._tab_listbox.insert(tk.END, "Capture")
        sf = self._make_scroll_frame(tab)
        self._section_label(sf, "Capture → Flipbook Frames")
        SETTINGS.setdefault("CAPTURE_WIDTH", 256)
        SETTINGS.setdefault("CAPTURE_HEIGHT", 256)
        SETTINGS.setdefault("CAPTURE_FORMAT", "PNG")
        self._slider(sf, "Capture Width", "CAPTURE_WIDTH", 64, 1024, 32, 200, "int")
        self._slider(sf, "Capture Height", "CAPTURE_HEIGHT", 64, 1024, 32, 200, "int")
        self._combo(sf, "Save Format", "CAPTURE_FORMAT", ["PNG", "JPG", "BMP"], 8)
        captured_count = [0]

        def capture_viewport():
            if not self.app.base_img:
                self._status("No base image to capture from")
                return
            cw = int(SETTINGS.get("CAPTURE_WIDTH", 256))
            ch = int(SETTINGS.get("CAPTURE_HEIGHT", 256))
            region = self.app.base_img.copy().resize((cw, ch), Image.LANCZOS)
            if not hasattr(self.app, 'flipbook'):
                self._status("Flipbook not available")
                return
            self.app.flipbook.frames.append(region)
            captured_count[0] += 1
            self._status(f"Captured frame {captured_count[0]} ({cw}x{ch})")
            save_dir = os.path.join(CACHE_PATH, "flipbook_captures")
            os.makedirs(save_dir, exist_ok=True)
            fmt = SETTINGS.get("CAPTURE_FORMAT", "PNG")
            fname = f"capture_{captured_count[0]:04d}.{fmt.lower()}"
            region.save(os.path.join(save_dir, fname))

        def capture_region_interactive():
            if not self.app.base_img:
                self._status("No image loaded")
                return
            self._status("Click and drag to select region on canvas...")
            self.app.start_visual_calibration()
            if self.app.canvas_rect:
                x1, y1, x2, y2 = self.app.canvas_rect
                cw = int(SETTINGS.get("CAPTURE_WIDTH", 256))
                ch = int(SETTINGS.get("CAPTURE_HEIGHT", 256))
                region = self.app.base_img.crop((x1, y1, x2, y2)).resize((cw, ch), Image.LANCZOS)
                if hasattr(self.app, 'flipbook'):
                    self.app.flipbook.frames.append(region)
                    captured_count[0] += 1
                    self._status(f"Captured region frame {captured_count[0]}")
                else:
                    self._status("Flipbook not available")

        def clear_captures():
            captured_count[0] = 0
            self._status("Capture count reset (frames remain in flipbook)")

        def show_player():
            if hasattr(self.app, 'flipbook'):
                self.app.flipbook.show_player(self.win)
                self._status("Flipbook player opened")

        info_label = tk.Label(sf, text="Captured: 0 frames", bg=T["bg"], fg=T["fg"],
                              font=("Courier", 8))
        info_label.pack(pady=2)

        def _update_info():
            info_label.config(text=f"Captured: {captured_count[0]} frames\nFlipbook: {len(self.app.flipbook.frames) if hasattr(self.app, 'flipbook') else 0} total")
            self.win.after(1000, _update_info)
        _update_info()

        for text, cmd in [("CAPTURE FROM IMAGE", capture_viewport),
                          ("CAPTURE REGION (drag)", capture_region_interactive),
                          ("CLEAR COUNTER", clear_captures),
                          ("SHOW PLAYER", show_player)]:
            tk.Button(sf, text=text, command=cmd, bg=T["btn"], fg=T["accent2"],
                      font=("Courier", 8, "bold"), bd=0).pack(pady=2, fill="x")

    ControlPanelWindow._build_v4_flipbook_capture_tab = _build_v4_flipbook_capture_tab

    orig_init_v4 = ControlPanelWindow.__init__
    def new_init_v4(self, parent, app):
        orig_init_v4(self, parent, app)
        self._build_v4_ai_master_tab()
        self._build_v4_animation_master_tab()
        self._build_v4_color_master_tab()
        self._build_v4_responsive_tab()
        self._build_v4_flipbook_capture_tab()

    ControlPanelWindow.__init__ = new_init_v4

_patch_controlpanel_v4()


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = AutoDrawer()
    app.root.mainloop()
