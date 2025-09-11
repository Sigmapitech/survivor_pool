import { useEffect, useRef, useState } from "react";

import "./style.scss";

const isTouchDevice = () =>
  typeof window !== "undefined" &&
  ("ontouchstart" in window || navigator.maxTouchPoints > 0);

const lerp = (a: number, b: number, n: number) => (1 - n) * a + n * b;

export default function CustomCursor() {
  const cursorRef = useRef<HTMLDivElement | null>(null);
  const rafRef = useRef<number | null>(null);

  const target = useRef({ x: 0, y: 0 });
  const pos = useRef({ x: 0, y: 0 });

  const [shrunk, setShrunk] = useState(false);
  const disabled = useRef<boolean>(isTouchDevice());

  useEffect(() => {
    if (disabled.current) return;

    const cursorEl = cursorRef.current!;
    if (!cursorEl) return;

    const onMove = (e: PointerEvent) => {
      if (e.pointerType && e.pointerType !== "mouse") return;

      target.current.x = e.clientX;
      target.current.y = e.clientY;
    };

    const onEnter = (e: MouseEvent) => {
      cursorEl.style.opacity = "1";
    };

    const onLeave = () => {
      cursorEl.style.opacity = "0";
    };

    const onDown = () => {
      cursorEl.style.transform += " scale(0.92)";
    };

    const onUp = () => {};

    window.addEventListener("pointermove", onMove);
    window.addEventListener("mousemove", onEnter);
    window.addEventListener("mouseleave", onLeave);
    window.addEventListener("mousedown", onDown);
    window.addEventListener("mouseup", onUp);

    const speed = 0.16;
    const baseSize = 20;
    const shrunkSize = 18;

    const loop = () => {
      pos.current.x = lerp(pos.current.x, target.current.x, speed);
      pos.current.y = lerp(pos.current.y, target.current.y, speed);

      const elUnder = document.elementFromPoint(
        target.current.x,
        target.current.y
      ) as HTMLElement | null;

      let hoveringClickable = false;
      if (elUnder) {
        const clickableSelector =
          "a, button, input, textarea, select, [role='button'], [tabindex]:not([tabindex='-1'])";
        if (elUnder.closest(clickableSelector)) hoveringClickable = true;
        else {
          try {
            const cs = getComputedStyle(elUnder);
            if (cs.cursor && cs.cursor.includes("pointer"))
              hoveringClickable = true;
          } catch (err) {}
        }
      }

      if (hoveringClickable !== shrunk) {
        setShrunk(hoveringClickable);
      }

      const diameter = hoveringClickable ? shrunkSize : baseSize;
      const x = pos.current.x - diameter / 2;
      const y = pos.current.y - diameter / 2;

      cursorEl.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${hoveringClickable ? 2 : 1})`;
      cursorEl.style.borderWidth = hoveringClickable ? "1px" : "2px";
      cursorEl.style.opacity = hoveringClickable ? "0.15" : "1";

      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("mousemove", onEnter);
      window.removeEventListener("mouseleave", onLeave);
      window.removeEventListener("mousedown", onDown);
      window.removeEventListener("mouseup", onUp);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [shrunk]);

  if (disabled.current) return null;

  return <div className="cursor" ref={cursorRef} aria-hidden />;
}
