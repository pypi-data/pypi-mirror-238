"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseSdp = void 0;
function parseSdp(sdp) {
    let lines = sdp.split('\r\n');
    let lookup = (prefix) => {
        for (let line of lines) {
            if (line.startsWith(prefix)) {
                return line.substr(prefix.length);
            }
        }
        return null;
    };
    let rawAudioSource = lookup('a=ssrc:');
    let rawVideoSource = lookup('a=ssrc-group:FID ');
    return {
        fingerprint: lookup('a=fingerprint:')?.split(' ')[1] ?? null,
        hash: lookup('a=fingerprint:')?.split(' ')[0] ?? null,
        setup: lookup('a=setup:'),
        pwd: lookup('a=ice-pwd:'),
        ufrag: lookup('a=ice-ufrag:'),
        audioSource: rawAudioSource ? parseInt(rawAudioSource.split(' ')[0]) : null,
        source_groups: rawVideoSource ? rawVideoSource.split(' ').map(obj => {
            return parseInt(obj);
        }) : null,
    };
}
exports.parseSdp = parseSdp;
