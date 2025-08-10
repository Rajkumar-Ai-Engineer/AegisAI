document.addEventListener('DOMContentLoaded', () => {
    
    const smokeContainer = document.createElement('div');
    smokeContainer.className = 'smoke-cursor';
    document.body.appendChild(smokeContainer);

    // Function to create smoke particles
    function createSmokeParticle(x, y) {
        for (let i = 0; i < 3; i++) { // Create three particles at once for more effect
            const particle = document.createElement('div');
            particle.className = 'smoke-particle';
            
            // Add slight offset to particles
            const offsetX = (Math.random() - 0.5) * 25;
            const offsetY = (Math.random() - 0.5) * 25;
            
            particle.style.left = (x + offsetX) + 'px';
            particle.style.top = (y + offsetY) + 'px';
            
            // Random starting hue with offset for each particle
            particle.style.setProperty('--hue', (Math.random() * 360) + (i * 120));
            
            // Random movement direction
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 100 + 50; // Increased spread
            const moveX = Math.cos(angle) * distance;
            const moveY = Math.sin(angle) * distance;
            
            particle.style.setProperty('--move-x', `${moveX}px`);
            particle.style.setProperty('--move-y', `${moveY}px`);
            
            smokeContainer.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                particle.remove();
            }, 1500);
        }
    }

    // Throttle function to limit particle creation
    let lastParticleTime = 0;
    function throttledCreateParticle(x, y) {
        const now = Date.now();
        if (now - lastParticleTime > 50) { // Create particle every 50ms
            createSmokeParticle(x, y);
            lastParticleTime = now;
        }
    }

    // Mouse movement animation
    document.addEventListener('mousemove', (e) => {
        throttledCreateParticle(e.clientX, e.clientY);
        
        // Add hover effect for interactive elements
        const interactiveElements = document.querySelectorAll('button, a, input');
        interactiveElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const distance = Math.hypot(
                e.clientX - (rect.left + rect.width/2),
                e.clientY - (rect.top + rect.height/2)
            );
            
            if (distance < 100) {
                el.style.transform = 'scale(1.05)';
                el.style.transition = 'transform 0.3s ease';
                
                // Create more particles near interactive elements
                if (Math.random() > 0.5) {
                    createSmokeParticle(e.clientX, e.clientY);
                }
            } else {
                el.style.transform = 'scale(1)';
            }
        });
    });

    // Handle mouse click for extra particles
    document.addEventListener('click', (e) => {
        // Create a burst of particles on click
        for (let i = 0; i < 8; i++) {
            createSmokeParticle(e.clientX, e.clientY);
        }
    });

    // Form handling
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.parentElement.classList.remove('focused');
            }
        });
    });

    // Form submission handling
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const button = form.querySelector('button');
            const originalText = button.textContent;
            
            button.textContent = 'Loading...';
            button.disabled = true;
            
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
                alert('Success!');
            }, 1500);
        });
    }

    // Add bubble interaction
    const bubbles = document.querySelectorAll('.bubble');
    bubbles.forEach(bubble => {
        bubble.addEventListener('mouseover', () => {
            bubble.style.transform = 'scale(1.5)';
            bubble.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        
        bubble.addEventListener('mouseout', () => {
            bubble.style.transform = 'scale(1)';
            bubble.style.background = 'rgba(255, 255, 255, 0.1)';
        });
    });
});
