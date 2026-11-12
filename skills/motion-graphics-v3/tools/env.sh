# MG V3 environment: source this first.  `source ~/.claude/skills/motion-graphics-v3/tools/env.sh`
export MGV3="${MGV3:-$HOME/.claude/skills/motion-graphics-v3}"
pick() { for p in "$@"; do [ -x "$p" ] && { echo "$p"; return; }; done; echo "$HOME/.cache/motion-graphics-v3/venv/bin/python"; }
export MGV3_TTS=$(pick "$HOME/.cache/motion-graphics-v3/venv/bin/python" "$HOME/.engaging-carousel/venv/bin/python" "$HOME/.faceless-videos/venv/bin/python")     # kokoro_onnx + soundfile
export MGV3_ALIGN=$(pick "$HOME/.cache/motion-graphics-v3/venv/bin/python" "$HOME/wx-env/bin/python")                                                          # torch + torchaudio + scipy
export MGV3_IMG=$(pick "$HOME/.cache/motion-graphics-v3/venv/bin/python" "$HOME/ai-video-editor/venv/bin/python" "$HOME/.cache/editor-v1/venv/bin/python")        # pillow + numpy + playwright
export MGV3_AUDIO=$(pick "$HOME/.cache/motion-graphics-v3/venv/bin/python" "$HOME/.one-prompt-mv/venv/bin/python")                                              # demucs + librosa + matplotlib (reference study only)
echo "MGV3=$MGV3"; echo "tts=$MGV3_TTS align=$MGV3_ALIGN img=$MGV3_IMG audio=$MGV3_AUDIO"
