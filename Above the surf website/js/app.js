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
    // --- SEARCH LOGIC ---
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    const executeSearch = () => {
        if (!searchInput) return;
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = 'properties.html?q=' + encodeURIComponent(query);
        }
    };

    if (searchBtn) searchBtn.addEventListener('click', executeSearch);
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeSearch();
        });
    }

    // If we are on properties page, filter the cards
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');
    
    if (searchQuery && window.location.pathname.includes('properties.html')) {
        const query = searchQuery.toLowerCase();
        const propertyCards = document.querySelectorAll('.property-card');
        
        // Update header if exists
        const pageHeader = document.querySelector('.page-header h1');
        if (pageHeader) {
            pageHeader.textContent = 'Search Results for "' + searchQuery + '"';
        }
        
        let matchCount = 0;
        propertyCards.forEach(card => {
            const title = card.querySelector('.property-title').textContent.toLowerCase();
            const location = card.querySelector('.property-location').textContent.toLowerCase();
            const country = (card.getAttribute('data-country') || '').toLowerCase();
            
            if (title.includes(query) || location.includes(query) || country.includes(query) || (query === "us" && country === "united states") || (query === "usa" && country === "united states") || (query === "america" && country === "united states")) {
                card.style.display = 'block';
                matchCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        if (matchCount === 0) {
            const grid = document.querySelector('.property-grid');
            if (grid) {
                const noResults = document.createElement('p');
                noResults.textContent = 'No properties found matching "' + searchQuery + '".';
                noResults.style.gridColumn = '1 / -1';
                noResults.style.textAlign = 'center';
                noResults.style.padding = '40px';
                grid.appendChild(noResults);
            }
        }
    }

});

// 6-Second Interval Crossfade Logic
    const video1 = document.getElementById('bg-video-1');
    const video2 = document.getElementById('bg-video-2');
    
    if (video1 && video2) {
        const playlist = [
            'Surf videos/7193316_compressed.mp4',
            'Surf videos/6981356_compressed.mp4',
            'Surf videos/13007362_1280_720_25fps.mp4',
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










