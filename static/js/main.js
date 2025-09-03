// VaultLogic Main JavaScript

(function() {
    'use strict';

    // DOM Ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeApp();
    });

    function initializeApp() {
        initSmoothScrolling();
        initFormValidation();
        initAnimations();
        initNavbarBehavior();
        initTooltips();
        initAccordions();
        initPricingCards();
        initContactForm();
    }

    // Smooth Scrolling for Navigation Links
    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Form Validation
    function initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    // Animation on Scroll
    function initAnimations() {
        const animatedElements = document.querySelectorAll('.feature-card, .testimonial-card, .pricing-card');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        animatedElements.forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(element);
        });
    }

    // Navbar Behavior
    function initNavbarBehavior() {
        const navbar = document.querySelector('.navbar');
        let lastScrollTop = 0;

        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Add shadow when scrolled
            if (scrollTop > 0) {
                navbar.classList.add('shadow');
            } else {
                navbar.classList.remove('shadow');
            }

            lastScrollTop = scrollTop;
        });

        // Mobile menu auto-close
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Initialize Tooltips
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Accordion Behavior
    function initAccordions() {
        const accordionButtons = document.querySelectorAll('.accordion-button');
        
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const icon = this.querySelector('i');
                if (icon) {
                    setTimeout(() => {
                        if (this.classList.contains('collapsed')) {
                            icon.style.transform = 'rotate(0deg)';
                        } else {
                            icon.style.transform = 'rotate(180deg)';
                        }
                    }, 150);
                }
            });
        });
    }

    // Pricing Cards Enhancement
    function initPricingCards() {
        const pricingCards = document.querySelectorAll('.pricing-card');
        
        pricingCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px)';
                this.style.boxShadow = '0 1rem 3rem rgba(0, 0, 0, 0.175)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '';
            });
        });
    }

    // Contact Form Enhancement
    function initContactForm() {
        const contactForm = document.querySelector('#contactForm, form[method="POST"]');
        if (!contactForm) return;

        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton ? submitButton.innerHTML : '';

        contactForm.addEventListener('submit', function(e) {
            if (submitButton && contactForm.checkValidity()) {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
                submitButton.disabled = true;
                
                // Re-enable button after 3 seconds (in case of redirect)
                setTimeout(() => {
                    if (submitButton) {
                        submitButton.innerHTML = originalText;
                        submitButton.disabled = false;
                    }
                }, 3000);
            }
        });

        // Real-time validation feedback
        const inputs = contactForm.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    }

    // Utility Functions
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 1050; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    function showLoading(element) {
        if (element) {
            element.classList.add('loading');
            const spinner = document.createElement('div');
            spinner.className = 'spinner-border spinner-border-sm me-2';
            spinner.setAttribute('role', 'status');
            element.insertBefore(spinner, element.firstChild);
        }
    }

    function hideLoading(element) {
        if (element) {
            element.classList.remove('loading');
            const spinner = element.querySelector('.spinner-border');
            if (spinner) {
                spinner.remove();
            }
        }
    }

    // Predefined Questions Handler (for demo page)
    function initPredefinedQuestions() {
        const predefinedButtons = document.querySelectorAll('.predefined-question');
        
        predefinedButtons.forEach(button => {
            button.addEventListener('click', function() {
                const question = this.getAttribute('data-question');
                const questionInput = document.querySelector('#question');
                
                if (questionInput && question) {
                    questionInput.value = question;
                    
                    // Trigger the chat if chat functionality is available
                    if (typeof window.submitChatQuestion === 'function') {
                        window.submitChatQuestion(question);
                    }
                }
            });
        });
    }

    // Initialize predefined questions if on demo page
    if (window.location.pathname.includes('/demo')) {
        initPredefinedQuestions();
    }

    // Performance Monitoring
    window.addEventListener('load', function() {
        // Log performance metrics (development only)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Performance:', {
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                    totalTime: perfData.loadEventEnd - perfData.navigationStart
                });
            }, 1000);
        }
    });

    // Expose utility functions globally
    window.VaultLogic = {
        showAlert,
        showLoading,
        hideLoading
    };

})();

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    
    // Show user-friendly error message in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        if (window.VaultLogic && window.VaultLogic.showAlert) {
            window.VaultLogic.showAlert('A JavaScript error occurred. Check the console for details.', 'warning');
        }
    }
});

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered:', registration))
        //     .catch(registrationError => console.log('SW registration failed:', registrationError));
    });
}
