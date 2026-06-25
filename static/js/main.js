document.addEventListener('DOMContentLoaded', () => {
    // ---------- Cursor glow (throttled with rAF) ----------
    const glow = document.querySelector('.cursor-glow');
    if (glow) {
        let glowX = 0, glowY = 0, glowTicking = false;
        window.addEventListener('mousemove', (e) => {
            glowX = e.clientX;
            glowY = e.clientY;
            glow.classList.add('active');
            if (!glowTicking) {
                glowTicking = true;
                requestAnimationFrame(() => {
                    glow.style.transform = `translate(${glowX}px, ${glowY}px) translate(-50%, -50%)`;
                    glowTicking = false;
                });
            }
        }, { passive: true });
        document.addEventListener('mouseleave', () => glow.classList.remove('active'));
    }

    // ---------- FAQ accordion ----------
    document.querySelectorAll('.faq-item').forEach(item => {
        const q = item.querySelector('.faq-q');
        if (q) q.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');
            item.closest('.faq-list')?.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
            if (!isOpen) item.classList.add('open');
        });
    });

    // ---------- Theme toggle ----------
    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            try { localStorage.setItem('studio-theme', next); } catch (e) {}
        });
    }

    // ---------- Nav background on scroll (throttled with rAF) ----------
    const nav = document.querySelector('.site-nav');
    if (nav) {
        let lastY = window.scrollY;
        let scrollTicking = false;
        const onScroll = () => {
            const y = window.scrollY;
            if (y > 40) nav.classList.add('scrolled');
            else nav.classList.remove('scrolled');
            if (y > lastY && y > 220) nav.classList.add('nav-hidden');
            else nav.classList.remove('nav-hidden');
            lastY = y;
            scrollTicking = false;
        };
        window.addEventListener('scroll', () => {
            if (!scrollTicking) {
                scrollTicking = true;
                requestAnimationFrame(onScroll);
            }
        }, { passive: true });
        onScroll();
    }

    // ---------- Mobile menu ----------
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.mobile-menu');
    const closeBtn = document.querySelector('.close-btn');

    function openMenu() {
        menu.classList.add('open');
        toggle.classList.add('active');
        toggle.setAttribute('aria-expanded', 'true');
        document.body.classList.add('no-scroll');
    }
    function closeMenu() {
        menu.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('no-scroll');
    }

    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            menu.classList.contains('open') ? closeMenu() : openMenu();
        });
        if (closeBtn) closeBtn.addEventListener('click', closeMenu);
        menu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu();
        });
    }

    // ---------- Scroll reveal ----------
    const revealEls = document.querySelectorAll('.reveal');
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });
    revealEls.forEach(el => io.observe(el));

    // Stagger index for groups
    document.querySelectorAll('.reveal-stagger').forEach(group => {
        Array.from(group.children).forEach((child, i) => {
            child.style.setProperty('--i', i);
            child.classList.add('reveal');
            io.observe(child);
        });
    });

    // ---------- Active nav link ----------
    const path = window.location.pathname;
    document.querySelectorAll('.nav-links a, .mobile-menu-links a').forEach(a => {
        if (a.getAttribute('href') === path) a.classList.add('active');
    });

    // ---------- Generic slider (data-slider) ----------
    document.querySelectorAll('[data-slider]').forEach(slider => {
        const track = slider.querySelector('.slider-track');
        const slides = Array.from(track.children);
        const prevBtn = slider.querySelector('.slider-prev');
        const nextBtn = slider.querySelector('.slider-next');
        const dotsWrap = slider.querySelector('.slider-dots');
        let index = 0;
        const perView = parseInt(slider.dataset.perView || '1', 10);

        function visibleCount() {
            return window.innerWidth < 760 ? 1 : perView;
        }

        function update() {
            const vc = visibleCount();
            const max = Math.max(0, slides.length - vc);
            index = Math.min(index, max);
            const pct = (100 / vc) * index;
            track.style.transform = `translate3d(-${pct}%, 0, 0)`;
            if (dotsWrap) {
                dotsWrap.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === index));
            }
        }

        function buildDots() {
            if (!dotsWrap) return;
            const vc = visibleCount();
            const count = Math.max(1, slides.length - vc + 1);
            dotsWrap.innerHTML = '';
            for (let i = 0; i < count; i++) {
                const d = document.createElement('span');
                d.className = 'dot';
                d.addEventListener('click', () => { index = i; update(); });
                dotsWrap.appendChild(d);
            }
        }

        if (nextBtn) nextBtn.addEventListener('click', () => {
            const vc = visibleCount();
            index = Math.min(index + 1, slides.length - vc);
            update();
        });
        if (prevBtn) prevBtn.addEventListener('click', () => {
            index = Math.max(index - 1, 0);
            update();
        });

        buildDots();
        update();

        let autoplay = slider.dataset.autoplay !== 'false';
        let timer = null;
        function startAuto() {
            if (!autoplay) return;
            timer = setInterval(() => {
                const vc = visibleCount();
                index = index + 1 > slides.length - vc ? 0 : index + 1;
                update();
            }, 4200);
        }
        function stopAuto() { if (timer) clearInterval(timer); }
        slider.addEventListener('mouseenter', stopAuto);
        slider.addEventListener('mouseleave', startAuto);
        startAuto();

        let resizeTimer = null;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => { buildDots(); update(); }, 120);
        });
    });

    // ---------- Tilt effect on premium cards (rAF-throttled, transform-only) ----------
    document.querySelectorAll('.tilt-card').forEach(card => {
        if (!card.querySelector('.shine')) {
            const shine = document.createElement('span');
            shine.className = 'shine';
            card.appendChild(shine);
        }

        let pendingX = 0, pendingY = 0, ticking = false;

        function applyTilt() {
            const rect = card.getBoundingClientRect();
            const px = pendingX / rect.width;
            const py = pendingY / rect.height;
            const rx = (py - 0.5) * -10;
            const ry = (px - 0.5) * 10;
            card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-8px) scale(1.015)`;
            card.style.setProperty('--mx', `${px * 100}%`);
            card.style.setProperty('--my', `${py * 100}%`);
            ticking = false;
        }

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            pendingX = e.clientX - rect.left;
            pendingY = e.clientY - rect.top;
            card.classList.add('tilting');
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(applyTilt);
            }
        }, { passive: true });

        card.addEventListener('mouseleave', () => {
            card.classList.remove('tilting');
            card.style.transform = 'perspective(900px) rotateX(0) rotateY(0) translateY(0) scale(1)';
        });
    });

    // ---------- Magnetic buttons (rAF-throttled) ----------
    document.querySelectorAll('.btn-magnetic').forEach(btn => {
        let pendingX = 0, pendingY = 0, ticking = false;

        function applyMagnet() {
            btn.style.transform = `translate3d(${pendingX * 0.18}px, ${pendingY * 0.3}px, 0)`;
            ticking = false;
        }

        btn.addEventListener('mousemove', (e) => {
            const r = btn.getBoundingClientRect();
            pendingX = e.clientX - r.left - r.width / 2;
            pendingY = e.clientY - r.top - r.height / 2;
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(applyMagnet);
            }
        }, { passive: true });

        btn.addEventListener('mouseleave', () => { btn.style.transform = 'translate3d(0,0,0)'; });
    });
});
