    const word = document.getElementById('word');
    const titleFit = document.getElementById('titleFit');
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
        const maxWidth = Math.min(window.innerWidth * 0.92, 1400);
        const maxHeight = Math.min(window.innerHeight * 0.18, 200);
        const naturalWidth = titleFit.offsetWidth;
        const naturalHeight = titleFit.offsetHeight;

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

    const captainInputs = Array.from(document.querySelectorAll('input[name="captain_index"]'));
    const participantCards = Array.from(document.querySelectorAll('.participant-card'));

    function syncCaptainState() {
      participantCards.forEach((card, index) => {
        const input = captainInputs[index];
        card.classList.toggle('captain-card', Boolean(input && input.checked));
      });
    }

    captainInputs.forEach((input) => {
      input.addEventListener('change', syncCaptainState);
    });

    const form = document.getElementById('registrationForm');
    const status = document.getElementById('formStatus');
    const successModal = document.getElementById('successModal');
    const successClose = document.getElementById('successClose');

    function openSuccessModal() {
      successModal.classList.add('is-open');
      successModal.setAttribute('aria-hidden', 'false');
      successClose.focus();
    }

    function closeSuccessModal() {
      successModal.classList.remove('is-open');
      successModal.setAttribute('aria-hidden', 'true');
    }

    successClose.addEventListener('click', closeSuccessModal);

    successModal.addEventListener('click', (event) => {
      if (event.target === successModal) {
        closeSuccessModal();
      }
    });

    window.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && successModal.classList.contains('is-open')) {
        closeSuccessModal();
      }
    });

    form.addEventListener('submit', (event) => {
      event.preventDefault();

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      const formData = new FormData(form);
      const members = [];
      for (let i = 0; i < 5; i += 1) {
        members.push({
          name: formData.get(`members[${i}][name]`) || '',
          is_captain: String(i + 1) === String(formData.get('captain_index')),
        });
      }

      const payload = {
        team_name: formData.get('team_name'),
        course: formData.get('course'),
        members,
      };

      fetch(form.action, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then(async (response) => {
          const data = await response.json().catch(() => ({}));
          if (!response.ok) {
            throw new Error(data.detail || 'Ошибка отправки заявки.');
          }
          if (status) {
            status.textContent = data.detail || 'Заявка успешно отправлена.';
          }
          form.reset();
          syncCaptainState();
          openSuccessModal();
        })
        .catch((error) => {
          if (status) {
            status.textContent = error.message;
          }
        });
    });

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => {
        fitWord();
        triggerBounce();
      });
    } else {
      fitWord();
      triggerBounce();
    }

    syncCaptainState();

    window.addEventListener('resize', fitWord);

    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      document.body.style.setProperty('--mx', x + '%');
      document.body.style.setProperty('--my', y + '%');
    });
