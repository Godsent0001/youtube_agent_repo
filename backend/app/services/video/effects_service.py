from moviepy.editor import vfx


class EffectsService:
    """
    Adds cinematic effects to video clips
    """

    def apply_effects(self, clip):

        clip = self._zoom_in_effect(clip)
        clip = self._fade_effect(clip)

        return clip

    def _zoom_in_effect(self, clip):

        """
        Slow zoom-in (retention booster)
        """

        return clip.fx(
            vfx.resize,
            lambda t: 1 + 0.02 * t  # gradual zoom
        )

    def _fade_effect(self, clip):

        """
        Smooth fade in/out transitions
        """

        return clip.fx(
            vfx.fadein, 0.5
        ).fx(
            vfx.fadeout, 0.5
        )


effects_service = EffectsService()