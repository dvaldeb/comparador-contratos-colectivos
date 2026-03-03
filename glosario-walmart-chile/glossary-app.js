// glossary-app.js — Interactive Glossary App Logic
(function() {
    'use strict';

    const searchInput = document.getElementById('search');
    const searchCount = document.getElementById('searchCount');
    const container = document.getElementById('glossaryContainer');
    const noResults = document.getElementById('noResults');
    const filtersContainer = document.getElementById('categoryFilters');
    const totalTermsEl = document.getElementById('totalTerms');

    let activeCategory = 'all';

    // Category colors for cards
    const catColors = {
        cultura:     { bg: 'bg-yellow-50',  border: 'border-yellow-200',  badge: 'bg-yellow-100 text-yellow-800' },
        tienda:      { bg: 'bg-blue-50',    border: 'border-blue-200',    badge: 'bg-blue-100 text-blue-800' },
        inventario:  { bg: 'bg-purple-50',  border: 'border-purple-200',  badge: 'bg-purple-100 text-purple-800' },
        ecommerce:   { bg: 'bg-cyan-50',    border: 'border-cyan-200',    badge: 'bg-cyan-100 text-cyan-800' },
        fulfillment: { bg: 'bg-orange-50',  border: 'border-orange-200',  badge: 'bg-orange-100 text-orange-800' },
        merma:       { bg: 'bg-red-50',     border: 'border-red-200',     badge: 'bg-red-100 text-red-800' },
        tech:        { bg: 'bg-indigo-50',  border: 'border-indigo-200',  badge: 'bg-indigo-100 text-indigo-800' },
        kpi:         { bg: 'bg-green-50',   border: 'border-green-200',   badge: 'bg-green-100 text-green-800' },
        rrhh:        { bg: 'bg-pink-50',    border: 'border-pink-200',    badge: 'bg-pink-100 text-pink-800' },
        finanzas:    { bg: 'bg-amber-50',   border: 'border-amber-200',   badge: 'bg-amber-100 text-amber-800' },
        formatos:    { bg: 'bg-teal-50',    border: 'border-teal-200',    badge: 'bg-teal-100 text-teal-800' },
    };

    function init() {
        totalTermsEl.textContent = GLOSSARY.length;
        renderFilters();
        renderGlossary();
        searchInput.addEventListener('input', debounce(renderGlossary, 200));
    }

    function renderFilters() {
        filtersContainer.innerHTML = '';
        for (const [key, cat] of Object.entries(CATEGORIES)) {
            const btn = document.createElement('button');
            btn.className = `category-btn whitespace-nowrap px-4 py-2 rounded-full text-sm font-medium border transition-colors
                ${key === activeCategory
                    ? 'bg-walmart-blue text-white border-walmart-blue'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-walmart-blue hover:text-walmart-blue'}`;
            btn.setAttribute('role', 'tab');
            btn.setAttribute('aria-selected', key === activeCategory);
            btn.textContent = `${cat.icon} ${cat.label}`;

            const count = key === 'all' ? GLOSSARY.length : GLOSSARY.filter(g => g.cat === key).length;
            const countSpan = document.createElement('span');
            countSpan.className = 'ml-1 text-xs opacity-60';
            countSpan.textContent = `(${count})`;
            btn.appendChild(countSpan);

            btn.addEventListener('click', () => {
                activeCategory = key;
                renderFilters();
                renderGlossary();
            });
            filtersContainer.appendChild(btn);
        }
    }

    function renderGlossary() {
        const query = searchInput.value.trim().toLowerCase();
        let items = GLOSSARY;

        // Filter by category
        if (activeCategory !== 'all') {
            items = items.filter(g => g.cat === activeCategory);
        }

        // Filter by search
        if (query) {
            items = items.filter(g =>
                g.term.toLowerCase().includes(query) ||
                g.full.toLowerCase().includes(query) ||
                g.desc.toLowerCase().includes(query)
            );
        }

        // Sort alphabetically
        items.sort((a, b) => a.term.localeCompare(b.term, 'es'));

        // Update count
        searchCount.textContent = query ? `${items.length} resultados` : '';

        // Render
        if (items.length === 0) {
            container.classList.add('hidden');
            noResults.classList.remove('hidden');
            return;
        }

        container.classList.remove('hidden');
        noResults.classList.add('hidden');
        container.innerHTML = items.map(item => createCard(item, query)).join('');
    }

    function createCard(item, query) {
        const colors = catColors[item.cat] || catColors.cultura;
        const catInfo = CATEGORIES[item.cat] || { label: item.cat, icon: '📌' };
        const termHtml = query ? highlightText(item.term, query) : escapeHtml(item.term);
        const fullHtml = query ? highlightText(item.full, query) : escapeHtml(item.full);
        const descHtml = query ? highlightText(item.desc, query) : escapeHtml(item.desc);

        return `
            <article class="term-card fade-in ${colors.bg} ${colors.border} border rounded-xl p-5">
                <div class="flex items-start justify-between gap-2 mb-2">
                    <h3 class="text-lg font-bold text-gray-900">${termHtml}</h3>
                    <span class="${colors.badge} text-xs px-2 py-1 rounded-full whitespace-nowrap">${catInfo.icon} ${escapeHtml(catInfo.label)}</span>
                </div>
                <p class="text-sm font-medium text-gray-500 mb-2">${fullHtml}</p>
                <p class="text-sm text-gray-700 leading-relaxed">${descHtml}</p>
            </article>
        `;
    }

    function highlightText(text, query) {
        const escaped = escapeHtml(text);
        const escapedQuery = escapeRegExp(query);
        const regex = new RegExp(`(${escapedQuery})`, 'gi');
        return escaped.replace(regex, '<mark class="highlight">$1</mark>');
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function escapeRegExp(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function debounce(fn, ms) {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), ms);
        };
    }

    // Go!
    init();
})();
