import io
import wave
import numpy as np


def analyze_voice(audio_file, transcript=""):
    """
    Analyze a recorded interview answer.

    Returns:
        duration
        speaking_pace
        pause_count
        silence_percentage
        voice_energy
        confidence_indicator
    """

    try:
        # -----------------------------------------
        # Read audio bytes
        # -----------------------------------------
        audio_bytes = audio_file.getvalue()

        with wave.open(io.BytesIO(audio_bytes), "rb") as wav:

            sample_rate = wav.getframerate()
            sample_width = wav.getsampwidth()
            channels = wav.getnchannels()
            frames = wav.getnframes()

            duration = frames / sample_rate

            raw_audio = wav.readframes(frames)

        # -----------------------------------------
        # Convert audio to numpy array
        # -----------------------------------------
        if sample_width == 2:
            audio = np.frombuffer(
                raw_audio,
                dtype=np.int16
            ).astype(np.float32)

        elif sample_width == 1:
            audio = np.frombuffer(
                raw_audio,
                dtype=np.uint8
            ).astype(np.float32)

            audio = audio - 128

        elif sample_width == 4:
            audio = np.frombuffer(
                raw_audio,
                dtype=np.int32
            ).astype(np.float32)

        else:
            return {
                "error": "Unsupported audio format."
            }

        # -----------------------------------------
        # Convert stereo to mono
        # -----------------------------------------
        if channels > 1:

            audio = audio.reshape(
                -1,
                channels
            )

            audio = np.mean(
                audio,
                axis=1
            )

        # -----------------------------------------
        # Prevent empty audio problems
        # -----------------------------------------
        if len(audio) == 0 or duration <= 0:

            return {
                "error": "Audio recording is empty."
            }

        # -----------------------------------------
        # Normalize audio
        # -----------------------------------------
        max_value = np.max(np.abs(audio))

        if max_value > 0:
            normalized_audio = audio / max_value
        else:
            normalized_audio = audio

        # -----------------------------------------
        # Calculate voice energy
        # -----------------------------------------
        rms = np.sqrt(
            np.mean(normalized_audio ** 2)
        )

        voice_energy = min(
            100,
            max(
                0,
                int(rms * 200)
            )
        )

        # -----------------------------------------
        # Detect silence
        # -----------------------------------------
        threshold = 0.02

        frame_size = int(sample_rate * 0.05)

        if frame_size <= 0:
            frame_size = 1

        frame_energies = []

        for i in range(
            0,
            len(normalized_audio),
            frame_size
        ):

            frame = normalized_audio[
                i:i + frame_size
            ]

            if len(frame) == 0:
                continue

            energy = np.sqrt(
                np.mean(frame ** 2)
            )

            frame_energies.append(energy)

        frame_energies = np.array(
            frame_energies
        )

        silent_frames = (
            frame_energies < threshold
        )

        silence_percentage = (
            np.mean(silent_frames) * 100
        )

        # -----------------------------------------
        # Count pauses
        # -----------------------------------------
        pause_count = 0
        currently_silent = False

        for silent in silent_frames:

            if silent and not currently_silent:

                pause_count += 1
                currently_silent = True

            elif not silent:

                currently_silent = False

        # -----------------------------------------
        # Calculate speaking pace
        # -----------------------------------------
        words = len(
            transcript.split()
        )

        if duration > 0:

            words_per_minute = (
                words / duration
            ) * 60

        else:

            words_per_minute = 0

        # -----------------------------------------
        # Classify speaking pace
        # -----------------------------------------
        if words_per_minute == 0:

            speaking_pace = "Not available"

        elif words_per_minute < 90:

            speaking_pace = "Slow"

        elif words_per_minute <= 160:

            speaking_pace = "Good"

        else:

            speaking_pace = "Fast"

        # -----------------------------------------
        # Confidence-related indicator
        # -----------------------------------------
        confidence_score = 70

        # Speaking pace
        if 90 <= words_per_minute <= 160:
            confidence_score += 10

        elif words_per_minute > 180:
            confidence_score -= 10

        elif 0 < words_per_minute < 70:
            confidence_score -= 5

        # Pauses
        if pause_count <= 5:
            confidence_score += 5

        elif pause_count > 10:
            confidence_score -= 10

        # Silence
        if silence_percentage < 20:
            confidence_score += 5

        elif silence_percentage > 40:
            confidence_score -= 10

        # Voice energy
        if voice_energy >= 25:
            confidence_score += 5

        elif voice_energy < 10:
            confidence_score -= 5

        # Keep score between 0 and 100
        confidence_score = max(
            0,
            min(
                100,
                confidence_score
            )
        )

        # -----------------------------------------
        # Return results
        # -----------------------------------------
        return {

            "duration": round(
                duration,
                2
            ),

            "words_per_minute": round(
                words_per_minute,
                1
            ),

            "speaking_pace": speaking_pace,

            "pause_count": pause_count,

            "silence_percentage": round(
                silence_percentage,
                1
            ),

            "voice_energy": voice_energy,

            "confidence_indicator": confidence_score

        }

    except Exception as e:

        return {
            "error": str(e)
        }
