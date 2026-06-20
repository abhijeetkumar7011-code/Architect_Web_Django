document.addEventListener('DOMContentLoaded', () => {
    // ---------- Cursor glow ----------
    const glow = document.querySelector('.cursor-glow');
    if (glow) {
        window.addEventListener('mousemove', (e) => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
            glow.classList.add('active');
        });
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
});

document.addEventListener('DOMContentLoaded', () => {
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

    // Nav background on scroll
    const nav = document.querySelector('.site-nav');
    const onScroll = () => {
        if (window.scrollY > 40) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll);
    onScroll();

    // Mobile menu
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.mobile-menu');
    const closeBtn = document.querySelector('.close-btn');
    if (toggle && menu) {
        toggle.addEventListener('click', () => menu.classList.add('open'));
        closeBtn.addEventListener('click', () => menu.classList.remove('open'));
        menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));
    }

    // Scroll reveal
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

    // Active nav link
    const path = window.location.pathname;
    document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(a => {
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
            track.style.transform = `translateX(-${pct}%)`;
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

        window.addEventListener('resize', () => { buildDots(); update(); });
    });

    // ---------- Tilt effect on premium cards ----------
    document.querySelectorAll('.tilt-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const rx = ((y / rect.height) - 0.5) * -8;
            const ry = ((x / rect.width) - 0.5) * 8;
            card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-6px)`;
            card.style.setProperty('--mx', `${(x / rect.width) * 100}%`);
            card.style.setProperty('--my', `${(y / rect.height) * 100}%`);
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(900px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // ---------- Magnetic buttons ----------
    document.querySelectorAll('.btn-magnetic').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const r = btn.getBoundingClientRect();
            const x = e.clientX - r.left - r.width / 2;
            const y = e.clientY - r.top - r.height / 2;
            btn.style.transform = `translate(${x * 0.18}px, ${y * 0.3}px)`;
        });
        btn.addEventListener('mouseleave', () => { btn.style.transform = 'translate(0,0)'; });
    });
});
