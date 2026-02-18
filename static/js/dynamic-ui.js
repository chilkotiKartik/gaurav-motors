/**
 * GAURAV MOTORS - Premium Dynamic UI/UX JavaScript
 * Advanced Animations, Interactions & Dynamic Effects
 */

(function() {
    'use strict';

    // ===== CONFIGURATION =====
    const CONFIG = {
        animationDuration: 300,
        scrollThreshold: 100,
        counterDuration: 2000,
        particleCount: 50,
        typingSpeed: 80
    };

    // ===== DOM READY =====
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        initPageLoader();
        initCursorGlow();
        initNavbarEffects();
        initScrollAnimations();
        initCounterAnimations();
        initParticleSystem();
        initRippleEffect();
        initMagneticButtons();
        initSmoothScroll();
        initScrollToTop();
        initImageLazyLoad();
        initFormEnhancements();
        initTooltips();
        initNotifications();
        initTypingEffect();
        initParallaxEffect();
        initCardTilt();
        initProgressBars();
        initAccordionAnimation();
        initGalleryLightbox();
        initDynamicNavLinks();
        initWhatsAppFloat();
        initServiceWorkerHints();
    }

    // ===== PAGE LOADER =====
    function initPageLoader() {
        const loader = document.querySelector('.page-loader');
        
        // Function to hide loader
        function hideLoader() {
            const pageLoader = document.querySelector('.page-loader');
            if (pageLoader && !pageLoader.classList.contains('hidden')) {
                pageLoader.classList.add('hidden');
                pageLoader.style.display = 'none';
                pageLoader.style.opacity = '0';
                pageLoader.style.visibility = 'hidden';
                document.body.style.overflow = '';
                
                // Trigger entrance animations
                setTimeout(() => {
                    triggerEntranceAnimations();
                }, 100);
            }
        }
        
        // Multiple fallbacks to ensure loader hides
        window.addEventListener('load', () => {
            setTimeout(hideLoader, 200);
        });
        
        // Fallback: hide after 1.5 seconds max
        setTimeout(hideLoader, 1500);
        
        // Fallback: hide when DOM is interactive
        if (document.readyState === 'complete') {
            setTimeout(hideLoader, 200);
        }
        
        // Immediate hide if already loaded
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(hideLoader, 300);
        }
    }

    function triggerEntranceAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-load');
        animatedElements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('animated');
            }, index * 100);
        });
    }

    // ===== CURSOR GLOW EFFECT =====
    function initCursorGlow() {
        if (window.matchMedia('(pointer: coarse)').matches) return; // Skip on touch devices

        const cursorGlow = document.createElement('div');
        cursorGlow.className = 'cursor-glow';
        document.body.appendChild(cursorGlow);

        let mouseX = 0, mouseY = 0;
        let glowX = 0, glowY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        function animateGlow() {
            glowX += (mouseX - glowX) * 0.1;
            glowY += (mouseY - glowY) * 0.1;
            
            cursorGlow.style.left = glowX + 'px';
            cursorGlow.style.top = glowY + 'px';
            
            requestAnimationFrame(animateGlow);
        }
        animateGlow();

        // Hide on inactive
        let timeout;
        document.addEventListener('mousemove', () => {
            cursorGlow.style.opacity = '1';
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                cursorGlow.style.opacity = '0';
            }, 3000);
        });
    }

    // ===== NAVBAR EFFECTS =====
    function initNavbarEffects() {
        const navbar = document.querySelector('.main-navbar');
        if (!navbar) return;

        let lastScrollY = window.scrollY;

        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > CONFIG.scrollThreshold) {
                navbar.classList.add('scrolled');
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('scrolled');
                navbar.classList.remove('navbar-scrolled');
            }

            // Hide/show on scroll direction
            if (currentScrollY > lastScrollY && currentScrollY > 300) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });

        // Nav link hover effect with mouse tracking
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('mousemove', (e) => {
                const rect = link.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                link.style.setProperty('--mouse-x', x + '%');
                link.style.setProperty('--mouse-y', y + '%');
            });
        });
    }

    // ===== SCROLL ANIMATIONS =====
    function initScrollAnimations() {
        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -100px 0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    
                    // Trigger stagger animation for children
                    if (entry.target.classList.contains('stagger-reveal')) {
                        const children = entry.target.children;
                        Array.from(children).forEach((child, index) => {
                            setTimeout(() => {
                                child.style.opacity = '1';
                                child.style.transform = 'translateY(0)';
                            }, index * 100);
                        });
                    }
                }
            });
        }, observerOptions);

        // Add reveal classes to elements
        const elementsToAnimate = document.querySelectorAll(
            '.card, .stat-card, .service-card, .timeline-item, section > .container, ' +
            '.reveal-on-scroll, .reveal-left, .reveal-right, .reveal-scale, .stagger-reveal'
        );

        elementsToAnimate.forEach(el => {
            if (!el.classList.contains('reveal-on-scroll') && 
                !el.classList.contains('reveal-left') && 
                !el.classList.contains('reveal-right') &&
                !el.classList.contains('reveal-scale')) {
                el.classList.add('reveal-on-scroll');
            }
            observer.observe(el);
        });
    }

    // ===== COUNTER ANIMATIONS =====
    function initCounterAnimations() {
        const counters = document.querySelectorAll('[data-counter], .stat-number, .counter-animate');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCounter(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    function animateCounter(element) {
        const text = element.textContent;
        const match = text.match(/(\d+)/);
        if (!match) return;

        const target = parseInt(match[0]);
        const suffix = text.replace(/[\d,]/g, '');
        const duration = CONFIG.counterDuration;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const eased = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(target * eased);
            
            element.textContent = current.toLocaleString() + suffix;
            element.classList.add('counting');

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.classList.remove('counting');
            }
        }

        requestAnimationFrame(update);
    }

    // ===== PARTICLE SYSTEM =====
    function initParticleSystem() {
        const heroSection = document.querySelector('.hero-wrapper, .hero-section, .jumbotron');
        if (!heroSection) return;

        // Disable particle system on small screens for clarity
        if (window.innerWidth < 768) return;

        // Create particle container
        let particleContainer = heroSection.querySelector('.hero-particles');
        if (!particleContainer) {
            particleContainer = document.createElement('div');
            particleContainer.className = 'hero-particles';
            heroSection.insertBefore(particleContainer, heroSection.firstChild);
        }

        // Create particles
        for (let i = 0; i < CONFIG.particleCount; i++) {
            createParticle(particleContainer);
        }
    }

    function createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'hero-particle';
        
        const size = Math.random() * 8 + 4;
        const left = Math.random() * 100;
        const delay = Math.random() * 15;
        const duration = Math.random() * 10 + 10;
        const opacity = Math.random() * 0.5 + 0.2;
        
        particle.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${left}%;
            animation-delay: ${delay}s;
            animation-duration: ${duration}s;
            opacity: ${opacity};
        `;
        
        container.appendChild(particle);
    }

    // ===== RIPPLE EFFECT =====
    function initRippleEffect() {
        document.querySelectorAll('.btn, .nav-link, .card').forEach(element => {
            element.classList.add('btn-ripple');
            
            element.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
                ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // ===== MAGNETIC BUTTONS =====
    function initMagneticButtons() {
        if (window.matchMedia('(pointer: coarse)').matches) return;

        document.querySelectorAll('.btn-primary, .btn-warning, .btn-lg').forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });
    }

    // ===== SMOOTH SCROLL =====
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ===== SCROLL TO TOP =====
    function initScrollToTop() {
        // If a call-top element exists (we replaced the upper arrow), don't create another scroll-to-top button
        if (document.querySelector('.call-top')) return;

        // avoid selecting the new call button (which also uses .scroll-top)
        let scrollBtn = document.querySelector('.fab-scroll-top, .scroll-top:not(.call-top)');
        
        if (!scrollBtn) {
            scrollBtn = document.createElement('button');
            scrollBtn.className = 'fab-modern fab-scroll-top';
            scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
            scrollBtn.setAttribute('aria-label', 'Scroll to top');
            document.body.appendChild(scrollBtn);
        }

        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
            }
        });

        scrollBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ===== IMAGE LAZY LOAD =====
    function initImageLazyLoad() {
        const images = document.querySelectorAll('img[data-src], img[loading="lazy"]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ===== FORM ENHANCEMENTS =====
    function initFormEnhancements() {
        // Floating label animation
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });

            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });

            // Real-time validation
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else if (this.value) {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });

        // Password strength indicator
        document.querySelectorAll('input[type="password"]').forEach(input => {
            const wrapper = input.parentElement;
            const strengthBar = document.createElement('div');
            strengthBar.className = 'password-strength mt-2';
            strengthBar.innerHTML = '<div class="strength-bar"></div>';
            wrapper.appendChild(strengthBar);

            input.addEventListener('input', function() {
                const strength = calculatePasswordStrength(this.value);
                const bar = strengthBar.querySelector('.strength-bar');
                bar.style.width = strength + '%';
                bar.style.background = strength < 33 ? '#ef4444' : strength < 66 ? '#f59e0b' : '#10b981';
            });
        });
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength += 25;
        if (password.match(/[a-z]/)) strength += 25;
        if (password.match(/[A-Z]/)) strength += 25;
        if (password.match(/[0-9]/)) strength += 12.5;
        if (password.match(/[^a-zA-Z0-9]/)) strength += 12.5;
        return Math.min(strength, 100);
    }

    // ===== TOOLTIPS =====
    function initTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(el => {
            el.classList.add('tooltip-modern');
        });
    }

    // ===== NOTIFICATIONS =====
    function initNotifications() {
        window.showNotification = function(message, type = 'info', duration = 5000) {
            const notification = document.createElement('div');
            notification.className = `notification-toast ${type}`;
            notification.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-3 fs-4"></i>
                    <div>
                        <strong class="d-block">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                        <span>${message}</span>
                    </div>
                    <button class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => notification.classList.add('show'), 10);
            
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 500);
            }, duration);
        };

        // Auto-convert Flask flash messages
        document.querySelectorAll('.alert').forEach(alert => {
            const message = alert.textContent.trim();
            const type = alert.classList.contains('alert-success') ? 'success' :
                        alert.classList.contains('alert-danger') ? 'error' :
                        alert.classList.contains('alert-warning') ? 'warning' : 'info';
            
            // Keep original for accessibility, but also show notification
            setTimeout(() => {
                if (message) {
                    // showNotification(message, type);
                }
            }, 1000);
        });
    }

    // ===== TYPING EFFECT =====
    function initTypingEffect() {
        document.querySelectorAll('[data-typing]').forEach(el => {
            const text = el.dataset.typing || el.textContent;
            el.textContent = '';
            el.style.borderRight = '2px solid';
            
            let index = 0;
            function type() {
                if (index < text.length) {
                    el.textContent += text.charAt(index);
                    index++;
                    setTimeout(type, CONFIG.typingSpeed);
                } else {
                    el.style.borderRight = 'none';
                }
            }
            
            // Start when visible
            const observer = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    type();
                    observer.disconnect();
                }
            });
            observer.observe(el);
        });
    }

    // ===== PARALLAX EFFECT =====
    function initParallaxEffect() {
        const parallaxElements = document.querySelectorAll('[data-parallax], .hero-bg');
        
        window.addEventListener('scroll', () => {
            parallaxElements.forEach(el => {
                const speed = parseFloat(el.dataset.parallax) || 0.5;
                const yPos = -(window.scrollY * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // ===== CARD TILT EFFECT =====
    function initCardTilt() {
        if (window.matchMedia('(pointer: coarse)').matches) return;

        document.querySelectorAll('.card-3d, [data-tilt]').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // ===== PROGRESS BARS =====
    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar, .progress-bar-modern');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.dataset.width || bar.style.width || '0%';
                    bar.style.width = '0%';
                    
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 200);
                    
                    observer.unobserve(bar);
                }
            });
        });

        progressBars.forEach(bar => observer.observe(bar));
    }

    // ===== ACCORDION ANIMATION =====
    function initAccordionAnimation() {
        document.querySelectorAll('.accordion').forEach(accordion => {
            accordion.classList.add('accordion-modern');
        });

        document.querySelectorAll('.accordion-button').forEach(button => {
            button.addEventListener('click', function() {
                const content = this.nextElementSibling;
                if (content) {
                    content.style.maxHeight = content.classList.contains('show') ? 
                        '0' : content.scrollHeight + 'px';
                }
            });
        });
    }

    // ===== GALLERY LIGHTBOX =====
    function initGalleryLightbox() {
        document.querySelectorAll('.gallery-item, .gallery-item-modern').forEach(item => {
            item.addEventListener('click', function() {
                const img = this.querySelector('img');
                if (!img) return;
                
                const lightbox = document.createElement('div');
                lightbox.className = 'lightbox-overlay';
                lightbox.innerHTML = `
                    <div class="lightbox-content">
                        <button class="lightbox-close">&times;</button>
                        <img src="${img.src}" alt="${img.alt}">
                    </div>
                `;
                
                lightbox.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.9);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                
                const content = lightbox.querySelector('.lightbox-content');
                content.style.cssText = `
                    max-width: 90%;
                    max-height: 90%;
                    position: relative;
                    transform: scale(0.8);
                    transition: transform 0.3s ease;
                `;
                
                const closeBtn = lightbox.querySelector('.lightbox-close');
                closeBtn.style.cssText = `
                    position: absolute;
                    top: -40px;
                    right: 0;
                    background: none;
                    border: none;
                    color: white;
                    font-size: 2rem;
                    cursor: pointer;
                `;
                
                const lightboxImg = lightbox.querySelector('img');
                lightboxImg.style.cssText = `
                    max-width: 100%;
                    max-height: 85vh;
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                `;
                
                document.body.appendChild(lightbox);
                document.body.style.overflow = 'hidden';
                
                setTimeout(() => {
                    lightbox.style.opacity = '1';
                    content.style.transform = 'scale(1)';
                }, 10);
                
                const close = () => {
                    lightbox.style.opacity = '0';
                    content.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        lightbox.remove();
                        document.body.style.overflow = '';
                    }, 300);
                };
                
                lightbox.addEventListener('click', (e) => {
                    if (e.target === lightbox) close();
                });
                closeBtn.addEventListener('click', close);
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') close();
                }, { once: true });
            });
        });
    }

    // ===== DYNAMIC NAV LINKS =====
    function initDynamicNavLinks() {
        const navLinks = document.querySelectorAll('.nav-link');
        const sections = document.querySelectorAll('section[id]');

        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 150;
                if (window.scrollY >= sectionTop) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }

    // ===== WHATSAPP FLOAT =====
    function initWhatsAppFloat() {
        // don't add if another whatsapp float already exists
        if (document.querySelector('.whatsapp-float')) return;

        // If there's a mobile bottom nav (we'll show WA there), avoid adding a floating WA on small screens
        if (window.innerWidth <= 991 && document.querySelector('.mobile-bottom-nav')) return;

        let whatsappBtn = document.querySelector('.fab-whatsapp');
        
        if (!whatsappBtn) {
            whatsappBtn = document.createElement('a');
            whatsappBtn.className = 'fab-modern fab-whatsapp';
            whatsappBtn.href = 'https://wa.me/919997612579?text=Hello! I need help with car service.';
            whatsappBtn.target = '_blank';
            whatsappBtn.innerHTML = '<i class="fab fa-whatsapp"></i>';
            whatsappBtn.setAttribute('aria-label', 'Chat on WhatsApp');
            document.body.appendChild(whatsappBtn);
        }

        // Add bounce animation on scroll
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            if (Math.abs(window.scrollY - lastScroll) > 100) {
                whatsappBtn.style.animation = 'none';
                setTimeout(() => {
                    whatsappBtn.style.animation = '';
                }, 10);
                lastScroll = window.scrollY;
            }
        });
    }

    // ===== SERVICE WORKER HINTS =====
    function initServiceWorkerHints() {
        // Add install prompt for PWA
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button
            const installBtn = document.createElement('button');
            installBtn.className = 'btn btn-warning position-fixed d-none d-lg-block';
            installBtn.style.cssText = 'bottom: 180px; right: 30px; z-index: 998; border-radius: 50px;';
            installBtn.innerHTML = '<i class="fas fa-download me-2"></i>Install App';
            document.body.appendChild(installBtn);
            
            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    if (outcome === 'accepted') {
                        installBtn.remove();
                    }
                    deferredPrompt = null;
                }
            });
        });
    }

    // ===== UTILITY FUNCTIONS =====
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Animate element
    window.animateElement = function(element, animation, duration = 1000) {
        return new Promise(resolve => {
            element.style.animation = `${animation} ${duration}ms ease forwards`;
            setTimeout(() => {
                element.style.animation = '';
                resolve();
            }, duration);
        });
    };

    // Scroll to element
    window.scrollToElement = function(selector, offset = 100) {
        const element = document.querySelector(selector);
        if (element) {
            const top = element.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    };

})();

// ===== ADDITIONAL DYNAMIC EFFECTS =====

// Intersection Observer for lazy animations
const lazyAnimations = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate__animated', 'animate__fadeInUp');
            lazyAnimations.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

// Apply to common elements
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card, .service-card, .stat-card, section').forEach(el => {
        lazyAnimations.observe(el);
    });
});

// Dynamic time display
function updateDynamicTime() {
    const timeElements = document.querySelectorAll('[data-dynamic-time]');
    const now = new Date();
    
    timeElements.forEach(el => {
        el.textContent = now.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        });
    });
}

setInterval(updateDynamicTime, 1000);

// Easter egg - Konami code
let konamiCode = [];
const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        document.body.style.animation = 'rainbow 2s linear infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
    }
});

// Add rainbow animation style
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(style);
