// ---- Utility ----
function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---- Saved Jobs (localStorage) ----
function getSavedJobs() {
    return JSON.parse(localStorage.getItem('savedJobs') || '{}');
}

function toggleSaveJob(job) {
    const saved = getSavedJobs();
    if (saved[job.job_id]) {
        delete saved[job.job_id];
    } else {
        saved[job.job_id] = {
            job_id: job.job_id,
            job_title: job.job_title,
            employer_name: job.employer_name,
            job_city: job.job_city,
            job_state: job.job_state,
            job_employment_type: job.job_employment_type,
            job_is_remote: job.job_is_remote,
            job_apply_link: job.job_apply_link,
        };
    }
    localStorage.setItem('savedJobs', JSON.stringify(saved));
    updateSavedCount();
    return !!saved[job.job_id];
}

function updateSavedCount() {
    const count = Object.keys(getSavedJobs()).length;
    const badge = document.getElementById('saved-count');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? '' : 'none';
    }
}

function updateSaveButtons() {
    const saved = getSavedJobs();
    document.querySelectorAll('.save-btn').forEach(function(btn) {
        try {
            const job = JSON.parse(btn.getAttribute('data-job'));
            const isSaved = !!saved[job.job_id];
            btn.innerHTML = isSaved
                ? '<i class="bi bi-bookmark-fill"></i>'
                : '<i class="bi bi-bookmark"></i>';
            btn.classList.toggle('btn-primary', isSaved);
            btn.classList.toggle('btn-outline-primary', !isSaved);
        } catch (e) { /* skip */ }
    });
}
