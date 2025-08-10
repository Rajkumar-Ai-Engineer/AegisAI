// Mouse cursor animation
const cursor = document.createElement('div');
cursor.className = 'cursor-follower';
document.body.appendChild(cursor);

// Mouse movement animation
document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
    
    // Add ripple effect when near interactive elements
    const interactiveElements = document.querySelectorAll('button, a, input');
    let isNearInteractive = false;
    
    interactiveElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const distance = Math.hypot(
            e.clientX - (rect.left + rect.width/2),
            e.clientY - (rect.top + rect.height/2)
        );
        
        if (distance < 100) {
            isNearInteractive = true;
            cursor.classList.add('active');
            el.style.transform = 'scale(1.05)';
            el.style.transition = 'transform 0.3s ease';
        } else {
            el.style.transform = 'scale(1)';
        }
    });
    
    if (!isNearInteractive) {
        cursor.classList.remove('active');
    }
});

// Handle mouse enter/leave
document.addEventListener('mouseenter', () => {
    cursor.style.opacity = '1';
});

document.addEventListener('mouseleave', () => {
    cursor.style.opacity = '0';
});
