"""ovos-stt-plugin-browser: the browser's own speech recognition as an OVOS STT plugin.

Chosen like any other STT plugin (`stt.module`, the control panel's voice
settings), it hands speech recognition to the browser's Web Speech API:
Google's recognition in Chrome on Android, Apple's on an iPhone. It is very
good in many languages the public OVOS STT servers do not handle (Danish,
for one), needs no download - and the audio goes to Google or Apple.

The browser listens to the microphone itself; it takes no recorded audio.
So when this plugin is chosen the page does not record: it starts the
browser's recognition, shows the words as they come, and passes the final
text on (worker_main.heard_text), which goes to OVOS as any STT result
does. `execute()`, the path for recorded audio, is therefore not used; a
caller that does use it (a browser without speech recognition, e.g.
Firefox) gets the configured `stt.fallback_module` instead, as a device
does when its STT fails.
"""
from ovos_plugin_manager.templates.stt import STT
from ovos_utils import classproperty

PLUGIN = "ovos-stt-plugin-browser"


class BrowserSTT(STT):
    """Speech recognition in the page (web/app.js, browserSTT)."""

    def __init__(self, config=None):
        super().__init__(config)

    def execute(self, audio, language=None):
        """Recorded audio, which this plugin never gets in a browser that has
        speech recognition: transcribe it with the fallback STT instead."""
        from ovos_config import Configuration
        from ovos_plugin_manager.stt import OVOSSTTFactory
        cfg = Configuration().get("stt", {})
        fallback = cfg.get("fallback_module") or "ovos-stt-plugin-server"
        if fallback == PLUGIN:
            fallback = "ovos-stt-plugin-server"
        stt = OVOSSTTFactory.create({"stt": {"module": fallback,
                                             fallback: cfg.get(fallback, {})}})
        return stt.execute(audio, language)

    @classproperty
    def available_languages(cls) -> set:
        # whatever the browser offers; that cannot be asked from here
        return set()
