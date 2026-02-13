/**
 * GAURAV MOTORS - Premium Dynamic UI JavaScript
 * Clean, Fast & Beautiful with Animations
 */

(function() {
    'use strict';

    // ===== DOM READY =====
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        initPageLoader();
        initNavbarEffects();
        initSmoothScroll();
        initScrollToTop();
        initFormEnhancements();
        initTooltips();
        initWhatsAppFloat();
        initScrollReveal();
        initCounterAnimation();
        initHoverEffects();
    }

    // ===== PAGE LOADER =====
    function initPageLoader() {
        function hideLoader() {
            const pageLoader = document.querySelector('.page-loader');
            if (pageLoader) {
                pageLoader.classList.add('hidden');
                pageLoader.style.opacity = '0';
                pageLoader.style.visibility = 'hidden';
                pageLoader.style.pointerEvents = 'none';
                document.body.style.overflow = '';
            }
        }
        
        // Hide loader on window load
        window.addEventListener('load', () => {
            setTimeout(hideLoader, 200);
        });
        
        // Fallback: hide after 2 seconds
        setTimeout(hideLoader, 2000);
        
        // Immediate hide if already loaded
        if (document.readyState === 'complete') {
            hideLoader();
        }
    }

    // ===== PREMIUM NAVBAR EFFECTS =====
    function initNavbarEffects() {
        const navbar = document.querySelector('.navbar');
        const topBar = document.querySelector('.top-bar-premium');
        if (!navbar) return;

        let lastScroll = 0;
        const scrollThreshold = 80;

        function updateNavbar() {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > scrollThreshold) {
                navbar.classList.add('navbar-scrolled');
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.1)';
                navbar.style.backdropFilter = 'blur(20px)';
                
                // Update nav links color
                navbar.querySelectorAll('.nav-link').forEach(link => {
                    link.style.color = '#1e293b';
                });
                
                // Update brand name color
                const brandName = navbar.querySelector('.brand-name');
                if (brandName) {
                    brandName.style.color = '#1e293b';
                    brandName.style.textShadow = 'none';
                }
                
                // Hide top bar smoothly
                if (topBar) {
                    topBar.style.transform = 'translateY(-100%)';
                    topBar.style.opacity = '0';
                }
            } else {
                navbar.classList.remove('navbar-scrolled');
                navbar.style.background = 'linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%)';
                navbar.style.boxShadow = '0 4px 30px rgba(13,110,253,0.3)';
                navbar.style.backdropFilter = 'none';
                
                // Reset nav links color
                navbar.querySelectorAll('.nav-link').forEach(link => {
                    link.style.color = '#fff';
                });
                
                // Reset brand name color
                const brandName = navbar.querySelector('.brand-name');
                if (brandName) {
                    brandName.style.color = '#fff';
                    brandName.style.textShadow = '2px 2px 8px rgba(0,0,0,0.3)';
                }
                
                // Show top bar
                if (topBar) {
                    topBar.style.transform = 'translateY(0)';
                    topBar.style.opacity = '1';
                }
            }
            
            lastScroll = currentScroll;
        }

        // Add transition to topBar
        if (topBar) {
            topBar.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        }
        navbar.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';

        window.addEventListener('scroll', updateNavbar, { passive: true });
        updateNavbar(); // Initial call
    }

    // ===== SCROLL REVEAL ANIMATION =====
    function initScrollReveal() {
        const revealElements = document.querySelectorAll('.reveal, [data-reveal]');
        
        if (revealElements.length === 0) {
            // Auto-add reveal to common elements
            const autoRevealSelectors = [
                'section > .container > .row > div',
                '.stat-card',
                '.feature-card',
                '.service-card',
                '.card'
            ];
            
            autoRevealSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((el, index) => {
                    if (!el.classList.contains('reveal')) {
                        el.classList.add('reveal');
                        el.style.animationDelay = `${index * 0.1}s`;
                    }
                });
            });
        }

        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -50px 0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.reveal').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(el);
        });
    }

    // ===== COUNTER ANIMATION =====
    function initCounterAnimation() {
        const counters = document.querySelectorAll('[data-counter], .counter-value');
        
        counters.forEach(counter => {
            const target = parseInt(counter.textContent.replace(/[^0-9]/g, ''));
            const suffix = counter.textContent.replace(/[0-9]/g, '');
            
            if (isNaN(target)) return;
            
            const observerOptions = {
                threshold: 0.5
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(counter, target, suffix);
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            observer.observe(counter);
        });
    }

    function animateCounter(element, target, suffix) {
        let current = 0;
        const increment = target / 50;
        const duration = 2000;
        const stepTime = duration / 50;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, stepTime);
    }

    // ===== HOVER EFFECTS =====
    function initHoverEffects() {
        // Add hover glow to buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px)';
            });
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        // Add tilt effect to cards
        document.querySelectorAll('.feature-card, .stat-card, .service-card').forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                
                this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
            });
        });
    }

    // ===== SMOOTH SCROLL =====
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const target = document.querySelector(targetId);
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

    // ===== SCROLL TO TOP BUTTON =====
    function initScrollToTop() {
        const scrollTopBtn = document.createElement('button');
        scrollTopBtn.className = 'scroll-top-btn';
        scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
        scrollTopBtn.style.cssText = `
            position: fixed;
            bottom: 90px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0d6efd, #0a58ca);
            color: white;
            border: none;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 999;
            box-shadow: 0 4px 15px rgba(13, 110, 253, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        `;
        document.body.appendChild(scrollTopBtn);

        // Show/hide based on scroll
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.style.opacity = '1';
                scrollTopBtn.style.visibility = 'visible';
            } else {
                scrollTopBtn.style.opacity = '0';
                scrollTopBtn.style.visibility = 'hidden';
            }
        }, { passive: true });

        // Scroll to top on click
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ===== FORM ENHANCEMENTS =====
    function initFormEnhancements() {
        // Floating labels
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
            
            // Check initial state
            if (input.value) {
                input.parentElement.classList.add('focused');
            }
        });
    }

    // ===== TOOLTIPS (Bootstrap) =====
    function initTooltips() {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.forEach(function(tooltipTriggerEl) {
                new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    // ===== WHATSAPP FLOAT BUTTON =====
    function initWhatsAppFloat() {
        // Check if already exists
        if (document.querySelector('.whatsapp-float')) return;

        const whatsappBtn = document.createElement('a');
        whatsappBtn.className = 'whatsapp-float';
        whatsappBtn.href = 'https://wa.me/919997612579?text=Hi%20Gaurav%20Motors!';
        whatsappBtn.target = '_blank';
        whatsappBtn.innerHTML = '<i class="fab fa-whatsapp"></i>';
        whatsappBtn.setAttribute('aria-label', 'Chat on WhatsApp');
        whatsappBtn.style.cssText = `
            position: fixed;
            bottom: 25px;
            right: 30px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #25d366, #128c7e);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            text-decoration: none;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
            transition: transform 0.3s ease;
        `;
        
        whatsappBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        whatsappBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        document.body.appendChild(whatsappBtn);
    }

})();
