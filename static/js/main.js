// ── FONT SIZE CONTROL ────────────────────────────────────────────
function changeFontSize(action) {
    const body = document.body
    const currentSize = parseFloat(window.getComputedStyle(body).fontSize)

    if (action === 'increase' && currentSize < 24) {
        body.style.fontSize = (currentSize + 2) + 'px'
    } else if (action === 'decrease' && currentSize > 12) {
        body.style.fontSize = (currentSize - 2) + 'px'
    }
}


// ── HIGH CONTRAST TOGGLE ─────────────────────────────────────────
function toggleContrast() {
    document.body.classList.toggle('high-contrast')
    const isHighContrast = document.body.classList.contains('high-contrast')
    localStorage.setItem('highContrast', isHighContrast)
}


// ── LOAD SAVED PREFERENCES ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

    // Restore high contrast
    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast')
    }

    // Setup loading spinner on all country links
    setupLoadingSpinner()
})


// ── LOADING SPINNER SETUP ────────────────────────────────────────
function setupLoadingSpinner() {
    const overlay = document.getElementById('loading-overlay')
    if (!overlay) return

    // Find all links that go to a country page
    const countryLinks = document.querySelectorAll('a[href*="/country/"]')

    countryLinks.forEach(link => {
        link.addEventListener('click', function (e) {

            // Get country name from the card
            const countryName = this.getAttribute('aria-label')
                ?.replace('Read news from ', '')
                || 'selected country'

            // Update loading text
            const loadingText = overlay.querySelector('.loading-text')
            const loadingSub = overlay.querySelector('.loading-subtext')

            if (loadingText) {
                loadingText.textContent = `Fetching ${countryName} news...`
            }
            if (loadingSub) {
                loadingSub.textContent = 'Getting the latest stories for you'
            }

            // Show the loading overlay
            showLoading()
        })
    })

    // Also setup continent links
    const continentLinks = document.querySelectorAll('a[href*="/continent/"]')
    continentLinks.forEach(link => {
        link.addEventListener('click', function () {
            const loadingText = overlay.querySelector('.loading-text')
            if (loadingText) {
                loadingText.textContent = 'Loading continent...'
            }
            showLoading()
        })
    })
}


// ── SHOW LOADING ─────────────────────────────────────────────────
function showLoading() {
    const overlay = document.getElementById('loading-overlay')
    if (overlay) {
        overlay.classList.remove('d-none')
        // Announce to screen readers
        overlay.setAttribute('aria-hidden', 'false')
    }
}


// ── HIDE LOADING ─────────────────────────────────────────────────
function hideLoading() {
    const overlay = document.getElementById('loading-overlay')
    if (overlay) {
        overlay.classList.add('d-none')
        overlay.setAttribute('aria-hidden', 'true')
    }
}


// ── HIDE SPINNER WHEN PAGE IS FULLY LOADED ───────────────────────
window.addEventListener('load', function () {
    hideLoading()
})

// Also hide if user presses back button
window.addEventListener('pageshow', function () {
    hideLoading()
})


// ── TEXT TO SPEECH ───────────────────────────────────────────────
function readAloud(text, lang = 'en') {
    window.speechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = lang
    utterance.rate = 1
    utterance.pitch = 1

    window.speechSynthesis.speak(utterance)
}

function stopReading() {
    window.speechSynthesis.cancel()
}