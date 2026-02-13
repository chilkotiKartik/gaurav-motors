/**
 * GAURAV MOTORS - Clean UI JavaScript
 * Minimal, fast, no gimmicks
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', init);

    function init() {
        hidePageLoader();
        initNavbar();
        initSmoothScroll();
        initScrollToTop();
        initTooltips();
        initWhatsAppFloat();
        initScrollReveal();
        initCounters();
        forceWhiteInputs();
    }

    // ===== PAGE LOADER =====
    function hidePageLoader() {
        function hide() {
            var loader = document.querySelector('.page-loader');
            if (loader) {
                loader.classList.add('hidden');
                loader.style.opacity = '0';
                loader.style.visibility = 'hidden';
                loader.style.pointerEvents = 'none';
                document.body.style.overflow = '';
            }
        }
        
        window.addEventListener('load', function() {
            setTimeout(hide, 150);
        });
        
        setTimeout(hide, 1500);
        
        if (document.readyState === 'complete') hide();
    }

    // ===== FORCE WHITE INPUTS (for dark mode users) =====
    function forceWhiteInputs() {
        var inputs = document.querySelectorAll('input, textarea, select, .form-control, .form-select');
        inputs.forEach(function(el) {
            el.style.backgroundColor = '#ffffff';
            el.style.color = '#334155';
        });

        // Also apply on any dynamically added inputs
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(m) {
                m.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) {
                        var newInputs = node.querySelectorAll ? node.querySelectorAll('input, textarea, select, .form-control, .form-select') : [];
                        newInputs.forEach(function(el) {
                            el.style.backgroundColor = '#ffffff';
                            el.style.color = '#334155';
                        });
                        if (node.matches && node.matches('input, textarea, select, .form-control, .form-select')) {
                            node.style.backgroundColor = '#ffffff';
                            node.style.color = '#334155';
                        }
                    }
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }

    // ===== NAVBAR =====
    function initNavbar() {
        var navbar = document.querySelector('.navbar');
        var topBar = document.querySelector('.top-bar-premium');
        if (!navbar) return;

        if (topBar) {
            topBar.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        }
        navbar.style.transition = 'background 0.3s ease, box-shadow 0.3s ease';

        function update() {
            var scrollY = window.pageYOffset;
            
            if (scrollY > 60) {
                navbar.classList.add('navbar-scrolled');
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 2px 12px rgba(0,0,0,0.06)';
                navbar.style.backdropFilter = 'blur(12px)';
                
                navbar.querySelectorAll('.nav-link').forEach(function(link) {
                    link.style.color = '#334155';
                });
                
                var brandName = navbar.querySelector('.brand-name');
                if (brandName) {
                    brandName.style.color = '#1e293b';
                    brandName.style.textShadow = 'none';
                }
                
                if (topBar) {
                    topBar.style.transform = 'translateY(-100%)';
                    topBar.style.opacity = '0';
                }
            } else {
                navbar.classList.remove('navbar-scrolled');
                navbar.style.background = '#2563eb';
                navbar.style.boxShadow = '0 2px 12px rgba(37,99,235,0.15)';
                navbar.style.backdropFilter = 'none';
                
                navbar.querySelectorAll('.nav-link').forEach(function(link) {
                    link.style.color = '#fff';
                });
                
                var brandName = navbar.querySelector('.brand-name');
                if (brandName) {
                    brandName.style.color = '#fff';
                    brandName.style.textShadow = '1px 1px 4px rgba(0,0,0,0.15)';
                }
                
                if (topBar) {
                    topBar.style.transform = 'translateY(0)';
                    topBar.style.opacity = '1';
                }
            }
        }

        window.addEventListener('scroll', update, { passive: true });
        update();
    }

    // ===== SCROLL REVEAL =====
    function initScrollReveal() {
        var elements = document.querySelectorAll('.reveal, [data-reveal]');
        
        if (elements.length === 0) {
            // Auto-add to common elements
            ['.stat-card', '.feature-card', '.service-card'].forEach(function(sel) {
                document.querySelectorAll(sel).forEach(function(el, i) {
                    if (!el.classList.contains('reveal')) {
                        el.classList.add('reveal');
                    }
                });
            });
        }

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            rootMargin: '0px 0px -30px 0px',
            threshold: 0.1
        });

        document.querySelectorAll('.reveal').forEach(function(el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(16px)';
            el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            observer.observe(el);
        });
    }

    // ===== COUNTER ANIMATION =====
    function initCounters() {
        var counters = document.querySelectorAll('[data-counter], .counter-value');
        
        counters.forEach(function(counter) {
            var target = parseInt(counter.textContent.replace(/[^0-9]/g, ''));
            var suffix = counter.textContent.replace(/[0-9]/g, '');
            if (isNaN(target)) return;
            
            var observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        animateCount(counter, target, suffix);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(counter);
        });
    }

    function animateCount(el, target, suffix) {
        var current = 0;
        var step = target / 40;
        var interval = setInterval(function() {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            el.textContent = Math.floor(current) + suffix;
        }, 40);
    }

    // ===== SMOOTH SCROLL =====
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                var id = this.getAttribute('href');
                if (id === '#') return;
                var target = document.querySelector(id);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    // ===== SCROLL TO TOP =====
    function initScrollToTop() {
        var btn = document.createElement('button');
        btn.className = 'scroll-top-btn';
        btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        btn.setAttribute('aria-label', 'Scroll to top');
        btn.style.cssText = 'position:fixed;bottom:90px;right:25px;width:44px;height:44px;border-radius:50%;background:#2563eb;color:white;border:none;cursor:pointer;opacity:0;visibility:hidden;transition:all 0.2s ease;z-index:999;box-shadow:0 2px 8px rgba(37,99,235,0.2);display:flex;align-items:center;justify-content:center;font-size:1rem;';
        document.body.appendChild(btn);

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                btn.style.opacity = '1';
                btn.style.visibility = 'visible';
            } else {
                btn.style.opacity = '0';
                btn.style.visibility = 'hidden';
            }
        }, { passive: true });

        btn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ===== TOOLTIPS =====
    function initTooltips() {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).forEach(function(el) {
                new bootstrap.Tooltip(el);
            });
        }
    }

    // ===== WHATSAPP FLOAT =====
    function initWhatsAppFloat() {
        if (document.querySelector('.whatsapp-float')) return;

        var btn = document.createElement('a');
        btn.className = 'whatsapp-float';
        btn.href = 'https://wa.me/919997612579?text=Hi%20Gaurav%20Motors!';
        btn.target = '_blank';
        btn.innerHTML = '<i class="fab fa-whatsapp"></i>';
        btn.setAttribute('aria-label', 'Chat on WhatsApp');
        btn.style.cssText = 'position:fixed;bottom:20px;right:25px;width:56px;height:56px;border-radius:50%;background:#25d366;color:white;display:flex;align-items:center;justify-content:center;font-size:1.8rem;text-decoration:none;z-index:1000;box-shadow:0 3px 12px rgba(37,211,102,0.3);transition:transform 0.2s ease;';
        
        btn.addEventListener('mouseenter', function() { this.style.transform = 'scale(1.08)'; });
        btn.addEventListener('mouseleave', function() { this.style.transform = 'scale(1)'; });
        
        document.body.appendChild(btn);
    }

})();
