const searchInput = document.getElementById('live-search');
const resultsBox = document.getElementById('live-results');
let debounceTimer;

searchInput.addEventListener('input', () => {
  clearTimeout(debounceTimer);
  const query = searchInput.value.trim();

  if (query.length < 2) {
    resultsBox.classList.add('hidden');
    resultsBox.innerHTML = '';
    return;
  }

  debounceTimer = setTimeout(() => {
    fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => {
        if (!data.results?.length) {
          resultsBox.innerHTML = '<p style="text-align:center;color:#777;">نتیجه‌ای یافت نشد.</p>';
          resultsBox.classList.remove('hidden');
          return;
        }

        const grouped = data.results.reduce((acc, item) => {
          if (!acc[item.type]) acc[item.type] = [];
          acc[item.type].push(item);
          return acc;
        }, {});

        resultsBox.innerHTML = Object.keys(grouped)
          .map(type => {
            const sectionItems = grouped[type]
              .map(
                item => `
                  <div class="item">
                    ${item.image ? `<img src="${item.image}" alt="${item.title}">` : ""}
                    <a href="${item.url}">${item.title}</a>
                  </div>
                `
              )
              .join('');

            return `
              <div class="result-section">
                <h4 class="result-title">${type}</h4>
                ${sectionItems}
              </div>
            `;
          })
          .join('');

        resultsBox.classList.remove('hidden');
      })
      .catch(err => {
        console.error("Search error:", err);
        resultsBox.innerHTML = '<p style="text-align:center;color:#e00;">خطا در جست‌وجو.</p>';
        resultsBox.classList.remove('hidden');
      });
  }, 300);
});

document.addEventListener('click', e => {
  if (!e.target.closest('.search-form') && !e.target.closest('#live-results')) {
    resultsBox.classList.add('hidden');
  }
});

const mobileSearchBtn = document.getElementById('mobile-search-btn');
const searchForm = document.querySelector('.search-form');
const searchInputMobile = document.getElementById('live-search');

if (mobileSearchBtn && searchForm) {
  mobileSearchBtn.addEventListener('click', () => {
    searchForm.classList.toggle('mobile-active');
    if (searchForm.classList.contains('mobile-active')) {
      searchInputMobile.focus();
    }
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      searchForm.classList.remove('mobile-active');
    }
  });
}
