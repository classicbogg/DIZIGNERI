    const word = document.getElementById('word');
    const wordFit = document.getElementById('wordFit');
    const wordStage = document.querySelector('.word-stage');
    const text = 'DIZIGNERI';

    word.innerHTML = text
      .split('')
      .map((char, index) => {
        const lift = (8 + ((index * 2) % 6)).toFixed(1);
        const tilt = (((index % 3) - 1) * 1.4).toFixed(2);
        return `<span class="letter" data-index="${index}" style="--lift:${lift}px; --tilt:${tilt}deg;">${char}</span>`;
      })
      .join('');

    function fitWord() {
      document.documentElement.style.setProperty('--word-fit-scale', '1');

      requestAnimationFrame(() => {
        const maxWidth = Math.min(window.innerWidth * 0.92, 1580);
        const maxHeight = window.innerHeight * 0.24;
        const naturalWidth = wordFit.offsetWidth;
        const naturalHeight = wordFit.offsetHeight;

        const scale = Math.min(
          1,
          maxWidth / Math.max(naturalWidth, 1),
          maxHeight / Math.max(naturalHeight, 1)
        );

        document.documentElement.style.setProperty('--word-fit-scale', scale.toFixed(4));
      });
    }

    const letters = Array.from(document.querySelectorAll('.letter'));
    let lastIndex = -1;

    function triggerBounce() {
      let index = Math.floor(Math.random() * letters.length);
      if (index === lastIndex) {
        index = (index + 1 + Math.floor(Math.random() * (letters.length - 1))) % letters.length;
      }
      lastIndex = index;

      const indices = [index];
      if (Math.random() < 0.22) {
        const neighbor = Math.max(0, Math.min(letters.length - 1, index + (Math.random() > 0.5 ? 1 : -1)));
        if (!indices.includes(neighbor)) indices.push(neighbor);
      }

      indices.forEach((i) => {
        const el = letters[i];
        el.classList.remove('jump');
        void el.offsetWidth;
        el.classList.add('jump');
      });

      const delay = 450 + Math.random() * 1200;
      setTimeout(triggerBounce, delay);
    }

    function initScene() {
      fitWord();
      triggerBounce();
    }

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(initScene);
    } else {
      initScene();
    }

    window.addEventListener('resize', fitWord);

    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      document.body.style.setProperty('--mx', x + '%');
      document.body.style.setProperty('--my', y + '%');
    });
