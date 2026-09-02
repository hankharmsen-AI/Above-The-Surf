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

    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if(navLinks.style.display === 'flex') {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = 0;
                navLinks.style.width = '100%';
                navLinks.style.background = 'var(--bg-main)';
                navLinks.style.padding = '20px';
            }
        });
    }

    // Toggle logic for Properties page
    const mapFilters = document.querySelectorAll('.map-filter');
    if (mapFilters.length > 0) {
        mapFilters.forEach(btn => {
            btn.addEventListener('click', function() {
                mapFilters.forEach(b => {
                    b.classList.remove('active-toggle');
                    b.classList.add('inactive-toggle');
                    b.style.background = '';
                    b.style.color = '';
                });
                
                this.classList.remove('inactive-toggle');
                this.classList.add('active-toggle');
            });
        });
    }

    // 6-Second Interval Crossfade Logic
    const video1 = document.getElementById('bg-video-1');
    const video2 = document.getElementById('bg-video-2');
    
    if (video1 && video2) {
        const playlist = [
            'Surf videos/13007362_1280_720_25fps.mp4',
            'Surf videos/7193316_compressed.mp4',
            'Surf videos/11901578_compressed.mp4',
            'Surf videos/16243013_compressed.mp4'
        ];
        
        let currentIndex = 0;
        let activeVideo = 1;
        
        // Ensure both are muted and loop is true for safety
        video1.muted = true;
        video2.muted = true;
        video1.loop = true;
        video2.loop = true;
        
        // Preload the second video
        video1.src = playlist[0];
        video1.play().catch(e=>console.log(e));
        video2.src = playlist[1];
        video2.load();
        
        // Error handling for robust fallback
        video1.onerror = () => {
            console.log("Video 1 failed to load, skipping to next.");
            currentIndex = (currentIndex + 1) % playlist.length;
            video1.src = playlist[currentIndex];
        };
        video2.onerror = () => {
            console.log("Video 2 failed to load, skipping to next.");
            const nextNextIndex = (currentIndex + 1) % playlist.length;
            video2.src = playlist[nextNextIndex];
        };
        
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
        }, 6000);
    }
    
    // Global Search Logic
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    const searchSelect = document.querySelector('.search-select select');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            const loc = searchInput ? searchInput.value.trim() : '';
            const typeVal = searchSelect ? searchSelect.value : '';
            
            let query = '?';
            if (loc) query += 'loc=' + encodeURIComponent(loc) + '&';
            if (typeVal) query += 'type=' + encodeURIComponent(typeVal);
            
            // Redirect to properties page with filters
            window.location.href = 'properties.html' + query;
        });
    }

    
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && searchBtn) {
                e.preventDefault();
                searchBtn.click();
            }
        });
    }

    // Filter properties on load if query params exist
    if (window.location.pathname.includes('properties.html') || window.location.pathname.endsWith('/')) {
        const urlParams = new URLSearchParams(window.location.search);
        const locFilter = urlParams.get('loc') ? urlParams.get('loc').toLowerCase() : '';
        const typeFilter = urlParams.get('type') ? urlParams.get('type').toLowerCase() : '';
        
        if (locFilter || typeFilter) {
            const cards = document.querySelectorAll('.property-card');
            cards.forEach(card => {
                let show = true;
                
                if (locFilter) {
                    const locText = card.querySelector('.property-location');
                    const titleText = card.querySelector('.property-title');
                    const combined = ((locText ? locText.textContent : '') + ' ' + (titleText ? titleText.textContent : '')).toLowerCase();
                    if (!combined.includes(locFilter)) {
                        show = false;
                    }
                }
                
                if (typeFilter) {
                    const badge = card.querySelector('.badge');
                    const badgeText = badge ? badge.textContent.toLowerCase().replace(/ /g, '-') : '';
                    if (!badgeText.includes(typeFilter)) {
                        show = false;
                    }
                }
                
                if (!show) {
                    card.style.display = 'none';
                }
            });
        }
    }
});
