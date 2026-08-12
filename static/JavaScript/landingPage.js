/* =====================================
   GESTFACT - JAVASCRIPT
===================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ================================
       ANIMATION DES CARTES
    ================================= */

    const cards = document.querySelectorAll(".document-card");

    cards.forEach((card) => {

        card.addEventListener("mousemove", (event) => {

            const rect = card.getBoundingClientRect();

            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 25;
            const rotateY = (centerX - x) / 25;

            card.style.transform =
                `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "";

        });

    });


    /* ================================
       BOUTON COMMENCER
    ================================= */

    const primaryButton = document.querySelector(".primary-btn");

    if (primaryButton) {

        primaryButton.addEventListener("click", () => {

            const features = document.querySelector("#fonctionnalites");

            if (features) {
                features.scrollIntoView({
                    behavior: "smooth"
                });
            }

        });

    }


    /* ================================
       BOUTON DÉCOUVRIR
    ================================= */

    const secondaryButton = document.querySelector(".secondary-btn");

    if (secondaryButton) {

        secondaryButton.addEventListener("click", () => {

            const features = document.querySelector("#fonctionnalites");

            if (features) {
                features.scrollIntoView({
                    behavior: "smooth"
                });
            }

        });

    }


    /* ================================
       BOUTON CONNEXION
    ================================= */

    const loginButton = document.querySelector(".login-btn");

    if (loginButton) {

        loginButton.addEventListener("click", () => {

            /*
             * Plus tard, tu peux remplacer ceci par :
             *
             * window.location.href = "login.html";
             */

            alert("Redirection vers la page de connexion...");

        });

    }


    /* ================================
       ANIMATION DES FEATURES
    ================================= */

    const features = document.querySelectorAll(".feature");

    const observer = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";

                    observer.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.15
        }
    );


    features.forEach((feature, index) => {

        feature.style.opacity = "0";
        feature.style.transform = "translateY(30px)";

        feature.style.transition =
            `opacity 0.6s ease ${index * 0.15}s,
             transform 0.6s ease ${index * 0.15}s`;

        observer.observe(feature);

    });


    /* ================================
       EFFET PARALLAXE DES CERCLES
    ================================= */

    const circles = document.querySelectorAll(".circle");

    document.addEventListener("mousemove", (event) => {

        const mouseX = (event.clientX / window.innerWidth - 0.5);
        const mouseY = (event.clientY / window.innerHeight - 0.5);

        circles.forEach((circle, index) => {

            const intensity = (index + 1) * 8;

            circle.style.marginLeft = `${mouseX * intensity}px`;
            circle.style.marginTop = `${mouseY * intensity}px`;

        });

    });


    /* ================================
       NAVBAR AU SCROLL
    ================================= */

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if (window.scrollY > 30) {

            navbar.style.background = "rgba(255,255,255,0.85)";
            navbar.style.backdropFilter = "blur(15px)";
            navbar.style.borderRadius = "0 0 15px 15px";

        } else {

            navbar.style.background = "transparent";
            navbar.style.backdropFilter = "none";
            navbar.style.borderRadius = "0";

        }

    });


    /* ================================
       ANIMATION DU TOTAL
    ================================= */

    const total = document.querySelector(".total strong");

    if (total) {

        let started = false;

        const totalObserver = new IntersectionObserver((entries) => {

            if (entries[0].isIntersecting && !started) {

                started = true;

                let current = 0;
                const target = 500000;
                const duration = 1200;
                const startTime = performance.now();

                function animate(time) {

                    const progress =
                        Math.min((time - startTime) / duration, 1);

                    current =
                        Math.floor(target * progress);

                    total.textContent =
                        current.toLocaleString("fr-FR") + " FCFA";

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }

                }

                requestAnimationFrame(animate);

                totalObserver.disconnect();

            }

        });

        totalObserver.observe(total);

    }

});