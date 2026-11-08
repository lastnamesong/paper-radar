/* The mark answers the pointer: the edge taxel on the pointer's side of the
   grid is pressed, as a tactile sensor reads a touch from that side. Loaded on
   every page, since the nav carries the mark everywhere; the mark is a static
   drawing without this file. */

(function () {
  "use strict";
  var marks = [].slice.call(document.querySelectorAll(".taxel-mark"));
  if (!marks.length) return;
  // A touch device has no pointer to follow, and a reader who asked for less
  // motion asked for this too.
  if (!matchMedia("(pointer: fine)").matches) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  // The twelve edge taxels, clockwise from the top-left corner, as `data-rc`.
  var ring = ["00", "01", "02", "03", "13", "23", "33", "32", "31", "30", "20", "10"];
  var frame = null;

  function press(e) {
    if (frame) return;
    frame = requestAnimationFrame(function () {
      frame = null;
      marks.forEach(function (svg) {
        var box = svg.getBoundingClientRect();
        if (!box.width) return;
        var dx = e.clientX - (box.left + box.width / 2);
        var dy = e.clientY - (box.top + box.height / 2);
        // Clockwise from the top-left corner, matching `ring`.
        var turn = (Math.atan2(dy, dx) / (2 * Math.PI) + 0.375 + 1) % 1;
        var rc = ring[Math.round(turn * ring.length) % ring.length];
        var on = svg.querySelector(".touch");
        if (on && on.getAttribute("data-rc") === rc) return;
        if (on) on.classList.remove("touch");
        var t = svg.querySelector('[data-rc="' + rc + '"]');
        if (t) t.classList.add("touch");
      });
    });
  }

  window.addEventListener("pointermove", press, { passive: true });
})();
