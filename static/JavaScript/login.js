/* ============================================
   ANIMATION DES CERCLES — Panneau de marque
   (même logique que la landing page)
   ============================================ */
(function () {
  const canvas = document.getElementById("circles-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const wrapper = canvas.parentElement;

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  let circles = [];
  let width, height;

  function resize() {
    width = canvas.width = wrapper.offsetWidth;
    height = canvas.height = wrapper.offsetHeight;
  }

  function createCircles() {
    circles = Array.from({ length: 10 }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: 25 + Math.random() * 70,
      speedX: (Math.random() - 0.5) * 0.25,
      speedY: (Math.random() - 0.5) * 0.25,
      pulseOffset: Math.random() * Math.PI * 2,
    }));
  }

  function draw(time) {
    ctx.clearRect(0, 0, width, height);
    circles.forEach((c) => {
      c.x += c.speedX;
      c.y += c.speedY;
      if (c.x < -c.radius) c.x = width + c.radius;
      if (c.x > width + c.radius) c.x = -c.radius;
      if (c.y < -c.radius) c.y = height + c.radius;
      if (c.y > height + c.radius) c.y = -c.radius;

      const pulse = Math.sin(time / 1200 + c.pulseOffset) * 3;
      ctx.beginPath();
      ctx.arc(c.x, c.y, c.radius + pulse, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
      ctx.fill();
    });
    if (!prefersReducedMotion) requestAnimationFrame(draw);
  }

  resize();
  createCircles();
  draw(0);
  window.addEventListener("resize", () => { resize(); createCircles(); });
})();

/* ============================================
   AFFICHER / MASQUER LE MOT DE PASSE
   ============================================ */
(function () {
  const toggle = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  if (!toggle || !passwordInput) return;

  toggle.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    toggle.textContent = isHidden ? "🙈" : "👁";
  });
})();