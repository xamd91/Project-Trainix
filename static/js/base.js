window.addEventListener('scroll', () => {
          document.querySelector('.site-header').classList.toggle('shrink', window.scrollY > 50);
        });

        const toggle = document.querySelector('.menu-toggle');
        const nav = document.querySelector('.nav-links');
        toggle.addEventListener('click', () => {
          nav.classList.toggle('active');
          toggle.textContent = nav.classList.contains('active') ? '✕' : '☰';
        });

        document.addEventListener('click', (e) => {
            if (!nav.contains(e.target) && !toggle.contains(e.target)) {
                nav.classList.remove('active');
                toggle.textContent = '☰';
            }
        });

        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                toggle.textContent = '☰';
            });
        });