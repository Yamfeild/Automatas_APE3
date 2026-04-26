let catalogo = {};
let pasoActualTimer = null;
let historial = [];
const DIAGRAM_W = 1200;
const DIAGRAM_H = 520;
let zoomLevel = 1;
let panOffsetX = 0;
let panOffsetY = 0;
let panInitialized = false;

function normalizePair(a, b) {
    return a < b ? `${a}__${b}` : `${b}__${a}`;
}

function edgeKey(from, to) {
    return `${from}|${to}`;
}

function updateZoomLabel() {
    document.getElementById("zoomLabel").textContent = `Zoom: ${Math.round(zoomLevel * 100)}%`;
}

function applyDiagramViewBox() {
    const svg = document.getElementById("diagrama");
    const w = DIAGRAM_W / zoomLevel;
    const h = DIAGRAM_H / zoomLevel;
    const baseX = (DIAGRAM_W - w) / 2;
    const baseY = (DIAGRAM_H - h) / 2;

    let x = baseX + panOffsetX;
    let y = baseY + panOffsetY;

    if (w <= DIAGRAM_W) {
        x = Math.max(0, Math.min(DIAGRAM_W - w, x));
        panOffsetX = x - baseX;
    } else {
        x = baseX;
        panOffsetX = 0;
    }

    if (h <= DIAGRAM_H) {
        y = Math.max(0, Math.min(DIAGRAM_H - h, y));
        panOffsetY = y - baseY;
    } else {
        y = baseY;
        panOffsetY = 0;
    }

    svg.setAttribute("viewBox", `${x} ${y} ${w} ${h}`);
    updateZoomLabel();
}

function setZoom(direction) {
    if (direction === "in") {
        zoomLevel = Math.min(2.6, zoomLevel + 0.2);
    } else if (direction === "out") {
        zoomLevel = Math.max(0.7, zoomLevel - 0.2);
    } else {
        zoomLevel = 1;
        panOffsetX = 0;
        panOffsetY = 0;
    }
    applyDiagramViewBox();
}

window.setZoom = setZoom;

function initDiagramPan() {
    if (panInitialized) return;

    const svg = document.getElementById("diagrama");
    let dragging = false;
    let lastX = 0;
    let lastY = 0;

    svg.addEventListener("pointerdown", (event) => {
        dragging = true;
        lastX = event.clientX;
        lastY = event.clientY;
        svg.style.cursor = "grabbing";
        if (svg.setPointerCapture) svg.setPointerCapture(event.pointerId);
    });

    svg.addEventListener("pointermove", (event) => {
        if (!dragging) return;
        const vb = svg.viewBox.baseVal;
        if (!vb || !svg.clientWidth || !svg.clientHeight) return;

        const scaleX = vb.width / svg.clientWidth;
        const scaleY = vb.height / svg.clientHeight;
        const dx = (event.clientX - lastX) * scaleX;
        const dy = (event.clientY - lastY) * scaleY;

        panOffsetX -= dx;
        panOffsetY -= dy;
        lastX = event.clientX;
        lastY = event.clientY;
        applyDiagramViewBox();
    });

    const stopDragging = (event) => {
        if (!dragging) return;
        dragging = false;
        svg.style.cursor = "grab";
        if (event && event.pointerId !== undefined && svg.releasePointerCapture) {
            try {
                svg.releasePointerCapture(event.pointerId);
            } catch (_) {
                // Ignorar si el puntero ya no esta capturado.
            }
        }
    };

    svg.addEventListener("pointerup", stopDragging);
    svg.addEventListener("pointercancel", stopDragging);
    svg.addEventListener("pointerleave", stopDragging);

    panInitialized = true;
}

function parseInput(value, automataDef = null) {
    const raw = (value || "").trim();
    if (!raw) return [];

    // Si viene con comas, respetamos el formato por tokens.
    if (raw.includes(",")) {
        return raw.split(",").map((x) => x.trim()).filter(Boolean);
    }

    // Para alfabetos de un caracter (ej. notacion cientifica), separar por simbolo.
    const alfabeto = automataDef?.alfabeto || [];
    const esAlfabetoUnitario = alfabeto.length > 0 && alfabeto.every((s) => typeof s === "string" && s.length === 1);
    if (esAlfabetoUnitario) {
        return raw.split("").filter(Boolean);
    }

    // En alfabetos con tokens largos (HDR, CRC, etc.), mantener la entrada completa como un token.
    return [raw];
}

function renderEjemplos(definicion) {
    const cont = document.getElementById("ejemplos");
    cont.innerHTML = "";
    (definicion.ejemplos_aceptados || []).forEach((txt, idx) => {
        const span = document.createElement("span");
        span.className = "chip";
        span.style.animationDelay = `${idx * 50}ms`;
        span.textContent = txt;
        span.onclick = () => { document.getElementById("input").value = txt; };
        cont.appendChild(span);
    });
}

function renderMeta(definicion) {
    const meta = document.getElementById("meta");
    meta.innerHTML = "";
    const items = [
        `Tipo: ${definicion.tipo}`,
        definicion.descripcion ? `Descripción: ${definicion.descripcion}` : null,
        `Estado inicial: ${definicion.estado_inicial}`,
        `Estado(s) final(es): ${(definicion.estados_finales || []).join(", ")}`,
        `Estados: ${(definicion.estados || []).join(", ")}`,
        `Alfabeto: ${(definicion.alfabeto || []).join(", ")}`,
    ].filter(Boolean);
    items.forEach((item) => {
        const div = document.createElement("div");
        div.textContent = item;
        meta.appendChild(div);
    });
}

function renderResumenCatalogo() {
    const host = document.getElementById("catalogoResumen");
    const total = Object.keys(catalogo).length;
    const dfa = Object.values(catalogo).filter((item) => item.tipo === "DFA").length;
    const nfa = Object.values(catalogo).filter((item) => item.tipo === "NFA").length;

    host.innerHTML = `
        <span class="summary-chip"><span class="dot"></span><strong>${total}</strong> ejercicios</span>
        <span class="summary-chip"><span class="dot" style="background:#38bdf8; box-shadow:0 0 0 3px rgba(56,189,248,0.14);"></span><strong>${dfa}</strong> AFD</span>
        <span class="summary-chip"><span class="dot" style="background:#f59e0b; box-shadow:0 0 0 3px rgba(245,158,11,0.14);"></span><strong>${nfa}</strong> AFND</span>
    `;
}

function renderTabla(definicion) {
    const host = document.getElementById("tabla");
    const alfabeto = definicion.alfabeto || [];
    const filas = definicion.tabla_transiciones || [];

    let html = "<table><thead><tr><th>Estado</th>";
    alfabeto.forEach((s) => { html += `<th>${s}</th>`; });
    html += "</tr></thead><tbody>";

    filas.forEach((fila) => {
        html += `<tr><td>${fila.estado}</td>`;
        alfabeto.forEach((simbolo) => {
            const destinos = fila[simbolo] || [];
            html += `<td>${destinos.length ? destinos.join(",") : "-"}</td>`;
        });
        html += "</tr>";
    });

    html += "</tbody></table>";
    host.innerHTML = html;
}

function buildTransitionRowMap(definicion) {
    const map = {};
    (definicion.tabla_transiciones || []).forEach((fila) => {
        map[fila.estado] = fila;
    });
    return map;
}

function getTraversedEdges(definicion, prevStates, simbolo) {
    if (!simbolo) return new Set();
    const rowMap = buildTransitionRowMap(definicion);
    const out = new Set();

    (prevStates || []).forEach((from) => {
        const fila = rowMap[from];
        if (!fila) return;
        const destinos = fila[simbolo] || [];
        destinos.forEach((to) => out.add(edgeKey(from, to)));
    });

    return out;
}

function drawDiagram(definicion, activos = [], highlightedEdges = new Set()) {
    const svg = document.getElementById("diagrama");
    const estados = definicion.estados || [];
    const finales = new Set(definicion.estados_finales || []);
    const activosSet = new Set(activos);
    const pos = {};
    const n = Math.max(estados.length, 1);
    const centerX = DIAGRAM_W / 2;
    const centerY = DIAGRAM_H / 2;
    const radius = Math.min(DIAGRAM_W, DIAGRAM_H) * (n <= 4 ? 0.33 : 0.37);
    const nodeR = n <= 4 ? 32 : 28;

    estados.forEach((estado, i) => {
        const ang = (2 * Math.PI * i) / n - Math.PI / 2;
        pos[estado] = {
            x: centerX + radius * Math.cos(ang),
            y: centerY + radius * Math.sin(ang),
        };
    });

    let content = `
        <defs>
            <marker id="arrowHead" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="strokeWidth">
                <path d="M0,0 L10,4 L0,8 z" fill="#64748b"></path>
            </marker>
        </defs>
    `;

    const edgeMap = {};

    (definicion.tabla_transiciones || []).forEach((fila) => {
        const from = fila.estado;
        if (!pos[from]) return;
        (definicion.alfabeto || []).forEach((simbolo) => {
            const destinos = fila[simbolo] || [];
            destinos.forEach((to) => {
                if (!pos[to]) return;

                const key = edgeKey(from, to);
                if (!edgeMap[key]) {
                    edgeMap[key] = { from, to, simbolos: [] };
                }
                edgeMap[key].simbolos.push(simbolo);
            });
        });
    });

    const edges = Object.values(edgeMap);
    const pairBucket = {};
    edges.forEach((e) => {
        if (e.from === e.to) return;
        const pKey = normalizePair(e.from, e.to);
        if (!pairBucket[pKey]) pairBucket[pKey] = [];
        pairBucket[pKey].push(e);
    });

    const directedOrder = {};
    Object.keys(pairBucket).forEach((pKey) => {
        const list = pairBucket[pKey];
        list.sort((a, b) => (a.from + a.to).localeCompare(b.from + b.to));
        list.forEach((edge, idx) => {
            directedOrder[edgeKey(edge.from, edge.to)] = { index: idx + 1, total: list.length, pairKey: pKey };
        });
    });

    const usedLabelPos = new Set();
    edges.forEach((edge) => {
        const a = pos[edge.from];
        const b = pos[edge.to];
        if (!a || !b) return;
        const isHighlighted = highlightedEdges.has(edgeKey(edge.from, edge.to));
        const stroke = isHighlighted ? "#fb923c" : "#94a3b8";
        const labelColor = isHighlighted ? "#fdba74" : "#d8e6f1";
        const strokeWidth = isHighlighted ? 2.9 : 1.55;
        const label = edge.simbolos.join("/");

        if (edge.from === edge.to) {
            const loopShift = 20;
            content += `<path d="M ${a.x} ${a.y - nodeR} C ${a.x + (26 + loopShift)} ${a.y - (88 + loopShift)}, ${a.x - (26 + loopShift)} ${a.y - (88 + loopShift)}, ${a.x} ${a.y - nodeR}" fill="none" stroke="${stroke}" stroke-width="${strokeWidth}" marker-end="url(#arrowHead)"/>`;
            content += `<text x="${a.x + 2}" y="${a.y - (96 + loopShift)}" font-size="13" fill="${labelColor}">${label}</text>`;
            return;
        }

        const mx = (a.x + b.x) / 2;
        const my = (a.y + b.y) / 2;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const len = Math.hypot(dx, dy) || 1;
        const nx = -dy / len;
        const ny = dx / len;

        const info = directedOrder[edgeKey(edge.from, edge.to)] || { index: 1, total: 1 };
        const center = (info.total + 1) / 2;
        const rank = info.index - center;
        const curveMag = rank * 38;

        const cpx = mx + nx * curveMag;
        const cpy = my + ny * curveMag;
        const startX = a.x + (dx / len) * nodeR;
        const startY = a.y + (dy / len) * nodeR;
        const endX = b.x - (dx / len) * nodeR;
        const endY = b.y - (dy / len) * nodeR;

        content += `<path d="M ${startX} ${startY} Q ${cpx} ${cpy} ${endX} ${endY}" fill="none" stroke="${stroke}" stroke-width="${strokeWidth}" marker-end="url(#arrowHead)"/>`;

        const tx = (startX + 2 * cpx + endX) / 4;
        const ty = (startY + 2 * cpy + endY) / 4;
        const labelPosKey = `${Math.round(tx)}_${Math.round(ty)}_${label}`;
        const extra = usedLabelPos.has(labelPosKey) ? 14 : 0;
        usedLabelPos.add(labelPosKey);
        content += `<text x="${tx + 3}" y="${ty - 4 - extra}" font-size="13" fill="${labelColor}">${label}</text>`;
    });

    estados.forEach((estado) => {
        const p = pos[estado];
        const activo = activosSet.has(estado);
        const baseColor = activo ? "#22c55e" : "#152436";
        const borderColor = activo ? "#86efac" : "#9fb3c4";
        const stateStroke = activo ? 3.2 : 2;
        content += `<circle cx="${p.x}" cy="${p.y}" r="${nodeR}" fill="${baseColor}" stroke="${borderColor}" stroke-width="${stateStroke}"/>`;
        if (finales.has(estado)) {
            content += `<circle cx="${p.x}" cy="${p.y}" r="${nodeR - 6}" fill="none" stroke="${borderColor}" stroke-width="1.8"/>`;
        }
        content += `<text x="${p.x}" y="${p.y + 5}" text-anchor="middle" font-size="14" fill="#eff6fb">${estado}</text>`;
    });

    const ini = definicion.estado_inicial;
    if (pos[ini]) {
        const p = pos[ini];
        content += `<line x1="${p.x - 92}" y1="${p.y}" x2="${p.x - (nodeR + 6)}" y2="${p.y}" stroke="#0f172a" stroke-width="2" marker-end="url(#arrowHead)"/>`;
        content += `<text x="${p.x - 114}" y="${p.y + 5}" font-size="13" fill="#0f172a">inicio</text>`;
    }

    svg.innerHTML = content;
    applyDiagramViewBox();
}

function renderHistorial() {
    const host = document.getElementById("historial");
    if (!historial.length) {
        host.innerHTML = '<span class="history-item">Sin ejecuciones todavía</span>';
        return;
    }

    host.innerHTML = historial
        .map((item, idx) => {
            const cls = item.aceptada ? "history-item ok" : "history-item bad";
            return `<span class="${cls}" style="animation-delay:${idx * 40}ms">${item.automata} | ${item.cadena} | ${item.aceptada ? "aceptada" : "rechazada"}</span>`;
        })
        .join("");
}

function animar(definicion, steps, aceptada) {
    if (pasoActualTimer) {
        clearTimeout(pasoActualTimer);
        pasoActualTimer = null;
    }

    const timeline = document.getElementById("timeline");
    const resultado = document.getElementById("resultado");
    resultado.className = "";
    resultado.textContent = "";
    let i = 0;
    const highlighted = new Set();

    function tick() {
        if (i >= steps.length) {
            resultado.className = aceptada ? "ok" : "bad";
            resultado.textContent = aceptada ? "Cadena aceptada" : "Cadena rechazada";
            return;
        }

        const s = steps[i];
        const txtEstados = (s.states || []).length ? s.states.join(",") : "∅";
        timeline.textContent = `Paso ${s.step} | Símbolo: ${s.input || "inicio"} | Estados: ${txtEstados}`;
        timeline.classList.remove("pulse");
        void timeline.offsetWidth;
        timeline.classList.add("pulse");

        if (i > 0) {
            const prev = steps[i - 1]?.states || [];
            const traversed = getTraversedEdges(definicion, prev, s.input);
            traversed.forEach((k) => highlighted.add(k));
        }

        drawDiagram(definicion, s.states || [], highlighted);
        i += 1;
        pasoActualTimer = setTimeout(tick, 900);
    }

    tick();
}

async function cargarAutomatas() {
    const res = await fetch("/automatas");
    catalogo = await res.json();
    renderResumenCatalogo();
    const select = document.getElementById("automata");
    select.innerHTML = "";

    Object.keys(catalogo).forEach((clave) => {
        const def = catalogo[clave];
        const option = document.createElement("option");
        option.value = clave;
        option.textContent = `${def.nombre} (${def.tipo})`;
        select.appendChild(option);
    });

    const primero = select.value;
    if (primero) {
        const definicion = catalogo[primero];
        renderEjemplos(definicion);
        renderMeta(definicion);
        renderTabla(definicion);
        drawDiagram(definicion, [definicion.estado_inicial]);
        renderHistorial();
    }

    select.addEventListener("change", () => {
        const definicion = catalogo[select.value];
        renderEjemplos(definicion);
        renderMeta(definicion);
        renderTabla(definicion);
        drawDiagram(definicion, [definicion.estado_inicial]);
        document.getElementById("timeline").textContent = "Sin simulación";
        document.getElementById("resultado").textContent = "";
    });
}

async function simular() {
    const automata = document.getElementById("automata").value;
    const eventos = parseInput(document.getElementById("input").value, catalogo[automata]);
    const res = await fetch(`/simular/${automata}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({eventos}),
    });

    const data = await res.json();
    if (data.error) {
        document.getElementById("timeline").textContent = data.error;
        document.getElementById("resultado").textContent = "";
        return;
    }

    renderMeta(data.definicion);
    renderTabla(data.definicion);
    animar(data.definicion, data.steps || [], data.aceptada);

    const cadenaMostrar = (data.cadena || []).join(",") || "ε";
    historial.unshift({
        automata: data.definicion?.nombre || automata,
        cadena: cadenaMostrar,
        aceptada: !!data.aceptada,
    });
    historial = historial.slice(0, 12);
    renderHistorial();
}

window.simular = simular;

cargarAutomatas();
initDiagramPan();
