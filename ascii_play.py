#!/usr/bin/env python3
"""터미널에서 영상을 아스키 아트로 재생하고 오디오를 함께 튼다.

사용법:
    python3 ascii_play.py <유튜브 링크 또는 로컬 영상 파일> [옵션]

화면 크기 (가로 글자 수, 최대 300):
    --size small|medium|large        120 / 200 / 300 칸
    --cols N                         직접 지정
  기본으로 영상 가장자리를 잘라 터미널 화면을 빈 곳 없이 채운다.
  원본 비율을 지켜 전체를 보려면 --no-fill 을 붙인다.
  VS Code 터미널에서는 지정한 크기가 화면에 꽉 차도록 터미널 글꼴 크기를
  재생하는 동안만 바꿨다가 끝나면 되돌린다. (--no-resize 로 끌 수 있다)

필요한 도구: ffmpeg(ffplay, ffprobe 포함), 링크를 쓸 때는 yt-dlp.
개인 감상용. 내려받은 영상이나 결과물을 재배포하지 말 것.
"""
import argparse
import array
import atexit
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "ascii_play")
# 터미널 글자는 세로가 가로보다 약 2배 길다.
CHAR_ASPECT = 0.5
# large 가 최대 사양이다. 이보다 많으면 터미널이 그리는 속도를 못 따라가 끊긴다.
SIZES = {"small": 120, "medium": 200, "large": 300}
MAX_COLS = 300
FONT_KEY = "terminal.integrated.fontSize"
GPU_KEY = "terminal.integrated.gpuAcceleration"
# VS Code 가 허용하는 터미널 글꼴 크기 하한과, 여기서 키울 상한.
FONT_MIN, FONT_MAX = 6, 40


def need(tool):
    if shutil.which(tool) is None:
        sys.exit(f"'{tool}' 을(를) 찾을 수 없습니다. 예: brew install ffmpeg yt-dlp")


def fetch(url):
    """링크의 영상을 저해상도로 내려받아 캐시하고 파일 경로를 돌려준다."""
    need("yt-dlp")
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()[:16]
    for name in os.listdir(CACHE_DIR):
        if name.startswith(key + ".") and not name.endswith(".part"):
            return os.path.join(CACHE_DIR, name)
    print("영상을 내려받는 중...", file=sys.stderr)
    cmd = [
        "yt-dlp", "--no-playlist", "--quiet", "--progress",
        # 아스키 격자는 작으므로 360p면 충분하다.
        "-f", "bv*[height<=360]+ba/b[height<=360]/b",
        "--merge-output-format", "mp4",
        "-o", os.path.join(CACHE_DIR, key + ".%(ext)s"),
        url,
    ]
    if subprocess.call(cmd) != 0:
        sys.exit("내려받기에 실패했습니다. yt-dlp 를 최신 버전으로 올려 보세요.")
    for name in os.listdir(CACHE_DIR):
        if name.startswith(key + ".") and not name.endswith(".part"):
            return os.path.join(CACHE_DIR, name)
    sys.exit("내려받은 파일을 찾지 못했습니다.")


def probe(path):
    """(가로, 세로, fps, 오디오 유무)를 돌려준다."""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate",
            "-of", "csv=p=0", path,
        ], text=True, stderr=subprocess.DEVNULL).strip().splitlines()
    except subprocess.CalledProcessError:
        sys.exit(f"영상 파일로 읽을 수 없습니다: {path}")
    if not out:
        sys.exit("영상 스트림이 없는 파일입니다.")
    w, h, rate = out[0].split(",")[:3]
    num, _, den = rate.partition("/")
    fps = float(num) / float(den or 1)
    audio = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=index", "-of", "csv=p=0", path,
    ], text=True).strip()
    return int(w), int(h), fps, bool(audio)


def grid_size(src_w, src_h, max_cols, fill=False):
    """터미널에 맞는 글자 격자 크기.

    기본은 원본 비율을 지키고, fill 이면 터미널 전체를 쓴다(넘치는 부분은 영상을 잘라 맞춘다).
    """
    term = shutil.get_terminal_size((80, 24))
    cols_limit = min(term.columns, max_cols or MAX_COLS)
    rows_limit = term.lines - 1
    if fill:
        return max(cols_limit, 2), max(rows_limit, 1)
    cols = cols_limit
    rows = int(cols * src_h / src_w * CHAR_ASPECT)
    if rows > rows_limit:
        rows = rows_limit
        cols = int(rows * src_w / src_h / CHAR_ASPECT)
    return max(cols, 2), max(rows, 1)


def workspace_settings_path():
    """현재 위치에서 위로 올라가며 VS Code 작업 폴더의 설정 파일 경로를 찾는다."""
    here = os.getcwd()
    folder = here
    while True:
        if os.path.isdir(os.path.join(folder, ".vscode")) or os.path.isdir(os.path.join(folder, ".git")):
            return os.path.join(folder, ".vscode", "settings.json")
        parent = os.path.dirname(folder)
        if parent == folder:
            return os.path.join(here, ".vscode", "settings.json")
        folder = parent


def load_settings(path):
    """설정 파일을 읽는다. 없으면 빈 설정, 해석할 수 없으면(주석 포함 등) None."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def wait_for_resize(before, timeout=4.0, settle=0.6):
    """터미널 크기가 바뀌고 더 변하지 않을 때까지 기다렸다가 새 크기를 돌려준다.

    VS Code 는 가로와 세로를 시차를 두고 바꾸므로, 처음 바뀐 값을 바로 믿지 않는다.
    """
    deadline = time.monotonic() + timeout
    last = before
    stable_since = None
    while time.monotonic() < deadline:
        time.sleep(0.1)
        now = shutil.get_terminal_size()
        if now != last:
            last = now
            stable_since = time.monotonic()
        elif stable_since is not None and time.monotonic() - stable_since >= settle:
            break
    return last


# 재생하는 동안 바꿔 둔 VS Code 작업 폴더 설정. 끝날 때 맨 처음 내용으로 되돌린다.
session = {}


def in_vscode_terminal():
    return os.environ.get("TERM_PROGRAM") == "vscode" and sys.stdout.isatty()


def workspace_settings():
    """작업 폴더 설정을 돌려준다. 처음 부를 때 원래 내용을 기록하고 복원을 예약한다.

    설정 파일을 해석할 수 없으면(주석 포함 등) None 을 돌려주고 아무것도 건드리지 않는다.
    """
    if "settings" in session:
        return session["settings"]
    path = workspace_settings_path()
    settings = load_settings(path)
    if settings is None:
        print(f"{path} 을(를) 해석할 수 없어 터미널 설정을 자동으로 맞추지 못했습니다.", file=sys.stderr)
    else:
        try:
            with open(path, encoding="utf-8") as f:
                session["original"] = f.read()
        except FileNotFoundError:
            session["original"] = None
        session["path"] = path
    session["settings"] = settings
    return settings


def restore_settings():
    path, original = session["path"], session["original"]
    if original is None:
        try:
            os.remove(path)
            os.rmdir(os.path.dirname(path))
        except OSError:
            pass
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(original)


def save_settings():
    path = session["path"]
    if not session.get("registered"):
        atexit.register(restore_settings)
        session["registered"] = True
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session["settings"], f, indent=2, ensure_ascii=False)
        f.write("\n")


def enable_gpu_rendering():
    """재생하는 동안 VS Code 터미널의 GPU 가속을 켠다.

    GPU 가속이 꺼져 있으면 색이 들어간 글자를 많이 그릴 때 터미널이 크게 느려진다.
    """
    if not in_vscode_terminal():
        return
    settings = workspace_settings()
    if settings is None or settings.get(GPU_KEY) == "on":
        return
    settings[GPU_KEY] = "on"
    save_settings()
    # 터미널이 그리는 방식을 바꿀 시간을 준다.
    time.sleep(0.5)


def fit_vscode_terminal(cols, src_w, src_h, fill=False):
    """VS Code 터미널 글꼴 크기를 바꿔 cols 칸짜리 화면이 창에 꽉 차게 한다.

    VS Code 에는 터미널 안의 프로그램이 크기를 바꾸는 API 가 없어서, 작업 폴더
    설정의 글꼴 크기를 고치는 방식으로 한다. 끝날 때 원래 설정으로 되돌린다.
    """
    if not in_vscode_terminal():
        return
    settings = workspace_settings()
    if settings is None:
        return

    def apply(size):
        settings[FONT_KEY] = size
        save_settings()

    font = settings.get(FONT_KEY)
    if not isinstance(font, (int, float)):
        user = load_settings(os.path.expanduser("~/Library/Application Support/Code/User/settings.json")) or {}
        font = user.get(FONT_KEY) if isinstance(user.get(FONT_KEY), (int, float)) else 12
    # 채우기 모드에서는 가로만 맞추면 되고, 세로는 남는 줄을 모두 쓴다.
    need_rows = 1 if fill else int(cols * src_h / src_w * CHAR_ASPECT) + 1
    term = shutil.get_terminal_size()
    # 칸 수는 글꼴 크기에 반비례하므로, 지금 칸 수와 필요한 칸 수의 비율로 글꼴을 정한다.
    target = int(font * min(term.columns / cols, term.lines / need_rows))
    for _ in range(4):
        target = max(FONT_MIN, min(FONT_MAX, target))
        if target == font:
            break
        apply(target)
        resized = wait_for_resize(term)
        if resized == term:
            # 설정을 바꿔도 반응이 없으면 이 폴더가 VS Code 작업 폴더가 아닌 것이다.
            break
        font, term = target, resized
        if term.columns >= cols and term.lines >= need_rows:
            break
        target = font - 1


def read_exact(pipe, size):
    buf = bytearray()
    while len(buf) < size:
        chunk = pipe.read(size - len(buf))
        if not chunk:
            return None
        buf += chunk
    return bytes(buf)


# 바뀐 부분을 찾을 때 한 줄을 이 칸 수 단위로 나눠 비교한다.
SEGMENT = 16


def changed_spans(frame, prev, cols, rows, bpp):
    """이전에 그린 프레임과 달라진 구간을 (줄, 시작 칸, 끝 칸) 으로 내놓는다."""
    if prev is None:
        for y in range(rows):
            yield y, 0, cols
        return
    new, old = memoryview(frame), memoryview(prev)
    stride = cols * bpp
    for y in range(rows):
        base = y * stride
        if new[base:base + stride] == old[base:base + stride]:
            continue
        start = None
        for x in range(0, cols, SEGMENT):
            lo = base + x * bpp
            hi = base + min(x + SEGMENT, cols) * bpp
            if new[lo:hi] != old[lo:hi]:
                if start is None:
                    start = x
            elif start is not None:
                yield y, start, x
                start = None
        if start is not None:
            yield y, start, cols


def render_gray(frame, prev, cols, rows, table):
    parts = []
    for y, x0, x1 in changed_spans(frame, prev, cols, rows, 1):
        base = y * cols
        parts.append(f"\x1b[{y + 1};{x0 + 1}H")
        parts.append(frame[base + x0:base + x1].translate(table).decode("ascii"))
    return "".join(parts)


# 색 키는 화면에 찍히지 않는 보조 평면 문자로 표현해 글자와 섞이지 않게 한다.
COLOR_BASE = 0x100000
COLOR_RUN = re.compile("([\U00100000-\U00107fff]).(?:\\1.)*")


def build_color_tables(lut, lift):
    """RGB565 값 -> (색 키 + 글자) 표와, 색 키 -> 색 전환 코드 표를 만든다."""
    cells = [None] * 65536
    for v in range(65536):
        r5, g6, b5 = v >> 11, (v >> 5) & 63, v & 31
        lum = (r5 * 255 // 31 * 299 + g6 * 255 // 63 * 587 + b5 * 255 // 31 * 114) // 1000
        key = (r5 << 10) | ((g6 >> 1) << 5) | b5
        cells[v] = chr(COLOR_BASE + key) + lut[lum]
    esc = {}
    for key in range(32768):
        # 글자 농도가 이미 밝기를 표현하므로 색은 조금 밝게 올려 어두워지지 않게 한다.
        r, g, b = (int(255 * (c / 31) ** lift) for c in (key >> 10, (key >> 5) & 31, key & 31))
        esc[chr(COLOR_BASE + key)] = f"\x1b[38;2;{r};{g};{b}m"
    return cells, esc


def make_packer(bits):
    """RGB 3바이트 프레임을 색 단계를 줄인 16비트(R5 G6 B5) 프레임으로 묶는 함수를 만든다.

    빨강·파랑은 bits 비트, 눈이 민감한 초록은 한 비트 더 남긴다. 색을 굵은 단계로
    묶으면 같은 색이 길게 이어져 색 전환 코드가 줄고, 미세한 색 흔들림이 사라져
    이전 프레임과 "달라진 칸"도 줄어든다.
    """
    def level(value, keep, slot):
        out = (value >> (8 - keep)) << (slot - keep)
        # 버린 비트 자리는 구간의 가운데 값으로 채워 전체가 어두워지지 않게 한다.
        return out | (1 << (slot - keep - 1)) if keep < slot else out

    red = [level(v, bits, 5) for v in range(256)]
    green = [level(v, bits + 1, 6) for v in range(256)]
    blue = [level(v, bits, 5) for v in range(256)]
    high_r = bytes(r << 3 for r in red)
    high_g = bytes(g >> 3 for g in green)
    low_g = bytes((g & 7) << 5 for g in green)
    low_b = bytes(blue)

    def merge(a, b, n):
        # 두 바이트열을 큰 정수로 바꿔 한 번에 OR 한다. 칸마다 도는 것보다 훨씬 빠르다.
        return (int.from_bytes(a, "little") | int.from_bytes(b, "little")).to_bytes(n, "little")

    def pack(frame):
        r, g, b = frame[0::3], frame[1::3], frame[2::3]
        n = len(r)
        packed = bytearray(2 * n)
        packed[0::2] = merge(g.translate(low_g), b.translate(low_b), n)
        packed[1::2] = merge(r.translate(high_r), g.translate(high_g), n)
        return bytes(packed)

    return pack


def render_color(frame, prev, cols, rows, cells, esc):
    pixels = array.array("H")
    pixels.frombytes(frame)
    lookup = cells.__getitem__
    # 같은 색이 이어지는 구간은 색 전환 코드를 한 번만 내보낸다.
    recolor = lambda m: esc[m.group(1)] + m.group(0)[1::2]
    parts = []
    for y, x0, x1 in changed_spans(frame, prev, cols, rows, 2):
        base = y * cols
        parts.append(f"\x1b[{y + 1};{x0 + 1}H")
        parts.append(COLOR_RUN.sub(recolor, "".join(map(lookup, pixels[base + x0:base + x1]))))
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser(description="영상을 아스키 아트로 재생합니다.")
    ap.add_argument("source", help="유튜브 등 영상 링크 또는 로컬 파일 경로")
    ap.add_argument("--mono", action="store_true", help="색 없이 흑백 글자로 표시")
    ap.add_argument("--color-bits", type=int, choices=[3, 4, 5], default=4,
                    help="색 채널당 비트 수. 낮을수록 색은 거칠지만 출력이 가벼워 덜 끊김 (기본: 4)")
    ap.add_argument("--fps", type=float, default=0, help="표시 fps 상한 (기본: 원본, 최대 30)")
    ap.add_argument("--size", choices=list(SIZES),
                    help="화면 크기: " + ", ".join(f"{k}={v}칸" for k, v in SIZES.items()))
    ap.add_argument("--cols", type=int, default=0,
                    help=f"가로 글자 수 직접 지정 (최대 {MAX_COLS}, 기본: 터미널 폭)")
    ap.add_argument("--no-fill", dest="fill", action="store_false",
                    help="화면을 채우려고 영상을 자르지 않고, 원본 비율대로 전체를 표시")
    ap.add_argument("--no-resize", action="store_true",
                    help="VS Code 터미널 글꼴 크기를 자동으로 맞추지 않음")
    ap.add_argument("--no-gpu", action="store_true",
                    help="재생 중 VS Code 터미널의 GPU 가속을 켜지 않음")
    ap.add_argument("--stats", action="store_true",
                    help="끝난 뒤 그린 프레임 수와 출력량 등 재생 통계를 표시")
    ap.add_argument("--invert", action="store_true", help="밝기 반전 (밝은 배경 터미널용)")
    ap.add_argument("--no-audio", action="store_true", help="오디오 없이 재생")
    ap.add_argument("--audio-offset", type=float, default=0.0,
                    help="화면을 오디오보다 늦출 초 (음수면 앞당김)")
    args = ap.parse_args()

    need("ffmpeg")
    need("ffprobe")
    is_url = args.source.startswith(("http://", "https://"))
    path = fetch(args.source) if is_url else args.source
    if not os.path.isfile(path):
        sys.exit(f"파일이 없습니다: {path}")

    src_w, src_h, src_fps, has_audio = probe(path)
    fps = min(src_fps, args.fps or 30.0)
    if not args.no_gpu:
        enable_gpu_rendering()
    want_cols = args.cols or SIZES.get(args.size, 0)
    if want_cols:
        want_cols = max(20, min(MAX_COLS, want_cols))
        if not args.no_resize:
            fit_vscode_terminal(want_cols, src_w, src_h, args.fill)
    cols, rows = grid_size(src_w, src_h, want_cols, args.fill)

    ramp = RAMP[::-1] if args.invert else RAMP
    lut = [ramp[v * (len(ramp) - 1) // 255] for v in range(256)]
    table = bytes(ord(c) for c in lut)
    color = not args.mono
    if color:
        cells, esc = build_color_tables(lut, 0.7)
        pack = make_packer(args.color_bits)
    # ffmpeg 에서 받는 프레임은 컬러면 칸당 3바이트, 흑백이면 1바이트다.
    bpp = 3 if color else 1

    def open_video(at):
        """지금 격자 크기로, 영상의 at 초 지점부터 프레임을 내보내는 디코더를 띄운다."""
        seek = ["-ss", f"{at:.3f}"] if at > 0 else []
        crop = ""
        if args.fill:
            # 격자의 화면 비율에 맞게 영상 가운데를 잘라 낸다.
            aspect = cols * CHAR_ASPECT / rows
            crop = f"crop='min(iw,ih*{aspect:.5f})':'min(ih,iw/{aspect:.5f})',"
        return subprocess.Popen(
            ["ffmpeg", "-v", "error"] + seek + [
                "-i", path, "-an",
                "-vf", f"fps={fps},{crop}scale={cols}:{rows}:flags=lanczos",
                "-pix_fmt", "rgb24" if color else "gray",
                "-f", "rawvideo", "-",
            ], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frame_size = cols * rows * bpp
    video = open_video(0)

    audio = None
    decoded = True
    # 재생 통계: 그린 프레임, 건너뛴 프레임, 보낸 글자 수, 계산에 쓴 시간, 터미널로 내보내는 데 쓴 시간.
    drawn = skipped = sent = 0
    compute_time = write_time = 0.0
    out = sys.stdout
    # 대체 화면으로 들어가고 커서를 숨긴다.
    out.write("\x1b[?1049h\x1b[?25l\x1b[2J")
    out.flush()

    def on_signal(signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, on_signal)
    # 터미널 탭을 닫아도 글꼴 설정을 되돌리고 끝나도록 한다.
    signal.signal(signal.SIGHUP, on_signal)

    # 터미널 크기가 마지막으로 바뀐 시각. 0 이면 처리할 변경이 없다.
    resized_at = [0.0]

    def on_resize(signum, _frame):
        resized_at[0] = time.monotonic()
    signal.signal(signal.SIGWINCH, on_resize)

    try:
        # 첫 프레임이 준비된 뒤 오디오를 시작해 출발선을 맞춘다.
        frame = read_exact(video.stdout, frame_size)
        decoded = frame is not None
        if decoded and has_audio and not args.no_audio:
            need("ffplay")
            audio = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
                stdin=subprocess.DEVNULL)
        start = time.monotonic() + args.audio_offset
        index = 0
        # 지금 디코더가 시작한 영상 시각(초).
        base = 0.0
        # 화면에 마지막으로 그린 프레임. 이것과 달라진 칸만 다시 보낸다.
        shown = None
        while frame is not None:
            # 터미널 크기가 바뀌고 잠잠해지면 격자를 다시 잡아 현재 위치부터 이어 그린다.
            if resized_at[0] and time.monotonic() - resized_at[0] > 0.4:
                if want_cols and not args.no_resize:
                    # 칸 수는 그대로 두고, 바뀐 창 크기에 꽉 차도록 글꼴 크기만 다시 맞춘다.
                    fit_vscode_terminal(want_cols, src_w, src_h, args.fill)
                resized_at[0] = 0.0
                fitted = grid_size(src_w, src_h, want_cols, args.fill)
                if fitted != (cols, rows):
                    cols, rows = fitted
                    frame_size = cols * rows * bpp
                    video.terminate()
                    video.stdout.close()
                    base = max(0.0, time.monotonic() - start)
                    video = open_video(base)
                    index = 0
                    shown = None
                    out.write("\x1b[0m\x1b[2J")
                    frame = read_exact(video.stdout, frame_size)
                    continue
            due = start + base + index / fps
            now = time.monotonic()
            if now < due:
                time.sleep(due - now)
            # 한 프레임 넘게 밀렸으면 그리지 않고 건너뛰어 오디오를 따라잡는다.
            if time.monotonic() - due < 1.0 / fps:
                t0 = time.monotonic()
                if color:
                    frame = pack(frame)
                    text = render_color(frame, shown, cols, rows, cells, esc)
                else:
                    text = render_gray(frame, shown, cols, rows, table)
                shown = frame
                t1 = time.monotonic()
                if text:
                    out.write(text)
                out.flush()
                compute_time += t1 - t0
                write_time += time.monotonic() - t1
                sent += len(text)
                drawn += 1
            else:
                skipped += 1
            index += 1
            frame = read_exact(video.stdout, frame_size)
        if audio is not None:
            audio.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (video, audio):
            if proc is not None and proc.poll() is None:
                proc.terminate()
        out.write("\x1b[0m\x1b[?25h\x1b[?1049l")
        out.flush()
    if args.stats and drawn:
        total = drawn + skipped
        print(f"격자 {cols}x{rows} | 그린 프레임 {drawn}/{total} (건너뜀 {skipped}, {100 * skipped // total}%) | "
              f"프레임당 평균: 출력 {sent / drawn / 1000:.0f}KB, 계산 {1000 * compute_time / drawn:.1f}ms, "
              f"터미널 전송 {1000 * write_time / drawn:.1f}ms", file=sys.stderr)
    if not decoded:
        sys.exit("영상을 읽지 못했습니다. ffmpeg 로 열 수 있는 파일인지 확인해 주세요.")


if __name__ == "__main__":
    main()
