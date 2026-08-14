/* ============================================
   ANIMATION DES CERCLES — Section Hero
   ============================================ */
(function () {
  const canvas = document.getElementById("circles-canvas");
  const ctx = canvas.getContext("2d");
  const hero = document.getElementById("hero");

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // Palette des cercles : rose, bleu, violet (avec transparence)
  const palette = [
    "rgba(255, 79, 163, 0.55)",  // rose
    "rgba(61, 107, 255, 0.5)",   // bleu
    "rgba(123, 47, 247, 0.5)",   // violet
    "rgba(255, 79, 163, 0.3)",
    "rgba(61, 107, 255, 0.3)",
  ];

  let circles = [];
  let width, height;

  function resize() {
    width = canvas.width = hero.offsetWidth;
    height = canvas.height = hero.offsetHeight;
  }

  function createCircles() {
    const count = width < 720 ? 9 : 16;
    circles = Array.from({ length: count }, () => {
      const radius = 30 + Math.random() * 90;
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        radius,
        color: palette[Math.floor(Math.random() * palette.length)],
        speedX: (Math.random() - 0.5) * 0.35,
        speedY: (Math.random() - 0.5) * 0.35,
        pulseOffset: Math.random() * Math.PI * 2,
      };
    });
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

      const pulse = Math.sin(time / 1200 + c.pulseOffset) * 4;

      ctx.beginPath();
      ctx.arc(c.x, c.y, c.radius + pulse, 0, Math.PI * 2);
      ctx.fillStyle = c.color;
      ctx.filter = "blur(1px)";
      ctx.fill();
    });

    if (!prefersReducedMotion) {
      requestAnimationFrame(draw);
    }
  }

  function init() {
    resize();
    createCircles();
    draw(0);
  }

  window.addEventListener("resize", () => {
    resize();
    createCircles();
  });

  init();
})();

/* ============================================
   GESTION DES VIDÉOS — Section Vitrine
   ============================================ */
/*(function () {
  const videos = document.querySelectorAll(".video-card__media");

  videos.forEach((card) => {
    const card = card.querySelectort(".video-card__frame");
    const placeholder = card.querySelector(".video-card__placeholder");

    video.addEventListener("loadeddata", () => {
      placeholder.style.display = "";
      video.style.display = "block";
    });

    video.addEventListener("error", () => {
      video.style.display = "none";
      placeholder.style.display = "flex";
    });

    video.style.display = "none";
  });
})();
*/

document.addEventListener('DOMContentLoaded', () => {
    
    const videos = document.querySelectorAll(".video-card_media");

    videos.forEach((card) => {
        const video = card.querySelector("video");
        const placeholder = card.querySelector(".video-card__placeholder");

        // 1. On affiche la vidéo direct, pas besoin d'attendre
        if(video) {
            video.style.display = "block";
        }
        if(placeholder) {
            placeholder.style.display = "none";
        }

        // 2. Si il y a une erreur, on le voit dans la console
        video.addEventListener("error", (e) => {
            console.error("Erreur de chargement de la vidéo:", e);
            // On laisse la vidéo visible pour voir le message d'erreur du navigateur
        });
    });

});