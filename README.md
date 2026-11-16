# ovos-stt-plugin-browser

An [OpenVoiceOS](https://openvoiceos.org) speech-to-text plugin that uses the
**browser's own speech recognition** (the Web Speech API): Google's in Chrome
on Android, Apple's on an iPhone.

It was made for [Emkay](https://github.com/emkay-voice/emkay), OpenVoiceOS in
the browser (Pyodide), and is what Emkay uses. It only makes sense where OVOS
runs in a web page.

- **Good** in many languages the public OVOS STT servers do not handle well
  (Danish, for one), and nothing to download.
- **Not private**: the browser sends the audio to Google or Apple. For speech
  that stays on the device, choose another STT plugin.

## How it works

The browser listens to the microphone itself and gives text, not audio. So
when this plugin is chosen (`stt.module: ovos-stt-plugin-browser`), the page
does not record: it starts the browser's recognition, shows the words as they
come, and passes the final text to OVOS as any STT result goes.

`execute()`, the path for recorded audio, is not used then. A caller that
does use it (a browser without speech recognition, such as Firefox) gets the
STT plugin in `stt.fallback_module` instead, as a device does when its STT
fails.

Emkay's page side is in [`web/app.js`](https://github.com/emkay-voice/emkay/blob/main/web/app.js)
(`browserSTT`), and the text goes to OVOS through `speech.heard_text`.

## Config

```json
"stt": {
  "module": "ovos-stt-plugin-browser",
  "fallback_module": "ovos-stt-plugin-server"
}
```

The language is OVOS' own (`lang`).

## License

Apache-2.0
