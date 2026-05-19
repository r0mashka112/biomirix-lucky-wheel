export class WheelCanvas {
    constructor(canvas, colors) {
        this.canvas   = canvas;
        this.ctx      = canvas.getContext('2d');
        this.colors   = colors;
        this.count    = colors.length;
        this.rotation = 0;

        this._animId    = null;
        this._startRot  = 0;
        this._targetRot = 0;
        this._startTime = null;
        this._duration  = 9000;
        this._onEnd     = null;

        this._init();
        window.addEventListener('resize', () => this._init());
    }

    _init() {
        const dpr  = window.devicePixelRatio || 1;
        const side = this.canvas.parentElement.clientWidth;

        this.canvas.width        = side * dpr;
        this.canvas.height       = side * dpr;
        this.canvas.style.width  = side + 'px';
        this.canvas.style.height = side + 'px';

        this.ctx.scale(dpr, dpr);
        this._W = side;
        this._draw();
    }

    spin(extraDegrees, onEnd) {
        this._startRot  = this.rotation;
        this._targetRot = this.rotation + extraDegrees * (Math.PI / 180);
        this._startTime = null;
        this._onEnd     = onEnd;
        cancelAnimationFrame(this._animId);
        this._animId = requestAnimationFrame(t => this._tick(t));
    }

    _tick(ts) {
        if (!this._startTime) this._startTime = ts;
        const p = Math.min((ts - this._startTime) / this._duration, 1);
        this.rotation = this._startRot + (this._targetRot - this._startRot) * this._ease(p);
        this._draw();
        if (p < 1) {
            this._animId = requestAnimationFrame(t => this._tick(t));
        } else {
            this.rotation = this._targetRot;
            this._draw();
            if (this._onEnd) this._onEnd();
        }
    }

    _ease(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    _draw() {
        const ctx    = this.ctx;
        const W      = this._W;
        const cx     = W / 2, cy = W / 2;
        const RIM    = W * 0.048;
        const outerR = W * 0.457;
        const faceR  = outerR - RIM;
        const N      = this.count;
        const SLICE  = (Math.PI * 2) / N;

        ctx.clearRect(0, 0, W, W);

        /* ── 1. Whole-wheel ambient drop shadow ── */
        ctx.save();
        ctx.shadowColor   = 'rgba(0,0,0,0.55)';
        ctx.shadowBlur    = W * 0.07;
        ctx.shadowOffsetY = W * 0.025;
        ctx.beginPath();
        ctx.arc(cx, cy, outerR, 0, Math.PI * 2);
        ctx.fillStyle = '#a07800';
        ctx.fill();
        ctx.restore();

        /* ── 2. Rim base — light top-left, dark bottom-right ── */
        ctx.beginPath();
        ctx.arc(cx, cy, outerR, 0, Math.PI * 2);
        ctx.fillStyle = '#f0c000';
        ctx.fill();

        /* ── 4. Dark groove between rim and face ── */
        ctx.beginPath();
        ctx.arc(cx, cy, faceR + 3, 0, Math.PI * 2);
        ctx.fillStyle = '#150a00';
        ctx.fill();

        /* ── 5. Sectors ── */
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(this.rotation);
        ctx.translate(-cx, -cy);

        for (let i = 0; i < N; i++) {
            const a0 = i * SLICE - Math.PI / 2;
            const a1 = a0 + SLICE;
            const color = this.colors[i];

            /* sector fill */
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.arc(cx, cy, faceR, a0, a1);
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();

            /* separator line */
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + Math.cos(a0) * faceR, cy + Math.sin(a0) * faceR);
            ctx.strokeStyle = 'rgba(0,0,0,0.22)';
            ctx.lineWidth   = 1.5;
            ctx.stroke();

            /* per-sector gloss */
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.arc(cx, cy, faceR, a0, a1);
            ctx.closePath();
            ctx.clip();
            const mid = a0 + SLICE / 2;
            const gl  = ctx.createLinearGradient(
                cx + Math.cos(a0) * faceR * 0.8, cy + Math.sin(a0) * faceR * 0.8,
                cx + Math.cos(mid) * faceR * 0.2, cy + Math.sin(mid) * faceR * 0.2
            );
            gl.addColorStop(0, 'rgba(255,255,255,0.16)');
            gl.addColorStop(1, 'rgba(255,255,255,0)');
            ctx.fillStyle = gl;
            ctx.fillRect(cx - faceR, cy - faceR, faceR * 2, faceR * 2);
            ctx.restore();

            /* gold dot */
            const da   = a0 + SLICE / 2;
            const dr   = faceR * 0.86;
            const dx   = cx + Math.cos(da) * dr;
            const dy   = cy + Math.sin(da) * dr;
            const dotR = W * 0.013;
            const dg   = ctx.createRadialGradient(dx - 2, dy - 2, 1, dx, dy, dotR);
            dg.addColorStop(0,   '#fffaaa');
            dg.addColorStop(0.5, '#f0c000');
            dg.addColorStop(1,   '#8a6000');
            ctx.beginPath();
            ctx.arc(dx, dy, dotR, 0, Math.PI * 2);
            ctx.fillStyle = dg;
            ctx.fill();
        }

        ctx.restore();

        /* ── 6. Recessed shadow on face ── */
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, faceR, 0, Math.PI * 2);
        ctx.clip();

        const rsh = ctx.createRadialGradient(cx, cy, faceR * 0.9, cx, cy, faceR);
        rsh.addColorStop(0,   'rgba(0,0,0,0)');
        rsh.addColorStop(0.5, 'rgba(0,0,0,0.35)');
        rsh.addColorStop(1,   'rgba(0,0,0,0.55)');
        ctx.fillStyle = rsh;
        ctx.fillRect(cx - faceR, cy - faceR, faceR * 2, faceR * 2);

        ctx.restore();

        /* ── 7. Repaint rim on top so face shadow never bleeds onto it ── */
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, outerR, 0, Math.PI * 2);
        ctx.arc(cx, cy, faceR + 2, 0, Math.PI * 2, true);
        ctx.fillStyle = '#f0c000';
        ctx.fill();
        ctx.restore();

        /* ── 8. Rim outer dark stroke ── */
        ctx.beginPath();
        ctx.arc(cx, cy, outerR, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(0,0,0,0.35)';
        ctx.lineWidth   = 2;
        ctx.stroke();

        /* pointer drawn before hub so hub covers its base */
        this._drawPointer(cx, cy, outerR, W);
        this._drawHub(cx, cy, W);
    }

    _drawPointer(cx, cy, outerR, W) {
        const ctx    = this.ctx;
        const hubR   = W * 0.065;
        const tipY   = cy - outerR * 0.62;
        const baseY  = cy - hubR + 6;
        const baseHW = W * 0.032;
        const stemW  = W * 0.022;

        /* outer dark shape */
        ctx.save();
        ctx.shadowColor   = 'rgba(0,0,0,0.4)';
        ctx.shadowBlur    = 8;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 4;

        ctx.beginPath();
        ctx.moveTo(cx,          tipY);
        ctx.lineTo(cx - baseHW, baseY + 10);
        ctx.lineTo(cx - stemW,  baseY + 10);
        ctx.lineTo(cx - stemW,  baseY);
        ctx.lineTo(cx + stemW,  baseY);
        ctx.lineTo(cx + stemW,  baseY + 10);
        ctx.lineTo(cx + baseHW, baseY + 10);
        ctx.closePath();

        const og = ctx.createRadialGradient(
            cx - baseHW * 0.3, tipY, 0,
            cx, tipY + (baseY - tipY) * 0.5, baseHW * 2.5
        );
        og.addColorStop(0,    '#f0c400');
        og.addColorStop(0.15, '#9a6400');
        og.addColorStop(0.5,  '#4a2b00');
        og.addColorStop(1,    '#140800');
        ctx.fillStyle = og;
        ctx.fill();
        ctx.restore();

        /* inner bright triangle (smaller, sits on top) */
        const inset = baseHW * 0.2;
        ctx.beginPath();
        ctx.moveTo(cx, tipY + 5);
        ctx.lineTo(cx - (baseHW - inset), baseY + 4);
        ctx.lineTo(cx + (baseHW - inset), baseY + 4);
        ctx.closePath();

        const ig = ctx.createLinearGradient(cx, tipY, cx, baseY);
        ig.addColorStop(0,    '#fff8d0');
        ig.addColorStop(0.15, '#ffe060');
        ig.addColorStop(0.45, '#f0bc20');
        ig.addColorStop(0.75, '#c08000');
        ig.addColorStop(1,    '#7a5000');
        ctx.fillStyle = ig;
        ctx.fill();

        /* specular gloss line */
        ctx.beginPath();
        ctx.moveTo(cx, tipY + 9);
        ctx.lineTo(cx - baseHW * 0.1, baseY - 2);
        ctx.lineTo(cx + baseHW * 0.1, baseY - 2);
        ctx.closePath();
        const gg = ctx.createLinearGradient(cx, tipY, cx, baseY);
        gg.addColorStop(0, 'rgba(255,255,255,0.8)');
        gg.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = gg;
        ctx.fill();
    }

    _drawHub(cx, cy, W) {
        const ctx  = this.ctx;
        const hubR = W * 0.065;

        ctx.save();
        ctx.shadowColor   = 'rgba(0,0,0,0.55)';
        ctx.shadowBlur    = 12;
        ctx.shadowOffsetY = 4;
        const hg = ctx.createRadialGradient(
            cx - hubR * 0.35, cy - hubR * 0.35, hubR * 0.05,
            cx, cy, hubR
        );
        hg.addColorStop(0,    '#ffffff');
        hg.addColorStop(0.2,  '#fff0a0');
        hg.addColorStop(0.45, '#f0cc40');
        hg.addColorStop(0.7,  '#b89000');
        hg.addColorStop(1,    '#5a3800');
        ctx.beginPath();
        ctx.arc(cx, cy, hubR, 0, Math.PI * 2);
        ctx.fillStyle = hg;
        ctx.fill();
        ctx.restore();

        ctx.beginPath();
        ctx.arc(cx, cy, hubR, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(0,0,0,0.3)';
        ctx.lineWidth   = 1.5;
        ctx.stroke();

        /* orange inner ring */
        const og = ctx.createRadialGradient(
            cx - hubR * 0.2, cy - hubR * 0.2, 1,
            cx, cy, hubR * 0.58
        );
        og.addColorStop(0,   '#ff9a40');
        og.addColorStop(0.5, '#d86000');
        og.addColorStop(1,   '#7a3200');
        ctx.beginPath();
        ctx.arc(cx, cy, hubR * 0.58, 0, Math.PI * 2);
        ctx.fillStyle = og;
        ctx.fill();

        /* white centre */
        const wg = ctx.createRadialGradient(
            cx - hubR * 0.1, cy - hubR * 0.1, 0,
            cx, cy, hubR * 0.28
        );
        wg.addColorStop(0, '#ffffff');
        wg.addColorStop(1, 'rgba(220,220,220,0.6)');
        ctx.beginPath();
        ctx.arc(cx, cy, hubR * 0.28, 0, Math.PI * 2);
        ctx.fillStyle = wg;
        ctx.fill();
    }
}