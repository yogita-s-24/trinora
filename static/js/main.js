// Trinora – Main JS (CaratLane-style animations + UI)

// ─── Search Overlay ───────────────────────────────────────
function openSearch() {
    const overlay = document.getElementById('searchOverlay');
    overlay.style.display = 'flex';
    setTimeout(() => document.getElementById('searchInput')?.focus(), 100);
    document.body.style.overflow = 'hidden';
}
function closeSearch() {
    document.getElementById('searchOverlay').style.display = 'none';
    document.body.style.overflow = '';
}
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
        closeSearch();
        closeMobileMenu();
    }
});

// ─── Mobile Menu ──────────────────────────────────────────
function openMobileMenu() {
    document.getElementById('mobilePanel').style.transform = 'translateX(0)';
    document.getElementById('mobileOverlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function closeMobileMenu() {
    document.getElementById('mobilePanel').style.transform = 'translateX(-100%)';
    document.getElementById('mobileOverlay').classList.add('hidden');
    document.body.style.overflow = '';
}

// ─── Mobile Submenu ───────────────────────────────────────
function toggleMobileSub(btn) {
    const sub = btn.nextElementSibling;
    const icon = btn.querySelector('svg');
    sub.classList.toggle('hidden');
    icon.style.transform = sub.classList.contains('hidden') ? '' : 'rotate(180deg)';
}

// ─── Back to Top ──────────────────────────────────────────
window.addEventListener('scroll', () => {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    btn.style.opacity    = window.scrollY > 400 ? '1' : '0';
    btn.style.visibility = window.scrollY > 400 ? 'visible' : 'hidden';
});

// ─── Sticky header shadow ─────────────────────────────────
window.addEventListener('scroll', () => {
    const header = document.getElementById('siteHeader');
    if (!header) return;
    header.style.boxShadow = window.scrollY > 10 ? '0 2px 20px rgba(0,0,0,0.1)' : '';
});

// ─── Scroll Reveal (IntersectionObserver – CaratLane style) ─
function initScrollReveal() {
    const els = document.querySelectorAll('[data-animate]');
    if (!els.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    els.forEach(el => observer.observe(el));
}

// ─── Stagger grid children ────────────────────────────────
function initStaggerGrids() {
    document.querySelectorAll('[data-stagger]').forEach(container => {
        const delay = parseInt(container.dataset.stagger) || 80;
        Array.from(container.children).forEach((child, i) => {
            child.setAttribute('data-animate', 'fade-up');
            child.style.transitionDelay = `${i * delay}ms`;
        });
    });
}

// ─── Counter Animation ────────────────────────────────────
function animateCounter(el) {
    const target   = parseInt(el.dataset.count, 10);
    const suffix   = el.dataset.suffix || '';
    const duration = 1600;
    const start    = performance.now();

    function step(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased    = 1 - Math.pow(1 - progress, 4); // ease-out quart
        el.textContent = Math.round(eased * target).toLocaleString('en-IN') + suffix;
        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            el.textContent = target.toLocaleString('en-IN') + suffix;
            el.classList.add('count-done');
        }
    }
    requestAnimationFrame(step);
}

function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(el => observer.observe(el));
}

// ─── Hero Slider ──────────────────────────────────────────
let heroIndex = 0;
let heroTimer = null;

function heroGo(idx) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots   = document.querySelectorAll('.hero-dot');
    if (!slides.length) return;

    slides.forEach((s, i) => {
        s.style.opacity    = i === idx ? '1' : '0';
        s.style.zIndex     = i === idx ? '10' : '1';
        s.style.transition = 'opacity 0.9s ease';
        s.style.position   = 'absolute';
        s.style.inset      = '0';
    });
    dots.forEach((d, i) => {
        d.classList.toggle('bg-white',     i === idx);
        d.classList.toggle('bg-white/40',  i !== idx);
    });
    heroIndex = idx;
}

function heroNext() {
    const n = document.querySelectorAll('.hero-slide').length;
    heroGo((heroIndex + 1) % n);
    resetHeroTimer();
}

function heroPrev() {
    const n = document.querySelectorAll('.hero-slide').length;
    heroGo((heroIndex - 1 + n) % n);
    resetHeroTimer();
}

function resetHeroTimer() {
    clearInterval(heroTimer);
    heroTimer = setInterval(heroNext, 5500);
}

function initHero() {
    if (!document.querySelectorAll('.hero-slide').length) return;
    heroGo(0);
    heroTimer = setInterval(heroNext, 5500);
}

// ─── Gold Sparkle particles on hero ──────────────────────
function initSparkles() {
    const zone = document.querySelector('.hero-sparkle-zone');
    if (!zone) return;

    function spawn() {
        const s = document.createElement('div');
        s.className = 'sparkle';
        s.style.cssText = `
            position:absolute;
            left:${Math.random() * 100}%;
            bottom:${Math.random() * 50}px;
            width:${4 + Math.random() * 5}px;
            height:${4 + Math.random() * 5}px;
            border-radius:50%;
            background:#C9A06E;
            pointer-events:none;
            animation: floatUp ${2 + Math.random() * 2}s ease-out ${Math.random() * 1.5}s both;
        `;
        zone.appendChild(s);
        setTimeout(() => s.remove(), 5000);
    }
    setInterval(spawn, 700);
}

// ─── Newsletter Form ──────────────────────────────────────
function initNewsletter() {
    const nlForm = document.getElementById('nlForm');
    if (!nlForm) return;
    nlForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const input = this.querySelector('input[type="email"]');
        if (input?.value) {
            input.value = '';
            showToast('Thank you for subscribing! Exclusive offers incoming.');
        }
    });
}

// ─── Wishlist toggle ──────────────────────────────────────
function initWishlist() {
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            const path = this.querySelector('svg path');
            if (!path) return;
            const filled = path.getAttribute('fill') === 'currentColor';
            path.setAttribute('fill', filled ? 'none' : 'currentColor');
            showToast(filled ? 'Removed from wishlist' : 'Added to wishlist!');
        });
    });
}

// ─── Auto-dismiss Django messages ─────────────────────────
function initMessages() {
    setTimeout(() => {
        document.querySelectorAll('[role="alert"]').forEach(el => {
            el.style.transition = 'opacity 0.5s';
            el.style.opacity    = '0';
            setTimeout(() => el.remove(), 500);
        });
    }, 5000);
}

// ─── Testimonial auto-rotate ──────────────────────────────
let testimonialIdx = 0;
function initTestimonials() {
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots   = document.querySelectorAll('.testimonial-dot');
    if (!slides.length) return;

    function goTo(idx) {
        slides.forEach((s, i) => {
            s.style.display    = i === idx ? 'block' : 'none';
        });
        dots.forEach((d, i) => {
            d.classList.toggle('bg-black',   i === idx);
            d.classList.toggle('bg-gray-300', i !== idx);
        });
        testimonialIdx = idx;
    }
    goTo(0);
    setInterval(() => goTo((testimonialIdx + 1) % slides.length), 5000);
}

// ─── Toast Notification ───────────────────────────────────
function showToast(msg) {
    const existing = document.getElementById('trinora-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'trinora-toast';
    toast.style.cssText = `
        position:fixed; bottom:6rem; right:1.5rem; z-index:9999;
        background:#000; color:#fff; padding:0.85rem 1.25rem;
        font-size:0.82rem; font-family:'Red Hat Text',sans-serif;
        box-shadow:0 8px 32px rgba(0,0,0,0.25); max-width:300px;
        opacity:0; transform:translateY(10px);
        transition:opacity 0.3s,transform 0.3s;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    requestAnimationFrame(() => {
        toast.style.opacity   = '1';
        toast.style.transform = 'translateY(0)';
    });
    setTimeout(() => {
        toast.style.opacity   = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ─── Boot everything ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initStaggerGrids();
    initScrollReveal();
    initCounters();
    initHero();
    initSparkles();
    initNewsletter();
    initWishlist();
    initMessages();
    initTestimonials();
});
