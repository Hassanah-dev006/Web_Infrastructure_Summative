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

// ---- Salary Estimate ----
function fetchSalaryEstimate(title, location) {
    const widget = document.getElementById('salaryWidget');
    if (!widget) return;

    const params = new URLSearchParams({ title: title, location: location });
    fetch('/api/salary?' + params)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.error) {
                widget.innerHTML = '<small class="text-muted">Estimate not available.</small>';
                return;
            }
            const salaries = data.data || [];
            if (salaries.length === 0) {
                widget.innerHTML = '<small class="text-muted">No salary data available for this role.</small>';
                return;
            }
            const s = salaries[0];
            const fmt = function(n) {
                return n ? '$' + Math.round(n).toLocaleString() : 'N/A';
            };
            widget.innerHTML =
                '<div class="text-start">' +
                '<div class="d-flex justify-content-between mb-1"><span class="text-muted">Min</span><strong>' + fmt(s.min_salary) + '</strong></div>' +
                '<div class="d-flex justify-content-between mb-1"><span class="text-muted">Median</span><strong>' + fmt(s.median_salary) + '</strong></div>' +
                '<div class="d-flex justify-content-between"><span class="text-muted">Max</span><strong>' + fmt(s.max_salary) + '</strong></div>' +
                '<small class="text-muted mt-2 d-block">' + escapeHtml(s.publisher_name || '') + ' &middot; ' + escapeHtml(s.salary_period || 'YEAR') + '</small>' +
                '</div>';
        })
        .catch(function() {
            widget.innerHTML = '<small class="text-muted">Could not load estimate.</small>';
        });
}
