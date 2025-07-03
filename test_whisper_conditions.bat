@echo off
REM Create test file for condition
echo test condition file > test_condition_met.txt

REM Run the test with whisper mode
echo Testing multi-condition logic...
python spiral_breathe.py test_multi_condition.breathe --whisper --interval 5
