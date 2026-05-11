import random

from moviepy.editor import vfx


class EffectsService:
    """
    Lightweight cinematic effects engine.

    OPTIMIZED FOR:
    - Faster rendering
    - Stable MoviePy transforms
    - Smooth Shorts motion
    - Less CPU usage
    - Better visual retention
    """

    def __init__(self):

        # ==============================================
        # SAFER SUBTLE MOTION
        # ==============================================

        self.min_zoom_speed = 0.004
        self.max_zoom_speed = 0.012

        # ==============================================
        # LIGHTWEIGHT FADES
        # ==============================================

        self.fade_duration = 0.20

    # ==================================================
    # MAIN ENTRY
    # ==================================================

    def apply_effects(self, clip):

        if clip is None:
            return clip

        try:

            # ==========================================
            # IMPORTANT:
            # Avoid expensive combo effects too often
            # ==========================================

            motion_type = random.choices(
                population=[
                    "zoom_in",
                    "zoom_out",
                    "pan_left",
                    "pan_right",
                    "none"
                ],
                weights=[35, 20, 15, 15, 15],
                k=1
            )[0]

            # ==========================================
            # APPLY MOTION
            # ==========================================

            if motion_type == "zoom_in":

                clip = self._zoom_in(clip)

            elif motion_type == "zoom_out":

                clip = self._zoom_out(clip)

            elif motion_type == "pan_left":

                clip = self._pan_left(clip)

            elif motion_type == "pan_right":

                clip = self._pan_right(clip)

            # ==========================================
            # LIGHTWEIGHT FADE
            # ==========================================

            clip = self._safe_fade(clip)

            return clip

        except Exception:
            return clip

    # ==================================================
    # ZOOM IN
    # ==================================================

    def _zoom_in(self, clip):

        try:

            speed = random.uniform(
                self.min_zoom_speed,
                self.max_zoom_speed
            )

            # ==========================================
            # smoother + more stable
            # ==========================================

            return clip.fx(
                vfx.resize,
                lambda t: 1 + (speed * t)
            )

        except Exception:
            return clip

    # ==================================================
    # ZOOM OUT
    # ==================================================

    def _zoom_out(self, clip):

        try:

            speed = random.uniform(
                0.002,
                0.006
            )

            duration = max(
                clip.duration,
                1
            )

            return clip.fx(
                vfx.resize,
                lambda t: 1.04 - (
                    speed * (
                        (t / duration) * 8
                    )
                )
            )

        except Exception:
            return clip

    # ==================================================
    # PAN LEFT
    # ==================================================

    def _pan_left(self, clip):

        try:

            move_speed = random.randint(
                3,
                10
            )

            return clip.set_position(
                lambda t: (
                    -move_speed * t,
                    "center"
                )
            )

        except Exception:
            return clip

    # ==================================================
    # PAN RIGHT
    # ==================================================

    def _pan_right(self, clip):

        try:

            move_speed = random.randint(
                3,
                10
            )

            return clip.set_position(
                lambda t: (
                    move_speed * t,
                    "center"
                )
            )

        except Exception:
            return clip

    # ==================================================
    # FADE
    # ==================================================

    def _safe_fade(self, clip):

        try:

            duration = min(
                self.fade_duration,
                clip.duration / 5
            )

            return (
                clip
                .fx(vfx.fadein, duration)
                .fx(vfx.fadeout, duration)
            )

        except Exception:
            return clip


# ==================================================
# SINGLETON
# ==================================================

effects_service = EffectsService()