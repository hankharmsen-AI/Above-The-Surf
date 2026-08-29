// Simple JS functionality for Above the Surf

document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            const currentStyle = window.getComputedStyle(navLinks).display;
            if (currentStyle === 'none') {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.background = 'var(--bg-card)';
                navLinks.style.padding = '20px';
                navLinks.style.boxShadow = 'var(--shadow-lg)';
            } else {
                navLinks.style.display = '';
            }
        });
    }

    // Theme Toggle Logic
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '<i class="fas fa-sun"></i> Light Theme';
    toggleBtn.style.position = 'fixed';
    toggleBtn.style.bottom = '20px';
    toggleBtn.style.left = '20px';
    toggleBtn.style.zIndex = '9999';
    toggleBtn.style.padding = '12px 20px';
    toggleBtn.style.background = '#0ea5e9';
    toggleBtn.style.color = '#fff';
    toggleBtn.style.border = 'none';
    toggleBtn.style.borderRadius = '50px';
    toggleBtn.style.cursor = 'pointer';
    toggleBtn.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
    toggleBtn.style.fontFamily = "'Montserrat', sans-serif";
    toggleBtn.style.fontWeight = '600';
    toggleBtn.style.display = 'flex';
    toggleBtn.style.alignItems = 'center';
    toggleBtn.style.gap = '8px';

    document.body.appendChild(toggleBtn);

    const styleSheet = document.querySelector('link[href*="style.css"]') || document.querySelector('link[href*="style-light.css"]');
    let isLight = localStorage.getItem('theme') === 'light';

    function updateTheme() {
        if (!styleSheet) return;
        if (isLight) {
            styleSheet.setAttribute('href', styleSheet.getAttribute('href').replace('style.css', 'style-light.css'));
            toggleBtn.innerHTML = '<i class="fas fa-moon"></i> Dark Theme';
            toggleBtn.style.background = '#1e293b';
        } else {
            styleSheet.setAttribute('href', styleSheet.getAttribute('href').replace('style-light.css', 'style.css'));
            toggleBtn.innerHTML = '<i class="fas fa-sun"></i> Light Theme';
            toggleBtn.style.background = '#0ea5e9';
        }
    }

    // Initialize
    if (isLight) updateTheme();

    toggleBtn.addEventListener('click', () => {
        isLight = !isLight;
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        updateTheme();
    });
});


                    // 6-Second Interval Crossfade Logic
    const video1 = document.getElementById('bg-video-1');
    const video2 = document.getElementById('bg-video-2');
    
    if (video1 && video2) {
        const playlist = [
            'Surf videos/7193316-hd_1920_1080_24fps.mp4',
            'Surf videos/16243013_3840_2160_60fps.mp4',
            'Surf videos/11901578_1920_1080_30fps.mp4',
            'Surf videos/6981356-hd_1920_1080_25fps.mp4',
            'Surf videos/13007362_1280_720_25fps.mp4'
        ];
        
        let currentIndex = 0;
        let activeVideo = 1;
        
        // Ensure both are muted and loop is true for safety
        video1.muted = true;
        video2.muted = true;
        video1.loop = true;
        video2.loop = true;
        
        // Preload the second video
        video2.src = playlist[1];
        video2.load();
        
        setInterval(() => {
            const currentVid = activeVideo === 1 ? video1 : video2;
            const nextVid = activeVideo === 1 ? video2 : video1;
            
            // Ensure next video starts from beginning
            nextVid.currentTime = 0;
            nextVid.play().then(() => {
                // Crossfade
                nextVid.style.opacity = 1;
                currentVid.style.opacity = 0;
                
                activeVideo = activeVideo === 1 ? 2 : 1;
                
                // After crossfade completes (1s), prep the hidden video
                setTimeout(() => {
                    currentVid.pause();
                    
                    currentIndex = (currentIndex + 1) % playlist.length;
                    const nextNextIndex = (currentIndex + 1) % playlist.length;
                    
                    currentVid.src = playlist[nextNextIndex];
                    currentVid.load();
                }, 1200);
            }).catch(err => {
                console.log('Autoplay error:', err);
            });
            
        }, 6000); // Trigger transition every 6 seconds exactly
    }

