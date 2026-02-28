// ============================================================
// CONFIGURACIÓN
// ============================================================
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let sfzRegions  = [];
let audioBuffers = {};

// Variables del intervalo anterior — se llenan en DOMContentLoaded
let previousRoot   = null;
let previousSecond = null;

// ============================================================
// CARGAR Y PARSEAR EL SFZ
// ============================================================
async function loadSFZ() {
    const response = await fetch(SFZ_URL);
    const text     = await response.text();
    sfzRegions     = parseSFZ(text);
    console.log(`SFZ cargado: ${sfzRegions.length} regiones encontradas`);
}

function parseSFZ(text) {
    const regions      = [];
    const regionBlocks = text.split(/<region>/i).slice(1);

    for (const block of regionBlocks) {
        const content = block.split(/<(?!\/)/)[0];
        const region  = {};

        const sampleMatch = content.match(/sample\s*=\s*([^\s\r\n]+)/i);
        if (sampleMatch) region.sample = sampleMatch[1].replace(/\\/g, '/');

        const lokeyMatch = content.match(/lokey\s*=\s*(\d+)/i);
        if (lokeyMatch) region.lokey = parseInt(lokeyMatch[1]);

        const hikeyMatch = content.match(/hikey\s*=\s*(\d+)/i);
        if (hikeyMatch) region.hikey = parseInt(hikeyMatch[1]);

        const pitchMatch = content.match(/pitch_keycenter\s*=\s*(\d+)/i);
        if (pitchMatch) region.pitch_keycenter = parseInt(pitchMatch[1]);

        const lovelMatch = content.match(/lovel\s*=\s*(\d+)/i);
        if (lovelMatch) region.lovel = parseInt(lovelMatch[1]);

        const hivelMatch = content.match(/hivel\s*=\s*(\d+)/i);
        if (hivelMatch) region.hivel = parseInt(hivelMatch[1]);

        if (region.sample && region.lokey !== undefined && region.hikey !== undefined) {
            if (region.pitch_keycenter === undefined) region.pitch_keycenter = region.lokey;
            regions.push(region);
        }
    }
    return regions;
}

// ============================================================
// BUSCAR REGIÓN SFZ PARA UNA NOTA MIDI
// ============================================================
function findRegion(midiNote, velocity = 80) {
    for (const region of sfzRegions) {
        const inKeyRange = midiNote >= region.lokey && midiNote <= region.hikey;
        const inVelRange = velocity >= (region.lovel ?? 0) && velocity <= (region.hivel ?? 127);
        if (inKeyRange && inVelRange) return region;
    }
    return null;
}

// ============================================================
// CARGAR WAV EN MEMORIA (CON CACHÉ)
// ============================================================
async function loadAudioBuffer(samplePath) {
    if (audioBuffers[samplePath]) return audioBuffers[samplePath];

    const safePath  = samplePath.replace(/#/g, '%23');
    const url       = SAMPLES_BASE + safePath;
    const response  = await fetch(url);
    const arrayBuf  = await response.arrayBuffer();
    const audioBuf  = await audioCtx.decodeAudioData(arrayBuf);
    audioBuffers[samplePath] = audioBuf;
    return audioBuf;
}

// ============================================================
// REPRODUCIR UNA NOTA MIDI
// ============================================================
async function playNote(midiNote, startTime, duration = 2.0) {
    const region = findRegion(midiNote);
    if (!region) {
        console.warn(`No se encontró región para nota MIDI ${midiNote}`);
        return;
    }
    const buffer = await loadAudioBuffer(region.sample);
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    const semitonesDiff = midiNote - region.pitch_keycenter;
    source.playbackRate.value = Math.pow(2, semitonesDiff / 12);
    source.connect(audioCtx.destination);
    source.start(startTime);
    source.stop(startTime + duration);
}

// ============================================================
// REPRODUCIR EL INTERVALO ACTUAL
// ============================================================
async function playInterval() {
    if (audioCtx.state === 'suspended') await audioCtx.resume();

    const rootMidi   = parseInt(document.getElementById('root_midi').value);
    const secondMidi = parseInt(document.getElementById('second_midi').value);

    // Guardamos como "anterior" para poder repetirlo después de contestar
    previousRoot   = rootMidi;
    previousSecond = secondMidi;
    document.getElementById('btn-previous').disabled = false;

    const now = audioCtx.currentTime;
    const direction = document.getElementById('direction').value;

    console.log(direction);
    if (direction === 'harmonic') {
        await playNote(rootMidi,   now, 2.0);
        await playNote(secondMidi, now, 2.0);
    } else {
        await playNote(rootMidi,   now,       1.5);
        await playNote(secondMidi, now + 1.2, 1.5);
    }
    
}
// ============================================================
// REPETIR EL INTERVALO ANTERIOR
// ============================================================
async function playPrevious() {
    if (previousRoot === null) return;
    if (audioCtx.state === 'suspended') await audioCtx.resume();

    const now = audioCtx.currentTime;
    await playNote(previousRoot,   now,       1.5);
    await playNote(previousSecond, now + 1.2, 1.5);
}

// ============================================================
// INICIALIZACIÓN — esperar a que el DOM y el SFZ estén listos
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log("Cargando SFZ...");
    await loadSFZ();
    console.log("Listo para reproducir");

    // Leer el intervalo anterior que Django guardó en los campos hidden
    const prevRootVal   = document.getElementById('prev_root').value;
    const prevSecondVal = document.getElementById('prev_second').value;

    // Solo habilitamos el botón si hay valores reales (no vacío ni "None")
    if (prevRootVal && prevRootVal !== 'None' && prevSecondVal && prevSecondVal !== 'None') {
        previousRoot   = parseInt(prevRootVal);
        previousSecond = parseInt(prevSecondVal);
        document.getElementById('btn-previous').disabled = false;
        console.log("Intervalo anterior listo:", previousRoot, "→", previousSecond);
    }
});
