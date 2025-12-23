/**
 * Main JavaScript for Blog Website
 */

document.addEventListener('DOMContentLoaded', () => {
    // Add subtle reveal animations for article cards
    const cards = document.querySelectorAll('.article-card');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach((card, index) => {
        // Set initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;

        observer.observe(card);
    });

    // Handle card clicks (make the whole card clickable for detail)
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            // If the user clicked a link or button inside, let that handle it
            if (e.target.closest('a') || e.target.closest('button')) {
                return;
            }

            const readMoreBtn = card.querySelector('.read-more-btn');
            if (readMoreBtn) {
                window.open(readMoreBtn.href, '_blank');
            }
        });
    });

    // Refresh data button (if we want to add one later, this provides the logic)
    const refreshCache = async () => {
        try {
            const response = await fetch('/api/refresh');
            const data = await response.json();
            if (data.success) {
                console.log(`Successfully refreshed ${data.count} articles.`);
                window.location.reload();
            }
        } catch (error) {
            console.error('Failed to refresh cache:', error);
        }
    };

    // Header scroll effect
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            header.style.boxShadow = 'var(--shadow-md)';
            header.style.padding = '4px 0';
        } else {
            header.style.boxShadow = 'none';
            header.style.padding = '0';
        }
    });
});
