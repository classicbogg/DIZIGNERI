    (function () {
      const body = document.body;
      body.classList.add('page-is-entering');

      requestAnimationFrame(() => {
        body.classList.add('page-ready');
        body.classList.remove('page-is-entering');
      });

      document.querySelectorAll('a[href$=".html"]').forEach((link) => {
        link.addEventListener('click', (event) => {
          if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey ||
            link.target === '_blank'
          ) {
            return;
          }

          const href = link.getAttribute('href');
          if (!href || href.startsWith('#')) return;

          event.preventDefault();
          body.classList.add('page-leaving');

          window.setTimeout(() => {
            window.location.href = href;
          }, 380);
        });
      });
    })();
